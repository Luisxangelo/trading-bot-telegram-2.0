# trading/signal_formatter.py

def format_signal_premium(trade: dict) -> str:
    """
    Formato profesional para señales VIP
    """
    symbol = trade["symbol"]
    side = trade["side"]
    entry = trade["entry"]
    sl = trade["sl"]
    tp1, tp2, tp3 = trade["tp"]
    rr = trade["rr"]

    emoji = "🟢 LONG" if side == "BUY" else "🔴 SHORT"

    message = (
        f"❗️ *SIGNAL ALERT* ❗️\n\n"
        f"📊 *{symbol}*\n\n"
        f"{emoji}\n\n"
        f"🎯 *Entrada:* `{entry}`\n"
        f"⛔️ *Stop Loss:* `{sl}`\n\n"
        f"🏆 *TP1:* `{tp1}`\n"
        f"🏆 *TP2:* `{tp2}`\n"
        f"🏆 *TP3:* `{tp3}`\n\n"
        f"⚖️ *RR:* 1:{round(rr,2)}\n\n"
        f"⚠️ Riesgo recomendado: *1–2%*\n"
        f"📌 Señal educativa – no es asesoría financiera"
    )

    return message
