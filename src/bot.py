import time
from ml_interface import MLInterface
from user_interface import UserInterface
from logger import Logger
from bybit import BybitAPI


class TradingBot:
    def __init__(self, mode):
        self.mode = mode
        self.ml_interface = MLInterface()
        self.user_interface = UserInterface()
        self.bybit = BybitAPI()
        self.logger = Logger()

    def run(self):
        while True:
            order_params = None

            if self.mode == 'ml':
                order_params = self.ml_interface.get_price_signal()
            elif self.mode == 'user':
                order_params = self.user_interface.create_order()

            self.execute_trade(order_params)
            time.sleep(1)

    def execute_trade(self, order_params):
        response = self.bybit.create_order(**order_params)

        print("Create Order Response:", response)


if __name__ == '__main__':
    mode = input("Enter mode (ml/user): ")
    bot = TradingBot(mode)
    bot.run()
