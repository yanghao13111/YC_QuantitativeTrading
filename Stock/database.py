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
        ((abs((df['EMA5'] - df['EMA10']) / df['EMA10']) < 0.03) & (abs((df['EMA10'] - df['EMA22']) / df['EMA22']) < 0.03)) &
        (df['Volume'] > 2 * df['Volume'].shift(1))
    )

    # 只返回最後一行（即今天）的數據
    return df[condition].tail(1)

# 讀取 CSV 文件以獲取台灣股票代碼列表
taiwan_stocks_df = pd.read_csv('Stock/taiwan_stock_codes.csv')  # 替換為您的 CSV 文件路徑
# 確保股票代碼為字串格式並添加 ".TW"
taiwan_stocks = taiwan_stocks_df['Stock Code'].apply(lambda x: f"{x}.TW").tolist()

# 篩選股票
selected_stocks = {symbol: screen_stock(symbol) for symbol in taiwan_stocks}

# 印出今天符合條件的股票代碼
print("今天符合條件的股票代碼:")
for symbol, data in selected_stocks.items():
    if data is not None and not data.empty:
        print(symbol)
