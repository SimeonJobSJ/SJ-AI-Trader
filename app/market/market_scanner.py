from app.services.market_service import load_market
from app.analysis.indicators import (
    calculate_sma,
    calculate_rsi,
    calculate_ema,
)
from app.analysis.market_analysis import (
    analyze_market,
    trading_signal,
)
from app.ai.decision_engine import calculate_confidence
from app.ai.risk_manager import calculate_risk


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
        market["RSI"] = calculate_rsi(market)

        analysis = analyze_market(market)
        signal = trading_signal(market)

        ai_data = {
            "trend": analysis["trend"],
            "rsi": market["RSI"].iloc[-1],
            "price": market["Close"].iloc[-1],
            "sma": market["SMA"].iloc[-1],
             "ema": market["EMA"].iloc[-1],
        }

        confidence, recommendation, reasons = calculate_confidence(ai_data)
        risk = calculate_risk(confidence)

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
            "risk": risk,
            "reasons": reasons,
        })

    results = sorted(
        results,
        key=lambda x: x["confidence"],
        reverse=True
    )

    return results