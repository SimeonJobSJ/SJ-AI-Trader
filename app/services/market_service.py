import pandas as pd
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


    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    return data.reset_index()