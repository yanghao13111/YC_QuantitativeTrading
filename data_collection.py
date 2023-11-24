# data_collection.py
import ccxt
import pandas as pd
from datetime import datetime, timedelta

def collect_data(symbol, timeframe, since):
    exchange = ccxt.binance({
        'rateLimit': 1200,
        'enableRateLimit': True,
    })

    # 將 since 從 ISO 8601 字符串轉換為毫秒時間戳記
    since_timestamp = exchange.parse8601(since)

    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since_timestamp)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    
    # 將 timestamp 轉換為可讀的日期時間格式，並轉換為台灣時區 (UTC+8)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms').dt.tz_localize('UTC').dt.tz_convert('Asia/Taipei')
    df['timestamp'] = df['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
    return df


# 例如：搜集BTC/USDT的數據
df = collect_data('BTC/USDT', '1h', '2023-01-01T00:00:00Z')
df.to_csv('market_data.csv', index=False)