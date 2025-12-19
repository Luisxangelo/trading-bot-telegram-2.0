# trading/signal_formatter.py

def format_signal_premium(trade):
    return (
        f"❗️*SIGNAL ALERT – VIP*\n\n"
        f"📊 #{trade['symbol']}\n"
        f"📈 *{trade['side']}*\n\n"
        f"🎯 Entrada: {trade['entry']}\n"
        f"⛔️ SL: {trade['sl']}\n\n"
        f"🏆 TP1: {trade['tp'][0]}\n"
        f"🏆 TP2: {trade['tp'][1]}\n"
        f"🏆 TP3: {trade['tp'][2]}\n\n"
        f"⚖️ RR: 1:{trade['rr']}\n\n"
        "⚠️ Educativo – no asesoría financiera"
    )

def format_signal_free(trade):
    return (
        f"📢 *SEÑAL FREE*\n\n"
        f"📊 #{trade['symbol']}\n"
        f"📈 *{trade['side']}*\n\n"
        f"🎯 Entrada: {trade['entry']}\n"
        f"⛔️ SL: {trade['sl']}\n\n"
        "💎 *TP completos solo en VIP*\n"
        "👉 Escríbenos para acceso"
    )

    
    
