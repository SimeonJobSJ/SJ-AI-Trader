import yfinance as yf

def get_live_data(pair):

    symbol = pair.replace("/", "") + "=X"

    data = yf.download(
        symbol,
        period="5d",
        interval="1h",
        progress=False,
        auto_adjust=False
    )

    # Flatten MultiIndex columns if present
    if hasattr(data.columns, "nlevels") and data.columns.nlevels > 1:
        data.columns = data.columns.get_level_values(0)

    return data