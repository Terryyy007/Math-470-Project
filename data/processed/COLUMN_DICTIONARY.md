# Column Dictionary for `modeling_dataset.csv`

这个文件解释 `data/processed/modeling_dataset.csv` 里每一列的含义。

## Important Notes

- 每一行是一个沪深300交易日。
- 模型输入不要包含 `future_*`、`high_risk_*`、`date`、`split`、`monthly_available_date`、`quarterly_available_date`。
- `future_*` 是未来信息，只能作为 label 或评价用。
- 推荐第一版模型使用 `high_risk_es_60d` 作为二分类 target。
- 月度宏观数据假设月末后 30 天才可用；季度宏观数据假设季末后 60 天才可用。

## Column Table

| Column | Group | Use as model input? | Meaning |
|---|---|---|---|
| `date` | date/index | No | 交易日期。每一行代表一个沪深300交易日，用当天及之前可得的信息预测未来风险。 |
| `open` | raw market | Yes | 沪深300当日开盘价。 |
| `high` | raw market | Yes | 沪深300当日最高价。 |
| `low` | raw market | Yes | 沪深300当日最低价。 |
| `close` | raw market | Yes | 沪深300当日收盘价。 |
| `change_pct_reported` | raw market | Yes | 原始指数表里给出的当日涨跌幅百分比。注意这是百分比单位，例如 1 表示上涨 1%。 |
| `volume_m_shares` | raw market | Yes | 成交量，原始单位为“万手”。 |
| `turnover_100m_cny` | raw market | Yes | 成交金额，原始单位为“亿元人民币”。 |
| `constituent_count` | raw market | Yes | 沪深300指数样本数量。 |
| `log_return` | market feature | Yes | 当日对数收益率，log(close_t / close_{t-1})。这是主要收益率变量。 |
| `simple_return` | market feature | Yes | 当日简单收益率，close_t / close_{t-1} - 1。 |
| `intraday_return` | market feature | Yes | 日内收益率，close_t / open_t - 1。 |
| `hl_range` | market feature | Yes | 当日高低价振幅，(high_t - low_t) / close_t。 |
| `volume_log_change` | market feature | Yes | 成交量的一日对数变化，log(volume_t / volume_{t-1})。 |
| `turnover_log_change` | market feature | Yes | 成交金额的一日对数变化，log(turnover_t / turnover_{t-1})。 |
| `ret_sum_5d` | market feature | Yes | 过去5个交易日累计对数收益率，sum of log_return over the rolling window。反映短/中/长期 momentum。 |
| `vol_5d` | market feature | Yes | 过去5个交易日对数收益率的滚动标准差。反映 realized volatility。 |
| `volume_chg_5d` | market feature | Yes | 成交量相对5个交易日前的对数变化，log(volume_t / volume_(t-5))。 |
| `turnover_chg_5d` | market feature | Yes | 成交金额相对5个交易日前的对数变化，log(turnover_t / turnover_(t-5))。 |
| `close_to_ma_5d` | market feature | Yes | 收盘价相对过去5日移动平均的偏离，close_t / MA_5 - 1。正数表示高于均线，负数表示低于均线。 |
| `drawdown_5d` | market feature | Yes | 过去5个交易日窗口内的最大回撤，表示为正的损失比例。数值越大说明近期回撤越严重。 |
| `downside_vol_5d` | market feature | Yes | 过去5个交易日中，只用负收益率计算的滚动标准差。反映 downside volatility。 |
| `ret_sum_20d` | market feature | Yes | 过去20个交易日累计对数收益率，sum of log_return over the rolling window。反映短/中/长期 momentum。 |
| `vol_20d` | market feature | Yes | 过去20个交易日对数收益率的滚动标准差。反映 realized volatility。 |
| `volume_chg_20d` | market feature | Yes | 成交量相对20个交易日前的对数变化，log(volume_t / volume_(t-20))。 |
| `turnover_chg_20d` | market feature | Yes | 成交金额相对20个交易日前的对数变化，log(turnover_t / turnover_(t-20))。 |
| `close_to_ma_20d` | market feature | Yes | 收盘价相对过去20日移动平均的偏离，close_t / MA_20 - 1。正数表示高于均线，负数表示低于均线。 |
| `drawdown_20d` | market feature | Yes | 过去20个交易日窗口内的最大回撤，表示为正的损失比例。数值越大说明近期回撤越严重。 |
| `downside_vol_20d` | market feature | Yes | 过去20个交易日中，只用负收益率计算的滚动标准差。反映 downside volatility。 |
| `ret_sum_60d` | market feature | Yes | 过去60个交易日累计对数收益率，sum of log_return over the rolling window。反映短/中/长期 momentum。 |
| `vol_60d` | market feature | Yes | 过去60个交易日对数收益率的滚动标准差。反映 realized volatility。 |
| `volume_chg_60d` | market feature | Yes | 成交量相对60个交易日前的对数变化，log(volume_t / volume_(t-60))。 |
| `turnover_chg_60d` | market feature | Yes | 成交金额相对60个交易日前的对数变化，log(turnover_t / turnover_(t-60))。 |
| `close_to_ma_60d` | market feature | Yes | 收盘价相对过去60日移动平均的偏离，close_t / MA_60 - 1。正数表示高于均线，负数表示低于均线。 |
| `drawdown_60d` | market feature | Yes | 过去60个交易日窗口内的最大回撤，表示为正的损失比例。数值越大说明近期回撤越严重。 |
| `downside_vol_60d` | market feature | Yes | 过去60个交易日中，只用负收益率计算的滚动标准差。反映 downside volatility。 |
| `ret_sum_120d` | market feature | Yes | 过去120个交易日累计对数收益率，sum of log_return over the rolling window。反映短/中/长期 momentum。 |
| `vol_120d` | market feature | Yes | 过去120个交易日对数收益率的滚动标准差。反映 realized volatility。 |
| `volume_chg_120d` | market feature | Yes | 成交量相对120个交易日前的对数变化，log(volume_t / volume_(t-120))。 |
| `turnover_chg_120d` | market feature | Yes | 成交金额相对120个交易日前的对数变化，log(turnover_t / turnover_(t-120))。 |
| `close_to_ma_120d` | market feature | Yes | 收盘价相对过去120日移动平均的偏离，close_t / MA_120 - 1。正数表示高于均线，负数表示低于均线。 |
| `drawdown_120d` | market feature | Yes | 过去120个交易日窗口内的最大回撤，表示为正的损失比例。数值越大说明近期回撤越严重。 |
| `downside_vol_120d` | market feature | Yes | 过去120个交易日中，只用负收益率计算的滚动标准差。反映 downside volatility。 |
| `ret_sum_250d` | market feature | Yes | 过去250个交易日累计对数收益率，sum of log_return over the rolling window。反映短/中/长期 momentum。 |
| `vol_250d` | market feature | Yes | 过去250个交易日对数收益率的滚动标准差。反映 realized volatility。 |
| `volume_chg_250d` | market feature | Yes | 成交量相对250个交易日前的对数变化，log(volume_t / volume_(t-250))。 |
| `turnover_chg_250d` | market feature | Yes | 成交金额相对250个交易日前的对数变化，log(turnover_t / turnover_(t-250))。 |
| `close_to_ma_250d` | market feature | Yes | 收盘价相对过去250日移动平均的偏离，close_t / MA_250 - 1。正数表示高于均线，负数表示低于均线。 |
| `drawdown_250d` | market feature | Yes | 过去250个交易日窗口内的最大回撤，表示为正的损失比例。数值越大说明近期回撤越严重。 |
| `downside_vol_250d` | market feature | Yes | 过去250个交易日中，只用负收益率计算的滚动标准差。反映 downside volatility。 |
| `future_cum_return_20d` | target/label | No | 未来20个交易日累计对数收益率，sum of log returns from t+1 to t+20。这是未来信息，只能作为 label 或辅助计算，不能作为模型输入。 |
| `future_loss_20d` | target/label | No | 未来20个交易日累计损失，等于 -future_cum_return_20d。数值越大表示未来跌得越多。这是回归型 target。 |
| `future_es_60d_5pct` | target/label | No | 未来60个交易日 realized Expected Shortfall，取未来60日最差5%日收益的平均损失，结果为正数。数值越大表示未来尾部风险越高。这是主要 ES target。 |
| `monthly_available_date` | macro alignment metadata | No | 对齐到该交易日时，最近一次可用的月度宏观数据日期。代码中假设月度数据在月末后30天才可用，以避免 look-ahead bias。 |
| `quarterly_available_date` | macro alignment metadata | No | 对齐到该交易日时，最近一次可用的季度宏观数据日期。代码中假设季度数据在季末后60天才可用，以避免 look-ahead bias。 |
| `split` | train/validation/test metadata | No | 时间序列切分标签：train、validation 或 test。不是随机切分。 |
| `high_risk_loss_20d` | target/label | No | 基于 future_loss_20d 的二分类标签。如果未来20日损失高于训练集90%分位数，则为1，否则为0。 |
| `high_risk_es_60d` | target/label | No | 基于 future_es_60d_5pct 的二分类标签。如果未来60日ES高于训练集90%分位数，则为1，否则为0。建议先用它作为 early-warning classification target。 |
| `m_0017` | macro feature | Yes | 月度宏观变量：商品零售价格指数 (上月=100)。已经按可得日期向后对齐到交易日，并对剩余缺失值用训练集median填补。 |
| `q_0004` | macro feature | Yes | 季度宏观变量：固定资产投资价格指数当季值 (上年同季=100)。已经按可得日期向后对齐到交易日，并对剩余缺失值用训练集median填补。 |
| `m_0019` | macro feature | Yes | 月度宏观变量：外商直接投资合同项目数累计值 (个)。已经按可得日期向后对齐到交易日，并对剩余缺失值用训练集median填补。 |
| `m_0022` | macro feature | Yes | 月度宏观变量：工业生产者购进价格指数 (上月=100)。已经按可得日期向后对齐到交易日，并对剩余缺失值用训练集median填补。 |
| `m_0021` | macro feature | Yes | 月度宏观变量：工业生产者出厂价格指数 (上月=100)。已经按可得日期向后对齐到交易日，并对剩余缺失值用训练集median填补。 |
| `m_0018` | macro feature | Yes | 月度宏观变量：固定资产投资额累计增长 (%)。已经按可得日期向后对齐到交易日，并对剩余缺失值用训练集median填补。 |
| `m_0030` | macro feature | Yes | 月度宏观变量：非制造业商务活动指数 (%)。已经按可得日期向后对齐到交易日，并对剩余缺失值用训练集median填补。 |
| `m_0020` | macro feature | Yes | 月度宏观变量：居民消费价格指数 (上月=100)。已经按可得日期向后对齐到交易日，并对剩余缺失值用训练集median填补。 |
| `m_0016` | macro feature | Yes | 月度宏观变量：制造业采购经理指数 (%)。已经按可得日期向后对齐到交易日，并对剩余缺失值用训练集median填补。 |
| `m_0026` | macro feature | Yes | 月度宏观变量：流通中现金 (M0) 供应量_期末值 (亿元)。已经按可得日期向后对齐到交易日，并对剩余缺失值用训练集median填补。 |
| `m_0027` | macro feature | Yes | 月度宏观变量：货币 (M1) 供应量_期末值 (亿元)。已经按可得日期向后对齐到交易日，并对剩余缺失值用训练集median填补。 |
| `m_0029` | macro feature | Yes | 月度宏观变量：进出口总值当期值 (千美元)。已经按可得日期向后对齐到交易日，并对剩余缺失值用训练集median填补。 |
| `m_0028` | macro feature | Yes | 月度宏观变量：货币和准货币 (M2) 供应量_期末值 (亿元)。已经按可得日期向后对齐到交易日，并对剩余缺失值用训练集median填补。 |
| `q_0005` | macro feature | Yes | 季度宏观变量：国内生产总值当季值 (亿元)。已经按可得日期向后对齐到交易日，并对剩余缺失值用训练集median填补。 |
| `q_0006` | macro feature | Yes | 季度宏观变量：工业增加值当季值 (亿元)。已经按可得日期向后对齐到交易日，并对剩余缺失值用训练集median填补。 |

