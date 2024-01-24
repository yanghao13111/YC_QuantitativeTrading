# main.py
import pandas as pd
from itertools import combinations, product
import backtest.single_backtest as single_backtest
from datetime import datetime, timedelta
import time
from joblib import Parallel, delayed
from tqdm import tqdm
import itertools
import indicators


def get_dates():
    start_date = datetime(2010, 1, 1)  
    end_date = datetime(2021, 1, 1)  
    return start_date, end_date

def generate_expressions(conditions, combined_number):
    expressions = []
    for r in range(1, min(len(conditions), combined_number) + 1):
        for subset in combinations(conditions, r):
            if len(subset) == 1:
                expressions.append(subset[0])
            else:
                operators = list(product([' and ', ' or '], repeat=len(subset)-1))
                for operator in operators:
                    expr = ''
                    for i, cond in enumerate(subset):
                        expr += cond
                        if i < len(operator):
                            expr += operator[i]
                    expressions.append(expr)
    return expressions

def run_backtests(signal_pool, combined_number, train_files, train_start, train_end):
    signal_expressions = generate_expressions(signal_pool, combined_number)
    tasks = tqdm(signal_expressions)

    backtest_results = Parallel(n_jobs=-1)(
        delayed(run_single_backtest)(file, train_start, train_end, expr) 
        for file in train_files for expr in tasks
    )
    return backtest_results

def run_single_backtest(data_file, start_date, end_date, signal_expr):
    return single_backtest.run_backtest(data_file, start_date, end_date, signal_expr, '', verbose=False)

def main():
    config = {
        'timeframe': '1d',
        # all indicators
        'signal_pool': [indicators.ema5_h, indicators.ema10_h, indicators.ema22_h, indicators.ema66_h, indicators.ema5_l, indicators.ema10_l, indicators.ema22_l, indicators.ema66_l, indicators.ema_uptrend_5, indicators.ema_uptrend_10, indicators.ema_uptrend_22, indicators.ema_uptrend_66, indicators.ema_downtrend_5, indicators.ema_downtrend_10, indicators.ema_downtrend_22, indicators.ema_downtrend_66],  
        'combined': 3,
    }

    train_start, train_end = get_dates()

    # 讀取 CSV 文件以獲取台灣股票代碼列表
    taiwan_stocks_df = pd.read_csv('Day_Trade/Data/test.csv')  # 替換為你的 CSV 文件路徑
    # 確保股票代碼為字符串格式
    taiwan_stocks = taiwan_stocks_df['StockID'].apply(lambda x: f"{x}").tolist()

    # 創建數據文件路徑列表
    data_folder = 'Day_Trade/trainDataSet'  # 設定你的數據集文件夾路徑
    data_files = [f'{data_folder}/{stock}.csv' for stock in taiwan_stocks]  # 假設每個股票的數據文件名是 '{股票代碼}.csv'

    start_time = time.time()
    results = run_backtests(config['signal_pool'], config['combined'], data_files, train_start, train_end)

    print('------------------------------Sort by win-------------------------------------------------')

    results.sort(key=lambda x: x[6] if x[6] is not None else 0, reverse=True)

    top_3_results_by_value = results[:3]

    for result in top_3_results_by_value:
        value, signal_expression, sharpe, drawdown, best_trades_by_profit, best_trades_by_win_ratio, win_ratio, total_trades = result
        print(f"信号策略组合: {signal_expression}, \n淨收益: {value}, \nsharpe: {sharpe}, \nMDD: {drawdown}\n")
        single_backtest.run_backtest(data_files[0], train_start, train_end, signal_expression, plot=True)

    # print('------------------------------Sort by sharpe-------------------------------------------------')

    # results.sort(key=lambda x: x[3] if x[3] is not None else 0, reverse=True)
    
    # top_3_results_by_sharpe = results[:3]
    # for result in top_3_results_by_sharpe:
    #     value, signal_expression, sharpe, drawdown, best_trades_by_profit, best_trades_by_win_ratio, win_ratio, total_trades = result
    #     print(f"信号策略组合: {signal_expression}, \n淨收益: {value}, \nsharpe: {sharpe}, \nMDD: {drawdown}\n")

    # end_time = time.time()
    # print(f"執行時間：{end_time - start_time} 秒")

if __name__ == "__main__":
    main()
