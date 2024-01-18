# main.py
import pandas as pd
import Stock.backtest.backTesting_logic as backTesting_logic
import indicators
import time
from datetime import datetime, timedelta

def get_dates():
    start_date = datetime(2019, 6, 1)  
    end_date = datetime(2021, 1, 1)  
    return start_date, end_date


def main():
    config = {
        'timeframe': '1d',  
        'buy_expression': f'{indicators.volume_indicator} and {indicators.red_bar} and d.volume[0] > 500 * 1000 and {indicators.bullish_alignment} and {indicators.angle_ema66} > 0 and d.close[0] > d.ema66[0]*1.05 ',
        'sell_expression': f'({indicators.green_bar} or {indicators.upper_wick_length}) and {indicators.volume_5}', 
        'add_expression': f'd.close[0] <= d.ema10[0] and {indicators.angle_ema22} >= 20 and d.close[0] > self.entry_prices[dn] * 1.08' 
    }

    train_start, train_end = get_dates()

    # 讀取 CSV 文件以獲取台灣股票代碼列表
    taiwan_stocks_df = pd.read_csv('Stock/test.csv')  # 替換為你的 CSV 文件路徑
    # 確保股票代碼為字符串格式
    taiwan_stocks = taiwan_stocks_df['StockID'].apply(lambda x: f"{x}").tolist()

    # 創建數據文件路徑列表
    data_folder = 'Stock/trainDataSet'  # 設定你的數據集文件夾路徑
    data_files = [f'{data_folder}/{stock}.csv' for stock in taiwan_stocks]  # 假設每個股票的數據文件名是 '{股票代碼}.csv'

    start_time = time.time()
    result = backTesting_logic.run_backtest(data_files, train_start, train_end, config['buy_expression'], config['sell_expression'], config['add_expression'], verbose=True)

    value, buy_expression, sell_expression, sharpe, drawdown, best_trades, worst_trades, win_rate, total_trades = result
    print(f"買入策略組合: {buy_expression}, \n賣出策略組合: {sell_expression}, \n淨收益: {value}, \nsharpe: {sharpe}, \nMDD: {drawdown}, \nwin_rate: {win_rate*100}%, \ntotal_trades: {total_trades}")

    # 格式化輸出
    print("Worst Trades:")
    for trade in worst_trades:
        print(f"Name: {trade['name']}, Profit: {trade['profit']}, Profit Ratio: {trade['profit_ratio']*100}%")

    # 格式化輸出
    print("Best Trades:")
    for trade in best_trades:
        print(f"Name: {trade['name']}, Profit: {trade['profit']}, Profit Ratio: {trade['profit_ratio']*100}%")

    end_time = time.time()
    print(f"執行時間：{end_time - start_time} 秒")

    for i in range(len(worst_trades)):
        data_file = [f'{data_folder}/{worst_trades[i]["name"]}.csv']
        result = backTesting_logic.run_backtest(data_file, train_start, train_end, config['buy_expression'], config['sell_expression'], config['add_expression'], plot=True, verbose=False)

    for i in range(len(best_trades)):
        data_file = [f'{data_folder}/{best_trades[i]["name"]}.csv']
        result = backTesting_logic.run_backtest(data_file, train_start, train_end, config['buy_expression'], config['sell_expression'], config['add_expression'], plot=True, verbose=False)

if __name__ == "__main__":
    main()
