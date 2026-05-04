from data import PriceDataFetchService, PriceDataRequest
from returns import ReturnCalculatorService


def main():
    request = PriceDataRequest(
        tickers=["AAPL", "GOOGL", "MSFT"],
        start_date="2020-01-01",
        end_date=None,
    )
    service = PriceDataFetchService()
    return_calculator = ReturnCalculatorService()

    prices = service.fetch_prices(request)
    service.save_prices(prices, "prices.csv")
    returns = return_calculator.calculate_returns(prices)
    return_calculator.save_returns(returns, "returns.csv")

    print("Fetched price data successfully.")
    print()
    print("Tickers:", list(request.tickers))
    print("Rows:", len(prices))
    print("Start date:", prices.index.min().date())
    print("End date:", prices.index.max().date())
    print()
    print("Latest prices:")
    print(prices.tail())
    print()
    print("Daily returns:")
    print(returns.head())
    print(returns.tail())


if __name__ == "__main__":
    main()
