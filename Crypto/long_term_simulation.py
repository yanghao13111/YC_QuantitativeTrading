# long_term_simulation.py
import data_collection
import matplotlib.pyplot as plt
import backTesting_logic
from datetime import datetime, timedelta
import time
from joblib import Parallel, delayed
from tqdm import tqdm
import itertools
import indicators

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
    return backtest_results[:1]

def run_single_backtest(data_file, start_date, end_date, buy_expr, sell_expr):
    return backTesting_logic.run_backtest(data_file, start_date, end_date, buy_expr, sell_expr)

def long_term_simulation():
    config = {
        'symbol': 'ETH/USDT',
        'timeframe': '1h',
        'buy_pool': [indicators.H, indicators.I, indicators.K, indicators.L],
        'sell_pool': [indicators.H, indicators.I, indicators.K, indicators.L],
        'buy_combined': 2,
        'sell_combined': 2,
    }

    # 用于存储每个月的净收益
    monthly_profits = []

    for month in range(12, 2, -1):
        print(f"------ Starting Simulation for {month} Months Back ------")
        train_start, train_end = get_dates(month + 1)
        validation_start, validation_end = get_dates(month)

        train_file = collect_and_save_data(config['symbol'], config['timeframe'], train_start, train_end, f'Crypto/Simulation/train_data_{month}.csv')
        validation_file = collect_and_save_data(config['symbol'], config['timeframe'], validation_start, validation_end, f'Crypto/Simulation/validation_data_{month}.csv')

        start_time = time.time()
        top_results = run_backtests(config['buy_pool'], config['sell_pool'], config['buy_combined'], config['sell_combined'], train_file, train_start, train_end)

        for result in top_results:
            value, buy_expression, sell_expression, sharpe, drawdown = result
            val_result = backTesting_logic.run_backtest(validation_file, validation_start, validation_end, buy_expression, sell_expression)
            val_value, val_buy_expression, val_sell_expression, val_sharpe, val_drawdown = val_result
            print(f"買入策略組合: {val_buy_expression}, 賣出策略組合: {val_sell_expression}, 淨收益: {val_value}, sharpe: {val_sharpe}, MDD: {val_drawdown}")
            monthly_profits.append(val_value)

        end_time = time.time()
        print(f"執行時間：{end_time - start_time} 秒")
        print(f"------ End of Simulation for {month} Months Back ------\n")

    # 绘制柱状图
    months = list(range(2, 1, -1))
    plt.bar(months, monthly_profits)
    plt.xlabel('Months Back')
    plt.ylabel('Net Profit')
    plt.title('Net Profit by Month')
    plt.show()

if __name__ == "__main__":
    long_term_simulation()
