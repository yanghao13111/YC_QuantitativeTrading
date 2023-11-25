# main.py
import data_collection
import backTesting_logic
from datetime import datetime, timedelta


# 參數設置
symbol = 'BTC/USDT'
timeframe = '1h'

# 調用數據搜集
df = data_collection.collect_data(symbol, timeframe)

# 保存數據供回測使用
df.to_csv('market_data.csv', index=False)

# 調用回測邏輯
backTesting_logic.run_backtest('market_data.csv', datetime(2022, 11, 24), datetime(2023, 11, 24))