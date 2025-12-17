# backtest.py

import pandas as pd

def backtest(symbol, start_date, end_date):
    """Simula las operaciones con datos históricos"""
    # Aquí debes obtener datos históricos, por ejemplo, desde Binance API
    # Usaremos un CSV con datos ficticios para el ejemplo
    data = pd.read_csv("historical_data.csv")  # Asegúrate de tener datos históricos en este archivo
    
    initial_balance = 1000
    balance = initial_balance
    qty = 0.001  # Cantidad de BTC a comprar/vender

    for i in range(1, len(data)):
        if data['Price'][i] < 30000:  # Condición de compra
            balance -= data['Price'][i] * qty
        elif data['Price'][i] > 35000:  # Condición de venta
            balance += data['Price'][i] * qty

    return balance

final_balance = backtest("BTCUSDT", "2021-01-01", "2021-07-01")
print(f"Balance final después del backtest: {final_balance} USDT")
