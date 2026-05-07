import numpy as np

from services.backtesting import RollingVaRBreachBacktestService
from services.data_fetch import PriceDataFetchService, PriceDataRequest
from services.returns import ReturnCalculatorService
from services.scenarios import (
    CorrelationSpikeScenario,
    EquityShock2008Scenario,
    ScenarioInput,
    TechDrawdownScenario,
)
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
    backtest_service = RollingVaRBreachBacktestService()
    scenarios = [
        EquityShock2008Scenario(),
        TechDrawdownScenario(),
        CorrelationSpikeScenario(parametric_var_service),
    ]

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
    scenario_input = ScenarioInput(
        returns=returns,
        weights=weights,
        portfolio_value=PORTFOLIO_VALUE,
    )
    scenario_results = [scenario.run(scenario_input) for scenario in scenarios]
    backtest_result = backtest_service.run(
        portfolio_returns,
        confidence_level=0.95,
        window=250,
    )

    print("Fetched price data successfully.")
    print("Tickers:", list(request.tickers))
    print("Rows:", len(prices))
    print("Start date:", prices.index.min().date())
    print("End date:", prices.index.max().date())
    print(f"Historical 95% VaR: ${historical_var_95.var_dollar:,.2f}")
    print(f"Parametric 95% VaR: ${parametric_var_95.var_dollar:,.2f}")
    print(f"Monte Carlo 95% VaR: ${monte_carlo_var.var_95_dollar:,.2f}")
    print(f"Stress scenarios: {len(scenario_results)}")
    print(
        "Rolling VaR backtest: "
        f"breaches={backtest_result.number_of_breaches}, "
        f"observations={backtest_result.observations}, "
        f"exceedance_rate={backtest_result.exceedance_rate:.2%}, "
        f"expected_exceedance_rate={backtest_result.expected_breach_rate:.2%}"
    )


if __name__ == "__main__":
    main()
