import sqlite3
from config import SQLITE_DB_PATH

class Logger:
    def __init__(self):
        self.conn = sqlite3.connect(SQLITE_DB_PATH)
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action TEXT,
            result TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
        with self.conn:
            self.conn.execute(query)

    def log_trade(self, action, result):
        query = "INSERT INTO logs (action, result) VALUES (?, ?)"
        with self.conn:
            self.conn.execute(query, (action, result))

    def close(self):
        self.conn.close()