## Macro Variable Mapping

宏观变量列名为了方便建模被改成了 `m_####` 或 `q_####`。下面是最终保留在 dataset 里的宏观列和原始中文变量名。

| Column | Frequency | Original Chinese indicator |
|---|---|---|
| `m_0017` | Monthly | 商品零售价格指数 (上月=100) |
| `q_0004` | Quarterly | 固定资产投资价格指数当季值 (上年同季=100) |
| `m_0019` | Monthly | 外商直接投资合同项目数累计值 (个) |
| `m_0022` | Monthly | 工业生产者购进价格指数 (上月=100) |
| `m_0021` | Monthly | 工业生产者出厂价格指数 (上月=100) |
| `m_0018` | Monthly | 固定资产投资额累计增长 (%) |
| `m_0030` | Monthly | 非制造业商务活动指数 (%) |
| `m_0020` | Monthly | 居民消费价格指数 (上月=100) |
| `m_0016` | Monthly | 制造业采购经理指数 (%) |
| `m_0026` | Monthly | 流通中现金 (M0) 供应量_期末值 (亿元) |
| `m_0027` | Monthly | 货币 (M1) 供应量_期末值 (亿元) |
| `m_0029` | Monthly | 进出口总值当期值 (千美元) |
| `m_0028` | Monthly | 货币和准货币 (M2) 供应量_期末值 (亿元) |
| `q_0005` | Quarterly | 国内生产总值当季值 (亿元) |
| `q_0006` | Quarterly | 工业增加值当季值 (亿元) |