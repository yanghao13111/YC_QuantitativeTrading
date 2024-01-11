# main.py
import pandas as pd
import backTesting_logic
from datetime import datetime, timedelta

def get_dates():
    start_date = datetime(2019, 1, 1)  
    end_date = datetime(2022, 12, 31)  
    return start_date, end_date


def main():
    config = {
        'timeframe': '1d',  
        'buy_expression': 'self.ema5[0] > self.ema10[0] and self.ema10[0] > self.ema22[0] and self.ema22[0] > self.ema66[0] and self.ema22[0] > self.ema264[0] and self.ema5[0] > self.ema5[-1] and self.ema10[0] > self.ema10[-1] and self.ema22[0] > self.ema22[-1] and self.ema66[0] > self.ema66[-1] and self.ema264[0] > self.ema264[-1] and (abs(self.ema5[0] - self.ema10[0]) / self.ema10[0] > 0.01) and (abs(self.ema5[0] - self.ema10[0]) / self.ema10[0] < 0.05) and (abs(self.ema10[0] - self.ema22[0]) / self.ema22[0] > 0.01) and (abs(self.ema10[0] - self.ema22[0]) / self.ema22[0] < 0.05) and (abs(self.ema22[0] - self.ema66[0]) / self.ema66[0] > 0.01) and (abs(self.ema22[0] - self.ema66[0]) / self.ema66[0] < 0.05) and (abs(self.ema22[0] - self.ema264[0]) / self.ema264[0] < 0.1) and self.volume[0] > 2 * self.volume[-1] and self.volume[0] > 500 * 1000',
        'sell_expression': 'angle_ema22 <= 0'
    }

    train_start, train_end = get_dates()

    # 讀取 CSV 文件以獲取台灣股票代碼列表
    taiwan_stocks_df = pd.read_csv('Stock/test.csv')  # 替換為你的 CSV 文件路徑
    # 確保股票代碼為字符串格式
    taiwan_stocks = taiwan_stocks_df['StockID'].apply(lambda x: f"{x}").tolist()

    # 創建數據文件路徑列表
    data_folder = 'Stock/trainDataSet'  # 設定你的數據集文件夾路徑
    data_files = [f'{data_folder}/{stock}.csv' for stock in taiwan_stocks]  # 假設每個股票的數據文件名是 '{股票代碼}.csv'

    result = backTesting_logic.run_backtest(data_files, train_start, train_end, config['buy_expression'], config['sell_expression'], verbose=False)

    value, buy_expression, sell_expression, sharpe, drawdown, best_trades, worst_trades = result
    print(f"買入策略組合: {buy_expression}, \n賣出策略組合: {sell_expression}, \n淨收益: {value}, \nsharpe: {sharpe}, \nMDD: {drawdown}, \nbest_trades: {best_trades}, \nworst_trades: {worst_trades}")

    for i in range(len(worst_trades)):
        data_file = [f'{data_folder}/{worst_trades[i]["name"]}.csv']
        result = backTesting_logic.run_backtest(data_file, train_start, train_end, config['buy_expression'], config['sell_expression'], plot=True, verbose=False)

    for i in range(len(best_trades)):
        data_file = [f'{data_folder}/{best_trades[i]["name"]}.csv']
        result = backTesting_logic.run_backtest(data_file, train_start, train_end, config['buy_expression'], config['sell_expression'], plot=True, verbose=False)

if __name__ == "__main__":
    main()
