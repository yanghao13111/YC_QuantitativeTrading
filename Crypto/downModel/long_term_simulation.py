# long_term_simulation.py
import matplotlib.pyplot as plt
import backTesting_logic
import time
import indicators
import main

def long_term_simulation():
    config = {
        'symbol': 'BTC/USDT',
        'timeframe': '1h',
        'buy_pool': [indicators.ema5_h, indicators.ema20_h, indicators.ema10_l, indicators.macd_g, indicators.macd_d, indicators.kd_g, indicators.kd_g],
        'sell_pool': [indicators.ema5_h, indicators.ema20_h, indicators.ema10_l, indicators.macd_g, indicators.macd_d, indicators.kd_g, indicators.kd_g],
        'buy_combined': 2,
        'sell_combined': 2,
    }

    # 用于存储每个月的净收益
    monthly_profits = []

    for month in range(6, 0, -1):
        print(f"------ Starting Simulation for {month} Months Back ------")
        train_start, train_end = main.get_dates(month + 1)
        validation_start, validation_end = main.get_dates(month)

        train_file = main.collect_and_save_data(config['symbol'], config['timeframe'], train_start, train_end, f'Crypto/Simulation/train_data_{month}.csv')
        validation_file = main.collect_and_save_data(config['symbol'], config['timeframe'], validation_start, validation_end, f'Crypto/Simulation/validation_data_{month}.csv')

        # train_file = f'Crypto/Simulation/train_data_{month}.csv'
        # validation_file = f'Crypto/Simulation/validation_data_{month}.csv'

        start_time = time.time()
        top_results = main.run_backtests(config['buy_pool'], config['sell_pool'], config['buy_combined'], config['sell_combined'], train_file, train_start, train_end)
        top_results = top_results[:1]

        for result in top_results:
            value, buy_expression, sell_expression, sharpe, drawdown = result
            val_result = backTesting_logic.run_backtest(validation_file, validation_start, validation_end, buy_expression, sell_expression)
            val_value, val_buy_expression, val_sell_expression, val_sharpe, val_drawdown = val_result
            print(f"買入策略組合: {val_buy_expression}, 賣出策略組合: {val_sell_expression}, 淨收益: {val_value}, sharpe: {val_sharpe}, MDD: {val_drawdown}")
            monthly_profits.append(val_value)

        end_time = time.time()
        print(f"執行時間：{end_time - start_time} 秒")
        print(f"------ End of Simulation for {month} Months Back ------\n")

    # 绘制柱状图
    months = list(range(6, 0, -1))
    plt.bar(months, monthly_profits)
    plt.xlabel('Months Back')
    plt.ylabel('Net Profit')
    plt.title('Net Profit by Month')
    plt.show()

if __name__ == "__main__":
    long_term_simulation()
