import uuid
from api.bybit_api import BybitAPI

bybit = BybitAPI()

response = bybit.create_order(category="spot",
                              symbol="BTCUSDT",
                              side="Buy",
                              order_type="Limit",
                              qty="0.001",
                              price="10000",
                              time_in_force="GTC")

print("Create Order Response:", response)

response = bybit.get_unfilled_orders(category="linear", settle_coin="USDT")
print("Unfilled Orders Response:", response)