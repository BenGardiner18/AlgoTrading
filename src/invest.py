import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def trade(df, portfolio, cash, eth_owned):
    time = df.name
    price = df["Close"]
    decision = df["Trade"] # -1 = sell, 1 = buy, 0 = do nothing
    eth_price = df["Close"]

    if decision == 1: # BUY 
        eth_purchased = np.floor(cash / eth_price)
        # print(f"Buying {eth_purchased} ETH at {eth_price} at {time}")

        eth_owned += eth_purchased
        cash -= eth_purchased * eth_price
    elif decision == -1: # SELL
        eth_sold = eth_owned
        # print(f"Selling {eth_sold} ETH at {eth_price} at {time}")

        eth_owned -= eth_sold
        cash += eth_sold * eth_price
    else: # HOLD / DO NOTHING
        pass

    eth_value = eth_owned * eth_price # how much the ETH we own is worth
    portfolio_value = eth_value + cash # total value of portfolio
    percent_cash = cash / portfolio_value
    
    portfolio.loc[time] = [
        time, 
        eth_price,
        eth_owned, 
        eth_value,
        cash,
        percent_cash,
        portfolio_value,
    ]

def invest_money(df, n=0):
    starting_money = 100000
    starting_price = df.iloc[0]["Close"]
    hold_eth_owned = np.floor(starting_money / starting_price)

    print(f"Starting portfolio value: ${starting_money}")
    print(f"Starting price of ETH: ${starting_price}")
    print(f"We can currently afford {hold_eth_owned} ETH")

    portfolio = pd.DataFrame(columns=["time","ETH Price","ETH Owned", "ETH Value","Cash", "percent cash","Portfolio Value"])

    eth_owned = hold_eth_owned 
    cash = 0 # cash available to buy ETH



    for i in range(len(df))[-n:]:
        trade(
            df.iloc[i,:], 
            portfolio, 
            cash, 
            eth_owned
        )

        cash = portfolio["Cash"].iloc[-1]
        eth_owned = portfolio["ETH Owned"].iloc[-1]

    
    print(f"\nFinal portfolio value: {portfolio['Portfolio Value'].iloc[-1]}")

    return portfolio

def visualize_returns(portfolio):
    """Visualize returns from trading strategy"""

    fig, ax = plt.subplots(figsize=(12, 8))

    time = portfolio.time
    closing_prices = portfolio["ETH Price"]
    hold_eth_owned = int(portfolio.iloc[0]["Portfolio Value"] / closing_prices[0])

    ax.plot(
        time,
        closing_prices * hold_eth_owned,
        label="(Buy and hold) Portfolio Value",
        alpha=0.5,
    )

    ax.plot(time, portfolio["Portfolio Value"], label="Trading Portfolio Value")

    ax.legend(loc="upper left")

    ax.set_xlabel("Time")
    ax.set_ylabel("Portfolio Value ($)")
    ax.set_title("Portfolio Value Over Time")

    plt.savefig("./images/portfolio_value.png")

    plt.show()

def calculate_returns(portfolio):
    starting_money = portfolio.iloc[0,-1]
    hold_eth_owned = np.floor(portfolio.iloc[0,4] / portfolio.iloc[0,1]) # how much ETH we could have bought at the start

    # starting portfolio value
    print(f"Starting value of portfolio: ${starting_money}\n")

    # ending portfolio value
    ending_value = portfolio.iloc[-1,-1]
    print(f"Ending value of portfolio: ${ending_value}")
    # CAGR 
    end_time = portfolio.iloc[-1,0]
    start_time = portfolio.iloc[0,0]

    # ending price of ETH
    ending_price = portfolio.iloc[-1,1]
    hold_ending_value = ending_price * hold_eth_owned
    print(f"Buy and hold ending value: ${hold_ending_value}")


    years = (end_time - start_time) / 365
    SMA_cagr = (ending_value / starting_money) ** (1/years) - 1 
    hold_cagr = (hold_ending_value / starting_money) ** (1/years) - 1 

    print(f"\nSMA Trading Strategy CAGR: {SMA_cagr}")
    print(f"Buy and Hold CAGR: {hold_cagr}")
