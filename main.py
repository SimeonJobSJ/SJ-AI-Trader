from app.market.market_scanner import scan_markets

results = scan_markets()

print("\n" + "=" * 90)
print("                     SJ AI TRADER v0.4")
print("=" * 90)

print(
    f"{'Pair':<10}"
    f"{'Signal':<10}"
    f"{'Confidence':<12}"
    f"{'Risk':<15}"
    f"{'Trend':<15}"
    f"{'RSI':<10}"
    f"{'Price':<10}"
)

print("-" * 90)

for result in results:
    print(
        f"{result['pair']:<10}"
        f"{result['signal']:<10}"
        f"{str(result['confidence']) + '%':<12}"
        f"{result['risk']:<15}"
        f"{result['trend']:<15}"
        f"{result['rsi']:<10}"
        f"{result['price']:<10}"
    )

print("=" * 90)

# Find the best trade
best = max(results, key=lambda x: x["confidence"])

print("\n⭐ Best Opportunity Today")
print(f"Pair        : {best['pair']}")
print(f"Signal      : {best['signal']}")
print(f"Confidence  : {best['confidence']}%")
print(f"Risk        : {best['risk']}")
print(f"Entry Price : {best['entry']:.5f}")
print(f"Stop Loss   : {best['stop_loss']:.5f}")
print(f"Take Profit : {best['take_profit']:.5f}")

print("\nReasons")
for reason in best["reasons"]:
    print(reason)

print("\n🏆 TOP 3 OPPORTUNITIES")

for i, trade in enumerate(results[:3], start=1):
    print(
        f"{i}. {trade['pair']} | "
        f"{trade['signal']} | "
        f"{trade['confidence']}% | "
        f"{trade['risk']}"
    )