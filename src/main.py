from data import get_data
from visualize_trades import visualize
from invest import *

if __name__ == "__main__":

    # ask user for params
    ticker,small_size,large_size = "ETH-USD", 50, 200

    # get data 
    data = get_data(ticker=ticker,small_size=small_size,large_size=large_size)

    # save data to csv for future reference
    data.to_csv("./data/pricing_data.csv")

    # visualize
    visualize(data)

    # invest money 
    portfolio = invest_money(data)

    # save portfolio to csv for future reference
    portfolio.to_csv("./data/portfolio.csv")

    # visualize portfolio
    visualize_returns(portfolio)

    # calculate CAGR
    calculate_returns(portfolio)





