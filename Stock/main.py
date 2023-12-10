# main.py
import data_collection
import backTesting_logic
from datetime import datetime, timedelta
import time
from joblib import Parallel, delayed
from tqdm import tqdm
import itertools
import indicators


def get_dates():
    start_date = datetime(2019, 1, 1)  # 指定年份为2022，月份为1，日期为1
    end_date = datetime.utcnow()  # 假设结束日期为当前日期
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
    return backtest_results

def run_single_backtest(data_file, start_date, end_date, buy_expr, sell_expr):
    return backTesting_logic.run_backtest(data_file, start_date, end_date, buy_expr, sell_expr)

def main():
    config = {
        'symbol': '2376.TW',
        'timeframe': '1d',  
        'buy_pool': [indicators.bullish_alignment, indicators.allup, indicators.no_5ma, indicators.is_divergence_less_than_3_percent_5_10, indicators.is_divergence_less_than_3_percent_10_22, indicators.is_divergence_less_than_3_percent_22_66, indicators.volume_indicator],  
        'sell_pool': [indicators.ema_downtrend_22, indicators.ema_downtrend_10],  
        'buy_combined': 7,
        'sell_combined': 2,
    }

    train_start, train_end = get_dates()

    filename = f'Stock/trainDataSet/{train_start.strftime("%Y-%m-%d")}_{config["symbol"]}.csv'
    train_file = collect_and_save_data(config['symbol'], config['timeframe'], train_start, train_end, filename)

    start_time = time.time()
    results = run_backtests(config['buy_pool'], config['sell_pool'], config['buy_combined'], config['sell_combined'], train_file, train_start, train_end)

    print('------------------------------Sort by value-------------------------------------------------')

    results.sort(key=lambda x: x[0], reverse=True)

    # 初始化一個空列表用來儲存前三名的結果
    top_3_results = []
    # 用來記錄已選取的值
    selected_values = set()

    for result in results:
        if len(top_3_results) >= 3:
            # 如果已經選取了三個不同的結果，則終止循環
            break

        value = result[0]
        if value not in selected_values:
            # 如果這個值尚未被選取，則將其添加到結果列表和選取值集合中
            top_3_results.append(result)
            selected_values.add(value)

    for result in top_3_results:
        value, buy_expression, sell_expression, sharpe, drawdown = result
        print(f"買入策略組合: {buy_expression}, \n賣出策略組合: {sell_expression}, \n淨收益: {value}, \nsharpe: {sharpe}, \nMDD: {drawdown}\n")
        backTesting_logic.run_backtest(train_file, train_start, train_end, buy_expression, sell_expression, True)


    print('------------------------------Sort by sharpe-------------------------------------------------')

    results.sort(key=lambda x: x[3] if x[3] is not None else 0, reverse=True)
    
    # 初始化一個空列表用來儲存前三名的結果
    top_3_results = []
    # 用來記錄已選取的sharpe值
    selected_sharpes = set()

    for result in results:
        if len(top_3_results) >= 3:
            # 如果已經選取了三個不同的結果，則終止循環
            break

        sharpe = result[3]
        if sharpe not in selected_sharpes:
            # 如果這個sharpe值尚未被選取，則將其添加到結果列表和選取值集合中
            top_3_results.append(result)
            selected_sharpes.add(sharpe)

    first_run = True
    for result in top_3_results:
        value, buy_expression, sell_expression, sharpe, drawdown = result
        print(f"買入策略組合: {buy_expression}, \n賣出策略組合: {sell_expression}, \n淨收益: {value}, \nsharpe: {sharpe}, \nMDD: {drawdown}\n")
        if first_run:
            backTesting_logic.run_backtest(train_file, train_start, train_end, buy_expression, sell_expression, True)
            first_run = False
        else:
            backTesting_logic.run_backtest(train_file, train_start, train_end, buy_expression, sell_expression)

    end_time = time.time()
    print(f"執行時間：{end_time - start_time} 秒")

if __name__ == "__main__":
    main()
