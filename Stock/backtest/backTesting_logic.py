import backtrader as bt
import math
from itertools import combinations, product
from datetime import datetime
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
        self.orders = {}
        self.entry_prices = {}
        self.entry_dates = {}  # 新增一个字典来跟踪买入日期
        self.trade_list = []
        self.win_count = 0
        self.loss_count = 0
        self.trade_analyzer = None

        for i, d in enumerate(self.datas):
            if self.params.verbose:  # 根據 verbose 參數決定是否打印
                print(f"Initializing indicators for {d._name}")  # 打印当前正在处理的股票名称
            # 对于每只股票，创建技术指标
            self.orders[d._name] = None
            self.entry_prices[d._name] = None

            try:
                # 创建和保存指标，可根据您的需要进行调整
                d.ema5 = bt.ind.EMA(d.close, period=5)
                d.ema10 = bt.ind.EMA(d.close, period=10)
                d.ema22 = bt.ind.EMA(d.close, period=22)
                d.ema66 = bt.ind.EMA(d.close, period=66)
                # d.ema264 = bt.ind.EMA(d.close, period=264)
                d.ema_volume_5 = bt.ind.EMA(d.volume, period=5) 
            except Exception as e:
                print(f"Error initializing indicators for {d._name}: {e}")
                continue


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


    def next(self):
        for i, d in enumerate(self.datas):
            dt, dn = self.datetime.date(), d._name
            try:
                if self.params.verbose:
                    print(f"Processing date: {dt}, stock: {dn}")

                current_order = self.orders[dn]
                current_position = self.getposition(d).size

                # 檢查是否存在賣出信號
                sell_signal = eval(self.params.sell_expression)

                # 如果當天有賣出信號且存在未完成的訂單，則取消該訂單
                if sell_signal and current_order and current_order.status in [bt.Order.Submitted, bt.Order.Accepted]:
                    self.cancel(current_order)
                    if self.params.debug:
                        print(f'{dt}: CANCEL ORDER - {dn}, Existing order canceled due to sell signal')
                    continue

                # 沒有持倉時，檢查是否應該買入
                if current_position == 0 and not sell_signal and eval(self.params.buy_expression):
                    if self.params.debug:
                        print(f'next {dt}: BUY EXECUTED - {dn}, Price: {d.close[0]}')
                    self.orders[dn] = self.buy(data=d)
                    self.entry_prices[dn] = d.close[0]
                    self.entry_dates[dn] = dt

                # 持有做多仓位时，检查是否应该平仓
                elif current_position > 0:
                    # 检查是否滿足原本的賣出條件
                    sell_condition = eval(self.params.sell_expression) and d.volume[0] >= 0
                    loss_condition = d.close[0] < self.entry_prices[dn] * 0.92
                    if sell_condition or loss_condition:
                        if self.params.debug:
                            print(f'next {dt}: SELL EXECUTED - {dn}, Price: {d.close[0]}')
                        self.orders[dn] = self.close(data=d)
                    # elif eval(self.params.add_expression):
                    #     self.orders[dn] = self.buy(data=d)

            except Exception as e:
                print(f"Error processing date: {dt}, stock: {dn}: {e}")


def run_backtest(data_files, from_date, to_date, buy_expression, sell_expression, add_expression, plot=False, verbose=True):
    cerebro = bt.Cerebro()
    cerebro.broker.set_coc(True)
    cerebro.addstrategy(MultiStrategy, buy_expression=buy_expression, sell_expression=sell_expression, add_expression=add_expression, verbose=verbose)

    for file in data_files:
        data = bt.feeds.GenericCSVData(
            dataname=file,
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
    win_rate = results[0].win_count / total_trades if total_trades > 0 else 0

    if plot:
        # 显示图表
        cerebro.plot(style='candlestick', barup='red', bardown='green')
    
    return final_value, buy_expression, sell_expression, sharpe_ratio, max_drawdown, best_trades, worst_trades, win_rate, total_trades

# # 測試代碼
# # 讀取 CSV 文件以獲取台灣股票代碼列表
# taiwan_stocks_df = pd.read_csv('Stock/test.csv')  # 替換為你的 CSV 文件路徑
# # 確保股票代碼為字符串格式並添加 ".TW"
# taiwan_stocks = taiwan_stocks_df['StockID'].apply(lambda x: f"{x}").tolist()

# # 創建數據文件路徑列表
# data_folder = 'Stock/trainDataSet'  # 設定你的數據集文件夾路徑
# data_files = [f'{data_folder}/{stock}.csv' for stock in taiwan_stocks]  # 假設每個股票的數據文件名是 '{股票代碼}.csv'

# # # 測試代碼
# # data_files = ['Stock/trainDataSet/2230.csv']  # 更新您的股票数据文件路径

# buy_expression = 'self.ema5[0] > self.ema10[0] and self.ema10[0] > self.ema22[0] and self.ema22[0] > self.ema66[0] and self.ema66[0] > self.ema264[0] and self.ema5[0] > self.ema5[-1] and self.ema10[0] > self.ema10[-1] and self.ema22[0] > self.ema22[-1] and self.ema66[0] > self.ema66[-1] and self.ema264[0] > self.ema264[-1] and abs((self.ema10[0] - self.ema22[0]) / self.ema22[0]) < 0.02 and abs((self.ema22[0] - self.ema66[0]) / self.ema66[0]) < 0.02 and abs((self.ema66[0] - self.ema264[0]) / self.ema264[0]) < 0.1 and self.volume[0] > 2 * self.volume[-1] and self.volume[0] > 300 * 1000'
# sell_expression = 'self.ema10[0] < self.ema10[-1]'

# results = run_backtest(data_files, '2015-01-01', '2019-01-01', buy_expression, sell_expression)
# print(results[0])