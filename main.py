# main.py
import data_collection
import backTesting_logic
from datetime import datetime, timedelta


# 參數設置
symbol = 'BTC/USDT'
timeframe = '1h'
ten_days_ago = datetime.utcnow() - timedelta(days=10) # 計算10天前的日期
since = ten_days_ago.strftime('%Y-%m-%dT%H:%M:%SZ')

# 調用數據搜集
df = data_collection.collect_data(symbol, timeframe, since)

# 保存數據供回測使用
df.to_csv('market_data.csv', index=False)

# 調用回測邏輯
backTesting_logic.run_backtest('market_data.csv', datetime(2023, 11, 14), datetime(2023, 11, 24))