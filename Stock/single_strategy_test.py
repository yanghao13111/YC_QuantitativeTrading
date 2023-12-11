# main.py
import data_collection
import backTesting_logic
from datetime import datetime, timedelta

def get_dates():
    start_date = datetime(2019, 1, 1)  # 指定年份为2022，月份为1，日期为1
    end_date = datetime.utcnow()  # 假设结束日期为当前日期
    return start_date, end_date

def collect_and_save_data(symbol, timeframe, start_date, end_date, filename):
    df = data_collection.collect_data(symbol, timeframe, start_date, end_date)
    df.to_csv(filename, index=False)
    return filename

def main():
    config = {
        'symbol': '6216.TW',
        'timeframe': '1d',  
        'buy_expression': 'self.ema5[0] > self.ema10[0] and self.ema10[0] > self.ema22[0] and self.ema22[0] > self.ema66[0] and self.ema5[0] > self.ema5[-1] and self.ema10[0] > self.ema10[-1] and self.ema22[0] > self.ema22[-1] and self.ema66[0] > self.ema66[-1] and abs((self.ema10[0] - self.ema22[0]) / self.ema22[0]) < 0.03 or abs((self.ema22[0] - self.ema66[0]) / self.ema66[0]) < 0.03',
        'sell_expression': 'self.ema22[0] < self.ema22[-1] and self.ema10[0] < self.ema10[-1] and self.ema66[0] < self.ema66[-1]'
    }

    train_start, train_end = get_dates()


    filename = f'Stock/trainDataSet/{train_start.strftime("%Y-%m-%d")}_{config["symbol"]}.csv'
    train_file = collect_and_save_data(config['symbol'], config['timeframe'], train_start, train_end, filename)

    result = backTesting_logic.run_backtest(train_file, train_start, train_end, config['buy_expression'], config['sell_expression'], True)

    value, buy_expression, sell_expression, sharpe, drawdown = result
    print(f"買入策略組合: {buy_expression}, \n賣出策略組合: {sell_expression}, \n淨收益: {value}, \nsharpe: {sharpe}, \nMDD: {drawdown}")

if __name__ == "__main__":
    main()
