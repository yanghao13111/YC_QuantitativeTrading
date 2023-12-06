# main.py
import data_collection
import backTesting_logic
from datetime import datetime, timedelta
import time
from joblib import Parallel, delayed
import itertools
import indicators

# 參數設置#######################################
symbol = 'ETH/USDT'
timeframe = '1h'

# Maximum is 9
buy_pool = [indicators.B, indicators.C, indicators.I, indicators.M, indicators.N]
sell_pool = [indicators.B, indicators.C, indicators.I, indicators.M, indicators.N]
# Approximately equal to conditions/2
buy_combined = 3
sell_combined = 3
##############################################

month = 5
# 训练数据时间范围: 一年前到半年前
train_start_date = datetime.utcnow() - timedelta(days=month*30)
train_end_date = datetime.utcnow() - timedelta(days=(month-1)*30 + 1)

# 验证数据时间范围: 半年前到现在
validation_start_date = datetime.utcnow() - timedelta(days=(month-1)*30)
validation_end_date = datetime.utcnow() - timedelta(days=(month-2)*30 + 1)

# 訓練數據搜集
df_train = data_collection.collect_data(symbol, timeframe, train_start_date, train_end_date)
df_train.to_csv('Crypto/train_data.csv', index=False)

# 驗證數據搜集
df_validation = data_collection.collect_data(symbol, timeframe, validation_start_date, validation_end_date)
df_validation.to_csv('Crypto/validation_data.csv', index=False)

start_time = time.time()
buy_expression = backTesting_logic.generate_expressions(buy_pool, buy_combined)
sell_expression = backTesting_logic.generate_expressions(sell_pool, sell_combined)

# 使用 joblib 平行處理回測
def run_single_backtest(buy_expr, sell_expr):
    return backTesting_logic.run_backtest('Crypto/train_data.csv', train_start_date, train_end_date, buy_expr, sell_expr)

# 生成所有可能的买入和卖出表达式组合
expression_combinations = list(itertools.product(buy_expression, sell_expression))

# 使用 joblib 平行处理回测
backtest_results = Parallel(n_jobs=-1)(delayed(run_single_backtest)(buy_expr, sell_expr) for buy_expr, sell_expr in expression_combinations)

# 根据资产价值排序结果
backtest_results.sort(key=lambda x: x[0], reverse=True)

# 选取前三个结果
top_3_results = backtest_results[:3]
end_time = time.time()

for value, buy_expression, sell_expression, sharpe, drawdown in top_3_results:
    print(f"買入策略組合: {buy_expression}, 賣出策略組合: {sell_expression}, 淨收益: {value}, sharpe: {sharpe}, MDD: {drawdown}")

    # 重新运行回测以绘制图表
    backTesting_logic.run_backtest('Crypto/train_data.csv', train_start_date, train_end_date, buy_expression, sell_expression, True)

print('-------------------------------------------------------------------------------')

for value, buy_expression, sell_expression, sharpe, drawdown in top_3_results:

    # 在验证数据集上运行相同的策略
    val_result = backTesting_logic.run_backtest('Crypto/validation_data.csv', validation_start_date, validation_end_date, buy_expression, sell_expression)
    val_value, val_buy_expression, val_sell_expression, val_sharpe, val_drawdown = val_result

    print(f"買入策略組合: {val_buy_expression}, 賣出策略組合: {val_sell_expression}, 淨收益: {val_value}, sharpe: {val_sharpe}, MDD: {val_drawdown}")
    backTesting_logic.run_backtest('Crypto/validation_data.csv', validation_start_date, validation_end_date, buy_expression, sell_expression, True)

print(f"執行時間：{end_time - start_time} 秒")
