from FinMind.data import DataLoader
import pandas as pd
import os
from datetime import datetime

class StockDatabase:
    def __init__(self, user_id, password):
        self.data_loader = DataLoader()
        self.data_loader.login(user_id=user_id, password=password)

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



if __name__ == "__main__":
    # 創建 StockDatabase 的實例，並登錄
    user_id = 'YC_Company'  # 用您的帳號替換
    password = '@qazwsxedc123'  # 用您的密碼替換
    stock_db = StockDatabase(user_id, password)

    # 獲取所有台灣股票代號的列表
    taiwan_stock_datalist = stock_db.data_loader.get_datalist(dataset='TaiwanStockInfo')
    stock_list = [data['stock_id'] for data in taiwan_stock_datalist['data']]
    print(f"台灣股票代號總共有 {len(stock_list)} 個")

# taiwan_stock_list = stock_db.data_loader.taiwan_stock_list()
# stock_list = taiwan_stock_list['stock_id'].tolist()
# print(f"台灣股票代號總共有 {len(stock_list)} 個")

# 抓取資料
# stock_db.fetch_and_save_stock_data(stock_list, "2013-01-01", "2023-01-01", "Stock/trainDataSet")
