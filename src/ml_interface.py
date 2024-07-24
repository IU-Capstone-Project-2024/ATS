import time
import zmq
import json
import csv
from test_algorithms import Algorithms
from bybit import BybitAPI
from logger import Logger
import sys

def create_order(side, qty):
    category = "spot"
    symbol = "BTCUSDT"
    side = side
    order_type = "Limit"
    qty = "0.001" if side == "buy" else qty
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


def final_position(positions):
    votes = {"Hold": 0, "Buy": 0, "Sell": 0}
    interpretation = {0: "Hold", 1: "Buy", -1: "Sell"}
    for position in positions:
        votes[interpretation[position]] += 1

    sorted_votes = sorted(votes.items(), key=lambda item: item[1], reverse=True)

    if sorted_votes[0][1] > sorted_votes[1][1]:
        return sorted_votes[0][0].capitalize()
    return 'Hold'


def voting(model_decisions, position):
    votes = {"Sell": 0, "Buy": 0, "Hold": -1}
    print("Decisions:", model_decisions)

    for decision in model_decisions:
        votes[decision] += 1

    votes[position] += 0.5

    sorted_votes = sorted(votes.items(), key=lambda item: item[1], reverse=True)

    if sorted_votes[0][1] > sorted_votes[1][1]:
        return sorted_votes[0][0].capitalize()
    return "Hold"


class MLInterface:
    def __init__(self, logger):
        print("Started...")
        self.logger = logger
        self.bybit = BybitAPI()
        self.qty = float(sys.argv[1]) if len(sys.argv) > 1 else 0
        print("Quantity at start:", self.qty)
        tb = Algorithms(mode='ml')
        tb.update()
        context = zmq.Context()
        knifeSocket = context.socket(zmq.REP)
        knifeSocket.bind("tcp://*:5555")
        sparseSocket = context.socket(zmq.REP)
        sparseSocket.bind("tcp://*:5556")
        print("Listening...")
        while True:
            knifeMessage = knifeSocket.recv()
            print("Received a message from knife:", knifeMessage)
            knifeAction = int(json.loads(knifeMessage))
            sparseMessage = sparseSocket.recv()
            print("Received a message from sparse:", sparseMessage)
            sparseAction = int(json.loads(sparseMessage))
            tb.update()
            knifeOrder = "Sell" if knifeAction == 2 else ("Buy" if knifeAction == 1 else "Hold")
            sparseOrder = "Sell" if sparseAction == 2 else ("Buy" if sparseAction == 1 else "Hold")
            position = final_position(tb.get_current_positions())
            result = voting([knifeOrder, sparseOrder], position)
            print("Position:", position)
            print(result)
            trade_qty = 0
            if result == "Buy":
                trade_qty = 0.001
                self.qty += 0.001
            if result == "Sell":
                trade_qty = self.qty
                self.qty = 0


            trade_qty = round(trade_qty, 3)
            if trade_qty > 0:
                order_params = create_order(result, trade_qty)
                respond = self.bybit.create_order(order_params)
                print(respond[0])
                self.logger.log_trade(result, trade_qty, respond[1])

            knifeSocket.send_string(result)
            sparseSocket.send_string(result)
            self.logger.log_decision("Algorithms", position)
            self.logger.log_decision("Knife", knifeOrder)
            self.logger.log_decision("Sparse", sparseOrder)
            self.logger.log_decision("Result", result)


if __name__ == '__main__':
    try:
        logger = Logger()
        ml_interface = MLInterface(logger)
    except Exception as e:
        print(e)
    finally:
        logger.close()
