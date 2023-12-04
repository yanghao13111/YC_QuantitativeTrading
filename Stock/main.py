import yfinance as yf
from joblib import Parallel, delayed
import data_collection
from datetime import datetime, timedelta
import time
import backTesting_logic

# 參數設置
ticker = "2330.TW"
interval = "1h"
# from_date = "2023-11-01"
# to_date = "2023-12-04"

#---------indicators expression----------#
# ma
A = "self.data.close[0] > self.sma25[0]"
B = "self.data.close[0] > self.sma50[0]"
C = "self.data.close[0] > self.sma100[0]"
G = "self.data.close[0] < self.sma25[0]"
H = "self.data.close[0] < self.sma50[0]" 
I = "self.data.close[0] < self.sma100[0]"

# macd
M = "self.macd.macd[0] > self.macd.signal[0]"
N = "self.macd.macd[0] < self.macd.signal[0]"
# rsi
O = "self.rsi[0] > 70"
P = "self.rsi[0] < 30"
# stoch
Q = "self.stoch[0] > 80"
R = "self.stoch[0] < 20"
# Maximum is 9
conditions = [A, B, C, M, N]
# Approximately equal to conditions/2
combined_number = 3

# # 收集數據
# 训练数据时间范围
train_start_date = datetime.utcnow() - timedelta(days=70)
train_end_date = datetime.utcnow() - timedelta(days=36)

# 验证数据时间范围
validation_start_date = datetime.utcnow() - timedelta(days=35)
validation_end_date = datetime.utcnow()

# 訓練數據搜集
df_train = data_collection.collect_data(ticker,train_start_date, train_end_date, interval)
df_train.to_csv('train_data.csv', index=False)

# 驗證數據搜集
df_validation = data_collection.collect_data(ticker, validation_start_date, validation_end_date, interval)
df_validation.to_csv('validation_data.csv', index=False)

start_time = time.time()
expressions = backTesting_logic.generate_expressions(conditions, combined_number)

# # 使用 joblib 平行處理回測
def run_single_backtest(expr):
    return backTesting_logic.run_backtest('train_data.csv', train_start_date, train_end_date, expr)

backtest_results = Parallel(n_jobs=-1)(delayed(run_single_backtest)(expr) for expr in expressions)

# 根据资产价值排序结果
backtest_results.sort(key=lambda x: x[0], reverse=True)

# 选取前三个结果
top_3_results = backtest_results[:3]

for value, expr, sharpe, drawdown in top_3_results:
    print(f"策略組合: {expr}, 淨收益: {value}, sharpe: {sharpe}, MDD: {drawdown}")

    # 重新运行回测以绘制图表
    backTesting_logic.run_backtest('train_data.csv', train_start_date, train_end_date, expr, True)

print('-------------------------------------------------------------------------------')

for value, expr, sharpe, drawdown in top_3_results:

    # 在验证数据集上运行相同的策略
    val_result = backTesting_logic.run_backtest('validation_data.csv', validation_start_date, validation_end_date, expr)
    val_value, val_expr, val_sharpe, val_drawdown = val_result

    print(f"策略組合: {val_expr}, 淨收益: {val_value}, sharpe: {val_sharpe}, MDD: {val_drawdown}")
    backTesting_logic.run_backtest('validation_data.csv', validation_start_date, validation_end_date, expr, True)

end_time = time.time()
print(f"执行时间：{end_time - start_time} 秒")