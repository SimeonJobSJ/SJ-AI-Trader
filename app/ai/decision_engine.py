def calculate_confidence(analysis):

    confidence = 50
    reasons = []

    signal = analysis.get("signal", "")

    # Determine trading direction
    if signal.startswith("BUY"):
        direction = "BUY"
    elif signal.startswith("SELL"):
        direction = "SELL"
    else:
        direction = "HOLD"

    # -------------------------
    # TREND
    # -------------------------
    if direction == "BUY":
        if analysis["trend"] == "Bullish":
            confidence += 20
            reasons.append("✓ Bullish Trend")
        elif analysis["trend"] == "Bearish":
            confidence -= 20
            reasons.append("✗ Bearish Trend")
        else:
            reasons.append("➖ Sideways Market")

    elif direction == "SELL":
        if analysis["trend"] == "Bearish":
            confidence += 20
            reasons.append("✓ Bearish Trend")
        elif analysis["trend"] == "Bullish":
            confidence -= 20
            reasons.append("✗ Bullish Trend")
        else:
            reasons.append("➖ Sideways Market")

    # -------------------------
    # RSI
    # -------------------------
    rsi = analysis["rsi"]

    if 40 <= rsi <= 60:
        confidence += 10
        reasons.append("✓ RSI Healthy")

    elif rsi > 70:
        if direction == "SELL":
            confidence += 15
            reasons.append("✓ RSI Overbought supports SELL")
        else:
            confidence -= 15
            reasons.append("✗ RSI Overbought")

    elif rsi < 30:
        if direction == "BUY":
            confidence += 15
            reasons.append("✓ RSI Oversold supports BUY")
        else:
            confidence -= 15
            reasons.append("✗ RSI Oversold")

    # -------------------------
    # SMA
    # -------------------------
    price = analysis["price"]
    sma = analysis["sma"]

    if direction == "BUY":
        if price > sma:
            confidence += 15
            reasons.append("✓ Price Above SMA")
        else:
            confidence -= 15
            reasons.append("✗ Price Below SMA")

    elif direction == "SELL":
        if price < sma:
            confidence += 15
            reasons.append("✓ Price Below SMA")
        else:
            confidence -= 15
            reasons.append("✗ Price Above SMA")

    # -------------------------
    # EMA
    # -------------------------
    ema = analysis["ema"]

    if direction == "BUY":
        if price > ema:
            confidence += 10
            reasons.append("✓ Price Above EMA")
        else:
            confidence -= 10
            reasons.append("✗ Price Below EMA")

    elif direction == "SELL":
        if price < ema:
            confidence += 10
            reasons.append("✓ Price Below EMA")
        else:
            confidence -= 10
            reasons.append("✗ Price Above EMA")

    # -------------------------
    # MACD
    # -------------------------
    macd = analysis["macd"]

    if direction == "BUY":
        if macd > 0:
            confidence += 15
            reasons.append("✓ MACD Bullish")
        else:
            confidence -= 15
            reasons.append("✗ MACD Bearish")

    elif direction == "SELL":
        if macd < 0:
            confidence += 15
            reasons.append("✓ MACD Bearish")
        else:
            confidence -= 15
            reasons.append("✗ MACD Bullish")

    # -------------------------
    # BOLLINGER BANDS
    # -------------------------
    upper = analysis["bb_upper"]
    lower = analysis["bb_lower"]

    if direction == "BUY":
        if price < lower:
            confidence += 10
            reasons.append("✓ Price Below Lower Band")
        elif price > upper:
            confidence -= 10
            reasons.append("✗ Price Above Upper Band")

    elif direction == "SELL":
        if price > upper:
            confidence += 10
            reasons.append("✓ Price Above Upper Band")
        elif price < lower:
            confidence -= 10
            reasons.append("✗ Price Below Lower Band")

    # -------------------------
    # LIMIT CONFIDENCE
    # -------------------------
    confidence = max(0, min(confidence, 100))

    # -------------------------
    # FINAL RECOMMENDATION
    # -------------------------
    if direction == "BUY":
        if confidence >= 80:
            recommendation = "STRONG BUY"
        elif confidence >= 65:
            recommendation = "BUY"
        else:
            recommendation = "HOLD"

    elif direction == "SELL":
        if confidence >= 80:
            recommendation = "STRONG SELL"
        elif confidence >= 65:
            recommendation = "SELL"
        else:
            recommendation = "HOLD"

    else:
        recommendation = "HOLD"

    return confidence, recommendation, reasons