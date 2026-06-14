# Column Dictionary for `modeling_dataset.csv`

This document explains each column in the cleaned modeling dataset for the MATH 470 project on Expected Shortfall (ES) and early-warning tail-risk prediction.

Each row of the dataset corresponds to one CSI 300 trading day. Market and macroeconomic information available up to that date is used to predict future downside risk. Future-looking variables are labels or targets only and must not be used as model inputs.

## Recommended first modeling target

For the first baseline classification models, use `high_risk_es_60d` as the target variable. It indicates whether the realized 60-day future ES is in the high-risk region based on the 90th percentile threshold estimated from the training period.

## Columns

| Column | Group | Description | Use as model input? |
|---|---|---|---|
| `date` | date/index | Trading date. Each row represents one CSI 300 trading day. Information available up to this date is used to predict future risk. | No |
| `open` | raw market | CSI 300 opening level on the trading day. | Yes |
| `high` | raw market | CSI 300 intraday high on the trading day. | Yes |
| `low` | raw market | CSI 300 intraday low on the trading day. | Yes |
| `close` | raw market | CSI 300 closing level on the trading day. | Yes |
| `change_pct_reported` | raw market | Daily percentage change reported in the original index file. The unit is percentage points; for example, 1 means a 1% increase. | Yes |
| `volume_m_shares` | raw market | Trading volume from the original file. The original unit is ten-thousand lots/shares depending on the data source convention. | Yes |
| `turnover_100m_cny` | raw market | Trading turnover from the original file. The original unit is 100 million CNY. | Yes |
| `constituent_count` | raw market | Number of constituents in the CSI 300 index. | Yes |
| `log_return` | market feature | Daily log return, defined as log(close_t / close_{t-1}). This is the main return variable. | Yes |
| `simple_return` | market feature | Daily simple return, defined as close_t / close_{t-1} - 1. | Yes |
| `intraday_return` | market feature | Intraday return, defined as close_t / open_t - 1. | Yes |
| `hl_range` | market feature | Daily high-low range, defined as (high_t - low_t) / close_t. | Yes |
| `volume_log_change` | market feature | One-day log change in trading volume, defined as log(volume_t / volume_{t-1}). | Yes |
| `turnover_log_change` | market feature | One-day log change in trading turnover, defined as log(turnover_t / turnover_{t-1}). | Yes |
| `ret_sum_5d` | market feature | Cumulative log return over the past 5 trading days. This is a momentum-type feature. | Yes |
| `vol_5d` | market feature | Rolling standard deviation of daily log returns over the past 5 trading days. This measures realized volatility. | Yes |
| `volume_chg_5d` | market feature | Log change in trading volume relative to 5 trading days earlier, defined as log(volume_t / volume_(t-5)). | Yes |
| `turnover_chg_5d` | market feature | Log change in trading turnover relative to 5 trading days earlier, defined as log(turnover_t / turnover_(t-5)). | Yes |
| `close_to_ma_5d` | market feature | Deviation of the closing level from its 5-day moving average, defined as close_t / MA_5 - 1. Positive values mean the index is above its moving average. | Yes |
| `drawdown_5d` | market feature | Maximum drawdown within the past 5 trading days, expressed as a positive loss ratio. Larger values indicate a more severe recent drawdown. | Yes |
| `downside_vol_5d` | market feature | Rolling downside volatility over the past 5 trading days, computed using only negative daily returns. | Yes |
| `ret_sum_20d` | market feature | Cumulative log return over the past 20 trading days. This is a momentum-type feature. | Yes |
| `vol_20d` | market feature | Rolling standard deviation of daily log returns over the past 20 trading days. This measures realized volatility. | Yes |
| `volume_chg_20d` | market feature | Log change in trading volume relative to 20 trading days earlier, defined as log(volume_t / volume_(t-20)). | Yes |
| `turnover_chg_20d` | market feature | Log change in trading turnover relative to 20 trading days earlier, defined as log(turnover_t / turnover_(t-20)). | Yes |
| `close_to_ma_20d` | market feature | Deviation of the closing level from its 20-day moving average, defined as close_t / MA_20 - 1. Positive values mean the index is above its moving average. | Yes |
| `drawdown_20d` | market feature | Maximum drawdown within the past 20 trading days, expressed as a positive loss ratio. Larger values indicate a more severe recent drawdown. | Yes |
| `downside_vol_20d` | market feature | Rolling downside volatility over the past 20 trading days, computed using only negative daily returns. | Yes |
| `ret_sum_60d` | market feature | Cumulative log return over the past 60 trading days. This is a momentum-type feature. | Yes |
| `vol_60d` | market feature | Rolling standard deviation of daily log returns over the past 60 trading days. This measures realized volatility. | Yes |
| `volume_chg_60d` | market feature | Log change in trading volume relative to 60 trading days earlier, defined as log(volume_t / volume_(t-60)). | Yes |
| `turnover_chg_60d` | market feature | Log change in trading turnover relative to 60 trading days earlier, defined as log(turnover_t / turnover_(t-60)). | Yes |
| `close_to_ma_60d` | market feature | Deviation of the closing level from its 60-day moving average, defined as close_t / MA_60 - 1. Positive values mean the index is above its moving average. | Yes |
| `drawdown_60d` | market feature | Maximum drawdown within the past 60 trading days, expressed as a positive loss ratio. Larger values indicate a more severe recent drawdown. | Yes |
| `downside_vol_60d` | market feature | Rolling downside volatility over the past 60 trading days, computed using only negative daily returns. | Yes |
| `ret_sum_120d` | market feature | Cumulative log return over the past 120 trading days. This is a momentum-type feature. | Yes |
| `vol_120d` | market feature | Rolling standard deviation of daily log returns over the past 120 trading days. This measures realized volatility. | Yes |
| `volume_chg_120d` | market feature | Log change in trading volume relative to 120 trading days earlier, defined as log(volume_t / volume_(t-120)). | Yes |
| `turnover_chg_120d` | market feature | Log change in trading turnover relative to 120 trading days earlier, defined as log(turnover_t / turnover_(t-120)). | Yes |
| `close_to_ma_120d` | market feature | Deviation of the closing level from its 120-day moving average, defined as close_t / MA_120 - 1. Positive values mean the index is above its moving average. | Yes |
| `drawdown_120d` | market feature | Maximum drawdown within the past 120 trading days, expressed as a positive loss ratio. Larger values indicate a more severe recent drawdown. | Yes |
| `downside_vol_120d` | market feature | Rolling downside volatility over the past 120 trading days, computed using only negative daily returns. | Yes |
| `ret_sum_250d` | market feature | Cumulative log return over the past 250 trading days. This is a momentum-type feature. | Yes |
| `vol_250d` | market feature | Rolling standard deviation of daily log returns over the past 250 trading days. This measures realized volatility. | Yes |
| `volume_chg_250d` | market feature | Log change in trading volume relative to 250 trading days earlier, defined as log(volume_t / volume_(t-250)). | Yes |
| `turnover_chg_250d` | market feature | Log change in trading turnover relative to 250 trading days earlier, defined as log(turnover_t / turnover_(t-250)). | Yes |
| `close_to_ma_250d` | market feature | Deviation of the closing level from its 250-day moving average, defined as close_t / MA_250 - 1. Positive values mean the index is above its moving average. | Yes |
| `drawdown_250d` | market feature | Maximum drawdown within the past 250 trading days, expressed as a positive loss ratio. Larger values indicate a more severe recent drawdown. | Yes |
| `downside_vol_250d` | market feature | Rolling downside volatility over the past 250 trading days, computed using only negative daily returns. | Yes |
| `future_cum_return_20d` | target/label | Cumulative log return over the next 20 trading days, computed from t+1 to t+20. This is future information and must not be used as a model input. | No |
| `future_loss_20d` | target/label | Cumulative loss over the next 20 trading days, defined as -future_cum_return_20d. Larger values mean larger future losses. This can be used as a regression target. | No |
| `future_es_60d_5pct` | target/label | Realized Expected Shortfall over the next 60 trading days at the 5% tail level. It is computed as the average loss of the worst 5% future daily returns and reported as a positive number. This is the main ES target. | No |
| `monthly_available_date` | macro alignment metadata | Date of the most recent monthly macroeconomic observation available for this trading day. The cleaning script assumes a 30-day publication lag after month-end to avoid look-ahead bias. | No |
| `quarterly_available_date` | macro alignment metadata | Date of the most recent quarterly macroeconomic observation available for this trading day. The cleaning script assumes a 60-day publication lag after quarter-end to avoid look-ahead bias. | No |
| `split` | train/validation/test metadata | Time-series split indicator: train, validation, or test. The split is chronological, not random. | No |
| `high_risk_loss_20d` | target/label | Binary classification label based on future_loss_20d. It equals 1 if the next-20-day loss is above the 90th percentile of the training period, and 0 otherwise. | No |
| `high_risk_es_60d` | target/label | Binary classification label based on future_es_60d_5pct. It equals 1 if the future 60-day ES is above the 90th percentile of the training period, and 0 otherwise. This is the recommended early-warning classification target for the first baseline models. | No |
| `m_0017` | macro feature | Monthly macro variable: Retail Price Index of Commodities (previous month = 100). It is aligned to trading days according to data availability, and remaining missing values are filled using the training-period median. | Yes |
| `q_0004` | macro feature | Quarterly macro variable: Fixed Asset Investment Price Index, current-quarter value (same quarter of previous year = 100). It is aligned to trading days according to data availability, and remaining missing values are filled using the training-period median. | Yes |
| `m_0019` | macro feature | Monthly macro variable: cumulative number of foreign direct investment contract projects. It is aligned to trading days according to data availability, and remaining missing values are filled using the training-period median. | Yes |
| `m_0022` | macro feature | Monthly macro variable: Industrial Producer Purchase Price Index (previous month = 100). It is aligned to trading days according to data availability, and remaining missing values are filled using the training-period median. | Yes |
| `m_0021` | macro feature | Monthly macro variable: Producer Price Index for Industrial Products (previous month = 100). It is aligned to trading days according to data availability, and remaining missing values are filled using the training-period median. | Yes |
| `m_0018` | macro feature | Monthly macro variable: cumulative growth rate of fixed asset investment (%). It is aligned to trading days according to data availability, and remaining missing values are filled using the training-period median. | Yes |
| `m_0030` | macro feature | Monthly macro variable: Non-Manufacturing Business Activity Index (%). This is commonly used as the non-manufacturing PMI-type indicator. It is aligned to trading days according to data availability, and remaining missing values are filled using the training-period median. | Yes |
| `m_0020` | macro feature | Monthly macro variable: Consumer Price Index (previous month = 100). It is aligned to trading days according to data availability, and remaining missing values are filled using the training-period median. | Yes |
| `m_0016` | macro feature | Monthly macro variable: Manufacturing Purchasing Managers’ Index, PMI (%). It is aligned to trading days according to data availability, and remaining missing values are filled using the training-period median. | Yes |
| `m_0026` | macro feature | Monthly macro variable: Money supply M0, end-of-period value (100 million CNY). It is aligned to trading days according to data availability, and remaining missing values are filled using the training-period median. | Yes |
| `m_0027` | macro feature | Monthly macro variable: Money supply M1, end-of-period value (100 million CNY). It is aligned to trading days according to data availability, and remaining missing values are filled using the training-period median. | Yes |
| `m_0029` | macro feature | Monthly macro variable: total imports and exports, current-period value (thousand USD). It is aligned to trading days according to data availability, and remaining missing values are filled using the training-period median. | Yes |
| `m_0028` | macro feature | Monthly macro variable: Money and quasi-money supply M2, end-of-period value (100 million CNY). It is aligned to trading days according to data availability, and remaining missing values are filled using the training-period median. | Yes |
| `q_0005` | macro feature | Quarterly macro variable: Gross Domestic Product, current-quarter value (100 million CNY). It is aligned to trading days according to data availability, and remaining missing values are filled using the training-period median. | Yes |
| `q_0006` | macro feature | Quarterly macro variable: Industrial Value Added, current-quarter value (100 million CNY). It is aligned to trading days according to data availability, and remaining missing values are filled using the training-period median. | Yes |

## Notes on model inputs

- Do not use `future_*` columns or `high_risk_*` columns as input features. These columns contain future information or labels.
- Do not use `date`, `split`, `monthly_available_date`, or `quarterly_available_date` as numerical model inputs. They are metadata columns.
- The market feature columns and macro feature columns can be used as predictors.
- The dataset uses a chronological train/validation/test split to reduce look-ahead bias.
