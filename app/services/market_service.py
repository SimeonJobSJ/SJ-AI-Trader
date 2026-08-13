import yfinance as yf


SYMBOLS = {
    "EUR/USD": "EURUSD=X",
    "GBP/USD": "GBPUSD=X",
    "USD/JPY": "JPY=X",
    "AUD/USD": "AUDUSD=X",
    "USD/CAD": "CAD=X",
}


def load_market(pair):

    symbol = SYMBOLS[pair]

    print(f"\nDownloading {pair}...")

    data = yf.download(
        symbol,
        period="3mo",
        interval="1h",
        auto_adjust=True,
        progress=False,
    )

    # Fix Yahoo Finance MultiIndex columns
    if hasattr(data.columns, "nlevels") and data.columns.nlevels > 1:
        data.columns = data.columns.get_level_values(0)

    data = data.reset_index()

    print(f"{pair} rows: {len(data)}")

    if data.empty:
        print(f"⚠️ WARNING: No data returned for {pair}")

    return data