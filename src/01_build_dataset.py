"""
Build a cleaned MATH 470 modeling dataset for CSI 300 Expected Shortfall / tail-risk prediction.

Run from project root:
    python src/01_build_dataset.py

Outputs:
    data/interim/market_features.csv
    data/interim/monthly_macro_clean.csv
    data/interim/quarterly_macro_clean.csv
    data/interim/macro_feature_dictionary.csv
    data/processed/modeling_dataset.csv
    data/processed/cleaning_report.txt
"""

from __future__ import annotations

import math
import re
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd

# ---------------------------------------------------------------------
# CONFIG: change these first if you want a different dataset definition
# ---------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
INTERIM_DIR = PROJECT_ROOT / "data" / "interim"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

INDEX_FILE = RAW_DIR / "沪深300指数数据.xlsx"
MONTHLY_FILES = [
    RAW_DIR / "月度数据 200001-201512.xlsx",
    RAW_DIR / "月度数据 201601-202012.xlsx",
    RAW_DIR / "月度数据 202101-202512.xlsx",
    RAW_DIR / "月度数据 202601-.xlsx",
]
QUARTERLY_FILE = RAW_DIR / "季度数据.xlsx"

# Financial prediction should be split by time, not by random split.
TRAIN_END = "2018-12-31"
VALID_END = "2021-12-31"

# Publication-lag assumption to avoid look-ahead bias.
MONTHLY_RELEASE_LAG_DAYS = 30
QUARTERLY_RELEASE_LAG_DAYS = 60

# Label choices.
LOSS_HORIZON_DAYS = 20
ES_HORIZON_DAYS = 60
ES_ALPHA = 0.05
HIGH_RISK_QUANTILE = 0.90

# Feature cleaning.
MAX_MACRO_MISSING_RATIO = 0.45
ROLLING_WINDOWS = [5, 20, 60, 120, 250]


# ---------------------------------------------------------------------
# Utility functions
# ---------------------------------------------------------------------
def ensure_dirs() -> None:
    INTERIM_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def parse_month_cn(x: object) -> pd.Timestamp | pd.NaT:
    """Parse strings like '2026年5月' to month-end Timestamp."""
    if pd.isna(x):
        return pd.NaT
    s = str(x).strip()
    m = re.match(r"(\d{4})年\s*(\d{1,2})月", s)
    if not m:
        return pd.NaT
    year, month = int(m.group(1)), int(m.group(2))
    return pd.Timestamp(year=year, month=month, day=1) + pd.offsets.MonthEnd(0)


def parse_quarter_cn(x: object) -> pd.Timestamp | pd.NaT:
    """Parse strings like '2026年第一季度' to quarter-end Timestamp."""
    if pd.isna(x):
        return pd.NaT
    s = str(x).strip()
    m = re.match(r"(\d{4})年\s*(第一|第二|第三|第四)季度", s)
    if not m:
        return pd.NaT
    year = int(m.group(1))
    quarter_map = {"第一": 1, "第二": 2, "第三": 3, "第四": 4}
    q = quarter_map[m.group(2)]
    month = q * 3
    return pd.Timestamp(year=year, month=month, day=1) + pd.offsets.MonthEnd(0)


def safe_numeric(s: pd.Series) -> pd.Series:
    """Convert series to numeric, treating common non-numeric placeholders as missing."""
    cleaned = (
        s.astype(str)
        .str.strip()
        .replace({"": np.nan, "nan": np.nan, "--": np.nan, "—": np.nan, "-": np.nan, "N/A": np.nan})
    )
    return pd.to_numeric(cleaned, errors="coerce")


def make_feature_ids(names: Iterable[str], prefix: str) -> dict[str, str]:
    """Map original Chinese indicator names to stable feature IDs."""
    mapping: dict[str, str] = {}
    for i, name in enumerate(sorted(set(names)), start=1):
        mapping[name] = f"{prefix}_{i:04d}"
    return mapping


def max_drawdown(values: pd.Series) -> float:
    """Maximum drawdown over a rolling close-price window, returned as a positive loss."""
    arr = values.to_numpy(dtype=float)
    if len(arr) == 0 or np.all(np.isnan(arr)):
        return np.nan
    running_max = np.maximum.accumulate(arr)
    drawdowns = arr / running_max - 1.0
    return -np.nanmin(drawdowns)


