import backtrader as bt
from datetime import datetime
import math
import backtrader.analyzers as btanalyzers

class MultiStrategy(bt.Strategy):
    params = (
        # 買入和賣出表達式參數
        ('buy_expression', ''),
        ('sell_expression', ''),
        ('add_expression', ''),
        ('verbose', True),
        ('debug', False),  # 新增 debug 參數，默認為 False
    )

    def __init__(self):
        # 创建一个字典来跟踪每个数据集的订单和价格
        self.order = None 
        self.entry_price = None 
        self.entry_date = None
        self.trade_list = []
        self.win_count = 0
        self.loss_count = 0
        self.trade_analyzer = None

        try:
            # EMA 指标
            self.ema5 = bt.indicators.EMA(self.data.close, period=5)
            self.ema10 = bt.indicators.EMA(self.data.close, period=10)
            self.ema22 = bt.indicators.EMA(self.data.close, period=22)
            self.ema66 = bt.indicators.EMA(self.data.close, period=66)
            # d.ema264 = bt.ind.EMA(d.close, period=264)
            self.ema_volume_5 = bt.ind.EMA(self.data.volume, period=5) 
        except Exception as e:
            print(f"Error initializing indicators for {self._name}: {e}")

    def next(self):

        dt, dn = self.datetime.date(), self.data._name
        try:
            if self.params.verbose:
                print(f"Processing date: {dt}, stock: {dn}")

            current_position = self.getposition().size

            # 檢查是否存在賣出信號
            sell_signal = eval(self.params.sell_expression)

            # 如果當天有賣出信號且存在未完成的訂單，則取消該訂單
            if sell_signal and self.order and self.order.status in [bt.Order.Submitted, bt.Order.Accepted]:
                self.cancel(self.order)
                if self.params.debug:
                    print(f'{dt}: CANCEL ORDER - {dn}, Existing order canceled due to sell signal')

            # 沒有持倉時，檢查是否應該買入
            if current_position == 0 and not sell_signal and eval(self.params.buy_expression):
                if self.params.debug:
                    print(f'next {dt}: BUY EXECUTED - {dn}, Price: {self.data.close[0]}')
                self.order = self.buy()
                self.entry_prices = self.data.close[0]
                self.entry_dates = dt

            # 持有做多仓位时，检查是否应该平仓
            elif current_position > 0:
                # 检查是否滿足原本的賣出條件
                sell_condition = eval(self.params.sell_expression) and self.data.volume[0] >= 0
                if sell_condition:
                    if self.params.debug:
                        print(f'next {dt}: SELL EXECUTED - {dn}, Price: {self.data.close[0]}')
                    self.orders = self.close()
                # elif eval(self.params.add_expression):
                #     self.orders[dn] = self.buy(data=d)

        except Exception as e:
            print(f"Error processing date: {dt}, stock: {dn}: {e}")
            raise

    def notify_trade(self, trade):
        if trade.isclosed:
            entry_price = trade.price * 1000  # 買入價格
            profit_ratio = trade.pnl / entry_price  # 計算損益比例

            if trade.pnlcomm > 0:
                self.win_count += 1
            else:
                self.loss_count += 1

            self.trade_list.append({
                'name': trade.data._name,
                'profit': trade.pnlcomm,
                'profit_ratio': profit_ratio
            })

    def notify_order(self, order):
        if self.params.debug:
            dt, dn = self.datetime.date(), order.data._name
            if order.status in [bt.Order.Submitted, bt.Order.Accepted]:
                # 订单被提交或接受时打印信息
                print(f'{dt}: Order Submitted/Accepted - {order.info["name"]}, Type: {"Buy" if order.isbuy() else "Sell"}')

            if order.status in [bt.Order.Completed]:
                if order.isbuy():
                    self.entry_prices[dn] = order.executed.price
                    self.entry_dates[dn] = dt
                    print(f'{dt}: BUY EXECUTED - {dn}, Price: {order.executed.price}, Cost: {order.executed.value}, Commission: {order.executed.comm}')
                elif order.issell():
                    print(f'{dt}: SELL EXECUTED - {dn}, Price: {order.executed.price}, Cost: {order.executed.value}, Commission: {order.executed.comm}')

            elif order.status in [bt.Order.Canceled, bt.Order.Margin, bt.Order.Rejected]:
                print(f'{dt}: Order Canceled/Margin/Rejected')


def run_backtest(data_file, from_date, to_date, buy_expression, sell_expression, add_expression, plot=False, verbose=True):
    cerebro = bt.Cerebro()
    cerebro.broker.set_coc(True)
    cerebro.addstrategy(MultiStrategy, buy_expression=buy_expression, sell_expression=sell_expression, add_expression=add_expression, verbose=verbose)

    data = bt.feeds.GenericCSVData(
        dataname=data_file,
        fromdate=from_date,
        todate=to_date,
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
    cerebro.broker.setcash(1000000000.0)

    # 设置每笔交易买入1股股票
    cerebro.addsizer(bt.sizers.FixedSize, stake=1000)

    # 设置佣金
    cerebro.broker.setcommission(commission=0.0035)

    # 添加分析器
    cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='trade_analyzer')
    cerebro.addanalyzer(btanalyzers.SharpeRatio, _name='sharpe_ratio', timeframe=bt.TimeFrame.Days)
    cerebro.addanalyzer(btanalyzers.DrawDown, _name='drawdown')

    # 运行策略
    results = cerebro.run()
    final_value = cerebro.broker.getvalue() - 1000000000.0
    sharpe_ratio = results[0].analyzers.sharpe_ratio.get_analysis()['sharperatio']
    max_drawdown = results[0].analyzers.drawdown.get_analysis()['max']['drawdown']

    # 根據損益比例排序交易，並選出虧損最多的前五名
    trades = sorted(results[0].trade_list, key=lambda x: x['profit_ratio'])

    # 选择盈利最高的前五名和虧損最多的前五名交易
    best_trades = trades[-5:]
    worst_trades = trades[:5]

    # 計算勝率
    total_trades = results[0].win_count + results[0].loss_count
    win_count = results[0].win_count

    if plot:
        # 显示图表
        cerebro.plot(style='candlestick', barup='red', bardown='green')
    
    return final_value, buy_expression, sell_expression, sharpe_ratio, max_drawdown, best_trades, worst_trades, win_count, total_trades


# # 測試代碼
# data_file = 'Stock/trainDataSet/2230.csv'  # 更新您的股票数据文件路径

# buy_expression = 'self.ema5[0] > self.ema10[0]'
# sell_expression = 'self.ema10[0] < self.ema10[-1]'

# results = run_backtest(data_file, datetime(2019, 1, 1), datetime(2020, 1, 1), buy_expression, sell_expression, '', plot=True)
# print(results[0])