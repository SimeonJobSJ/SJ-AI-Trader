from app.services.market_service import load_market
from backtesting.backtester import backtest_strategy


# ==========================================
# SJ AI TRADER v0.6.4
# CONFIDENCE THRESHOLD EXPERIMENT
# ==========================================

data = load_market("EUR/USD")

thresholds = [65, 70, 75, 80, 85]

results = []


# ==========================================
# RUN ALL CONFIDENCE THRESHOLDS
# ==========================================

for threshold in thresholds:

    print(
        f"\nRunning confidence threshold: {threshold}%"
    )

    result = backtest_strategy(
        data,
        initial_balance=10000,
        risk_per_trade=0.01,
        reward_ratio=2.0,
        min_confidence=threshold,
    )

    results.append({
        "threshold": threshold,
        "final_balance": result["final_balance"],
        "profit": result["total_profit"],
        "trades": result["total_trades"],
        "wins": result["wins"],
        "losses": result["losses"],
        "win_rate": result["win_rate"],
        "profit_factor": result["profit_factor"],
        "max_drawdown": result["max_drawdown"],
    })

# ==========================================
# DISPLAY COMPARISON TABLE
# ==========================================

print("\n")
print("=" * 100)
print("              SJ AI TRADER v0.6.4")
print("           CONFIDENCE THRESHOLD TEST")
print("=" * 100)

print(
    "Threshold   Final Balance   Profit        "
    "Trades    Win Rate    Profit Factor   Max Drawdown"
)

print("-" * 100)

for result in results:
    print(
        f"{result['threshold']}%".ljust(12)
        + f"${result['final_balance']:.2f}".ljust(16)
        + f"${result['profit']:.2f}".ljust(14)
        + f"{result['trades']}".ljust(10)
        + f"{result['win_rate']:.2f}%".ljust(12)
        + f"{result['profit_factor']:.2f}".ljust(16)
        + f"${result['max_drawdown']:.2f}".ljust(15)
    )

print("=" * 100)

# ==========================================
# BEST PROFIT FACTOR
# ==========================================

best_pf = max(
    results,
    key=lambda x: x["profit_factor"]
)

print("\n🏆 BEST PROFIT FACTOR")
print(f"Threshold      : {best_pf['threshold']}%")
print(f"Profit Factor  : {best_pf['profit_factor']:.2f}")
print(f"Final Balance  : ${best_pf['final_balance']:.2f}")
print(f"Total Profit   : ${best_pf['profit']:.2f}")
print(f"Trades         : {best_pf['trades']}")
print(f"Win Rate       : {best_pf['win_rate']:.2f}%")
print(f"Max Drawdown   : ${best_pf['max_drawdown']:.2f}")

# ==========================================
# BEST FINAL BALANCE
# ==========================================

best_return = max(
    results,
    key=lambda x: x["final_balance"]
)

print("\n💰 BEST FINAL BALANCE")
print(f"Threshold      : {best_return['threshold']}%")
print(f"Final Balance  : ${best_return['final_balance']:.2f}")
print(f"Total Profit   : ${best_return['profit']:.2f}")

# ==========================================
# LOWEST DRAWDOWN
# ==========================================

lowest_drawdown = min(
    results,
    key=lambda x: x["max_drawdown"]
)

print("\n🛡️ LOWEST MAX DRAWDOWN")
print(f"Threshold      : {lowest_drawdown['threshold']}%")
print(f"Max Drawdown   : ${lowest_drawdown['max_drawdown']:.2f}")

print("=" * 100)