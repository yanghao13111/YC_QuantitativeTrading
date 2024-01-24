# main.py
import pandas as pd
from collections import defaultdict
import backtest.single_backtest as single_backtest
from datetime import datetime, timedelta
import time
from joblib import Parallel, delayed
from tqdm import tqdm
import itertools
import Stock.temp.test_ind as test_ind


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


def main():
    config = {
        'timeframe': '1d',  
        'buy_fixed': f'{test_ind.ema10_h}',
        'sell_fixed': f'{test_ind.ema10_h}',
    }
    # 使用函数从indicators模块获取所有指标
    indicators_dict = get_indicators_from_module(test_ind)
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

    buy_expression = generate_expressions(indicators_list, test_ind.ema10_h)
    sell_expression = generate_expressions(indicators_list, test_ind.ema10_h)
    expression_combinations = list(itertools.product(buy_expression, sell_expression))
    print(len(buy_expression))
    for expr in buy_expression:
        print(expr)
    

if __name__ == "__main__":
    main()
