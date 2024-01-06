import os
import pandas as pd
import talib

# 設定資料夾路徑
folder_path = 'Stock/trainDataSet'  # 更改為你的資料夾路徑

# 列出資料夾內所有檔案
files = os.listdir(folder_path)

# 遍歷每個檔案
for file in files:
    if file.endswith('.csv'):
        file_path = os.path.join(folder_path, file)
        df = pd.read_csv(file_path)
        
        # 檢查是否有足夠的數據點來計算每個EMA
        if len(df) >= 5:
            df['5ema'] = talib.EMA(df['close'], timeperiod=5)
        if len(df) >= 10:
            df['10ema'] = talib.EMA(df['close'], timeperiod=10)
        if len(df) >= 22:
            df['22ema'] = talib.EMA(df['close'], timeperiod=22)
        if len(df) >= 66:
            df['66ema'] = talib.EMA(df['close'], timeperiod=66)
        if len(df) >= 264:
            df['264ema'] = talib.EMA(df['close'], timeperiod=264)
        
        # 將更新後的數據儲存回CSV檔案
        df.to_csv(file_path, index=False)
