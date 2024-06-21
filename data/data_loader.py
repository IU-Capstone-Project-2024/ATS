import pandas as pd
import sqlite3

def load_data(file_path: str) -> pd.DataFrame:
    return pd.read_csv(file_path)
