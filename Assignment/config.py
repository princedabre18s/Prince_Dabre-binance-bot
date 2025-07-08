import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://testnet.binancefuture.com"
WEBSOCKET_URL = "wss://fstream.binancefuture.com"

BINANCE_API_KEY = os.environ.get("BINANCE_API_KEY")
BINANCE_SECRET_KEY = os.environ.get("BINANCE_SECRET_KEY")
