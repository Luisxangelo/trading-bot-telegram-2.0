import asyncio
import time
from datetime import datetime, date
from telegram import Bot

from config import TOKEN, CANAL_VIP, CANAL_FREE, SYMBOLS, CHECK_INTERVAL
from trading.strategy import analyze
from trading.signal_formatter import (
    format_signal_premium,
    format_signal_free
)
from trading.dashboard import daily_dashboard

bot = Bot(token=TOKEN)

# ================= SESIÓN =================

SESSION_START = 12   # UTC
SESSION_END = 20     # UTC

sent_open = False
sent_close = False

# ================= CONTROL FREE =================

FREE_SIGNALS_PER_DAY = 2
free_counter = {
    "date": date.today(),
    "count": 0
}

def reset_free_counter():
    today = date.today()
    if free_counter["date"] != today:
        free_counter["date"] = today
        free_counter["count"] = 0

# ================= SESIÓN =================

def session_open():
    hour = datetime.utcnow().hour
    return SESSION_START <= hour < SESSION_END

# ================= MENSAJES =================

async def send_good_morning():
    msg = (
        "🌅 *Buenos días traders*\n\n"
        "🤖 Sistema ACTIVADO\n"
        "📊 Pares: BTC / ETH\n"
        "⏱ TF: 5m + 15m\n\n"
        "⚠️ Gestiona tu riesgo"
    )
    await bot.send_message(chat_id=CANAL_VIP, text=msg, parse_mode="Markdown")

async def send_good_night():
    msg = (
        "🌙 *Cierre de sesión*\n\n"
        "🤖 Sistema DESACTIVADO\n"
        "📊 Revisa el resumen del día\n\n"
        "Nos vemos mañana 🚀"
    )
    await bot.send_message(chat_id=CANAL_VIP, text=msg, parse_mode="Markdown")

# ================= EJECUCIÓN =================

async def run():
    reset_free_counter()

    for symbol in SYMBOLS:
        trade = analyze(symbol)
        if not trade:
            continue

        # ===== VIP (SIEMPRE) =====
        vip_msg = format_signal_premium(trade)
        await bot.send_message(
            chat_id=CANAL_VIP,
            text=vip_msg,
            parse_mode="Markdown"
        )

        # ===== FREE (LIMITADO) =====
        if free_counter["count"] < FREE_SIGNALS_PER_DAY:
            free_msg = format_signal_free(trade)
            await bot.send_message(
                chat_id=CANAL_FREE,
                text=free_msg,
                parse_mode="Markdown"
            )
            free_counter["count"] += 1

# ================= LOOP PRINCIPAL =================

async def main_loop():
    global sent_open, sent_close

    while True:
        if session_open():
            if not sent_open:
                await send_good_morning()
                sent_open = True
                sent_close = False

            await run()

        else:
            if not sent_close and sent_open:
                await send_good_night()
                dashboard = daily_dashboard()
                await bot.send_message(
                    chat_id=CANAL_VIP,
                    text=dashboard,
                    parse_mode="Markdown"
                )
                sent_close = True
                sent_open = False

        await asyncio.sleep(CHECK_INTERVAL)  # ✅ CORRECTO


if __name__ == "__main__":
    asyncio.run(main_loop())
