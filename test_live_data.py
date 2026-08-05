import yfinance as yf

# Yahoo Finance ticker for EUR/USD
ticker = yf.Ticker("EURUSD=X")

data = ticker.history(period="5d", interval="1h")

print(data.tail())