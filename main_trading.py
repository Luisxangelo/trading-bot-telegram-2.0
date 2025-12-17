# main_trading.py

import time
from executor import execute_trade
from trading.signal_formatter import format_signal

def main():
    """Motor principal de trading"""
    while True:
        execute_trade("BTCUSDT")  # Ejecutar la estrategia para BTC
        time.sleep(60)  # Espera 1 minuto para la siguiente ejecución

if __name__ == "__main__":
    main()
