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


def calculate_macd(data):
    ema12 = data["Close"].ewm(span=12, adjust=False).mean()
    ema26 = data["Close"].ewm(span=26, adjust=False).mean()

    macd = ema12 - ema26
    signal = macd.ewm(span=9, adjust=False).mean()
    histogram = macd - signal

    return macd, signal, histogram


def calculate_bollinger_bands(data, period=20):
    sma = data["Close"].rolling(window=period).mean()

    std = data["Close"].rolling(window=period).std()

    upper_band = sma + (std * 2)
    lower_band = sma - (std * 2)

    return upper_band, lower_band


def calculate_atr(data, period=14):
    high_low = data["High"] - data["Low"]

    high_close = (data["High"] - data["Close"].shift()).abs()

    low_close = (data["Low"] - data["Close"].shift()).abs()

    true_range = high_low.combine(high_close, max).combine(low_close, max)

    atr = true_range.rolling(period).mean()

    return atr