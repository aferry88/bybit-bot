
import time
import os
from pybit.unified_trading import HTTP

API_KEY = os.environ.get("BYBIT_API_KEY")
API_SECRET = os.environ.get("BYBIT_API_SECRET")

symbols = ["BTCUSDT", "ETHUSDT", "XRPUSDT"]
last_prices = {}

session = HTTP(
    testnet=False,
    api_key=API_KEY,
    api_secret=API_SECRET,
)

def get_price(symbol):
    try:
        res = session.get_tickers(category="linear", symbol=symbol)
        return float(res["result"]["list"][0]["lastPrice"])
    except Exception as e:
        print(f"Error getting price for {symbol}: {e}")
        return None

def place_order(symbol, side, qty):
    try:
        print(f"Placing {side} order for {symbol}, qty: {qty}")
        order = session.place_order(
            category="linear",
            symbol=symbol,
            side=side,
            order_type="Market",
            qty=qty,
            time_in_force="GoodTillCancel",
            reduce_only=False
        )
        print(order)
    except Exception as e:
        print(f"Error placing order for {symbol}: {e}")

def usd_to_qty(symbol, usd_amount):
    price = get_price(symbol)
    return round(usd_amount / price, 4) if price else 0

while True:
    for symbol in symbols:
        price = get_price(symbol)
        if not price:
            continue

        last_price = last_prices.get(symbol)
        if last_price:
            if price < last_price:
                qty = usd_to_qty(symbol, 2.5)
                place_order(symbol, "Buy", qty)
            elif price > last_price:
                qty = usd_to_qty(symbol, 1.5)
                place_order(symbol, "Sell", qty)

        last_prices[symbol] = price

    time.sleep(20)
