import numpy as np

from services.data_fetch import PriceDataFetchService, PriceDataRequest
from services.returns import ReturnCalculatorService
from services.var import HistoricalVaRService


PORTFOLIO_VALUE = 1_000_000


def main():
    request = PriceDataRequest(
        tickers=["AAPL", "GOOGL", "MSFT"],
        start_date="2020-01-01",
        end_date=None,
    )
    service = PriceDataFetchService()
    return_calculator = ReturnCalculatorService()
    var_service = HistoricalVaRService()

    prices = service.fetch_prices(request)
    service.save_prices(prices, "prices.csv")

    returns = return_calculator.calculate_returns(prices)
    return_calculator.save_returns(returns, "returns.csv")

    weights = np.array([0.40, 0.35, 0.25])
    portfolio_returns = return_calculator.calculate_portfolio_returns(returns, weights)
    return_calculator.save_portfolio_returns(
        portfolio_returns,
        "portfolio_returns.csv",
    )
    var_95 = var_service.calculate_var(
        portfolio_returns,
        PORTFOLIO_VALUE,
        confidence_level=0.95,
    )
    var_99 = var_service.calculate_var(
        portfolio_returns,
        PORTFOLIO_VALUE,
        confidence_level=0.99,
    )

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
    print()
    print("Portfolio daily returns:")
    print(portfolio_returns.head())
    print(portfolio_returns.tail())
    print()
    print("Historical VaR")
    print(f"95% VaR return: {var_95.var_return:.4%}")
    print(f"95% VaR dollar: ${var_95.var_dollar:,.2f}")
    print(f"99% VaR return: {var_99.var_return:.4%}")
    print(f"99% VaR dollar: ${var_99.var_dollar:,.2f}")


if __name__ == "__main__":
    main()
