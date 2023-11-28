# main.py
import data_collection
import backTesting_logic
from datetime import datetime, timedelta
import time


# 參數設置
symbol = 'BTC/USDT'
timeframe = '1h'

# 時間範圍設置
start_date = datetime.utcnow() - timedelta(days=365)
end_date = datetime.utcnow()

# 調用數據搜集
df = data_collection.collect_data(symbol, timeframe, start_date, end_date)

# 保存數據供回測使用
df.to_csv('market_data.csv', index=False)

start_time = time.time()
# indicators expression
A = "self.data.close[0] > self.sma5[0]"
B = "self.data.close[0] > self.sma10[0]"
C = "self.data.close[0] > self.sma20[0]"
D = "self.data.close[0] > self.sma60[0]"
E = "self.data.close[0] > self.sma120[0]"
F = "self.data.close[0] > self.sma240[0]" 
G = "self.data.close[0] < self.sma5[0]"
H = "self.data.close[0] < self.sma10[0]" 
I = "self.data.close[0] < self.sma20[0]"
J = "self.data.close[0] < self.sma60[0]"
K = "self.data.close[0] < self.sma120[0]"
L = "self.data.close[0] < self.sma240[0]"

conditions = [E, F, G, H]
expressions = backTesting_logic.generate_expressions(conditions)


# 創建一個列表来存储每次回测的结果
backtest_results = []

# 对每个生成的表达式运行回测
for expr in expressions:
    result = backTesting_logic.run_backtest('market_data.csv', start_date, end_date, expr)
    backtest_results.append(result)


# 根据资产价值排序结果
backtest_results.sort(key=lambda x: x[0], reverse=True)

# 选取前三个结果
top_3_results = backtest_results[:3]

for value, expr, sharpe, drawdown in top_3_results:
    print(f"策略組合: {expr}, 淨收益: {value}, sharpe: {sharpe}, MDD: {drawdown}")

    # # 重新运行回测以绘制图表
    # backTesting_logic.run_backtest('market_data.csv', start_date, end_date, expr, True)

end_time = time.time()
print(f"执行时间：{end_time - start_time} 秒")
