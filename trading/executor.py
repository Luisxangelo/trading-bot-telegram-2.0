from binance.client import Client
from config import BINANCE_API_KEY, BINANCE_API_SECRET

client = Client(BINANCE_API_KEY, BINANCE_API_SECRET)

def execute_trade(trade):
    # SOLO TU CUENTA
    print("Ejecutando trade:", trade)
    # Aquí luego colocas órdenes reales si activas permisos
