import backtrader as bt
from itertools import combinations, product
from datetime import datetime

# 定义一个函数来生成所有条件的组合
def generate_expressions(conditions):
    expressions = []
    for r in range(1, len(conditions) + 1):
        for subset in combinations(conditions, r):
            operators = list(product([' and ', ' or '], repeat=r-1))
            for operator in operators:
                expr = ''
                for i, cond in enumerate(subset):
                    expr += cond
                    if i < len(operator):
                        expr += operator[i]
                expressions.append(expr)
    return expressions

class MultiStrategy(bt.Strategy):
    params = (('expression', ''),)  # 添加一个参数用于接收买入条件表达式

    def __init__(self):
        self.order = None
        self.sma5 = bt.indicators.SimpleMovingAverage(self.data.close, period=5)
        self.sma10 = bt.indicators.SimpleMovingAverage(self.data.close, period=10)
        self.sma20 = bt.indicators.SimpleMovingAverage(self.data.close, period=20)

    def next(self):
        if self.order:
            self.cancel(self.order)

        # 使用 eval 来计算动态生成的布尔表达式
        if not self.position and eval(self.params.expression):
            self.order = self.buy()

        # 出场条件需要根据您的策略来定义
        elif self.position and not eval(self.params.expression):  # 这里的条件需要根据实际策略进行调整
            self.order = self.close()

def run_backtest(data_file, from_date, to_date, expression):
    cerebro = bt.Cerebro()
    cerebro.addstrategy(MultiStrategy, expression=expression)

    data = bt.feeds.GenericCSVData(
        dataname=data_file,
        fromdate=datetime.strptime(from_date, '%Y-%m-%d'),
        todate=datetime.strptime(to_date, '%Y-%m-%d'),
        nullvalue=0.0,
        dtformat=('%Y-%m-%d %H:%M:%S'), 
        datetime=0,
        open=1,
        high=2,
        low=3,
        close=4,
        volume=5,
        openinterest=-1
    )

    cerebro.adddata(data)
    cerebro.broker.setcash(1000000.0)
    cerebro.addsizer(bt.sizers.FixedSize, stake=10)
    cerebro.broker.setcommission(commission=0.001)
    cerebro.run()
    print(f'Final Portfolio Value: {cerebro.broker.getvalue() - 1000000.0}')
    cerebro.plot()

# 假设的市场条件布尔表达式
A = "self.data.close[0] > self.sma5[0]"  # 例如：今日收盘价高于5日均线
B = "self.data.close[0] < self.sma10[0]" # 另一个市场条件的例子
C = "self.data.close[0] < self.sma20[0]"


# 创建一个包含这些条件的列表
conditions = [A, B, C]
expressions = generate_expressions(conditions)

# 对每个生成的表达式运行回测
for expr in expressions:
    run_backtest('/Users/cchtony/Desktop/YC_QuantitativeTrading/market_data.csv', '2022-11-24', '2023-11-24', expr)
    print(expr)
