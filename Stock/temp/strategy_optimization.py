# main.py
import pandas as pd
import Stock.backtest.backTesting_logic as backTesting_logic
import indicators
from datetime import datetime, timedelta
from tqdm import tqdm
from joblib import Parallel, delayed

def get_dates():
    start_date = datetime(2019, 1, 1)  
    end_date = datetime(2022, 12, 31)  
    return start_date, end_date

def run_single_backtest(i, data_files, train_start, train_end):
    buy_expression =  f'{indicators.bullish_alignment} and d.ema22[0] > d.ema264[0] and {indicators.allup} and {indicators.divergence_5_10} > 0.01 and {indicators.divergence_5_10} < 0.05 and {indicators.divergence_10_22} > 0.01 and {indicators.divergence_10_22} < 0.05 and {indicators.divergence_22_66} > 0.01 and {indicators.divergence_22_66} < 0.05 and {indicators.divergence_22_264} < 0.1 and {indicators.volume_indicator} and d.volume[0] > 500 * 1000'
    sell_expression = f'{indicators.angle_ema22} <= -5 or {indicators.loss_condition}'
    add_expression = f'{False}'
    result = backTesting_logic.run_backtest(data_files, train_start, train_end, buy_expression, sell_expression, add_expression, verbose=False)
    return (result, i)

def main():

    train_start, train_end = get_dates()

    # 讀取 CSV 文件以獲取台灣股票代碼列表
    taiwan_stocks_df = pd.read_csv('Stock/test.csv')  # 替換為你的 CSV 文件路徑
    # 確保股票代碼為字符串格式
    taiwan_stocks = taiwan_stocks_df['StockID'].apply(lambda x: f"{x}").tolist()

    # 創建數據文件路徑列表
    data_folder = 'Stock/trainDataSet'  # 設定你的數據集文件夾路徑
    data_files = [f'{data_folder}/{stock}.csv' for stock in taiwan_stocks]  # 假設每個股票的數據文件名是 '{股票代碼}.csv'

    # 使用 joblib 并行化
    num_cores = -1  # 使用所有可用核心
    results = Parallel(n_jobs=num_cores)(delayed(run_single_backtest)(i, data_files, train_start, train_end) for i in range(-6, -4))

    # 处理并打印结果
    for result, i in results:
        value, buy_expression, sell_expression, sharpe, drawdown, best_trades, worst_trades, win_rate, total_trades = result
        print(f"i: {i}, \n淨收益: {value}, \nsharpe: {sharpe}, \nMDD: {drawdown}, \nwin_rate: {win_rate*100}%, \ntotal_trades: {total_trades}")

        # 格式化輸出
        print("Worst Trades:")
        for trade in worst_trades:
            print(f"Name: {trade['name']}, Profit: {trade['profit']}, Profit Ratio: {trade['profit_ratio']*100}%")

        # 格式化輸出
        print("Best Trades:")
        for trade in best_trades:
            print(f"Name: {trade['name']}, Profit: {trade['profit']}, Profit Ratio: {trade['profit_ratio']*100}%")
        print("------------------------------------")

if __name__ == "__main__":
    main()
