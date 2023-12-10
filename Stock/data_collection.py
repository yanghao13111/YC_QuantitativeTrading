import yfinance as yf
import pandas as pd

# 參數設置
# ticker = "2330.TW"
# interval = "1h"
# from_date = "2023-11-01"
# to_date = "2023-12-04"

def collect_data(symbol, timeframe, start_date, end_date):
    stock = yf.Ticker(symbol)
    hist_data = stock.history(start=start_date, end=end_date, interval=timeframe)

    # 因為 yfinance 已經返回了一個 DataFrame，所以我們直接操作它
    # 重命名 DataFrame 的索引列名稱為 'Datetime'
    if isinstance(hist_data.index, pd.DatetimeIndex) and hist_data.index.tz is not None:
        hist_data.index = hist_data.index.tz_localize(None) 
    hist_data.reset_index(inplace=True)
    hist_data.rename(columns={'Date': 'Datetime'}, inplace=True)


    # 重命名其他列（如果需要）
    hist_data.rename(columns={
        'Open': 'Open',
        'High': 'High',
        'Low': 'Low',
        'Close': 'Close',
        'Volume': 'Volume'
    }, inplace=True)

    # 四捨五入到小數點第一位（如果需要）
    hist_data = hist_data.round(1)

    return hist_data

# df_train = collect_data(ticker,from_date, to_date, interval)
# print(df_train)
# df_train.to_csv('Stock/train_data.csv', index=True)