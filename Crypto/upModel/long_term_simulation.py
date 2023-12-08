# long_term_simulation.py
import matplotlib.pyplot as plt
import backTesting_logic
import main


Start_month = 60
End_month = 0

def long_term_simulation():
    config = {
        'symbol': 'BTC/USDT',
        'timeframe': '1h',
        'buy_expression': 'self.rsi[0] < 30',
        'sell_expression': 'self.ema10[0] < self.ema20[0] and self.data.close[0] > self.ema20[0] and self.macd.macd[0] < self.macd.signal[0]'
    }

    # 用于存储每个月的净收益
    monthly_profits = []

    for month in range(Start_month, End_month, -1):
        print(f"------ Starting Simulation for {month} Months Back ------")
        test_start, test_end = main.get_dates(month)

        test_file = main.collect_and_save_data(config['symbol'], config['timeframe'], test_start, test_end, f'Crypto/upModel/Simulation/test_data_{month}.csv')
        # test_file = f'Crypto/upModel/Simulation/test_data_{month}.csv'

        result = backTesting_logic.run_backtest(test_file, test_start, test_end, config['buy_expression'], config['sell_expression'])
        value, buy_expression, sell_expression, sharpe, drawdown = result
        print(f"""買入策略組合: {buy_expression}, 
賣出策略組合: {sell_expression}, 
淨收益: {value}, 
sharpe: {sharpe}, 
MDD: {drawdown}""")


        monthly_profits.append(value)

        print(f"------ End of Simulation for {month} Months Back ------\n")

    # 計算總淨利潤
    total_profit = sum(monthly_profits)

    # 將月份和總淨利潤添加到列表中
    months = [str(month) for month in range(Start_month, End_month, -1)]
    months.append('Total')  # 添加特殊標籤
    monthly_profits.append(total_profit)  # 添加總淨利潤

    # 繪製柱狀圖
    plt.bar(months, monthly_profits)
    plt.xlabel('Months Back / Total')
    plt.ylabel('Net Profit')
    plt.title('Net Profit by Month and Total Profit')
    plt.show()

if __name__ == "__main__":
    long_term_simulation()
