# binance_client.py

from binance.client import Client
from config import API_KEY, API_SECRET

# Conexión con Binance
client = Client(API_KEY, API_SECRET)

def get_price(symbol):
    """Obtiene el precio actual de un símbolo"""
    price = client.get_symbol_ticker(symbol=symbol)
    return float(price['price'])

def get_balance():
    """Obtiene el saldo disponible"""
    balance = client.get_asset_balance(asset='USDT')
    return float(balance['free'])

def place_order(symbol, side, quantity, price):
    """Realiza una orden de compra o venta"""
    if side == 'buy':
        order = client.order_limit_buy(
            symbol=symbol,
            quantity=quantity,
            price=str(price)
        )
    elif side == 'sell':
        order = client.order_limit_sell(
            symbol=symbol,
            quantity=quantity,
            price=str(price)
        )
    return order
