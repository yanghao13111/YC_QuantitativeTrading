# main.py
import data_collection
import backTesting_logic
from datetime import datetime, timedelta

MONTH = 46

def get_dates(months_back):
    current_time = datetime.utcnow()
    start_date = current_time - timedelta(days=months_back * 30 + 3)
    end_date = current_time - timedelta(days=(months_back - 1) * 30 + 1)
    return start_date, end_date


def collect_and_save_data(symbol, timeframe, start_date, end_date, filename):
    df = data_collection.collect_data(symbol, timeframe, start_date, end_date)
    df.to_csv(filename, index=False)
    return filename


def main():
    config = {
        'symbol': 'BTC/USDT',
        'timeframe': '1h',
        'buy_expression': 'self.macd.macd[0] > self.macd.signal[0] and self.rsi[0] < 30',
        'sell_expression': 'self.macd.macd[0] < self.macd.signal[0] and self.k[0] < self.j[0] and self.d[0] < self.j[0] and self.rsi[0] > 70'
    }

    train_start, train_end = get_dates(MONTH)

    train_file = collect_and_save_data(config['symbol'], config['timeframe'], train_start, train_end, f'Crypto/upModel/Simulation/test_data_{MONTH}.csv')
    # test_file = f'Crypto/upModel/Simulation/train_data_{MONTH}.csv'

    result = backTesting_logic.run_backtest(train_file, train_start, train_end, config['buy_expression'], config['sell_expression'], True)

    value, buy_expression, sell_expression, sharpe, drawdown = result
    print(f"買入策略組合: {buy_expression}, 賣出策略組合: {sell_expression}, 淨收益: {value}, sharpe: {sharpe}, MDD: {drawdown}")

if __name__ == "__main__":
    main()
