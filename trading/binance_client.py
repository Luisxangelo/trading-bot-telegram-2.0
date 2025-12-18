# trading/binance_client.py

from binance.client import Client
from config import BINANCE_API_KEY, BINANCE_API_SECRET

client = Client(BINANCE_API_KEY, BINANCE_API_SECRET)

def get_price(symbol: str) -> float:
    """Precio actual"""
    ticker = client.get_symbol_ticker(symbol=symbol)
    return float(ticker["price"])


def get_klines(symbol: str, interval="5m", limit=200):
    """
    Velas OHLCV reales de Binance
    """
    klines = client.get_klines(
        symbol=symbol,
        interval=interval,
        limit=limit
    )

    candles = []
    for k in klines:
        candles.append({
            "open": float(k[1]),
            "high": float(k[2]),
            "low": float(k[3]),
            "close": float(k[4]),
            "volume": float(k[5]),
            "timestamp": int(k[0])
        })

    return candles


def get_klines_history(symbol: str, interval="5m", start_str=None, end_str=None):
    """
    Velas históricas (para backtesting real)
    """
    klines = client.get_historical_klines(
        symbol,
        interval,
        start_str,
        end_str
    )

    candles = []
    for k in klines:
        candles.append({
            "open": float(k[1]),
            "high": float(k[2]),
            "low": float(k[3]),
            "close": float(k[4]),
            "volume": float(k[5]),
            "timestamp": int(k[0])
        })

    return candles

