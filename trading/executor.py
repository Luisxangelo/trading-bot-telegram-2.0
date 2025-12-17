# executor.py

from strategy import should_buy, should_sell
from binance_client import place_order, get_price

def execute_trade(symbol):
    """Ejecuta el trading en vivo según la estrategia"""
    if should_buy(symbol):
        price = get_price(symbol)
        order = place_order(symbol, 'buy', 0.001, price)
        print(f"Orden de compra ejecutada: {order}")
    
    if should_sell(symbol):
        price = get_price(symbol)
        order = place_order(symbol, 'sell', 0.001, price)
        print(f"Orden de venta ejecutada: {order}")
