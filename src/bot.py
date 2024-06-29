import time
from ml_interface import MLInterface
from user_interface import UserInterface
from logger import Logger
from bybit import BybitAPI

import questionary


class TradingBot:
    def __init__(self, mode):
        self.mode = mode
        self.ml_interface = MLInterface()
        self.user_interface = UserInterface()
        self.bybit = BybitAPI()
        self.logger = Logger()

    def run(self):
        while True:
            action = self.select_action()

            self.do_action(action)

            time.sleep(1)

    def select_action(self):
        actions = ["create_order", "get_unfilled_orders", "cancel_order", "get_historical_data"]

        return questionary.select("Select action", choices=actions).ask()

    def do_action(self, action):
        if action == "create_order":
            order_params = None
            if self.mode == 'ml':
                order_params = self.ml_interface.get_price_signal()
            elif self.mode == 'user':
                order_params = self.user_interface.create_order()

            return self.execute_trade(order_params)
        elif action == "get_unfilled_orders":
            return self.bybit.get_unfilled_orders()
        elif action == "cancel_order":
            order_id = input("Enter order ID: ")
            return self.bybit.cancel_order(order_id)
        elif action == "get_historical_data":
            return self.bybit.get_historical_data()


if __name__ == '__main__':
    mode = questionary.select("Select mode", choices=["ml", "user"]).ask()
    bot = TradingBot(mode)
    bot.run()
