from data import get_data
from visualize_trades import visualize

if __name__ == "__main__":
    # params
    ticker = "ETH-USD"
    small_size = 20
    large_size = 50


    # get data 
    data = get_data(
        ticker=ticker,
        small_size=small_size,
        large_size=large_size
    )

    data.to_csv("./data/pricing_data.csv")


    # visualize
    visualize(data)

