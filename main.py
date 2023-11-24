# main.py
import data_collection
import backTesting_logic
from datetime import datetime, timedelta

# 假設這裡是一些參數設置
symbol = 'BTC/USDT'
timeframe = '1h'
since = '2023-01-01T00:00:00Z'

# 計算10天前的日期
ten_days_ago = datetime.utcnow() - timedelta(days=10)
since = ten_days_ago.strftime('%Y-%m-%dT%H:%M:%SZ')

# 調用數據搜集
df = data_collection.collect_data(symbol, timeframe, since)

# 保存數據供回測使用
df.to_csv('market_data.csv', index=False)

# 調用回測邏輯
backTesting_logic.backtest_strategy(df)
