import csv
import time
import random
from curl_cffi import requests
import yfinance as yf
import json

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
]

def get_session():
    s = requests.Session()
    s.headers.update({"User-Agent": random.choice(USER_AGENTS)})
    return s

# Read first symbol from your input file
with open("ghIn", newline="") as fin:
    reader = csv.DictReader(fin)
    symbols = [row["T"] for row in reader]
    test_symbol = symbols[0] if symbols else "AAPL"

print(f"Testing with symbol: {test_symbol}")
print("=" * 60)

sess = get_session()
yf.utils.requests = sess
ticker = yf.Ticker(test_symbol)
info = ticker.info or {}

print("\n1. Checking info dict for recommendation-related keys:")
print("-" * 60)
for key in sorted(info.keys()):
    if 'recommend' in key.lower() or 'analyst' in key.lower() or 'target' in key.lower():
        value = info[key]
        if isinstance(value, (dict, list)):
            print(f"{key}: {type(value)}")
            print(json.dumps(value, indent=2, default=str)[:500])
        else:
            print(f"{key}: {value}")

print("\n2. Checking ticker object properties:")
print("-" * 60)
for attr in dir(ticker):
    if 'recommend' in attr.lower() or 'upgrade' in attr.lower():
        print(f"Found attribute: {attr}")
        try:
            value = getattr(ticker, attr)
            if hasattr(value, 'empty'):  # It's a DataFrame
                print(f"  Type: DataFrame, Empty: {value.empty}")
                if not value.empty:
                    print(f"  Columns: {list(value.columns)}")
                    print(f"  Shape: {value.shape}")
                    print(f"  First few rows:\n{value.head()}")
            elif callable(value):
                print(f"  Type: function/method")
            else:
                print(f"  Value: {value}")
        except Exception as e:
            print(f"  Error accessing: {e}")

print("\n3. Specific check for numberOfAnalystOpinions:")
print("-" * 60)
print(f"numberOfAnalystOpinions: {info.get('numberOfAnalystOpinions', 'NOT FOUND')}")

print("\n4. All keys in info dict:")
print("-" * 60)
print(f"Total keys: {len(info.keys())}")
print("Keys:", ', '.join(sorted(info.keys())[:20]), "...")
