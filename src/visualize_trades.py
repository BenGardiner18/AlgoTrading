import matplotlib.pyplot as plt

def plot_price_n_moving_averages(df):
    """Plot price and moving averages"""

    fig, ax = plt.subplots(figsize=(10, 6))

    time_period = df.index
    closing_prices = df['Close']
    
    # plotting prices
    ax.plot(
        time_period,
        closing_prices, 
        label='Close',
        alpha=0.5
    )

    # plotting fast moving average 
    ax.plot(
        time_period, 
        df.iloc[:,-3], 
        label='fast moving average', 
        alpha=1
    )

    # plotting slow moving average
    ax.plot(
        df.index, 
        df.iloc[:,-4], 
        label='slow moving average', 
        alpha=1
    )

    leg = ax.legend(loc='upper left')
    ax.set_title('ETH-USD')

    plt.savefig("./images/price_n_moving_averages.png")

    plt.show()

def plot_decisions(df,n=0):
    time_period = df.index 
    start_time = time_period[-n]

    fig, ax = plt.subplots(figsize=(10, 6))

    closing_prices = df['Close'].astype(float)
    slow_ma = df.iloc[:,-4].astype(float)
    fast_ma = df.iloc[:,-3].astype(float)
    
    ax.plot(time_period[-n:], closing_prices[-n:], label='Close')
    ax.plot(time_period[-n:], fast_ma[-n:], label='fast moving average')
    ax.plot(time_period[-n:], slow_ma[-n:], label='slow moving average')

    for i in range(len(df)):
        time = df.index[i]
        trade = df.iloc[i,-1]

        if time <= start_time:
            continue
        else:
            if trade == 1: # buy 
                ax.scatter(time, df.loc[time, "Close"], color="green", marker="^", s=100) # type: ignore
            elif trade == -1: # sell
                ax.scatter(time, df.loc[time, "Close"], color="red", marker="v", s=100) # type: ignore
            else: # do nothing
                continue
    leg = ax.legend(loc='upper right')
    ax.set_title('ETH-USD')

    plt.savefig("./images/decisions.png")

    plt.show()
    

def visualize(df):
    plot_price_n_moving_averages(df)
    plot_decisions(df,n=365)

