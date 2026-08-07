def create_trade_plan(price, atr, signal):

    if signal == "BUY 🟢":
        entry = price
        stop_loss = price - (atr * 2)
        take_profit = price + (atr * 4)

    else:
        entry = price
        stop_loss = price + (atr * 2)
        take_profit = price - (atr * 4)

    return {
        "entry": round(entry, 5),
        "stop_loss": round(stop_loss, 5),
        "take_profit": round(take_profit, 5),
    }