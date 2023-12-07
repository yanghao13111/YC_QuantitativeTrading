import ccxt
import pandas as pd
import pytz
from datetime import datetime

def collect_data(symbol, timeframe, start_date, end_date):
    exchange = ccxt.binance({
        'rateLimit': 1200,
        'enableRateLimit': True,
    })

    limit = 1000  # 每次请求的数据点数上限
    
    # 转换为 UTC 时间并格式化为 ISO 8601
    since = int(start_date.astimezone(pytz.utc).timestamp()) * 1000
    end = int(end_date.astimezone(pytz.utc).timestamp()) * 1000

    all_data = []

    while since < end:
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
