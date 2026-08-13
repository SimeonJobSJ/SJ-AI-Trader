from app.services.market_service import load_market
from backtesting.backtester import backtest_strategy


data = load_market("EUR/USD")


results = backtest_strategy(
    data,
    initial_balance=10000,
    risk_per_trade=0.01,
    reward_ratio=2.0,
    min_confidence=65,
)


print("\n" + "=" * 65)
print("              SJ AI TRADER v0.6.3 BACKTEST")
print("=" * 65)

print(
    f"Initial Balance : "
    f"${results['initial_balance']:.2f}"
)

print(
    f"Final Balance   : "
    f"${results['final_balance']:.2f}"
)

print(
    f"Total Profit    : "
    f"${results['total_profit']:.2f}"
)

print("-" * 65)

print(
    f"Total Trades    : "
    f"{results['total_trades']}"
)

print(
    f"Winning Trades  : "
    f"{results['wins']}"
)

print(
    f"Losing Trades   : "
    f"{results['losses']}"
)

print(
    f"Win Rate        : "
    f"{results['win_rate']:.2f}%"
)

print("-" * 65)

print(
    f"Profit Factor   : "
    f"{results['profit_factor']:.2f}"
)

print(
    f"Max Drawdown    : "
    f"${results['max_drawdown']:.2f}"
)

print("=" * 65)