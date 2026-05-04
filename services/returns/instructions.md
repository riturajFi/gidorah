# Return Calculator Service Instructions

## Purpose

Calculate daily stock returns and daily portfolio returns.

## Files

- `service.py`: `ReturnCalculatorService`
- `__init__.py`: public exports

## Public API

- `calculate_returns(prices)`: returns `prices.pct_change().dropna()`
- `calculate_portfolio_returns(returns, weights)`: returns `returns @ weights`
- `save_returns(returns, path)`: writes stock-wise daily returns CSV
- `save_portfolio_returns(portfolio_returns, path)`: writes one-column portfolio returns CSV
- `load_returns(path)`: reads stock-wise returns CSV
- `load_portfolio_returns(path)`: reads `portfolio_return` series

## Rules

- Keep formulas direct and visible.
- Daily return formula is `today_price / yesterday_price - 1`.
- Use pandas `pct_change().dropna()` for stock-wise returns.
- Use matrix multiplication `returns @ weights` for portfolio returns.
- Do not fetch market data here.
- Do not calculate VaR here.
