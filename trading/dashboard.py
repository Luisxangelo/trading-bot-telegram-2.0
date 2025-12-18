# trading/dashboard.py

from datetime import date
import json
import os

FILE = "trades_log.json"

def load_trades():
    if not os.path.exists(FILE):
        return []
    with open(FILE, "r") as f:
        return json.load(f)

def daily_dashboard():
    today = str(date.today())
    trades = load_trades()

    today_trades = [t for t in trades if t["date"] == today]

    if not today_trades:
        return "📊 *RESUMEN DEL DÍA*\n\nNo se ejecutaron operaciones hoy."

    wins = sum(1 for t in today_trades if t["result"] == "win")
    losses = sum(1 for t in today_trades if t["result"] == "loss")
    total = len(today_trades)

    winrate = (wins / total) * 100

    msg = (
        f"📊 *RESUMEN DEL DÍA*\n\n"
        f"📈 Operaciones: {total}\n"
        f"✅ Ganadas: {wins}\n"
        f"❌ Perdidas: {losses}\n"
        f"🎯 Win Rate: {round(winrate,2)}%\n\n"
        f"⚠️ Resultados educativos – disciplina > emoción"
    )

    return msg
