from FinMind.data import DataLoader
import pandas as pd
import os
from datetime import datetime

class StockDatabase:
    def __init__(self):
        self.data_loader = DataLoader()

    def get_stock_price(self, stock_id, start_date, end_date):
        return self.data_loader.taiwan_stock_daily(stock_id, start_date, end_date)

    def fetch_and_save_stock_data(self, stock_list, start_date, end_date, folder_path):
        for stock_id in stock_list:
            try:
                stock_data = self.get_stock_price(stock_id, start_date, end_date)
                # 確保日期欄位是 datetime 物件
                stock_data['date'] = pd.to_datetime(stock_data['date'])
                # 確保資料包含所需的欄位
                required_columns = ['date', 'open', 'close', 'max', 'min', 'Trading_Volume']
                if all(column in stock_data.columns for column in required_columns):
                    # 為每個股票代號儲存整個資料集
                    file_name = f"{stock_id}.csv"
                    file_path = os.path.join(folder_path, file_name)
                    stock_data.to_csv(file_path, index=False)
                    print(f"為 {stock_id} 儲存資料於 {file_path}")
                else:
                    print(f"{stock_id} 的資料缺少所需的欄位")
            except Exception as e:
                print(f"提取 {stock_id} 資料時出錯：{e}")

# 使用範例
stock_db = StockDatabase()
stock_list = ["2330", "2317", "1301"]  # 股票代號列表
stock_db.fetch_and_save_stock_data(stock_list, "2013-01-01", "2023-01-01", "Stock/trainDataSet")
