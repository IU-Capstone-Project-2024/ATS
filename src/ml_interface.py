import time
import zmq
import json
import csv
from test_algorithms import Algorithms
from bybit import BybitAPI


def create_order(side):
    category = "spot"
    symbol = "BTCUSDT"
    side = side
    order_type = "Limit"
    qty = "0.001"
    price = None
    time_in_force = "GTC"

    order_params = {
        "category": category,
        "symbol": symbol,
        "side": side,
        "order_type": order_type,
        "qty": qty,
        "price": price,
        "time_in_force": time_in_force
    }

    return order_params


def voting(model_decisions, positions):
    votes = {"Buy": 0, "Sell": 0, "Hold": 0}

    for decision in model_decisions:
        if int(decision) == 2:
            votes["Buy"] += 1
        elif int(decision) == 1:
            votes["Sell"] += 1
        elif int(decision) == 0:
            votes["Hold"] += 1

    for position in positions:
        if int(position) == 1:
            votes["Buy"] += 0.2
        elif int(position) == 0:
            votes["Hold"] += 0.2
        elif int(position) == -1:
            votes["Sell"] += 0.2

    sorted_votes = sorted(votes.items(), key=lambda item: item[1], reverse=True)

    if sorted_votes[0][1] > sorted_votes[1][1]:
        return sorted_votes[0][0].capitalize()
    return "Hold"


class MLInterface:
    def __init__(self):
        self.bybit = BybitAPI()
        print("I started!")
        tb = Algorithms(mode='ml')
        tb.update()
        context = zmq.Context()
        knifeSocket = context.socket(zmq.REP)
        knifeSocket.bind("tcp://*:5555")
        sparseSocket = context.socket(zmq.REP)
        sparseSocket.bind("tcp://*:5556")
        while True:
            knifeMessage = knifeSocket.recv()
            print("Received a message from knife:", knifeMessage)
            knifeSocket.send_string("ACK")
            knifeOrder = json.loads(knifeMessage)
            sparseMessage = sparseSocket.recv()
            print("Received a message from sparse:", sparseMessage)
            sparseSocket.send_string("ACK")
            sparseOrder = json.loads(sparseMessage)
            tb.update()
            positions = tb.get_current_positions()
            result = voting([knifeOrder, sparseOrder], positions)
            print("Positions:", positions)
            print(result)
            if result != "Hold":
                order_params = create_order(result)
                print(self.bybit.create_order(order_params))


MLInterface()
