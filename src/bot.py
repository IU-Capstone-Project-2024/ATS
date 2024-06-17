import time
from ml_interface import MLInterface
from user_interface import UserInterface
from trade_executor import TradeExecutor
from logger.py import Logger


class TradingBot:
    def __init__(self, mode):
        self.mode = mode
        self.ml_interface = MLInterface()
        self.user_interface = UserInterface()
        self.trade_executor = TradeExecutor()
        self.logger = Logger()

    def run(self):
        while True:
            if self.mode == 'ml':
                signal = self.ml_interface.get_price_signal()
                self.execute_trade(signal)
            elif self.mode == 'user':
                command = self.user_interface.get_user_command()
                self.execute_trade(command)
            time.sleep(1)

    def execute_trade(self, signal):
        # signal should have the structure {'action': 'buy'/'sell', 'symbol': 'BTCUSD', 'qty': 1}
        action = signal.get('action')
        symbol = signal.get('symbol')
        qty = signal.get('qty')

        if action == 'buy':
            response = self.trade_executor.buy(symbol, qty)
        elif action == 'sell':
            response = self.trade_executor.sell(symbol, qty)

        trade_log = {
            'action': action,
            'symbol': symbol,
            'qty': qty,
            'response': response,
            'timestamp': time.time()
        }
        self.logger.log_trade(trade_log)


if __name__ == '__main__':
    mode = input("Enter mode (ml/user): ")
    bot = TradingBot(mode)
    bot.run()
