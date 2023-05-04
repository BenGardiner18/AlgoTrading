import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def get_historical_prices(ticker:str):
    """Get historical prices for a given ticker"""

    # get data on this ticker
    tickerData = yf.Ticker(ticker)
    
    # get the historical prices for this ticker
    tickerDf = tickerData.history(period='max')

    # return the historical prices
    return tickerDf


def create_moving_averages(small_size,large_size,df):
    """Create moving averages for a given dataframe"""
    
    df[f'{small_size}ma'] = df['Close'].rolling(window=small_size).mean()
    df[f'{large_size}ma'] = df['Close'].rolling(window=large_size).mean()

    # create signal column
    df["signal"] = np.where(df[f'{small_size}ma'] > df[f'{large_size}ma'], 1, -1)

    # column to determine whether to buy or sell or do nothing
    df["Trade"] = np.where(df["signal"] != df["signal"].shift(1), df["signal"], 0)

    return df

def get_data(ticker,small_size,large_size):
    
    # use yfinance to get price data 
    df = get_historical_prices(ticker)

    # create moving averages
    df = create_moving_averages(small_size,large_size,df)

    return df
