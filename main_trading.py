import asyncio
import time
from datetime import datetime
from telegram import Bot

from config import TOKEN, CANAL_VIP, SYMBOLS, CHECK_INTERVAL
from trading.strategy import analyze
from trading.signal_formatter import format_signal_premium
from trading.dashboard import daily_dashboard

bot = Bot(token=TOKEN)

SESSION_START = 12   # UTC
SESSION_END = 20     # UTC

sent_open = False
sent_close = False

def session_open():
    hour = datetime.utcnow().hour
    return SESSION_START <= hour < SESSION_END

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

async def run():
    for symbol in SYMBOLS:
        trade = analyze(symbol)
        if trade:
            msg = format_signal_premium(trade)
            await bot.send_message(chat_id=CANAL_VIP, text=msg, parse_mode="Markdown")

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
                await bot.send_message(chat_id=CANAL_VIP, text=dashboard, parse_mode="Markdown")
                sent_close = True
                sent_open = False

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    asyncio.run(main_loop())
