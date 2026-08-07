from app.services.market_service import load_market

from app.analysis.indicators import (
    calculate_sma,
    calculate_rsi,
    calculate_ema,
    calculate_macd,
    calculate_bollinger_bands,
    calculate_atr,
)

from app.analysis.market_analysis import (
    analyze_market,
    trading_signal,
)

from app.ai.decision_engine import calculate_confidence
from app.ai.risk_manager import calculate_risk
from app.ai.trade_planner import create_trade_plan


PAIRS = [
    "EUR/USD",
    "GBP/USD",
    "USD/JPY",
    "AUD/USD",
    "USD/CAD",
]


def scan_markets():
    results = []

    for pair in PAIRS:
        market = load_market(pair)

        market["SMA"] = calculate_sma(market)
        market["EMA"] = calculate_ema(market)
        market["MACD"], market["MACD_SIGNAL"], market["MACD_HIST"] = calculate_macd(market)
        market["BB_UPPER"], market["BB_LOWER"] = calculate_bollinger_bands(market)
        market["ATR"] = calculate_atr(market)
        market["RSI"] = calculate_rsi(market)

        analysis = analyze_market(market)
        signal = trading_signal(market)

        ai_data = {
            "trend": analysis["trend"],
            "rsi": market["RSI"].iloc[-1],
            "price": market["Close"].iloc[-1],
            "sma": market["SMA"].iloc[-1],
            "ema": market["EMA"].iloc[-1],
            "macd": market["MACD"].iloc[-1],
            "bb_upper": market["BB_UPPER"].iloc[-1],
            "bb_lower": market["BB_LOWER"].iloc[-1],
            "atr": market["ATR"].iloc[-1],
        }

        confidence, recommendation, reasons = calculate_confidence(ai_data)
        risk = calculate_risk(confidence)


        trade = create_trade_plan(
            market["Close"].iloc[-1],
            market["ATR"].iloc[-1],
            signal,
        )

        results.append({
            "pair": pair,
            "signal": signal,
            "confidence": confidence,
            "recommendation": recommendation,
            "trend": analysis["trend"],
            "price": round(market["Close"].iloc[-1], 5),
            "rsi": round(market["RSI"].iloc[-1], 2),
            "sma": round(market["SMA"].iloc[-1], 5),
            "ema": round(market["EMA"].iloc[-1], 5),
            "atr": round(market["ATR"].iloc[-1], 5),
            "entry": trade["entry"],
            "stop_loss": trade["stop_loss"],
            "take_profit": trade["take_profit"],
            "risk": risk,
            "reasons": reasons,
        })

    results = sorted(
        results,
        key=lambda x: x["confidence"],
        reverse=True,
    )

    return results