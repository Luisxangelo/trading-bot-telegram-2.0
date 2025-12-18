# trading/signal_formatter.py

def format_signal(symbol, direction, entry_price):
    risk_pct = 0.003  # 0.3% SL (scalping)

    if direction == "BUY":
        sl = entry_price * (1 - risk_pct)
        tp1 = entry_price * (1 + risk_pct)
        tp2 = entry_price * (1 + risk_pct * 2)
        tp3 = entry_price * (1 + risk_pct * 3)
    else:
        sl = entry_price * (1 + risk_pct)
        tp1 = entry_price * (1 - risk_pct)
        tp2 = entry_price * (1 - risk_pct * 2)
        tp3 = entry_price * (1 - risk_pct * 3)

    return (
        f"❗️SIGNAL ALERT❗️\n\n"
        f"📊 #{symbol}\n"
        f"📈 {'BUY' if direction=='BUY' else 'SELL'}\n\n"
        f"🎯 Entrada: {entry_price:.2f}\n"
        f"⛔️ SL: {sl:.2f}\n\n"
        f"🏆 TP1: {tp1:.2f}\n"
        f"🏆 TP2: {tp2:.2f}\n"
        f"🏆 TP3: {tp3:.2f}\n\n"
        f"⚠️ Riesgo recomendado: 1–2%"
    )
