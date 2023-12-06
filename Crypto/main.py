# main.py
import data_collection
import backTesting_logic
from datetime import datetime, timedelta
import time
from joblib import Parallel, delayed
from tqdm import tqdm
import itertools
import indicators

MONTH = 4

def get_dates(months_back):
    current_time = datetime.utcnow()
    start_date = current_time - timedelta(days=months_back * 30 + 20)
    end_date = current_time - timedelta(days=(months_back - 1) * 30 + 1)
    return start_date, end_date

def collect_and_save_data(symbol, timeframe, start_date, end_date, filename):
    df = data_collection.collect_data(symbol, timeframe, start_date, end_date)
    df.to_csv(filename, index=False)
    return filename

def run_backtests(buy_pool, sell_pool, buy_combined, sell_combined, train_file, train_start, train_end):
    buy_expression = backTesting_logic.generate_expressions(buy_pool, buy_combined)
    sell_expression = backTesting_logic.generate_expressions(sell_pool, sell_combined)
    expression_combinations = list(itertools.product(buy_expression, sell_expression))
    tasks = tqdm(expression_combinations)

    backtest_results = Parallel(n_jobs=-1)(
        delayed(run_single_backtest)(train_file, train_start, train_end, buy_expr, sell_expr) 
        for buy_expr, sell_expr in tasks
    )

    backtest_results.sort(key=lambda x: x[0], reverse=True)
    return backtest_results[:3]

def run_single_backtest(data_file, start_date, end_date, buy_expr, sell_expr):
    return backTesting_logic.run_backtest(data_file, start_date, end_date, buy_expr, sell_expr)

def main():
    config = {
        'symbol': 'ETH/USDT',
        'timeframe': '1h',
        'buy_pool': [indicators.ema5_h, indicators.ema10_h, indicators.macd_g, indicators.kdj_b, indicators.rsi_b, indicators.dmi_pdi, indicators.BBI_h],
        'sell_pool': [indicators.ema5_h, indicators.ema10_h, indicators.macd_d, indicators.kdj_s, indicators.rsi_s, indicators.dmi_mdi, indicators.BBI_l],
        'buy_combined': 2,
        'sell_combined': 2,
    }

    train_start, train_end = get_dates(MONTH)
    validation_start, validation_end = get_dates(MONTH-1)

    train_file = collect_and_save_data(config['symbol'], config['timeframe'], train_start, train_end, 'Crypto/train_data.csv')
    validation_file = collect_and_save_data(config['symbol'], config['timeframe'], validation_start, validation_end, 'Crypto/validation_data.csv')

    start_time = time.time()
    top_3_results = run_backtests(config['buy_pool'], config['sell_pool'], config['buy_combined'], config['sell_combined'], train_file, train_start, train_end)

    for result in top_3_results:
        value, buy_expression, sell_expression, sharpe, drawdown = result
        print(f"買入策略組合: {buy_expression}, 賣出策略組合: {sell_expression}, 淨收益: {value}, sharpe: {sharpe}, MDD: {drawdown}")
        backTesting_logic.run_backtest(train_file, train_start, train_end, buy_expression, sell_expression, True)

    print('-------------------------------------------------------------------------------')

    for result in top_3_results:
        value, buy_expression, sell_expression, sharpe, drawdown = result
        val_result = backTesting_logic.run_backtest(validation_file, validation_start, validation_end, buy_expression, sell_expression, True)
        val_value, val_buy_expression, val_sell_expression, val_sharpe, val_drawdown = val_result
        print(f"買入策略組合: {val_buy_expression}, 賣出策略組合: {val_sell_expression}, 淨收益: {val_value}, sharpe: {val_sharpe}, MDD: {val_drawdown}")

    end_time = time.time()
    print(f"執行時間：{end_time - start_time} 秒")

if __name__ == "__main__":
    main()
