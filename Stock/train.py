# main.py
import pandas as pd
from collections import defaultdict
import backtest.single_backtest as single_backtest
from datetime import datetime, timedelta
import time
from joblib import Parallel, delayed
from tqdm import tqdm
import itertools
import indicators


def get_dates():
    start_date = datetime(2019, 1, 1)  
    end_date = datetime(2021, 1, 1)  
    return start_date, end_date

# 定义一个函数来生成所有条件的组合，固定一个条件
def generate_expressions(conditions, fixed_condition):
    expressions = []
    
    # 从条件列表中移除固定条件
    other_conditions = [cond for cond in conditions if cond != fixed_condition]
    
    # 当固定条件为空时，直接将条件添加到表达式列表
    if fixed_condition == '':
        expressions.extend(other_conditions)
    else:
        # 生成固定条件与其他条件的 'and' 和 'or' 组合
        for cond in other_conditions:
            for operator in [' and ', ' or ']:
                expr = fixed_condition + operator + cond
                expressions.append(expr)

    return expressions

def get_indicators_from_module(module):
    indicators_dict = {}
    for name in dir(module):
        if not name.startswith('__'):  # 过滤掉魔术方法
            value = getattr(module, name)
            if isinstance(value, str):  # 确保是字符串类型的指标
                indicators_dict[name] = value
    return indicators_dict


def run_backtests(buy_pool, sell_pool, buy_fixed, sell_fixed, train_files, train_start, train_end):
    buy_expression = generate_expressions(buy_pool, buy_fixed)
    sell_expression = generate_expressions(sell_pool, sell_fixed)
    expression_combinations = list(itertools.product(buy_expression, sell_expression))

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
             for buy_expr, sell_expr in expression_combinations
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
        'buy_fixed': f'{indicators.angle20_ema10h}',
        'sell_fixed': f'{indicators.angle50_ema66h}',
    }
    # 使用函数从indicators模块获取所有指标
    indicators_dict = get_indicators_from_module(indicators)
    train_start, train_end = get_dates()

    # 创建包含所有指标表达式的列表
    indicators_list = [expr for name, expr in indicators_dict.items()]

    # 讀取 CSV 文件以獲取台灣股票代碼列表
    taiwan_stocks_df = pd.read_csv('Stock/test.csv')  # 替換為你的 CSV 文件路徑
    # 確保股票代碼為字符串格式
    taiwan_stocks = taiwan_stocks_df['StockID'].apply(lambda x: f"{x}").tolist()

    # 創建數據文件路徑列表
    data_folder = 'Stock/trainDataSet'  # 設定你的數據集文件夾路徑
    data_files = [f'{data_folder}/{stock}.csv' for stock in taiwan_stocks]  # 假設每個股票的數據文件名是 '{股票代碼}.csv'


    start_time = time.time()
    results = run_backtests(indicators_list, indicators_list, config['buy_fixed'], config['sell_fixed'], data_files, train_start, train_end)

    results_list = list(results.items())
    # 对 all_results 按照胜率进行排序
    sorted_results = sorted(results_list, key=lambda x: x[1]['sum_win_count'] / x[1]['sum_total_trades'] if x[1]['sum_total_trades'] > 0 else 0, reverse=True)

    print('------------------------------Sort by winrate-------------------------------------------------')

    # 初始化一個空列表用來儲存前三名的結果
    top_3_results = []
    # 用來記錄已選取的值
    selected_values = set()

    for strategy_key, metrics in sorted_results:
        if len(top_3_results) >= 3:
            # 如果已经选取了三个不同的结果，则终止循环
            break

        value = metrics['sum_final_value']
        if value not in selected_values:
            # 如果这个值尚未被选取，则将其添加到结果列表和选取值集合中
            top_3_results.append((strategy_key, metrics))
            selected_values.add(value)

    for strategy_key, metrics in top_3_results:
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


    # print('------------------------------Sort by sharpe-------------------------------------------------')

    # results.sort(key=lambda x: x[3] if x[3] is not None else 0, reverse=True)
    
    # # 初始化一個空列表用來儲存前三名的結果
    # top_3_results = []
    # # 用來記錄已選取的sharpe值
    # selected_sharpes = set()

    # for result in results:
    #     if len(top_3_results) >= 3:
    #         # 如果已經選取了三個不同的結果，則終止循環
    #         break

    #     sharpe = result[3]
    #     if sharpe not in selected_sharpes:
    #         # 如果這個sharpe值尚未被選取，則將其添加到結果列表和選取值集合中
    #         top_3_results.append(result)
    #         selected_sharpes.add(sharpe)

    # for result in top_3_results:
    #     value, buy_expression, sell_expression, sharpe, drawdown = result
    #     print(f"買入策略組合: {buy_expression}, \n賣出策略組合: {sell_expression}, \n淨收益: {value}, \nsharpe: {sharpe}, \nMDD: {drawdown}\n")

    end_time = time.time()
    print(f"執行時間：{end_time - start_time} 秒")

if __name__ == "__main__":
    main()
