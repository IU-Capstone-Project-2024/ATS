import time
import questionary
import pandas as pd
from algorithms.sma_algorithm import SMAAlgorithm
from algorithms.rsi_algorithm import RSIAlgorithm
from user_interface import UserInterface
from logger import Logger
from bybit import BybitAPI

class TradingBot:
    def __init__(self, mode):
        self.mode = mode
        self.user_interface = UserInterface()
        self.bybit = BybitAPI()
        self.logger = Logger()
        self.algorithm = None

        if self.mode == 'ml':
            data = self.get_historical_data()
            data['close'] = pd.to_numeric(data['close'])
            data = data.sort_values(by='timestamp')
            # self.algorithm = SMAAlgorithm(symbol="BTCUSDT", data=data, short_window=40, long_window=100)
            self.algorithm = RSIAlgorithm(symbol="BTCUSDT", data=data, period=10)
            self.algorithm.generate_signals()
            self.algorithm.plot_signals(n_intervals=200)

    def run(self):
        while True:
            try:
                action = self.select_action()
                print(self.do_action(action))
            except Exception as e:
                print(f"Error: {e}")
            time.sleep(1)

    def select_action(self):
        actions = ["create_order", "get_unfilled_orders", "cancel_order", "get_historical_data", "exit"]
        return questionary.select("Select action", choices=actions).ask()

    def do_action(self, action):
        if action == "create_order":
            order_params = None
            if self.mode == 'ml':
                order_params = self.get_ml_order_params()
            elif self.mode == 'user':
                order_params = self.user_interface.create_order()

            response = self.bybit.create_order(order_params)
            self.logger.log_trade(order_params)
            return response
        elif action == "get_unfilled_orders":
            return self.bybit.get_unfilled_orders()
        elif action == "cancel_order":
            order_id = input("Enter order ID: ")
            return self.bybit.cancel_order(order_id)
        elif action == "get_historical_data":
            return self.get_historical_data()
        elif action == "exit":
            exit()

    def get_ml_order_params(self):
        latest_signal = self.algorithm.get_signals().iloc[-1]

        order_params = {
            "category": "spot",
            "symbol": "BTCUSDT",
            "side": "Buy" if latest_signal['signal'] == 1.0 else "Sell",
            "order_type": "Limit",
            "qty": "0.001",
            "price": "1000",
            "time_in_force": "GTC"
        }

        return order_params

    def get_historical_data(self):
        interval = "15"
        end_time = int(time.time() * 1000)
        start_time = end_time - 60 * 60 * 24 * 30 * 1000

        all_data = pd.DataFrame()

        while start_time < end_time:
            df = self.bybit.get_historical_data(interval, start_time, 4 * 24)
            if df.empty:
                break
            all_data = pd.concat([all_data, df])
            start_time = start_time + 86400 * 1000

        all_data.to_csv('historical_data.csv')
        return all_data


if __name__ == '__main__':
    mode = questionary.select("Select mode", choices=["ml", "user"]).ask()
    bot = TradingBot(mode)
    try:
        bot.run()
    except Exception as e:
        print(e)
