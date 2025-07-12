```python
import ccxt
import time
import os

# Initialize Bybit
bybit = ccxt.bybit({
    'apiKey': os.getenv(s5ClZo03oKNBRiAajv),
    'secret': os.getenv(yTLiiRrhVrL7RUYYiRx8kGhgHSLS3brKsZLs),
    'enableRateLimit': True
})

# Configuration
PAIRS = ['XRP/USDT', 'ETH/USDT']  # Trading pairs
TRADE_AMOUNT_USD = 10              # $10 per trade
TIMEFRAME = '1h'                   # Candle interval
SHORT_MA_PERIOD = 10               # 10-period MA
LONG_MA_PERIOD = 30                # 30-period MA

def get_moving_averages(pair):
    candles = bybit.fetch_ohlcv(pair, TIMEFRAME, limit=LONG_MA_PERIOD)
    closes = [candle[4] for candle in candles]
    short_ma = sum(closes[-SHORT_MA_PERIOD:]) / SHORT_MA_PERIOD
    long_ma = sum(closes[-LONG_MA_PERIOD:]) / LONG_MA_PERIOD
    return short_ma, long_ma

def execute_trade(pair, signal):
    try:
        ticker = bybit.fetch_ticker(pair)
        amount = TRADE_AMOUNT_USD / ticker['last']  # Dynamic amount
        if signal == 'BUY':
            bybit.create_market_buy_order(pair, amount)
            print(f"✅ BUY {pair} | Amount: {amount:.4f}")
        else:
            bybit.create_market_sell_order(pair, amount)
            print(f"✅ SELL {pair} | Amount: {amount:.4f}")
    except Exception as e:
        print(f"❌ Trade failed for {pair}: {str(e)}")

def run_bot():
    for pair in PAIRS:
        short_ma, long_ma = get_moving_averages(pair)
        if short_ma > long_ma:
            execute_trade(pair, 'BUY')
        elif short_ma < long_ma:
            execute_trade(pair, 'SELL')

if __name__ == "__main__":
    print("🚀 Bot started - Monitoring XRP/USDT & ETH/USDT")
    while True:
        run_bot()
        time.sleep(3600)  # Runs 
