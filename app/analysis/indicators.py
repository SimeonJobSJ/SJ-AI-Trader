def calculate_sma(data, period=3):
    return data["Close"].rolling(window=period).mean()


def calculate_rsi(data, period=3):
    delta = data["Close"].diff()

    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()

    rs = avg_gain / avg_loss

    rsi = 100 - (100 / (1 + rs))

    return rsi


def calculate_ema(data, period=9):
    return data["Close"].ewm(span=period, adjust=False).mean()