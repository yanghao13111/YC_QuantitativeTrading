import ccxt
import pandas as pd

exchange = ccxt.binance({
    'rateLimit': 1200,
    'enableRateLimit': True,
})

symbol = 'BTC/USDT'
timeframe = '1h'  # 可以更改為 '1d' 獲取每日數據
since = exchange.parse8601('2022-01-01T00:00:00Z')  # 開始日期

# 獲取數據
ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since)
df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

print(df)
