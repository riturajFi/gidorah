# Codex Repo Instructions

## Navigation

Start here before reading implementation files.

1. Read this file first.
2. Identify target capability.
3. Open target folder `instructions.md`.
4. Open only referenced files in that folder.
5. Use `portfolio_var_analysis.ipynb` for notebook workflow.
6. Use `main.py` only as CLI mirror.

## Repo Map

- `portfolio_var_analysis.ipynb`: primary notebook workflow with cell-by-cell exploration.
- `main.py`: CLI mirror. No business logic should live here.
- `README.md`: quick run and project overview for humans.
- `services/data_fetch/`: market data fetch, validation, price CSV read/write.
- `services/returns/`: daily stock returns and daily portfolio returns.
- `services/var/`: Historical Simulation VaR, Parametric VaR, Monte Carlo VaR.
- `services/scenarios/`: scenario interface and stress scenario implementations.
- `services/backtesting/`: rolling VaR breach backtest.
- `requirements.txt`: Python dependencies.
- generated CSV files: `prices.csv`, `returns.csv`, `portfolio_returns.csv`.

## Folder Guides

- For price fetching, read `services/data_fetch/instructions.md`.
- For return calculation, read `services/returns/instructions.md`.
- For VaR calculation, read `services/var/instructions.md`.
- For stress scenarios, read `services/scenarios/instructions.md`.
- For rolling VaR backtest, read `services/backtesting/instructions.md`.

## Design Style

- Keep services small and single-purpose.
- Put each service in its own folder.
- Export public classes from folder `__init__.py`.
- Keep `main.py` and notebook outside service folders.
- Let `main.py` and notebook coordinate services only.
- Notebook code should call services in separate domain cells, not reimplement service logic inline.
- Prefer explicit service class names: `PriceDataFetchService`, `ReturnCalculatorService`, `HistoricalVaRService`, `ParametricVaRService`, `MonteCarloVaRService`.
- Prefer immutable dataclasses for request/result objects.
- Keep formulas visible and close to domain names.
- Use pandas/numpy built-ins for financial calculations.
- Keep file IO close to the service that owns the data type.
- Raise `ValueError` early when input data is unusable.

## Avoid

- Do not put calculations directly in `main.py` or notebook cells.
- Do not mix fetch, return, and VaR logic in one file.
- Do not add abstractions unless they remove real duplication or clarify a domain boundary.
- Do not hide simple formulas behind many helper methods.
- Do not hand-roll pandas operations that already exist, such as `pct_change`, `quantile`, or matrix multiplication.
- Do not commit generated CSV files unless explicitly requested.
- Do not make service folders depend on each other unless there is a clear domain reason.

## Current Flow

Notebook and `main.py` run this same pipeline:

1. `PriceDataFetchService.fetch_prices(...)`
2. `PriceDataFetchService.save_prices(...)`
3. `ReturnCalculatorService.calculate_returns(...)`
4. `ReturnCalculatorService.save_returns(...)`
5. `ReturnCalculatorService.calculate_portfolio_returns(...)`
6. `ReturnCalculatorService.save_portfolio_returns(...)`
7. `HistoricalVaRService.calculate_var(...)`
8. `ParametricVaRService.calculate_var(...)`
9. `MonteCarloVaRService.calculate_var(...)`
10. `Scenario.run(...)` for each stress scenario
11. `RollingVaRBreachBacktestService.run(...)`
12. Notebook builds tables/charts from service outputs

## Data Contracts

- Prices: `pd.DataFrame`, date index, ticker columns, adjusted close prices.
- Stock returns: `pd.DataFrame`, date index, ticker columns, daily percentage returns as decimals.
- Portfolio returns: `pd.Series`, date index, name `portfolio_return`.
- VaR result: `HistoricalVaRResult`, fields `confidence_level`, `var_return`, `var_dollar`.
- Parametric VaR result: `ParametricVaRResult`, fields `confidence_level`, `portfolio_volatility`, `var_dollar`.
- Monte Carlo VaR result: `MonteCarloVaRResult`, fields `var_95_return`, `var_95_dollar`, `var_99_return`, `var_99_dollar`, `num_simulations`, `seed`.
- Scenario input: `ScenarioInput`, fields `returns`, `weights`, `portfolio_value`.
- Scenario result: `ScenarioResult`, fields `name`, `metrics`.
- Scenario contract: every scenario inherits `Scenario` and implements `run(scenario_input)`.
- Rolling VaR backtest result: `RollingVaRBacktestResult`, fields `breach_count`, `breach_rate`, `expected_breach_rate`, `comment`, `backtest_data`.
