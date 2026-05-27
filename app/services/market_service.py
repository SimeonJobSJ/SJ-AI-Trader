import pandas as pd
import os


def load_market(pair):
    filename = pair.lower().replace("/", "") + ".csv"
    filepath = os.path.join("data", filename)

    print(f"\nLoading: {filename}")

    return pd.read_csv(filepath)