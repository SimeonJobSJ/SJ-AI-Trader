def analyze_market(data):

    print(type(data["Close"]))
    print(data["Close"].head())

    highest = data["High"].max()
    ...
    lowest = data["Low"].min()
    average_close = data["Close"].mean()

    bullish = (data["Close"] > data["Open"]).sum()
    bearish = (data["Close"] < data["Open"]).sum()

    first_close = data["Close"].iloc[0]
    last_close = data["Close"].iloc[-1]

    if last_close > first_close:
        trend = "Bullish"
    elif last_close < first_close:
        trend = "Bearish"
    else:
        trend = "Sideways"

    return {
        "highest": highest,
        "lowest": lowest,
        "average_close": average_close,
        "bullish": bullish,
        "bearish": bearish,
        "trend": trend,
    }


def trading_signal(data):
    latest_close = data["Close"].iloc[-1]
    latest_sma = data["SMA"].iloc[-1]

    if latest_close > latest_sma:
        return "BUY 🟢"
    elif latest_close < latest_sma:
        return "SELL 🔴"
    else:
        return "HOLD 🟡"