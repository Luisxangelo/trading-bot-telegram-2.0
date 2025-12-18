# trading/strategy.py

import pandas as pd
from trading.binance_client import get_klines

# ================= INDICADORES =================

def ema(series, period):
    return series.ewm(span=period, adjust=False).mean()

def rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))


# ================= ESTRATEGIA =================

def analyze(symbol: str):
    candles = get_klines(symbol, interval="5m", limit=200)
    df = pd.DataFrame(candles)

    if len(df) < 200:
        return None

    df["ema50"] = ema(df["close"], 50)
    df["ema200"] = ema(df["close"], 200)
    df["rsi"] = rsi(df["close"], 14)
    df["vol_ma"] = df["volume"].rolling(20).mean()

    last = df.iloc[-1]
    prev = df.iloc[-2]

    # ========= LONG =========
    if (
        last["ema50"] > last["ema200"] and
        prev["close"] < prev["ema50"] and
        last["close"] > last["ema50"] and
        40 <= last["rsi"] <= 55 and
        last["volume"] > last["vol_ma"]
    ):
        return "BUY"

    # ========= SHORT =========
    if (
        last["ema50"] < last["ema200"] and
        prev["close"] > prev["ema50"] and
        last["close"] < last["ema50"] and
        45 <= last["rsi"] <= 60 and
        last["volume"] > last["vol_ma"]
    ):
        return "SELL"

    return None
