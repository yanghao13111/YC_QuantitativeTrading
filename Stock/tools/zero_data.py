import os
import pandas as pd
import talib

# # 設定資料夾路徑
folder_path = 'Stock/trainDataSet'  # 更改為你的資料夾路徑

def calculate_ema(data, column='close'):
    if len(data) >= 5:
        data['5ema'] = talib.EMA(data[column].values, timeperiod=5)
    if len(data) >= 10:
        data['10ema'] = talib.EMA(data[column].values, timeperiod=10)
    if len(data) >= 22:
        data['22ema'] = talib.EMA(data[column].values, timeperiod=22)
    if len(data) >= 66:
        data['66ema'] = talib.EMA(data[column].values, timeperiod=66)
    if len(data) >= 264:
        data['264ema'] = talib.EMA(data[column].values, timeperiod=264)
    return data

def update_file(file_path):
    # 讀取CSV檔案
    data = pd.read_csv(file_path)
    data['date'] = pd.to_datetime(data['date'])
    
    # 檢查每一行是否開高收低都為0
    for i in range(1, len(data)):
        row = data.iloc[i]
        if row['open'] == 0.0 and row['max'] == 0.0 and row['min'] == 0.0 and row['close'] == 0.0:
            # 如果開高收低都是0，則用前一天的數據替換
            data.iloc[i, data.columns.get_loc('Trading_Volume')] = data.iloc[i-1]['Trading_Volume']
            data.iloc[i, data.columns.get_loc('Trading_money')] = data.iloc[i-1]['Trading_money']
            data.iloc[i, data.columns.get_loc('open')] = data.iloc[i-1]['open']
            data.iloc[i, data.columns.get_loc('max')] = data.iloc[i-1]['max']
            data.iloc[i, data.columns.get_loc('min')] = data.iloc[i-1]['min']
            data.iloc[i, data.columns.get_loc('close')] = data.iloc[i-1]['close']
            data.iloc[i, data.columns.get_loc('spread')] = data.iloc[i-1]['spread']
            data.iloc[i, data.columns.get_loc('Trading_turnover')] = data.iloc[i-1]['Trading_turnover']
    
    # 重新計算EMA
    data = calculate_ema(data)
    
    # 儲存更新後的CSV檔案
    data.to_csv(file_path, index=False)
    print(f"檔案 {file_path} 已更新。")

# 遍歷資料夾中的每個檔案
for file_name in os.listdir(folder_path):
    if file_name.endswith('.csv'):
        update_file(os.path.join(folder_path, file_name))



# for single data update
# file_path = 'Stock/trainDataSet/5438.csv'  # Replace with the path to your file

# # Read the CSV file
# data = pd.read_csv(file_path)
# data['date'] = pd.to_datetime(data['date'])

# # Check each row for open, high, low, close values of 0 and replace with the previous day's data if so
# for i in range(1, len(data)):
#     if data.loc[i, 'open'] == 0.0 and data.loc[i, 'max'] == 0.0 and data.loc[i, 'min'] == 0.0 and data.loc[i, 'close'] == 0.0:
#         data.loc[i, ['Trading_Volume', 'Trading_money', 'open', 'max', 'min', 'close', 'spread', 'Trading_turnover']] = data.loc[i-1, ['Trading_Volume', 'Trading_money', 'open', 'max', 'min', 'close', 'spread', 'Trading_turnover']]

# # Calculate EMA
# data = calculate_ema(data)

# # Save the updated CSV file
# data.to_csv(file_path, index=False)
# print(f"File {file_path} has been updated.")