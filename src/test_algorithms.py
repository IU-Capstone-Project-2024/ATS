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
        self.data = None

        if self.mode == 'ml':
            self.data = self.get_historical_data(60 * 60 * 24 * 31)
            self.data['close'] = pd.to_numeric(self.data['close'])
            self.data = self.data.sort_values(by='timestamp')
            self.algorithm = SMAAlgorithm(symbol="BTCUSDT", data=self.data, short_window=40, long_window=100)
            self.algorithm.generate_signals()
            # self.algorithm.plot_signals(n_intervals=100)

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
            return self.get_historical_data(60 * 60 * 24 * 30)
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

    def get_historical_data(self, period):
        interval = "5"
        end_time = int(time.time() * 1000)
        start_time = end_time - period * 1000

        all_data = pd.DataFrame()

        while start_time <= end_time:
            df = self.bybit.get_historical_data(interval, start_time, int(1440 // int(interval)))
            if df.empty:
                break
            all_data = pd.concat([all_data, df])
            start_time = start_time + 86400 * 1000

        # all_data.to_csv('historical_data.csv')
        # print(all_data)
        return all_data

    def get_current_position(self):
        return self.algorithm.signals['positions'].iloc[-1]

    def update(self):
        new_data = self.get_historical_data(60 * 15)
        new_data = new_data.sort_values(by='timestamp')
        self.data.join(new_data, how='outer', lsuffix='timestamp')
        self.algorithm = SMAAlgorithm(symbol="BTCUSDT", data=self.data, short_window=40, long_window=100)
        self.algorithm.generate_signals()


if __name__ == '__main__':
    mode = questionary.select("Select mode", choices=["ml", "user"]).ask()
    bot = TradingBot(mode)
    try:
        bot.run()
    except Exception as e:
        print(e)
