import backtrader as bt
import indicators
from itertools import combinations, product
from datetime import datetime
import backtrader.analyzers as btanalyzers


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
    return expression.replace('self.', f'd.{data._name}.')

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

        for i, d in enumerate(self.datas):
            # 对于每只股票，创建技术指标
            self.orders[d._name] = None
            self.entry_prices[d._name] = None

            # 创建和保存指标，可根据您的需要进行调整
            d.ema5 = bt.ind.EMA(d.close, period=5)
            d.ema10 = bt.ind.EMA(d.close, period=10)
            d.ema22 = bt.ind.EMA(d.close, period=22)
            d.ema66 = bt.ind.EMA(d.close, period=66)

            # MACD 指标
            d.macd = bt.indicators.MACD(d.close)

            # KDJ 指標
            d.stochastic = bt.indicators.Stochastic(d)
            d.k = d.stochastic.percK
            d.d = d.stochastic.percD
            d.j = 3 * d.k - 2 * d.d  # J線計算公式
        
            # RSI 指标
            d.rsi = bt.indicators.RSI(d.close, period=14)
        
            # DMI 指标
            d.dmi = bt.indicators.DMI(d, period=14)
            d.plusDI = d.dmi.plusDI
            d.minusDI = d.dmi.minusDI


    def next(self):
        for i, d in enumerate(self.datas):
            dt, dn = self.datetime.date(), d._name

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


def run_backtest(data_files, from_date, to_date, buy_expression, sell_expression, plot=False):
    cerebro = bt.Cerebro()
    cerebro.addstrategy(MultiStrategy, buy_expression=buy_expression, sell_expression=sell_expression)

    # 修改此处以接受多个数据文件
    for file in data_files:
        data = bt.feeds.GenericCSVData(
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
            timeframe=bt.TimeFrame.Days 
        )
        cerebro.adddata(data)

    # 设置初始资本
    cerebro.broker.setcash(1000000.0)

    # 设置每笔交易使用的股票百分比
    cerebro.addsizer(bt.sizers.PercentSizer, percents=90)

    # 设置佣金
    cerebro.broker.setcommission(commission=0.0035)

    # 添加分析器
    cerebro.addanalyzer(btanalyzers.SharpeRatio, _name='sharpe_ratio', timeframe=bt.TimeFrame.Days)
    cerebro.addanalyzer(btanalyzers.DrawDown, _name='drawdown')

    # 运行策略
    results = cerebro.run()
    final_value = cerebro.broker.getvalue() - 1000000.0
    sharpe_ratio = results[0].analyzers.sharpe_ratio.get_analysis()['sharperatio']
    max_drawdown = results[0].analyzers.drawdown.get_analysis()['max']['drawdown']

    if plot:
        # 显示图表
        cerebro.plot(style='candlestick', barup='red', bardown='green')
    
    return final_value, buy_expression, sell_expression, sharpe_ratio, max_drawdown

# 测试代码
data_files = ['Stock/trainDataSet/2230.csv', 'Stock/trainDataSet/2331.csv']  # 更新您的股票数据文件路径
buy_expression = 'self.ema5[0] > self.ema10[0] and self.ema10[0] > self.ema22[0] and self.ema22[0] > self.ema66[0] and self.ema5[0] > self.ema5[-1] and self.ema10[0] > self.ema10[-1] and self.ema22[0] > self.ema22[-1] and self.ema66[0] > self.ema66[-1] and abs((self.ema10[0] - self.ema22[0]) / self.ema22[0]) < 0.03 or abs((self.ema22[0] - self.ema66[0]) / self.ema66[0]) < 0.03'
sell_expression = 'self.ema22[0] < self.ema22[-1] and self.ema10[0] < self.ema10[-1] and self.ema66[0] < self.ema66[-1]'

results = run_backtest(data_files, '2015-01-01', '2019-01-01', buy_expression, sell_expression, plot=True)
print(results)
