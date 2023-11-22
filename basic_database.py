import yfinance as yf

# 取得歷史資料
stock = yf.Ticker("2330.TW")  # 取得個股資料，以台積電為例，股票代號後加上.TW
hist_data = stock.history(period="1y")  # 獲取歷史數據 'max'獲取全部可用歷史數據，也可以指定其他範圍，如"1y"表示一年

# 整理數據
hist_data = hist_data.drop(columns=['Dividends', 'Stock Splits']) # 移除 'Dividends' 和 'Stock Splits' 欄位
hist_data.index = hist_data.index.tz_localize(None) # 移除時區信息
hist_data = hist_data.round(1) # 將所有數值欄位四捨五入到小數點第一位

# 顯示數據
print(hist_data) # 顯示數據

# 輸出
hist_data.to_csv("2330_data.csv") # 輸出成CSV檔
