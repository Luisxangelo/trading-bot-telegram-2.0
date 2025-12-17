# strategy.py

from binance_client import get_price

def should_buy(symbol):
    """Determina si debe comprar en base a la estrategia"""
    price = get_price(symbol)
    if price < 30000:  # Por ejemplo, si el precio es menor que 30,000
        return True
    return False

def should_sell(symbol):
    """Determina si debe vender en base a la estrategia"""
    price = get_price(symbol)
    if price > 35000:  # Si el precio es mayor que 35,000
        return True
    return False
