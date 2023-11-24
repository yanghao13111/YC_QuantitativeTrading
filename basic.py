import ccxt
import pandas as pd
from datetime import datetime, timedelta

# 創建交易所對象
exchange = ccxt.binance({
    'rateLimit': 1200,
    'enableRateLimit': True,
})

# 設定交易對和時間框架
symbol = 'BTC/USDT'
timeframe = '1h'

# 計算10天前的日期
ten_days_ago = datetime.now() - timedelta(days=10)
since = exchange.parse8601(ten_days_ago.strftime('%Y-%m-%dT%H:%M:%SZ'))

# 獲取數據
ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since)
df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])

# 將 timestamp 轉換為可讀的日期時間格式，並轉換為台灣時區 (UTC+8)
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms').dt.tz_localize('UTC').dt.tz_convert('Asia/Taipei')
df['timestamp'] = df['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')

# 顯示表格
print(df)