def future_es_from_returns(returns: pd.Series, horizon: int, alpha: float) -> pd.Series:
    """Realized future ES from daily returns r_{t+1}, ..., r_{t+horizon}.

    ES is reported as a positive loss: negative of the average of the worst alpha fraction
    of future returns.
    """
    r = returns.to_numpy(dtype=float)
    out = np.full(len(r), np.nan)
    k = max(1, int(math.ceil(horizon * alpha)))
    for i in range(len(r) - horizon):
        window = r[i + 1 : i + 1 + horizon]
        if np.isnan(window).any():
            continue
        worst = np.sort(window)[:k]
        out[i] = -float(np.mean(worst))
    return pd.Series(out, index=returns.index)


def assign_split(dates: pd.Series) -> pd.Series:
    train_end = pd.Timestamp(TRAIN_END)
    valid_end = pd.Timestamp(VALID_END)
    return np.select(
        [dates <= train_end, dates <= valid_end],
        ["train", "validation"],
        default="test",
    )


# ---------------------------------------------------------------------
# Market data cleaning and feature engineering
# ---------------------------------------------------------------------
def load_market_features() -> pd.DataFrame:
    raw = pd.read_excel(INDEX_FILE, sheet_name=0)
    col_map = {
        "日期Date": "date",
        "开盘Open": "open",
        "最高High": "high",
        "最低Low": "low",
        "收盘Close": "close",
        "涨跌幅(%)Change(%)": "change_pct_reported",
        "成交量（万手）Volume(M Shares)": "volume_m_shares",
        "成交金额（亿元）Turnover": "turnover_100m_cny",
        "样本数量ConsNumber": "constituent_count",
    }
    df = raw.rename(columns=col_map)[list(col_map.values())].copy()
    df["date"] = pd.to_datetime(df["date"].astype(str), format="%Y%m%d")
    df = df.sort_values("date").drop_duplicates("date").reset_index(drop=True)

    numeric_cols = [c for c in df.columns if c != "date"]
    for c in numeric_cols:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    df["log_return"] = np.log(df["close"] / df["close"].shift(1))
    df["simple_return"] = df["close"].pct_change()
    df["intraday_return"] = df["close"] / df["open"] - 1.0
    df["hl_range"] = (df["high"] - df["low"]) / df["close"]
    df["volume_log_change"] = np.log(df["volume_m_shares"] / df["volume_m_shares"].shift(1))
    df["turnover_log_change"] = np.log(df["turnover_100m_cny"] / df["turnover_100m_cny"].shift(1))

    for w in ROLLING_WINDOWS:
        df[f"ret_sum_{w}d"] = df["log_return"].rolling(w).sum()
        df[f"vol_{w}d"] = df["log_return"].rolling(w).std()
        df[f"volume_chg_{w}d"] = np.log(df["volume_m_shares"] / df["volume_m_shares"].shift(w))
        df[f"turnover_chg_{w}d"] = np.log(df["turnover_100m_cny"] / df["turnover_100m_cny"].shift(w))
        df[f"close_to_ma_{w}d"] = df["close"] / df["close"].rolling(w).mean() - 1.0
        df[f"drawdown_{w}d"] = df["close"].rolling(w).apply(max_drawdown, raw=False)
        df[f"downside_vol_{w}d"] = (
            df["log_return"].where(df["log_return"] < 0).rolling(w, min_periods=max(2, w // 3)).std()
        )

    # Future labels. Shifted so features at date t predict outcomes after t.
    df[f"future_cum_return_{LOSS_HORIZON_DAYS}d"] = (
        df["log_return"].shift(-1).rolling(LOSS_HORIZON_DAYS).sum().shift(-(LOSS_HORIZON_DAYS - 1))
    )
    df[f"future_loss_{LOSS_HORIZON_DAYS}d"] = -df[f"future_cum_return_{LOSS_HORIZON_DAYS}d"]
    df[f"future_es_{ES_HORIZON_DAYS}d_{int(ES_ALPHA * 100)}pct"] = future_es_from_returns(
        df["log_return"], ES_HORIZON_DAYS, ES_ALPHA
    )

    return df


# ---------------------------------------------------------------------
# Macro data cleaning
# ---------------------------------------------------------------------
def read_wide_macro_file(path: Path, frequency: str) -> pd.DataFrame:
    """Read Chinese macro Excel files where row 2 stores period headers and col 1 stores indicators."""
    raw = pd.read_excel(path, sheet_name=0, header=None)
    header = raw.iloc[2].tolist()
    data = raw.iloc[3:].copy()
    data.columns = header
    data = data.rename(columns={header[0]: "indicator"})
    data = data.dropna(subset=["indicator"])

    long = data.melt(id_vars="indicator", var_name="period_raw", value_name="value")
    long = long.dropna(subset=["period_raw"])
    if frequency == "M":
        long["period_end"] = long["period_raw"].apply(parse_month_cn)
    elif frequency == "Q":
        long["period_end"] = long["period_raw"].apply(parse_quarter_cn)
    else:
        raise ValueError("frequency must be 'M' or 'Q'")
    long = long.dropna(subset=["period_end"])
    long["indicator"] = long["indicator"].astype(str).str.strip()
    long["value"] = safe_numeric(long["value"])
    long["source_file"] = path.name
    long["frequency"] = frequency
    return long


def build_macro_tables() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    monthly_long = pd.concat([read_wide_macro_file(p, "M") for p in MONTHLY_FILES], ignore_index=True)
    quarterly_long = read_wide_macro_file(QUARTERLY_FILE, "Q")

    # Drop duplicated records across files and pivot to wide format.
    monthly_long = monthly_long.drop_duplicates(["period_end", "indicator"], keep="last")
    quarterly_long = quarterly_long.drop_duplicates(["period_end", "indicator"], keep="last")

    month_map = make_feature_ids(monthly_long["indicator"], "m")
    quarter_map = make_feature_ids(quarterly_long["indicator"], "q")
    monthly_long["feature_id"] = monthly_long["indicator"].map(month_map)
    quarterly_long["feature_id"] = quarterly_long["indicator"].map(quarter_map)

    dictionary = pd.concat(
        [
            monthly_long[["feature_id", "indicator", "frequency"]].drop_duplicates(),
            quarterly_long[["feature_id", "indicator", "frequency"]].drop_duplicates(),
        ],
        ignore_index=True,
    ).sort_values(["frequency", "feature_id"])

    monthly = (
        monthly_long.pivot_table(index="period_end", columns="feature_id", values="value", aggfunc="last")
        .sort_index()
        .reset_index()
    )
    quarterly = (
        quarterly_long.pivot_table(index="period_end", columns="feature_id", values="value", aggfunc="last")
        .sort_index()
        .reset_index()
    )

    monthly["available_date"] = monthly["period_end"] + pd.Timedelta(days=MONTHLY_RELEASE_LAG_DAYS)
    quarterly["available_date"] = quarterly["period_end"] + pd.Timedelta(days=QUARTERLY_RELEASE_LAG_DAYS)
    return monthly, quarterly, dictionary


# ---------------------------------------------------------------------
# Merge and final cleaning
# ---------------------------------------------------------------------
def merge_market_macro(market: pd.DataFrame, monthly: pd.DataFrame, quarterly: pd.DataFrame) -> pd.DataFrame:
    df = market.sort_values("date").copy()
    monthly_sorted = monthly.sort_values("available_date").drop(columns=["period_end"])
    quarterly_sorted = quarterly.sort_values("available_date").drop(columns=["period_end"])

    df = pd.merge_asof(
        df,
        monthly_sorted,
        left_on="date",
        right_on="available_date",
        direction="backward",
        suffixes=("", "_monthly"),
    ).rename(columns={"available_date": "monthly_available_date"})

    df = pd.merge_asof(
        df.sort_values("date"),
        quarterly_sorted,
        left_on="date",
        right_on="available_date",
        direction="backward",
        suffixes=("", "_quarterly"),
    ).rename(columns={"available_date": "quarterly_available_date"})

    return df


def final_cleaning(df: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, object]]:
    df = df.copy()
    df["split"] = assign_split(df["date"])

    # Drop rows without enough rolling history or without future labels.
    label_cols = [f"future_loss_{LOSS_HORIZON_DAYS}d", f"future_es_{ES_HORIZON_DAYS}d_{int(ES_ALPHA * 100)}pct"]
    needed_feature_cols = [f"vol_{w}d" for w in [20, 60]] + [f"drawdown_{w}d" for w in [20, 60]]
    before_drop = len(df)
    df = df.dropna(subset=label_cols + needed_feature_cols).reset_index(drop=True)

    train_mask = df["split"] == "train"
    loss_threshold = df.loc[train_mask, label_cols[0]].quantile(HIGH_RISK_QUANTILE)
    es_threshold = df.loc[train_mask, label_cols[1]].quantile(HIGH_RISK_QUANTILE)
    df[f"high_risk_loss_{LOSS_HORIZON_DAYS}d"] = (df[label_cols[0]] >= loss_threshold).astype(int)
    df[f"high_risk_es_{ES_HORIZON_DAYS}d"] = (df[label_cols[1]] >= es_threshold).astype(int)

    # Drop macro columns with too much missingness, based on post-merge data.
    macro_cols = [c for c in df.columns if re.match(r"^[mq]_\d{4}$", str(c))]
    missing_ratio = df[macro_cols].isna().mean().sort_values(ascending=False)
    keep_macro = missing_ratio[missing_ratio <= MAX_MACRO_MISSING_RATIO].index.tolist()
    drop_macro = missing_ratio[missing_ratio > MAX_MACRO_MISSING_RATIO].index.tolist()

    # Keep non-macro columns and selected macro columns only.
    non_macro_cols = [c for c in df.columns if c not in macro_cols]
    df = df[non_macro_cols + keep_macro]

    # Median-impute remaining numeric feature missing values with train-period medians.
    do_not_impute = {"date", "monthly_available_date", "quarterly_available_date", "split"}
    numeric_cols = [c for c in df.select_dtypes(include=[np.number]).columns if c not in label_cols]
    train_medians = df.loc[df["split"] == "train", numeric_cols].median(numeric_only=True)
    df[numeric_cols] = df[numeric_cols].fillna(train_medians)

    # Infinite values can appear when previous volume/turnover is zero; replace and impute again.
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df[numeric_cols] = df[numeric_cols].fillna(train_medians).fillna(0.0)

    report = {
        "raw_rows_before_drop": before_drop,
        "rows_after_drop": len(df),
        "date_min": str(df["date"].min().date()),
        "date_max": str(df["date"].max().date()),
        "train_rows": int((df["split"] == "train").sum()),
        "validation_rows": int((df["split"] == "validation").sum()),
        "test_rows": int((df["split"] == "test").sum()),
        "loss_threshold_train_q90": float(loss_threshold),
        "es_threshold_train_q90": float(es_threshold),
        "macro_cols_total": len(macro_cols),
        "macro_cols_kept": len(keep_macro),
        "macro_cols_dropped_missing": len(drop_macro),
    }
    return df, report


def write_report(report: dict[str, object], df: pd.DataFrame) -> None:
    lines = ["Cleaning report", "===============", ""]
    for k, v in report.items():
        lines.append(f"{k}: {v}")
    lines.extend([
        "",
        "Final columns by group",
        "----------------------",
        f"Total columns: {df.shape[1]}",
        f"Market/date/label columns: {sum(not re.match(r'^[mq]_\d{4}$', str(c)) for c in df.columns)}",
        f"Macro columns: {sum(bool(re.match(r'^[mq]_\d{4}$', str(c))) for c in df.columns)}",
        "",
        "Suggested next step",
        "-------------------",
        "Start with high_risk_es_60d as the classification target and use AUC / precision@10% for evaluation.",
    ])
    (PROCESSED_DIR / "cleaning_report.txt").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    ensure_dirs()

    print("1/5 Loading and engineering market features...")
    market = load_market_features()
    market.to_csv(INTERIM_DIR / "market_features.csv", index=False, encoding="utf-8-sig")

    print("2/5 Cleaning monthly and quarterly macro data...")
    monthly, quarterly, dictionary = build_macro_tables()
    monthly.to_csv(INTERIM_DIR / "monthly_macro_clean.csv", index=False, encoding="utf-8-sig")
    quarterly.to_csv(INTERIM_DIR / "quarterly_macro_clean.csv", index=False, encoding="utf-8-sig")
    dictionary.to_csv(INTERIM_DIR / "macro_feature_dictionary.csv", index=False, encoding="utf-8-sig")

    print("3/5 Aligning macro data to trading days...")
    merged = merge_market_macro(market, monthly, quarterly)

    print("4/5 Final cleaning, label construction, and imputation...")
    final_df, report = final_cleaning(merged)

    print("5/5 Saving outputs...")
    final_df.to_csv(PROCESSED_DIR / "modeling_dataset.csv", index=False, encoding="utf-8-sig")
    write_report(report, final_df)

    print("Done.")
    print(f"Rows x columns: {final_df.shape}")
    print(f"Date range: {report['date_min']} to {report['date_max']}")
    print(f"Output: {PROCESSED_DIR / 'modeling_dataset.csv'}")


if __name__ == "__main__":
    main()
