import backtrader as bt
from itertools import combinations, product
from datetime import datetime
import backtrader.analyzers as btanalyzers

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

        # SMA 指标
        self.sma5 = bt.indicators.SimpleMovingAverage(self.data.close, period=5)
        self.sma10 = bt.indicators.SimpleMovingAverage(self.data.close, period=10)
        self.sma20 = bt.indicators.SimpleMovingAverage(self.data.close, period=20)
        self.sma60 = bt.indicators.SimpleMovingAverage(self.data.close, period=60)
        self.sma120 = bt.indicators.SimpleMovingAverage(self.data.close, period=120)
        self.sma240 = bt.indicators.SimpleMovingAverage(self.data.close, period=240)

        # MACD 指标
        self.macd = bt.indicators.MACD(self.data.close)
        
        # RSI 指标
        self.rsi = bt.indicators.RSI(self.data.close)
        
        # Stochastic 指标
        self.stoch = bt.indicators.Stochastic(self.data)

    def next(self):
        if self.order:
            self.cancel(self.order)

        # 使用 eval 来计算动态生成的布尔表达式
        if not self.position and eval(self.params.expression):
            self.order = self.buy()

        # 出场条件需要根据您的策略来定义
        elif self.position and not eval(self.params.expression):  # 这里的条件需要根据实际策略进行调整
            self.order = self.close()

def run_backtest(data_file, from_date, to_date, expression, plot=False):
    cerebro = bt.Cerebro()
    cerebro.addstrategy(MultiStrategy, expression=expression)

    data = bt.feeds.GenericCSVData(
        dataname=data_file,
        fromdate=from_date,
        todate=to_date,
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

    # 添加分析器
    cerebro.addanalyzer(btanalyzers.SharpeRatio, _name='sharpe_ratio')
    cerebro.addanalyzer(btanalyzers.DrawDown, _name='drawdown')


    results = cerebro.run()
    final_value = cerebro.broker.getvalue() - 1000000.0
    sharpe_ratio = results[0].analyzers.sharpe_ratio.get_analysis()['sharperatio']
    max_drawdown = results[0].analyzers.drawdown.get_analysis()['max']['drawdown']

    if plot:
        cerebro.plot()
    else:
        return final_value, expression, sharpe_ratio, max_drawdown