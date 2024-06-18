from pybit.unified_trading import HTTP
from config import BYBIT_API_KEY, BYBIT_API_SECRET


class TradeExecutor:
    def __init__(self):
        self.session = HTTP(
            testnet=True,
            api_key=BYBIT_API_KEY,
            api_secret=BYBIT_API_SECRET,
        )

    def buy(self, symbol, qty):
        response = {}
        return response

    def sell(self, symbol, qty):
        response = {}
        return response
