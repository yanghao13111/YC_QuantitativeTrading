import ccxt
import pandas as pd
from datetime import datetime

def collect_data(symbol, timeframe):
    exchange = ccxt.binance({
        'rateLimit': 1200,
        'enableRateLimit': True,
    })

    limit = 1000  # 每次请求的数据点数上限
    now = datetime.utcnow()
    since = exchange.parse8601((now - pd.Timedelta(days=365)).isoformat())  # 近一年的数据

    all_data = []

    while True:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since=since, limit=limit)
        if not ohlcv:
            break
        all_data.extend(ohlcv)
        since = ohlcv[-1][0] + 1  # 准备下一个请求
        if len(ohlcv) < limit:
            break  # 如果返回的数据点少于请求的限制，说明已经到达数据的末尾

    df = pd.DataFrame(all_data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms').dt.tz_localize('UTC').dt.tz_convert('Asia/Taipei')
    df['timestamp'] = df['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')

    return df
