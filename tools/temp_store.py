# main.py

# 時間範圍設置 method1: datetime
# start_date = datetime.utcnow() - timedelta(days=365) 
# end_date = datetime.utcnow()

# 時間範圍設置 method2: str to datetime
# start_date_str = '2022-11-24'
# end_date_str = '2023-11-24'  
# start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
# end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

# # 調用數據搜集
# df = data_collection.collect_data(symbol, timeframe, start_date, end_date)

# # 保存數據供回測使用
# df.to_csv('market_data.csv', index=False)