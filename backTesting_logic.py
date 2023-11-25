import backtrader as bt
import os
from datetime import datetime

class MultiMATradingStrategy(bt.Strategy):
    params = (
        ("ma5_period", 5),
        ("ma10_period", 10),
        ("ma20_period", 20),
        ("ma50_period", 50),
        ("ma100_period", 100),
        ("ma200_period", 200)
    )

    def __init__(self):
        # 初始化移动平均线指标
        self.ma5 = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.ma5_period)
        self.ma10 = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.ma10_period)
        self.ma20 = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.ma20_period)
        self.ma50 = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.ma50_period)
        self.ma100 = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.ma100_period)
        self.ma200 = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.ma200_period)

        self.order = None

    def next(self):
        # 取消未完成的订单
        if self.order:
            self.cancel(self.order)

        # 入场条件
        if not self.position and self.ma5[-1] <= self.ma10[-1] and self.ma5[0] > self.ma10[0]:
            self.order = self.buy()

        # 出场条件
        elif self.position and (self.ma5[0] < self.ma10[0] or self.ma10[0] < self.ma20[0] or self.data.close[0] < self.ma50[0]):
            self.order = self.close()

    def notify_order(self, order):
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f'BUY EXECUTED, Price: {order.executed.price}, Cost: {order.executed.value}, Comm {order.executed.comm}')
            elif order.issell():
                self.log(f'SELL EXECUTED, Price: {order.executed.price}, Cost: {order.executed.value}, Comm {order.executed.comm}')
            self.bar_executed = len(self)

    def log(self, txt, dt=None):
        ''' Logging function '''
        dt = dt or self.datas[0].datetime.date(0)
        print(f'{dt.isoformat()} {txt}')


# 目前策略
def run_backtest(data_file, from_date, to_date):
    cerebro = bt.Cerebro()
    cerebro.addstrategy(MultiMATradingStrategy)

    data = bt.feeds.GenericCSVData(
        dataname=data_file,
        fromdate=from_date,  # 根据您的数据起始日期调整
        todate=to_date,      # 根据您的数据结束日期调整
        nullvalue=0.0,
        dtformat=('%Y-%m-%d %H:%M:%S'),
        datetime=0,
        time=-1,  # 没有单独的时间列
        open=1,
        high=2,
        low=3,
        close=4,
        volume=5,
        openinterest=-1,
        timeframe=bt.TimeFrame.Minutes,  # 由于数据是每小时的，我们将时间框架设置为分钟
        compression=60  # 将数据压缩设置为每 60 分钟
    )

    cerebro.adddata(data)

    # 设置初始资金
    cerebro.broker.setcash(1000000.0)

    # 设置每次交易的股票数量（可选）
    cerebro.addsizer(bt.sizers.FixedSize, stake=10)

    # 设置佣金（可选）
    cerebro.broker.setcommission(commission=0.001)

    # 运行策略
    cerebro.run()

    # 打印最终结果
    print(f'Final Portfolio Value: {cerebro.broker.getvalue()}')

    # 绘制结果
    cerebro.plot(style='candlestick')