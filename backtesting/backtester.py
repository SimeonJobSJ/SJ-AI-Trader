import pandas as pd

from app.analysis.indicators import (
    calculate_sma,
    calculate_rsi,
    calculate_ema,
    calculate_macd,
    calculate_bollinger_bands,
    calculate_atr,
)

from app.ai.decision_engine import calculate_confidence


def backtest_strategy(
    data,
    initial_balance=10000,
    risk_per_trade=0.01,
    reward_ratio=2.0,
    min_confidence=65,
):

    balance = initial_balance
    peak_balance = initial_balance
    max_drawdown = 0

    trades = []

    # =========================================
    # CALCULATE INDICATORS
    # =========================================

    data = data.copy()

    data["SMA"] = calculate_sma(data)
    data["RSI"] = calculate_rsi(data)
    data["EMA"] = calculate_ema(data)

    macd, macd_signal, macd_histogram = calculate_macd(data)

    data["MACD"] = macd
    data["MACD_SIGNAL"] = macd_signal
    data["MACD_HISTOGRAM"] = macd_histogram

    upper_band, lower_band = calculate_bollinger_bands(data)

    data["BB_UPPER"] = upper_band
    data["BB_LOWER"] = lower_band

    data["ATR"] = calculate_atr(data)

    # =========================================
    # START BACKTEST
    # =========================================

    i = 30

    while i < len(data) - 1:

        current = data.iloc[i]

        # =====================================
        # CHECK REQUIRED VALUES
        # =====================================

        required_values = [
            current["Close"],
            current["SMA"],
            current["RSI"],
            current["EMA"],
            current["MACD"],
            current["BB_UPPER"],
            current["BB_LOWER"],
            current["ATR"],
        ]

        if any(
            pd.isna(value).any()
            if isinstance(value, pd.Series)
            else pd.isna(value)
            for value in required_values
        ):
            i += 1
            continue

        # =====================================
        # CONVERT VALUES TO FLOAT
        # =====================================

        price = float(current["Close"])
        sma = float(current["SMA"])
        rsi = float(current["RSI"])
        ema = float(current["EMA"])
        macd_value = float(current["MACD"])
        bb_upper = float(current["BB_UPPER"])
        bb_lower = float(current["BB_LOWER"])
        atr = float(current["ATR"])

        if atr <= 0:
            i += 1
            continue

        # =====================================
        # BASIC SIGNAL
        # =====================================

        if price > sma:
            signal = "BUY 🟢"

        elif price < sma:
            signal = "SELL 🔴"

        else:
            i += 1
            continue

        # =====================================
        # HISTORICAL TREND
        # =====================================

        lookback = 20

        if i < lookback:
            i += 1
            continue

        first_close = float(
            data["Close"].iloc[i - lookback]
        )

        last_close = price

        if last_close > first_close:
            trend = "Bullish"

        elif last_close < first_close:
            trend = "Bearish"

        else:
            trend = "Sideways"

        # =====================================
        # ANALYSIS
        # =====================================

        analysis = {
            "signal": signal,
            "trend": trend,
            "rsi": rsi,
            "price": price,
            "sma": sma,
            "ema": ema,
            "macd": macd_value,
            "bb_upper": bb_upper,
            "bb_lower": bb_lower,
        }

        # =====================================
        # DECISION ENGINE
        # =====================================

        (
            confidence,
            recommendation,
            reasons,
            signal_strength,
            trend_alignment,
            supporting,
            opposing,
        ) = calculate_confidence(analysis)

        # =====================================
        # CONFIDENCE FILTER
        # =====================================

        if confidence < min_confidence:
            i += 1
            continue

        if recommendation not in [
            "BUY",
            "STRONG BUY",
            "SELL",
            "STRONG SELL",
        ]:
            i += 1
            continue

        # =====================================
        # CONFIRM DIRECTION
        # =====================================

        if signal.startswith("BUY"):

            if not recommendation.endswith("BUY"):
                i += 1
                continue

            direction = "BUY"

        else:

            if not recommendation.endswith("SELL"):
                i += 1
                continue

            direction = "SELL"

        # =====================================
        # POSITION SIZING
        # =====================================

        risk_amount = balance * risk_per_trade

        if direction == "BUY":

            entry = price

            stop_loss = entry - atr

            take_profit = entry + (
                atr * reward_ratio
            )

        else:

            entry = price

            stop_loss = entry + atr

            take_profit = entry - (
                atr * reward_ratio
            )

        risk_per_unit = abs(
            entry - stop_loss
        )

        if risk_per_unit <= 0:
            i += 1
            continue

        position_size = (
            risk_amount / risk_per_unit
        )

        # =====================================
        # FIND EXIT
        # =====================================

        trade_result = None
        exit_price = None
        exit_index = None

        j = i + 1

        while j < len(data):

            future = data.iloc[j]

            high = float(future["High"])
            low = float(future["Low"])

            # ---------------------------------
            # BUY TRADE
            # ---------------------------------

            if direction == "BUY":

                if low <= stop_loss:

                    exit_price = stop_loss
                    trade_result = "LOSS"
                    exit_index = j

                    break

                if high >= take_profit:

                    exit_price = take_profit
                    trade_result = "WIN"
                    exit_index = j

                    break

            # ---------------------------------
            # SELL TRADE
            # ---------------------------------

            else:

                if high >= stop_loss:

                    exit_price = stop_loss
                    trade_result = "LOSS"
                    exit_index = j

                    break

                if low <= take_profit:

                    exit_price = take_profit
                    trade_result = "WIN"
                    exit_index = j

                    break

            j += 1

        # =====================================
        # NO EXIT
        # =====================================

        if trade_result is None:
            break

        # =====================================
        # CALCULATE PROFIT
        # =====================================

        if direction == "BUY":

            profit = (
                exit_price - entry
            ) * position_size

        else:

            profit = (
                entry - exit_price
            ) * position_size

        balance += profit

        # =====================================
        # DRAW DOWN
        # =====================================

        if balance > peak_balance:
            peak_balance = balance

        drawdown = peak_balance - balance

        if drawdown > max_drawdown:
            max_drawdown = drawdown

        # =====================================
        # SAVE TRADE
        # =====================================

        trades.append({
            "signal": direction,
            "confidence": confidence,
            "recommendation": recommendation,
            "reasons": reasons,
            "signal_strength": signal_strength,
            "trend": trend,
            "trend_alignment": trend_alignment,
            "supporting": supporting,
            "opposing": opposing,
            "entry": entry,
            "stop_loss": stop_loss,
            "take_profit": take_profit,
            "exit": exit_price,
            "position_size": position_size,
            "profit": profit,
            "result": trade_result,
            "entry_index": i,
            "exit_index": exit_index,
        })

        # =====================================
        # MOVE TO NEXT TRADE
        # =====================================

        i = exit_index + 1

    # =========================================
    # STATISTICS
    # =========================================

    total_trades = len(trades)

    wins = sum(
        1
        for trade in trades
        if trade["result"] == "WIN"
    )

    losses = sum(
        1
        for trade in trades
        if trade["result"] == "LOSS"
    )

    win_rate = (
        (wins / total_trades) * 100
        if total_trades > 0
        else 0
    )

    total_profit = sum(
        trade["profit"]
        for trade in trades
    )

    gross_profit = sum(
        trade["profit"]
        for trade in trades
        if trade["profit"] > 0
    )

    gross_loss = abs(
        sum(
            trade["profit"]
            for trade in trades
            if trade["profit"] < 0
        )
    )

    profit_factor = (
        gross_profit / gross_loss
        if gross_loss > 0
        else 0
    )

    # =========================================
    # RETURN RESULTS
    # =========================================

    return {
        "initial_balance": initial_balance,
        "final_balance": balance,
        "total_profit": total_profit,
        "total_trades": total_trades,
        "wins": wins,
        "losses": losses,
        "win_rate": win_rate,
        "profit_factor": profit_factor,
        "max_drawdown": max_drawdown,
        "trades": trades,
    }