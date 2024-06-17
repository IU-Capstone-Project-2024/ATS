import sqlite3
from config import SQLITE_DB_PATH


class Logger:
    def __init__(self):
        self.conn = sqlite3.connect(SQLITE_DB_PATH)
        self.cursor = self.conn.cursor()
        self.create_table()

    def log_trade(self, trade):
        self.cursor.execute(
            'INSERT INTO trades (action, symbol, qty, response, timestamp) VALUES (?, ?, ?, ?, ?)',
            (trade['action'], trade['symbol'], trade['qty'], trade['response'], trade['timestamp'])
        )
        self.conn.commit()
