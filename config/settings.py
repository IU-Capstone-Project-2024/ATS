import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
SQLITE_DB_PATH = os.getenv('SQLITE_DB_PATH')
BASE_URL = "https://api.bybit.com"
TEST_URL = "https://api-testnet.bybit.com"
