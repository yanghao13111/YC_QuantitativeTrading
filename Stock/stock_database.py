from FinMind.data import DataLoader
import pandas as pd
import os
from datetime import datetime, timedelta
import talib

class StockDatabase:
    # # account: (user_id, password)
    def __init__(self, user_id, password):
        self.data_loader = DataLoader()
        self.data_loader.login(user_id=user_id, password=password)

    # # token
    # def __init__(self, token):
    #     self.data_loader = DataLoader()
    #     self.data_loader.login_by_token(api_token=token)

    def get_stock_price(self, stock_id, start_date, end_date):
        return self.data_loader.taiwan_stock_daily(stock_id, start_date, end_date)

    def fetch_and_save_stock_data(self, stock_list, start_date, end_date, folder_path):
        for stock_id in stock_list:
            try:
                stock_data = self.get_stock_price(stock_id, start_date, end_date)
                stock_data['date'] = pd.to_datetime(stock_data['date'])
                required_columns = ['date', 'open', 'close', 'max', 'min', 'Trading_Volume']
                if all(column in stock_data.columns for column in required_columns):
                    file_name = f"{stock_id}.csv"
                    file_path = os.path.join(folder_path, file_name)
                    stock_data.to_csv(file_path, index=False)
                    print(f"為 {stock_id} 儲存資料於 {file_path}")
                else:
                    print(f"{stock_id} 的資料缺少所需的欄位")
            except Exception as e:
                print(f"提取 {stock_id} 資料時出錯：{e}")

    def calculate_ema(self, data, column='close'):
        """
        Calculate EMAs for 5, 10, 22, 66, and 264 days if enough data is present.
        Adds the EMAs as new columns to the dataframe.
        """
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

    def update_stock_data(self, stock_list, folder_path):
        for stock_id in stock_list:
            file_path = os.path.join(folder_path, f"{stock_id}.csv")
            try:
                if os.path.exists(file_path):
                    # 讀取現有數據並找到最後一筆數據的日期
                    existing_data = pd.read_csv(file_path)
                    existing_data['date'] = pd.to_datetime(existing_data['date'])
                    last_date = existing_data['date'].max()

                    # 設置更新的起始日期為最後一筆數據日期的次日
                    start_date = (last_date + timedelta(days=1)).strftime('%Y-%m-%d')
                else:
                    # 如果文件不存在，從較早的日期開始更新
                    start_date = "2008-01-01"
                
                # 設置結束日期為今天
                end_date = datetime.now().strftime('%Y-%m-%d')

                # 獲取新數據
                new_data = self.get_stock_price(stock_id, start_date, end_date)
                new_data['date'] = pd.to_datetime(new_data['date'])

                # 檢查並儲存最新一筆數據
                if not new_data.empty:
                    # 合併舊數據和新數據
                    full_data = pd.concat([existing_data, new_data], ignore_index=True)
                    # 計算EMA
                    full_data = self.calculate_ema(full_data)
                    # 儲存數據
                    full_data.to_csv(file_path, index=False)
                    print(f"為 {stock_id} 更新數據並計算EMA至 {file_path}")
                else:
                    print(f"{stock_id} 沒有新的數據可更新")
            except Exception as e:
                print(f"更新 {stock_id} 資料時出錯：{e}")

def read_stock_ids_from_excel(file_path):
    data = pd.read_csv(file_path)
    stock_ids = data['StockID'].tolist()
    return stock_ids

def split_list(alist, wanted_parts=1):
    length = len(alist)
    return [ alist[i*length // wanted_parts: (i+1)*length // wanted_parts] 
             for i in range(wanted_parts) ]

if __name__ == "__main__":
    # 讀取股票代號
    excel_path = 'Stock/taiwan_stock_codes.csv'
    stock_list = read_stock_ids_from_excel(excel_path)

    # 將股票代號分成三等份
    stock_lists = split_list(stock_list, 3)

    # 檢查每一個part的數量
    for i, part in enumerate(stock_lists):
        print(f"第 {i+1} 部分有 {len(part)} 個股票代號。")

    # 檢查每一個part的股票代號
    print(stock_lists[2])
    # for i, part in enumerate(stock_lists):
    #     print(f"第 {i+1} 部分的股票代號：{part}")

    # 為每個部分創建一個 StockDatabase 實例並登錄
    accounts = [
        ('YC_Company', '@qazwsxedc123'),
        ('YC_Company2', '@qazwsxedc123'),
        ('YC_Company3', '@qazwsxedc123')
    ]

    stock_db = StockDatabase('YC_Company2', '@qazwsxedc123')
    stock_db.update_stock_data([8432, 8433, 8435, 8436, 8437, 8438, 8440, 8442, 8443, 8444, 8446, 8450, 8454, 8455, 8462, 8463, 8464, 8466, 8467, 8472, 8473, 8476, 8477, 8478, 8481, 8482, 8488, 8489, 8499, 8905, 8906, 8908, 8916, 8917, 8921, 8923, 8924, 8926, 8927, 8928, 8929, 8930, 8931, 8932, 8933, 8935, 8936, 8937, 8938, 8940, 8941, 8942, 8996, 9105, 9802, 9902, 9904, 9905, 9906, 9907, 9908, 9910, 9911, 9912, 9914, 9917, 9918, 9919, 9921, 9924, 9925, 9926, 9927, 9928, 9929, 9930, 9931, 9933, 9934, 9935, 9937, 9938, 9939, 9940, 9941, 9942, 9943, 9944, 9945, 9946, 9949, 9950, 9951, 9955, 9958, 9960, 9962, 911608, 911622], "Stock/trainDataSet")

    api_tokens = [
        'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRlIjoiMjAyNC0wMS0wMiAxNjowNzoxOCIsInVzZXJfaWQiOiJZQ19Db21wYW55IiwiaXAiOiIxMTQuMzMuNy4xMTYifQ.4KDQU_-oQiy5eKDek3-4EyBCA7EEdRwbCjXvkdi9UTM',  # 將這些值替換為您的實際 API 令牌
        'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRlIjoiMjAyNC0wMS0wMiAxNjowNjozNiIsInVzZXJfaWQiOiJZQ19Db21wYW55MiIsImlwIjoiMTE0LjMzLjcuMTE2In0.5DmMY73riuTlRBCbT2N4v0RmCQLMCJbSfM7cagWMNkU',
        'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRlIjoiMjAyNC0wMS0wMiAxNTo0NjowNyIsInVzZXJfaWQiOiJZQ19Db21wYW55MyIsImlwIjoiMTE0LjMzLjcuMTE2In0.z-uIQoQbsEp40EcXzCkSapMb2rMB1U743E3OY2ss5Aw'
    ]

    # 分批抓取資料
    # for i, part in enumerate(stock_lists):
    #     if i == 0 or i == 1:
    #         continue
    #     user_id, password = accounts[i]
    #     stock_db = StockDatabase(user_id, password)
    #     # stock_db.fetch_and_save_stock_data(part, "2008-01-01", "2024-01-02", "Stock/trainDataSet")
    #     stock_db.update_stock_data(part, "Stock/trainDataSet")
    #     print(f"已完成第 {i+1} 批的資料抓取。")
