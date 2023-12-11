import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def calculate_ema(prices, span):
    """
    計算指數移動平均線(EMA)
    """
    return prices.ewm(span=span, adjust=False).mean()

def screen_stock(symbol):
    """
    篩選單一股票
    """
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=100)

    # 獲取股票數據
    df = yf.download(symbol, start=start_date, end=end_date)

    if df.empty:
        return None

    # 計算各 EMA
    df['EMA5'] = calculate_ema(df['Close'], 5)
    df['EMA10'] = calculate_ema(df['Close'], 10)
    df['EMA22'] = calculate_ema(df['Close'], 22)
    df['EMA66'] = calculate_ema(df['Close'], 66)

    # 條件判斷
    condition = (
        (df['EMA5'] > df['EMA10']) &
        (df['EMA10'] > df['EMA22']) &
        (df['EMA22'] > df['EMA66']) &
        (df['EMA5'] > df['EMA5'].shift(1)) &
        (df['EMA10'] > df['EMA10'].shift(1)) &
        (df['EMA22'] > df['EMA22'].shift(1)) &
        (df['EMA66'] > df['EMA66'].shift(1)) &
        ((abs((df['EMA10'] - df['EMA22']) / df['EMA22']) < 0.03) | (abs((df['EMA22'] - df['EMA66']) / df['EMA66']) < 0.03))
    )

    # 只返回最後一行（即今天）的數據
    return df[condition].tail(1)


# 篩選股票
screen_stock('2331.TW')
