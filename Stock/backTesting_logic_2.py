import backtrader as bt
import pandas as pd
import indicators
from itertools import combinations, product
from datetime import datetime
import backtrader.analyzers as btanalyzers
from tqdm import tqdm


# 定义一个函数来生成所有条件的组合
def generate_expressions(conditions, combined_number):
    expressions = []
    
    # 针对长度为 1 到 combined_number 的组合生成表达式
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

def replace_self_with_data(expression, data):
    # 替换表达式中的'self'为当前数据集的引用，同时确保数字前有下划线避免语法错误
    return expression.replace('self.', f'd.')


class CustomCSVData(bt.feeds.GenericCSVData):
    # Define new lines for additional data
    lines = ('ema5', 'ema10', 'ema22', 'ema66', 'ema264')

    # Map the new lines to the corresponding columns in the CSV
    params = (
        ('ema5', -1),
        ('ema10', -1),
        ('ema22', -1),
        ('ema66', -1),
        ('ema264', -1),
    )


class MultiStrategy(bt.Strategy):
    params = (
        # 買入和賣出表達式參數
        ('buy_expression', ''),
        ('sell_expression', ''),
    )

    def __init__(self):
        # 创建一个字典来跟踪每个数据集的订单和价格
        self.orders = {}
        self.entry_prices = {}
        self.trade_list = [] 

        for i, d in enumerate(self.datas):
            print(f"Initializing indicators for {d._name}")  # 打印当前正在处理的股票名称
            # 对于每只股票，创建技术指标
            self.orders[d._name] = None
            self.entry_prices[d._name] = None

            try:
                assert hasattr(d, 'ema5'), "EMA5 not found"
                assert hasattr(d, 'ema10'), "EMA10 not found"
                assert hasattr(d, 'ema22'), "EMA22 not found"
                assert hasattr(d, 'ema66'), "EMA66 not found"
                assert hasattr(d, 'ema264'), "EMA264 not found"
            except Exception as e:
                print(f"Error initializing indicators for {d._name}: {e}")

            # # MACD 指标
            # d.macd = bt.indicators.MACD(d.close)

            # # KDJ 指標
            # d.stochastic = bt.indicators.Stochastic(d)
            # d.k = d.stochastic.percK
            # d.d = d.stochastic.percD
            # d.j = 3 * d.k - 2 * d.d  # J線計算公式
        
            # # RSI 指标
            # d.rsi = bt.indicators.RSI(d.close, period=14)
        
            # # DMI 指标
            # d.dmi = bt.indicators.DMI(d, period=14)
            # d.plusDI = d.dmi.plusDI
            # d.minusDI = d.dmi.minusDI


    def next(self):
        for i, d in enumerate(self.datas):
            dt, dn = self.datetime.date(), d._name
            try:
                # 打印当前日期和正在处理的股票名称
                print(f"Processing date: {dt}, stock: {dn}")

                # 获取当前数据集的订单和持仓
                current_order = self.orders[dn]
                current_position = self.getposition(d).size

                # 检查是否有未完成的订单
                if current_order and current_order.status in [bt.Order.Submitted, bt.Order.Accepted]:
                    continue

                # 准备买入和卖出条件
                buy_conditions = replace_self_with_data(self.params.buy_expression, d)
                sell_conditions = replace_self_with_data(self.params.sell_expression, d)

                # 没有持仓时，检查是否应该买入
                if current_position == 0 and eval(buy_conditions):
                    self.orders[dn] = self.buy(data=d)
                    self.entry_prices[dn] = d.close[0]

                # 持有做多仓位时，检查是否应该平仓
                elif current_position > 0 and eval(sell_conditions):
                    self.orders[dn] = self.close(data=d)
            except Exception as e:
                # 如果在处理特定股票时发生异常，打印错误信息
                print(f"Error processing date: {dt}, stock: {dn}: {e}")


