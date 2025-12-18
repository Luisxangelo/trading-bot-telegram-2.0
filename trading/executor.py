from trading.strategy import analyze

def run_once():
    for symbol in ["BTCUSDT", "ETHUSDT"]:
        signal = analyze(symbol)
        if signal:
            print(f"{symbol} => {signal}")
