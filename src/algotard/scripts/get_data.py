import ccxt
import pandas as pd

kraken = ccxt.kraken()


def get_data(symbol: str, timeframe: str, since_date: str):
    since = kraken.parse8601(since_date)  # Fetch data since this time

    # Fetch OHLCV data
    ohlcv = kraken.fetch_ohlcv(symbol, timeframe, since=since)

    # Convert data to a DataFrame
    df = pd.DataFrame(
        ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"]
    )
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    return df
