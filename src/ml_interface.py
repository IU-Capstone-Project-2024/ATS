import time
import zmq
import json
import csv
from test_algorithms import TradingBot


class MLInterface:
    def __init__(self):
        print("I started!")
        tb = TradingBot(mode='ml')
        tb.update()
        # print(tb.get_current_positions())
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
            print(knifeOrder, sparseOrder)


MLInterface()
