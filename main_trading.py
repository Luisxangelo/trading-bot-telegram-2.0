import time
import asyncio
from telegram import Bot

from config import TOKEN, CANAL_VIP, SYMBOLS, CHECK_INTERVAL
from trading.strategy import analyze
from trading.signal_formatter import format_signal
from trading.binance_client import get_price

bot = Bot(token=TOKEN)

async def run():
    for symbol in SYMBOLS:
        direction = analyze(symbol)
        if direction:
            price = get_price(symbol)
            msg = format_signal(symbol, direction, price)
            await bot.send_message(chat_id=CANAL_VIP, text=msg)

async def main_loop():
    while True:
        await run()
        time.sleep(CHECK_INTERVAL)  # 5 minutos

if __name__ == "__main__":
    asyncio.run(main_loop())


