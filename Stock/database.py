import pandas as pd
from datetime import datetime, timedelta

# # 獲取今天的日期，格式化為 'YYYY-MM-DD'，與數據中的日期格式相匹配
# today = datetime.today().strftime('%Y-%m-%d')

# 指定日期為 2023年1月1日
specified_date = '2024-01-04'

def calculate_ema(prices, span):
    """
    計算指數移動平均線(EMA)
    """
    return prices.ewm(span=span, adjust=False).mean()

def screen_stock(symbol, data_folder):
    """
    篩選單一股票
    """
    # 假設每個股票的數據存儲在一個單獨的 CSV 文件中，文件名為股票代碼
    file_path = f"{data_folder}/{symbol}.csv"  # 確保路徑與文件名格式正確

    try:
        # 讀取股票數據
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"File not found for {symbol}")
        return None

    if df.empty:
        return None
    

    # 選取最近365天的數據
    df = df.tail(365)

    # 計算各 EMA
    df['EMA5'] = calculate_ema(df['close'], 5)
    df['EMA10'] = calculate_ema(df['close'], 10)
    df['EMA22'] = calculate_ema(df['close'], 22)
    df['EMA66'] = calculate_ema(df['close'], 66)
    df['EMA264'] = calculate_ema(df['close'], 264)

    # 條件判斷
    condition = (
        (df['EMA5'] > df['EMA10']) &
        (df['EMA10'] > df['EMA22']) 
    )

    # 只返回最後一行（即今天）的數據
    return df[condition].tail(1)

# 讀取 CSV 文件以獲取台灣股票代碼列表
taiwan_stocks_df = pd.read_csv('Stock/taiwan_stock_codes.csv')  # 替換為您的 CSV 文件路徑
# 確保股票代碼為字串格式並添加 ".TW"
taiwan_stocks = taiwan_stocks_df['Stock Code'].apply(lambda x: f"{x}").tolist()

data_folder = 'Stock/trainDataSet'  # 設定你的數據集文件夾路徑

# 篩選股票
selected_stocks = {symbol: screen_stock(symbol, data_folder) for symbol in taiwan_stocks}

# 印出今天符合條件的股票代碼
print("今天符合條件的股票代碼:")
for symbol, data in selected_stocks.items():
    if data is not None and not data.empty and data.iloc[-1]['date'] == specified_date:
        print(symbol)
