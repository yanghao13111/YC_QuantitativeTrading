import backtrader as bt
import math
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
    return expression.replace('self.', f'd.')

class MultiStrategy(bt.Strategy):
    params = (
        # 買入和賣出表達式參數
        ('buy_expression', ''),
        ('sell_expression', ''),
        ('verbose', True),
    )

    def __init__(self):
        # 创建一个字典来跟踪每个数据集的订单和价格
        self.orders = {}
        self.entry_prices = {}
        self.entry_dates = {}  # 新增一个字典来跟踪买入日期
        self.trade_list = []
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
                d.ema264 = bt.ind.EMA(d.close, period=264)
            except Exception as e:
                print(f"Error initializing indicators for {d._name}: {e}")
                continue

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


    def notify_trade(self, trade):
        if trade.isclosed:
            entry_price = trade.price * 1000  # 買入價格
            profit_ratio = trade.pnl / entry_price  # 計算損益比例

            self.trade_list.append({
                'name': trade.data._name,
                'profit': trade.pnlcomm,
                'profit_ratio': profit_ratio
            })


    def notify_order(self, order):
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
                if self.params.verbose:  # 根據 verbose 參數決定是否打印
                    print(f"Processing date: {dt}, stock: {dn}")

                # 获取当前数据集的订单和持仓
                current_order = self.orders[dn]
                current_position = self.getposition(d).size

                # 斜率
                slope_ema5 = (d.ema5[0] - d.ema5[-1])
                slope_ema10 = (d.ema10[0] - d.ema10[-1])
                slope_ema22 = (d.ema22[0] - d.ema22[-1])
                slope_ema66 = (d.ema66[0] - d.ema66[-1])
                angle_ema5 = math.atan(slope_ema5) * (180 / math.pi)  # 轉換為角度
                angle_ema10 = math.atan(slope_ema10) * (180 / math.pi)  # 轉換為角度
                angle_ema22 = math.atan(slope_ema22) * (180 / math.pi)  # 轉換為角度
                angle_ema66 = math.atan(slope_ema66) * (180 / math.pi)  # 轉換為角度

                # 检查是否有未完成的订单
                if current_order and current_order.status in [bt.Order.Submitted, bt.Order.Accepted]:
                    continue

                # 准备买入和卖出条件
                buy_conditions = replace_self_with_data(self.params.buy_expression, d)
                sell_conditions = replace_self_with_data(self.params.sell_expression, d)

                # 没有持仓时，检查是否应该买入
                if current_position == 0 and eval(buy_conditions):
                    print(f'next {dt}: BUY EXECUTED - {dn}, Price: {d.close[0]}')
                    self.orders[dn] = self.buy(data=d)
                    self.entry_prices[dn] = d.close[0]
                    self.entry_dates[dn] = dt

                # 持有做多仓位时，检查是否应该平仓
                elif current_position > 0 and eval(sell_conditions) and d.volume[0] >= 0:
                    print(f'next {dt}: SELL EXECUTED - {dn}, Price: {d.close[0]}')
                    self.orders[dn] = self.close(data=d)

            except Exception as e:
                # 如果在处理特定股票时发生异常，打印错误信息
                print(f"Error processing date: {dt}, stock: {dn}: {e}")


def run_backtest(data_files, from_date, to_date, buy_expression, sell_expression, plot=False, verbose=True):
    cerebro = bt.Cerebro()
    cerebro.broker.set_coc(True)
    cerebro.addstrategy(MultiStrategy, buy_expression=buy_expression, sell_expression=sell_expression, verbose=verbose)

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

    if plot:
        # 显示图表
        cerebro.plot(style='candlestick', barup='red', bardown='green')
    
    return final_value, buy_expression, sell_expression, sharpe_ratio, max_drawdown, best_trades, worst_trades

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