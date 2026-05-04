# Data Fetch Service Instructions

## Purpose

Fetch daily adjusted close prices for ticker symbols.

## Files

- `service.py`: `PriceDataFetchService`, `PriceDataRequest`
- `__init__.py`: public exports

## Public API

- `PriceDataRequest`: immutable request object with `tickers`, `start_date`, `end_date`
- `PriceDataFetchService.fetch_prices(request)`: fetches prices from Yahoo Finance
- `PriceDataFetchService.validate_prices(prices, tickers)`: rejects unusable price data
- `PriceDataFetchService.save_prices(prices, path)`: writes CSV
- `PriceDataFetchService.load_prices(path)`: reads CSV

## Rules

- Keep Yahoo Finance access inside this service.
- Return clean `pd.DataFrame` with date index and ticker columns.
- Use adjusted close prices by calling `yf.download(..., auto_adjust=True)` and reading `Close`.
- Drop rows with missing prices.
- Raise `ValueError` early for empty, missing, short, or non-positive price data.
- Do not calculate returns, portfolio returns, or VaR here.
