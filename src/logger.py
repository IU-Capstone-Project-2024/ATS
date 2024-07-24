import sqlite3
from config import SQLITE_DB_PATH

class Logger:
    def __init__(self):
        self.conn = sqlite3.connect(SQLITE_DB_PATH)
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS decisions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model TEXT,
            action TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
        query1 = """
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action TEXT,
            price TEXT,
            qty TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
        with self.conn:
            self.conn.execute(query)
            self.conn.execute(query1)

    def log_decision(self, model, action):
        query = "INSERT INTO decisions (model, action) VALUES (?, ?)"
        with self.conn:
            self.conn.execute(query, (model, action))

    def log_trade(self, action, price, qty):
        query = "INSERT INTO logs (action, price, qty) VALUES (?, ?, ?)"
        with self.conn:
            self.conn.execute(query, (action, price, qty))

    def close(self):
        self.conn.close()
