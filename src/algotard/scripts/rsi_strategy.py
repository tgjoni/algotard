"""Strategy 1.

Check if the RSI of a given asset is under 30.
"""

import time

import numpy as np
import pandas as pd
import ta
from loguru import logger

from algotard.scripts.email_utils import send_email
from algotard.scripts.get_data import get_data


class MissingColumn:
    """A column is missing from the dataframe"""


def get_rsi(df: pd.DataFrame) -> pd.DataFrame:
    """Get the RSI of the given Close price.

    Parameters
    ----------
    df : pd.DataFrame
        Data that has close price.

    Returns
    -------
    pd.DataFrame
        Dataframe witht Close and RSI.
    """
    df["rsi"] = ta.momentum.RSIIndicator(df["close"], window=14).rsi()
    return df


def strategy_1(df: pd.DataFrame) -> bool:
    """BUY order for when the RSI is below 30."""
    if "rsi" not in df.columns:
        raise MissingColumn("RSI data column is missing!")
    if df["rsi"].iloc[-1] < np.float64(30):
        return True
    return False


def run():
    tickers = ["BTC/USD", "ETH/USD", "XRP/USD", "LINK/USD"]
    for ticker in tickers:
        # TODO: Change to a dynamic date range
        df = get_data(ticker, "15m", "2024-09-02")
        df = get_rsi(df)
        result = strategy_1(df)
        if result:
            logger.success("RSI below! Sending alert . . .")
            send_email("RSI below 30!", f"RSI below 30 for {ticker}")
        else:
            logger.info("Strategy not triggered!")


if __name__ == "__main__":
    while True:
        logger.info("Checking Strategy 1 . . .")
        run()
        time.sleep(300)
