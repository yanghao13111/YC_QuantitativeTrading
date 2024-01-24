# main.py
import pandas as pd
import backtest.single_backtest as single_backtest
from collections import defaultdict
from joblib import Parallel, delayed
from tqdm import tqdm
import indicators
import time
from datetime import datetime, timedelta

def get_dates():
    start_date = datetime(2019, 1, 1)  
    end_date = datetime(2021, 1, 1)  
    return start_date, end_date


def run_backtests(buy_expr, sell_expr, train_files, train_start, train_end):

    all_results = defaultdict(lambda: {
        'final_value': [],
        'sharpe_ratio': [],
        'max_drawdown': [],
        'best_trades': [],  # 列表
        'worst_trades': [],  # 列表
        'win_count': [],
        'total_trades': [],
        'sum_final_value': 0.0,  # 初始化为浮点数
        'sum_win_count': 0,      # 初始化为整数
        'sum_total_trades': 0    # 初始化为整数
    })

    # 准备并行执行的任务
    tasks = [(data_file, train_start, train_end, buy_expr, sell_expr)
             for data_file in train_files]
    
    # 使用 joblib 并行执行任务
    results = Parallel(n_jobs=-1, verbose=0)(
        delayed(run_single_backtest)(data_file, start, end, buy_expr, sell_expr)
        for data_file, start, end, buy_expr, sell_expr in tqdm(tasks, desc='Running backtests')
    )

    # 处理结果并更新 all_results
    for result, (_, _, _, buy_expr, sell_expr) in zip(results, tasks):
        final_value, buy_expression, sell_expression, sharpe_ratio, max_drawdown, best_trades, worst_trades, win_count, total_trades = result
        # 对于同一策略的结果，进行累积
        strategy_key = (buy_expr, sell_expr)
        # 追加列表数据
        all_results[strategy_key]['final_value'].append(final_value)
        all_results[strategy_key]['best_trades'].extend(best_trades)
        all_results[strategy_key]['worst_trades'].extend(worst_trades)
        all_results[strategy_key]['win_count'].append(win_count)
        all_results[strategy_key]['total_trades'].append(total_trades)
        
        # 进行加总
        all_results[strategy_key]['sum_final_value'] += final_value
        all_results[strategy_key]['sum_win_count'] += win_count
        all_results[strategy_key]['sum_total_trades'] += total_trades

    return all_results

def run_single_backtest(data_file, start_date, end_date, buy_expr, sell_expr):
    return single_backtest.run_backtest(data_file, start_date, end_date, buy_expr, sell_expr, '', verbose=False)

def main():
    config = {
        'timeframe': '1d',  
        'buy_expression': f'{indicators.double_volume} and {indicators.red_bar} and {indicators.volume_over_500} and {indicators.all_uptrend} and {indicators.bullish_alignment}',
        'sell_expression': f'(({indicators.green_bar} or {indicators.upper_wick_length}) and {indicators.green_down} and {indicators.volume_5})', 
        'add_expression': f'' 
    }

    start_date, end_date = get_dates()

    # 讀取 CSV 文件以獲取台灣股票代碼列表
    taiwan_stocks_df = pd.read_csv('Stock/test.csv')  # 替換為你的 CSV 文件路徑
    # 確保股票代碼為字符串格式
    taiwan_stocks = taiwan_stocks_df['StockID'].apply(lambda x: f"{x}").tolist()

    # 創建數據文件路徑列表
    data_folder = 'Stock/trainDataSet'  # 設定你的數據集文件夾路徑
    data_files = [f'{data_folder}/{stock}.csv' for stock in taiwan_stocks]  # 假設每個股票的數據文件名是 '{股票代碼}.csv'

    start_time = time.time()
    results = run_backtests(config['buy_expression'], config['sell_expression'], data_files, start_date, end_date)
    results_list = list(results.items())

    # 提取排序后的第一个元素
    strategy_key, metrics = results_list[0]

    print('------------------------------Result-------------------------------------------------')

    final_value = metrics['sum_final_value']
    win_count = metrics['sum_win_count']
    total_trades = metrics['sum_total_trades']
    win_rate = win_count / total_trades if total_trades > 0 else 0
    buy_expression = strategy_key[0]
    sell_expression = strategy_key[1]
    print(f"買入策略組合: {buy_expression}, \n賣出策略組合: {sell_expression}, \n淨收益: {final_value}, \nwin_rate: {win_rate*100}%, \ntotal_trades: {total_trades}")

    # 根據損益比例排序交易，並選出虧損最多的前五名
    worst_trades = sorted(metrics['worst_trades'], key=lambda x: x['profit_ratio'])
    worst_trades = worst_trades[:5]

    # 选择盈利最高的前五名和虧損最多的前五名交易
    best_trades = sorted(metrics['best_trades'], key=lambda x: x['profit_ratio'], reverse=True)
    best_trades = best_trades[:5]

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
        data_file = f'{data_folder}/{worst_trades[i]["name"]}.csv'
        result = single_backtest.run_backtest(data_file, start_date, end_date, config['buy_expression'], config['sell_expression'], '', plot=True, verbose=False)

    for i in range(len(best_trades)):
        data_file = f'{data_folder}/{best_trades[i]["name"]}.csv'
        result = single_backtest.run_backtest(data_file, start_date, end_date, config['buy_expression'], config['sell_expression'], '', plot=True, verbose=False)

if __name__ == "__main__":
    main()
