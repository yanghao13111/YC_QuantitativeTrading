import pandas as pd
import os

def get_first_date_of_stock(file_path):
    try:
        data = pd.read_csv(file_path)
        data['date'] = pd.to_datetime(data['date'])
        return data['date'].min()
    except Exception as e:
        print(f"處理 {file_path} 時出現錯誤: {e}")
        return None

# trainDataSet 資料夾的路徑
folder_path = 'Stock/trainDataSet'

# 初始化一個字典來存儲股票代號和其第一筆資料的日期
stock_first_date = {}

# 遍歷資料夾中的所有CSV文件
for file_name in os.listdir(folder_path):
    if file_name.endswith('.csv'):
        stock_id = file_name.replace('.csv', '')
        file_path = os.path.join(folder_path, file_name)
        first_date = get_first_date_of_stock(file_path)
        if first_date:
            stock_first_date[stock_id] = first_date

# 將結果轉換為DataFrame
first_dates_df = pd.DataFrame(list(stock_first_date.items()), columns=['StockID', 'FirstDate'])

# 首先根据StockID进行稳定排序
first_dates_df.sort_values('StockID', inplace=True, kind='mergesort')

# 然后根据FirstDate进行稳定排序
first_dates_df.sort_values('FirstDate', inplace=True, kind='mergesort')

print(first_dates_df)

# 保存到Excel文件
first_dates_df.to_csv('Stock/tools/stock_date.csv', index=False)
