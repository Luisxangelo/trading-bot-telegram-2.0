# trading/backtest.py

from datetime import datetime, timedelta
from trading.binance_client import get_klines_history
from trading.strategy import analyze

def backtest(symbol):
    start = (datetime.utcnow() - timedelta(days=180)).strftime("%d %b %Y")
    candles = get_klines_history(symbol, "5m", start)

    wins = 0
    losses = 0

    for i in range(200, len(candles)):
        window = candles[i-200:i]
        direction = analyze(symbol)

        if direction:
            wins += 1  # simplificado, luego refinamos

    total = wins + losses
    winrate = (wins / total * 100) if total > 0 else 0

    print(f"{symbol} | Trades: {total} | Winrate aprox: {winrate:.2f}%")

if __name__ == "__main__":
    backtest("BTCUSDT")
    backtest("ETHUSDT")
