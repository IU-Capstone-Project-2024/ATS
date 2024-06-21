import requests
import time
import hashlib
import hmac
import uuid
import pandas as pd
from dotenv import load_dotenv
import os
import json

load_dotenv()

class BybitAPI:
    def __init__(self, url: str = "https://api-testnet.bybit.com"):
        self.api_key = os.getenv("API_KEY")
        self.secret_key = os.getenv("API_SECRET")
        self.url = url
        self.recv_window = str(5000)
        self.session = requests.Session()

    def _get_timestamp(self) -> str:
        return str(int(time.time() * 10 ** 3))

    def _generate_signature(self, payload: str) -> str:
        param_str = self._get_timestamp() + self.api_key + self.recv_window + payload
        hash = hmac.new(bytes(self.secret_key, "utf-8"), param_str.encode("utf-8"), hashlib.sha256)
        return hash.hexdigest()

    def _http_request(self, endpoint: str, method: str, payload: str) -> requests.Response:
        timestamp = self._get_timestamp()
        signature = self._generate_signature(payload)
        headers = {
            'X-BAPI-API-KEY': self.api_key,
            'X-BAPI-SIGN': signature,
            'X-BAPI-SIGN-TYPE': '2',
            'X-BAPI-TIMESTAMP': timestamp,
            'X-BAPI-RECV-WINDOW': self.recv_window,
            'Content-Type': 'application/json'
        }
        url = self.url + endpoint
        if method == "POST":
            response = self.session.request(method, url, headers=headers, data=payload)
        else:
            response = self.session.request(method, url + "?" + payload, headers=headers)
        return response

    def create_order(self, category: str, symbol: str, side: str, order_type: str, qty: str, price: str,
                     time_in_force: str):
        endpoint = "/v5/order/create"
        method = "POST"
        order_link_id = uuid.uuid4().hex
        payload = {
            "category": category,
            "symbol": symbol,
            "side": side,
            "positionIdx": 0,
            "orderType": order_type,
            "qty": qty,
            "price": price,
            "timeInForce": time_in_force,
            "orderLinkId": order_link_id
        }
        response = self._http_request(endpoint, method, json.dumps(payload))
        return response.json()

    def get_unfilled_orders(self, category: str, settle_coin: str):
        endpoint = "/v5/order/realtime"
        method = "GET"
        payload = f'category={category}&settleCoin={settle_coin}'
        response = self._http_request(endpoint, method, payload)
        return response.json()

    def cancel_order(self, category: str, symbol: str, order_link_id: str):
        endpoint = "/v5/order/cancel"
        method = "POST"
        payload = {
            "category": category,
            "symbol": symbol,
            "orderLinkId": order_link_id
        }
        response = self._http_request(endpoint, method, json.dumps(payload))
        return response.json()

    def get_historical_data(self, symbol: str, interval: str, start_time: int, limit: int = 200):
        """
        Получение исторических данных с Bybit API v5

        :param symbol: Торговая пара
        :param interval: Интервал (1, 3, 5, 15, 30, 60, 120, 240, 360, 720, D, W, M)
        :param start_time: Время начала в формате UNIX timestamp
        :param limit: Максимальное количество свечей (до 200 за запрос)
        :return: DataFrame с историческими данными
        """
        endpoint = "/v5/market/kline"
        params = {
            "category": "linear",
            "symbol": symbol,
            "interval": interval,
            "start": start_time,
            "limit": limit
        }
        response = self.session.get(self.url + endpoint, params=params, headers=self._get_headers())
        data = response.json()['result']['list']
        df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        return df