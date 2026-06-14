# MATH 470 ES Early-Warning Risk Project

This project builds a cleaned dataset for predicting Expected Shortfall / tail-risk warnings for the CSI 300 index.

## Project idea

- Sequential market information: CSI 300 daily prices, returns, volatility, drawdown, volume and turnover features.
- Non-sequential macro information: monthly and quarterly Chinese macro indicators aligned to each trading day with a publication lag to avoid look-ahead bias.
- Labels: future realized downside loss, future realized ES, and high-risk labels based on the training-period quantile.

## Folder structure

```text
math470_es_project/
  data/raw/            # original Excel files
  data/interim/        # cleaned intermediate market/macro files
  data/processed/      # final modeling dataset
  src/                 # Python scripts
  notebooks/           # optional notebooks
  reports/             # figures/tables for report
```

## How to run

From the project root:

```bash
python src/01_build_dataset.py
```

The main output will be:

```text
data/processed/modeling_dataset.csv
```

## Important assumptions

1. Monthly macro data are assumed to become usable only after a 30-day lag.
2. Quarterly macro data are assumed to become usable only after a 60-day lag.
3. High-risk labels are defined using the 90th percentile of future realized loss / ES in the training period only, so the test period is not used to choose thresholds.
4. Missing macro features with too many missing values after alignment are dropped. Remaining missing values are median-imputed using training-period medians.

These assumptions can be changed in the CONFIG section of `src/01_build_dataset.py`.
