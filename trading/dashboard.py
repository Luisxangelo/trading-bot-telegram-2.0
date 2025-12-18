from datetime import date
import json

FILE = "daily_stats.json"

def log_trade(result: str):
    today = str(date.today())

    data = {}
    try:
        with open(FILE, "r") as f:
            data = json.load(f)
    except:
        pass

    if today not in data:
        data[today] = {"win": 0, "loss": 0}

    data[today][result] += 1

    with open(FILE, "w") as f:
        json.dump(data, f, indent=2)

def daily_report() -> str:
    today = str(date.today())

    try:
        with open(FILE, "r") as f:
            data = json.load(f)
    except:
        return "📊 No hay datos hoy"

    d = data.get(today, {"win": 0, "loss": 0})
    total = d["win"] + d["loss"]
    winrate = (d["win"] / total * 100) if total > 0 else 0

    return (
        "📊 *RESUMEN DEL DÍA*\n\n"
        f"📈 Operaciones: {total}\n"
        f"✅ Ganadas: {d['win']}\n"
        f"❌ Perdidas: {d['loss']}\n"
        f"🎯 Win Rate: {round(winrate, 2)}%\n\n"
        "⚠️ Resultados educativos"
    )
