import pandas as pd
import os

# trainDataSet 資料夾的路徑
folder_path = 'Stock/trainDataSet'

# 初始化一個字典來存儲股票代號和其對應的資料行數
stock_row_counts = {}

# 遍歷資料夾中的所有CSV文件
for file_name in os.listdir(folder_path):
    if file_name.endswith('.csv'):
        stock_id = file_name.replace('.csv', '')
        file_path = os.path.join(folder_path, file_name)
        try:
            data = pd.read_csv(file_path)
            row_count = len(data)
            stock_row_counts[stock_id] = row_count
        except Exception as e:
            print(f"處理 {file_path} 時出現錯誤: {e}")

# 將結果轉換為DataFrame
row_counts_df = pd.DataFrame(list(stock_row_counts.items()), columns=['StockID', 'RowCount'])

# 首先根据StockID进行稳定排序
row_counts_df.sort_values('StockID', inplace=True, kind='mergesort')

# 根據行數進行稳定排序，由大到小
row_counts_df.sort_values('RowCount', inplace=True, ascending=False, kind='mergesort')

# 保存到CSV文件
row_counts_df.to_csv('Stock/tools/csv_number.csv', index=False)
