# Codex Repo Instructions

## Navigation

Start here before reading implementation files.

1. Read this file first.
2. Identify target capability.
3. Open target folder `instructions.md`.
4. Open only referenced files in that folder.
5. Use `main.py` only to understand orchestration.

## Repo Map

- `main.py`: top-level workflow. No business logic should live here.
- `services/data_fetch/`: market data fetch, validation, price CSV read/write.
- `services/returns/`: daily stock returns and daily portfolio returns.
- `services/var/`: Historical Simulation VaR.
- `requirements.txt`: Python dependencies.
- generated CSV files: `prices.csv`, `returns.csv`, `portfolio_returns.csv`.

## Folder Guides

- For price fetching, read `services/data_fetch/instructions.md`.
- For return calculation, read `services/returns/instructions.md`.
- For VaR calculation, read `services/var/instructions.md`.

## Design Style

- Keep services small and single-purpose.
- Put each service in its own folder.
- Export public classes from folder `__init__.py`.
- Keep `main.py` outside service folders.
- Let `main.py` coordinate services only.
- Prefer explicit service class names: `PriceDataFetchService`, `ReturnCalculatorService`, `HistoricalVaRService`.
- Prefer immutable dataclasses for request/result objects.
- Keep formulas visible and close to domain names.
- Use pandas/numpy built-ins for financial calculations.
- Keep file IO close to the service that owns the data type.
- Raise `ValueError` early when input data is unusable.

## Avoid

- Do not put calculations directly in `main.py`.
- Do not mix fetch, return, and VaR logic in one file.
- Do not add abstractions unless they remove real duplication or clarify a domain boundary.
- Do not hide simple formulas behind many helper methods.
- Do not hand-roll pandas operations that already exist, such as `pct_change`, `quantile`, or matrix multiplication.
- Do not commit generated CSV files unless explicitly requested.
- Do not make service folders depend on each other unless there is a clear domain reason.

## Current Flow

`main.py` runs this pipeline:

1. `PriceDataFetchService.fetch_prices(...)`
2. `PriceDataFetchService.save_prices(...)`
3. `ReturnCalculatorService.calculate_returns(...)`
4. `ReturnCalculatorService.save_returns(...)`
5. `ReturnCalculatorService.calculate_portfolio_returns(...)`
6. `ReturnCalculatorService.save_portfolio_returns(...)`
7. `HistoricalVaRService.calculate_var(...)`

## Data Contracts

- Prices: `pd.DataFrame`, date index, ticker columns, adjusted close prices.
- Stock returns: `pd.DataFrame`, date index, ticker columns, daily percentage returns as decimals.
- Portfolio returns: `pd.Series`, date index, name `portfolio_return`.
- VaR result: `HistoricalVaRResult`, fields `confidence_level`, `var_return`, `var_dollar`.
