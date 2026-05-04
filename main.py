import numpy as np

from services.data_fetch import PriceDataFetchService, PriceDataRequest
from services.returns import ReturnCalculatorService
from services.scenarios import CorrelationSpikeScenarioService
from services.var import (
    HistoricalVaRService,
    MonteCarloVaRService,
    ParametricVaRService,
)


PORTFOLIO_VALUE = 1_000_000


def main():
    request = PriceDataRequest(
        tickers=["AAPL", "GOOGL", "MSFT"],
        start_date="2020-01-01",
        end_date=None,
    )
    service = PriceDataFetchService()
    return_calculator = ReturnCalculatorService()
    historical_var_service = HistoricalVaRService()
    parametric_var_service = ParametricVaRService()
    monte_carlo_var_service = MonteCarloVaRService()
    correlation_spike_service = CorrelationSpikeScenarioService(parametric_var_service)

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
    historical_var_95 = historical_var_service.calculate_var(
        portfolio_returns,
        PORTFOLIO_VALUE,
        confidence_level=0.95,
    )
    historical_var_99 = historical_var_service.calculate_var(
        portfolio_returns,
        PORTFOLIO_VALUE,
        confidence_level=0.99,
    )
    parametric_var_95 = parametric_var_service.calculate_var(
        returns,
        weights,
        PORTFOLIO_VALUE,
        confidence_level=0.95,
    )
    parametric_var_99 = parametric_var_service.calculate_var(
        returns,
        weights,
        PORTFOLIO_VALUE,
        confidence_level=0.99,
    )
    monte_carlo_var = monte_carlo_var_service.calculate_var(
        returns,
        weights,
        portfolio_value=PORTFOLIO_VALUE,
        num_simulations=10_000,
        seed=42,
    )
    correlation_spike = correlation_spike_service.run(
        returns,
        weights,
        PORTFOLIO_VALUE,
        correlation=0.85,
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
    print(f"95% VaR return: {historical_var_95.var_return:.4%}")
    print(f"95% VaR dollar: ${historical_var_95.var_dollar:,.2f}")
    print(f"99% VaR return: {historical_var_99.var_return:.4%}")
    print(f"99% VaR dollar: ${historical_var_99.var_dollar:,.2f}")
    print()
    print("Parametric VaR")
    print(
        "Portfolio daily volatility: "
        f"{parametric_var_95.portfolio_volatility:.4%}"
    )
    print(f"95% VaR: ${parametric_var_95.var_dollar:,.2f}")
    print(f"99% VaR: ${parametric_var_99.var_dollar:,.2f}")
    print()
    print("Monte Carlo VaR")
    print(f"Simulations: {monte_carlo_var.num_simulations}")
    print(f"Seed: {monte_carlo_var.seed}")
    print(f"95% VaR return: {monte_carlo_var.var_95_return:.4%}")
    print(f"95% VaR dollar: ${monte_carlo_var.var_95_dollar:,.2f}")
    print(f"99% VaR return: {monte_carlo_var.var_99_return:.4%}")
    print(f"99% VaR dollar: ${monte_carlo_var.var_99_dollar:,.2f}")
    print()
    print("Correlation Spike Scenario")
    print(f"Stressed correlation: {correlation_spike.stressed_corr:.2f}")
    print(f"Stressed daily volatility: {correlation_spike.portfolio_vol:.4%}")
    print(f"95% stressed VaR: ${correlation_spike.var_95_dollar:,.2f}")
    print(f"99% stressed VaR: ${correlation_spike.var_99_dollar:,.2f}")


if __name__ == "__main__":
    main()
