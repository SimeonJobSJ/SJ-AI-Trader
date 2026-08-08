def calculate_confidence(analysis):

    confidence = 50
    reasons = []

    signal = analysis.get("signal", "")

    # Determine direction
    if signal.startswith("BUY"):
        direction = "BUY"
    elif signal.startswith("SELL"):
        direction = "SELL"
    else:
        direction = "HOLD"

    # Track confluence
    supporting = 0
    opposing = 0

    # -------------------------
    # TREND
    # -------------------------
    trend = analysis["trend"]

    if direction == "BUY":
        if trend == "Bullish":
            confidence += 20
            supporting += 1
            trend_alignment = "ALIGNED"
            reasons.append("✓ Bullish Trend supports BUY")
        elif trend == "Bearish":
            confidence -= 20
            opposing += 1
            trend_alignment = "OPPOSED"
            reasons.append("✗ Bearish Trend opposes BUY")
        else:
            trend_alignment = "MIXED"
            reasons.append("➖ Sideways Market")

    elif direction == "SELL":
        if trend == "Bearish":
            confidence += 20
            supporting += 1
            trend_alignment = "ALIGNED"
            reasons.append("✓ Bearish Trend supports SELL")
        elif trend == "Bullish":
            confidence -= 20
            opposing += 1
            trend_alignment = "OPPOSED"
            reasons.append("✗ Bullish Trend opposes SELL")
        else:
            trend_alignment = "MIXED"
            reasons.append("➖ Sideways Market")

    else:
        trend_alignment = "MIXED"
        reasons.append("➖ No active trade direction")

    # -------------------------
    # RSI
    # -------------------------
    rsi = analysis["rsi"]

    if 40 <= rsi <= 60:
        confidence += 10
        supporting += 1
        reasons.append("✓ RSI Healthy")

    elif rsi > 70:
        if direction == "SELL":
            confidence += 15
            supporting += 1
            reasons.append("✓ RSI Overbought supports SELL")
        elif direction == "BUY":
            confidence -= 15
            opposing += 1
            reasons.append("✗ RSI Overbought opposes BUY")

    elif rsi < 30:
        if direction == "BUY":
            confidence += 15
            supporting += 1
            reasons.append("✓ RSI Oversold supports BUY")
        elif direction == "SELL":
            confidence -= 15
            opposing += 1
            reasons.append("✗ RSI Oversold opposes SELL")

    # -------------------------
    # SMA
    # -------------------------
    price = analysis["price"]
    sma = analysis["sma"]

    if direction == "BUY":
        if price > sma:
            confidence += 15
            supporting += 1
            reasons.append("✓ Price Above SMA")
        else:
            confidence -= 15
            opposing += 1
            reasons.append("✗ Price Below SMA")

    elif direction == "SELL":
        if price < sma:
            confidence += 15
            supporting += 1
            reasons.append("✓ Price Below SMA")
        else:
            confidence -= 15
            opposing += 1
            reasons.append("✗ Price Above SMA")

    # -------------------------
    # EMA
    # -------------------------
    ema = analysis["ema"]

    if direction == "BUY":
        if price > ema:
            confidence += 10
            supporting += 1
            reasons.append("✓ Price Above EMA")
        else:
            confidence -= 10
            opposing += 1
            reasons.append("✗ Price Below EMA")

    elif direction == "SELL":
        if price < ema:
            confidence += 10
            supporting += 1
            reasons.append("✓ Price Below EMA")
        else:
            confidence -= 10
            opposing += 1
            reasons.append("✗ Price Above EMA")

    # -------------------------
    # MACD
    # -------------------------
    macd = analysis["macd"]

    if direction == "BUY":
        if macd > 0:
            confidence += 15
            supporting += 1
            reasons.append("✓ MACD Bullish")
        else:
            confidence -= 15
            opposing += 1
            reasons.append("✗ MACD Bearish")

    elif direction == "SELL":
        if macd < 0:
            confidence += 15
            supporting += 1
            reasons.append("✓ MACD Bearish")
        else:
            confidence -= 15
            opposing += 1
            reasons.append("✗ MACD Bullish")

    # -------------------------
    # BOLLINGER BANDS
    # -------------------------
    upper = analysis["bb_upper"]
    lower = analysis["bb_lower"]

    if direction == "BUY":
        if price < lower:
            confidence += 10
            supporting += 1
            reasons.append("✓ Price Below Lower Band")
        elif price > upper:
            confidence -= 10
            opposing += 1
            reasons.append("✗ Price Above Upper Band")

    elif direction == "SELL":
        if price > upper:
            confidence += 10
            supporting += 1
            reasons.append("✓ Price Above Upper Band")
        elif price < lower:
            confidence -= 10
            opposing += 1
            reasons.append("✗ Price Below Lower Band")

    # -------------------------
    # CONFIDENCE LIMIT
    # -------------------------
    confidence = max(0, min(confidence, 100))

    # -------------------------
    # SIGNAL STRENGTH
    # -------------------------
    if supporting >= 5 and opposing == 0:
        signal_strength = "STRONG"

    elif supporting >= 4 and opposing <= 1:
        signal_strength = "MODERATE"

    elif supporting >= 3:
        signal_strength = "WEAK"

    else:
        signal_strength = "VERY WEAK"

    # -------------------------
    # RECOMMENDATION
    # -------------------------
    if direction == "BUY":

        if confidence >= 80 and signal_strength in ["STRONG", "MODERATE"]:
            recommendation = "STRONG BUY"

        elif confidence >= 65:
            recommendation = "BUY"

        else:
            recommendation = "HOLD"

    elif direction == "SELL":

        if confidence >= 80 and signal_strength in ["STRONG", "MODERATE"]:
            recommendation = "STRONG SELL"

        elif confidence >= 65:
            recommendation = "SELL"

        else:
            recommendation = "HOLD"

    else:
        recommendation = "HOLD"

    # -------------------------
    # RETURN RESULTS
    # -------------------------
    return (
        confidence,
        recommendation,
        reasons,
        signal_strength,
        trend_alignment,
        supporting,
        opposing,
    )