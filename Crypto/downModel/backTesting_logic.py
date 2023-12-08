import backtrader as bt
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

class MultiStrategy(bt.Strategy):
    params = (
        ('stop_loss_percent', 3),  # 設定停損百分比
        # 買入和賣出表達式參數
        ('buy_expression', ''),
        ('sell_expression', ''),
    )

    def __init__(self):
        self.order = None
        self.entry_price = None

        # SMA 指标
        self.sma5 = bt.ind.SMA(self.data.close, period=5)
        self.sma10 = bt.ind.SMA(self.data.close, period=10)
        self.sma20 = bt.ind.SMA(self.data.close, period=20)
        self.sma60 = bt.ind.SMA(self.data.close, period=60)

        # EMA 指标
        self.ema5 = bt.ind.EMA(self.data.close, period=5)
        self.ema10 = bt.ind.EMA(self.data.close, period=10)
        self.ema20 = bt.ind.EMA(self.data.close, period=20)

        # MACD 指标
        self.macd = bt.indicators.MACD(self.data.close)

        # KDJ 指標
        self.stochastic = bt.indicators.Stochastic(self.data)
        self.k = self.stochastic.percK
        self.d = self.stochastic.percD
        self.j = 3 * self.k - 2 * self.d  # J線計算公式
        
        # RSI 指标
        self.rsi = bt.indicators.RSI(self.data.close, period=14)
        
        # DMI 指标
        self.dmi = bt.indicators.DMI(self.data, period=14)
        self.plusDI = self.dmi.plusDI  # 正確的屬性名稱
        self.minusDI = self.dmi.minusDI

    def next(self):
        # 檢查是否有未完成的訂單
        if self.order and self.order.status in [bt.Order.Submitted, bt.Order.Accepted]:
            return
        
        # 如果沒有持倉且符合做空條件，則下達做空訂單
        if not self.position and eval(self.params.sell_expression):
            self.order = self.sell()  # 做空
            self.entry_price = self.data.close[0]  # 記錄進場價格

        # 如果持有做空倉位且符合平倉條件，則平掉做空倉位
        elif self.position.size < 0 and eval(self.params.buy_expression):
            self.order = self.close()  # 平掉做空倉位


def run_backtest(data_file, from_date, to_date, buy_expression, sell_expression, plot=False, plot_path=None):
    cerebro = bt.Cerebro()
    cerebro.addstrategy(MultiStrategy, buy_expression=buy_expression, sell_expression=sell_expression)

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
        openinterest=-1,
        timeframe=bt.TimeFrame.Minutes,
        compression=60
    )

    cerebro.adddata(data)
    cerebro.broker.setcash(1000000.0)
    cerebro.addsizer(bt.sizers.PercentSizer, percents = 90)
    cerebro.broker.setcommission(commission=0.0035)

    # 添加分析器
    cerebro.addanalyzer(btanalyzers.SharpeRatio, _name='sharpe_ratio', timeframe=bt.TimeFrame.Minutes, compression=60, riskfreerate=2.28e-6)
    cerebro.addanalyzer(btanalyzers.DrawDown, _name='drawdown')


    results = cerebro.run()
    final_value = cerebro.broker.getvalue() - 1000000.0
    sharpe_ratio = results[0].analyzers.sharpe_ratio.get_analysis()['sharperatio']
    max_drawdown = results[0].analyzers.drawdown.get_analysis()['max']['drawdown']

    if plot:
        # 显示图表
        img = cerebro.plot(
            style='candlestick', 
            barup='red', 
            bardown='green',
            start=3
        )
        # filename = f'{from_date}.png'
        # img[0][0].savefig(filename)
        return final_value, buy_expression, sell_expression, sharpe_ratio, max_drawdown
    else:
        return final_value, buy_expression, sell_expression, sharpe_ratio, max_drawdown