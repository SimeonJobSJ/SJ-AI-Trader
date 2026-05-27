import pandas as pd


def load_market_data():
    data = pd.read_csv("data/eurusd.csv")
    return data