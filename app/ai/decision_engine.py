def calculate_confidence(analysis):

    confidence = 50
    reasons = []

    # Trend
    if analysis["trend"] == "Bullish":
        confidence += 20
        reasons.append("✓ Bullish Trend")
    elif analysis["trend"] == "Bearish":
        confidence -= 10
        reasons.append("✗ Bearish Trend")
    else:
        reasons.append("➖ Sideways Market")

    # RSI
    if 40 <= analysis["rsi"] <= 60:
        confidence += 20
        reasons.append("✓ RSI Healthy")
    elif analysis["rsi"] > 70:
        confidence -= 15
        reasons.append("✗ RSI Overbought")
    elif analysis["rsi"] < 30:
        confidence += 10
        reasons.append("✓ RSI Oversold")

    # SMA
    if analysis["price"] > analysis["sma"]:
        confidence += 20
        reasons.append("✓ Price Above SMA")
    else:
        confidence -= 15
        reasons.append("✗ Price Below SMA")

    # EMA
    if analysis["price"] > analysis["ema"]:
        confidence += 10
        reasons.append("✓ Price Above EMA")
    else:
        confidence -= 10
        reasons.append("✗ Price Below EMA")

    # MACD
    if analysis["macd"] > 0:
        confidence += 15
        reasons.append("✓ MACD Bullish")
    else:
        confidence -= 15
        reasons.append("✗ MACD Bearish")

    # Bollinger Bands
    if analysis["price"] > analysis["bb_upper"]:
        confidence -= 10
        reasons.append("✗ Price Above Upper Band")
    elif analysis["price"] < analysis["bb_lower"]:
        confidence += 10
        reasons.append("✓ Price Below Lower Band")

    confidence = max(0, min(confidence, 100))

    if confidence >= 80:
        recommendation = "STRONG BUY"
    elif confidence >= 65:
        recommendation = "BUY"
    elif confidence >= 50:
        recommendation = "HOLD"
    else:
        recommendation = "SELL"

    return confidence, recommendation, reasons