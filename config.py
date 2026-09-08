import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OANDA_API_KEY = os.getenv("OANDA_API_KEY")
OANDA_ACCOUNT_ID = os.getenv("OANDA_ACCOUNT_ID")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# Trading Configuration
FOREX_PAIRS = os.getenv("FOREX_PAIRS", "EUR_USD,GBP_USD,USD_JPY").split(",")
RISK_LEVEL = float(os.getenv("RISK_LEVEL", "0.02"))
CANDLE_INTERVAL = "H1"  # 1 hour candles

# AI Model Configuration
MODEL = "gpt-4"
TEMPERATURE = 0.7
MAX_TOKENS = 2000

# System Control Settings
ALLOW_PC_CONTROL = True
COMMAND_TIMEOUT = 30  # seconds
