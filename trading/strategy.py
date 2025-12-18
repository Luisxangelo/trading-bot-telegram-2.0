import time
from datetime import datetime
from trading.binance_client import get_klines

EMA_FAST = 9
EMA_SLOW = 21
RSI_PERIOD = 14

MIN_VOLATILITY = 0.0015
MAX_VOLATILITY = 0.015
MIN_VOLUME_MULT = 1.2

SESSION_START = 12   # UTC
SESSION_END = 20

COOLDOWN_WIN = 15 * 60
COOLDOWN_LOSS = 30 * 60

last_trade = {}

# ---------- INDICADORES ----------

def ema(values, period):
    k = 2 / (period + 1)
    ema_val = sum(values[:period]) / period
    result = []
    for v in values:
        ema_val = v * k + ema_val * (1 - k)
        result.append(ema_val)
    return result

def rsi(values, period=14):
    gains, losses = [], []
    for i in range(1, len(values)):
        diff = values[i] - values[i - 1]
        gains.append(max(diff, 0))
        losses.append(abs(min(diff, 0)))
    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period
    rsis = []
    for i in range(period, len(gains)):
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period
        rs = avg_gain / avg_loss if avg_loss != 0 else 0
        rsis.append(100 - (100 / (1 + rs)))
    return rsis

def volatility(closes):
    return abs(closes[-1] - closes[-2]) / closes[-2]

def in_session():
    h = datetime.utcnow().hour
    return SESSION_START <= h <= SESSION_END

def in_cooldown(symbol):
    if symbol not in last_trade:
        return False
    elapsed = time.time() - last_trade[symbol]["time"]
    if last_trade[symbol]["result"] == "win":
        return elapsed < COOLDOWN_WIN
    return elapsed < COOLDOWN_LOSS

def rr_dynamic(vol):
    if vol < 0.003:
        return 2.5
    if vol < 0.007:
        return 2.0
    return 1.5

# ---------- ANALYZE ----------

def analyze(symbol):
    if not in_session():
        return None

    candles = get_klines(symbol, "5m", 150)
    closes = [c["close"] for c in candles]
    volumes = [c["volume"] for c in candles]

    ema_f = ema(closes, EMA_FAST)
    ema_s = ema(closes, EMA_SLOW)
    rsi_v = rsi(closes)

    if len(rsi_v) < 2:
        return None

    vol = volatility(closes)
    avg_vol = sum(volumes[-20:]) / 20

    if vol < MIN_VOLATILITY or vol > MAX_VOLATILITY:
        return None

    if volumes[-1] < avg_vol * MIN_VOLUME_MULT:
        return None

    if in_cooldown(symbol):
        return None

    price = closes[-1]
    rr = rr_dynamic(vol)

    # LONG
    if ema_f[-1] > ema_s[-1] and 55 < rsi_v[-1] < 70:
        sl = price * 0.996
        risk = price - sl
        last_trade[symbol] = {"time": time.time(), "result": "win"}
        return {
            "symbol": symbol,
            "side": "BUY",
            "entry": round(price, 2),
            "sl": round(sl, 2),
            "tp": [
                round(price + risk * rr * 0.5, 2),
                round(price + risk * rr, 2),
                round(price + risk * rr * 1.5, 2)
            ],
            "rr": rr
        }

    # SHORT
    if ema_f[-1] < ema_s[-1] and 30 < rsi_v[-1] < 45:
        sl = price * 1.004
        risk = sl - price
        last_trade[symbol] = {"time": time.time(), "result": "loss"}
        return {
            "symbol": symbol,
            "side": "SELL",
            "entry": round(price, 2),
            "sl": round(sl, 2),
            "tp": [
                round(price - risk * rr * 0.5, 2),
                round(price - risk * rr, 2),
                round(price - risk * rr * 1.5, 2)
            ],
            "rr": rr
        }

    return None