def run_backtest(data_files, from_date, to_date, buy_expression, sell_expression, plot=False):
    cerebro = bt.Cerebro()
    cerebro.addstrategy(MultiStrategy, buy_expression=buy_expression, sell_expression=sell_expression)

    for file in data_files:
        # Use CustomCSVData instead of GenericCSVData
        data = CustomCSVData(
            dataname=file,
            fromdate=datetime.strptime(from_date, '%Y-%m-%d'),
            todate=datetime.strptime(to_date, '%Y-%m-%d'),
            nullvalue=0.0,
            dtformat=('%Y-%m-%d'),
            datetime=0,
            open=4,
            high=5,
            low=6,
            close=7,
            volume=2,
            openinterest=-1,
            timeframe=bt.TimeFrame.Days,
            ema5=10,  # Update the column index for ema5
            ema10=11,  # Update the column index for ema10
            ema22=12, # Update the column index for ema22
            ema66=13, # Update the column index for ema66
            ema264=14 # Update the column index for ema264
        )
        cerebro.adddata(data)

    # 设置初始资本
    cerebro.broker.setcash(1000000000.0)

    # 设置每笔交易买入1股股票
    cerebro.addsizer(bt.sizers.FixedSize, stake=1000)


    # 设置佣金
    cerebro.broker.setcommission(commission=0.0035)

    # 添加分析器
    cerebro.addanalyzer(btanalyzers.SharpeRatio, _name='sharpe_ratio', timeframe=bt.TimeFrame.Days)
    cerebro.addanalyzer(btanalyzers.DrawDown, _name='drawdown')

    # 运行策略
    results = cerebro.run()
    final_value = cerebro.broker.getvalue() - 1000000000.0
    sharpe_ratio = results[0].analyzers.sharpe_ratio.get_analysis()['sharperatio']
    max_drawdown = results[0].analyzers.drawdown.get_analysis()['max']['drawdown']

    if plot:
        # 显示图表
        cerebro.plot(style='candlestick', barup='red', bardown='green')
    
    return final_value, buy_expression, sell_expression, sharpe_ratio, max_drawdown

# 測試代碼
# 讀取 CSV 文件以獲取台灣股票代碼列表
taiwan_stocks_df = pd.read_csv('Stock/tets.csv')  # 替換為你的 CSV 文件路徑
# 確保股票代碼為字符串格式並添加 ".TW"
taiwan_stocks = taiwan_stocks_df['StockID'].apply(lambda x: f"{x}").tolist()

# 創建數據文件路徑列表
data_folder = 'Stock/trainDataSet'  # 設定你的數據集文件夾路徑
data_files = [f'{data_folder}/{stock}.csv' for stock in taiwan_stocks]  # 假設每個股票的數據文件名是 '{股票代碼}.csv'

# # 測試代碼
# data_files = ['Stock/trainDataSet/2230.csv']  # 更新您的股票数据文件路径

buy_expression = 'self.ema5[0] > self.ema10[0] and self.ema10[0] > self.ema22[0] and self.ema22[0] > self.ema66[0] and self.ema66[0] > self.ema264[0] and self.ema5[0] > self.ema5[-1] and self.ema10[0] > self.ema10[-1] and self.ema22[0] > self.ema22[-1] and self.ema66[0] > self.ema66[-1] and self.ema264[0] > self.ema264[-1] and abs((self.ema10[0] - self.ema22[0]) / self.ema22[0]) < 0.02 and abs((self.ema22[0] - self.ema66[0]) / self.ema66[0]) < 0.02 and abs((self.ema66[0] - self.ema264[0]) / self.ema264[0]) < 0.1 and self.volume[0] > 2 * self.volume[-1] and self.volume[0] > 300 * 1000'
sell_expression = 'self.ema10[0] < self.ema10[-1]'

results = run_backtest(data_files, '2015-01-01', '2019-01-01', buy_expression, sell_expression)
print(results[0])
