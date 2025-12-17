# signal_formatter.py

def format_signal(symbol, action, price, tp1, tp2, tp3, sl):
    """Formatea las señales de trading"""
    return (
        f"📊 *{symbol}*\n\n"
        f"🔻 Acción: {action.upper()}\n"
        f"📈 Entrada: {price}\n"
        f"⛔️ Stop Loss: {sl}\n"
        f"🎯 TP1: {tp1}\n"
        f"🎯 TP2: {tp2}\n"
        f"🎯 TP3: {tp3}\n\n"
        "⚠️ No es asesoría financiera."
    )
