# Backtesting Service Instructions

## Purpose

Backtest VaR models against realized portfolio returns.

## Files

- `service.py`: `RollingVaRBreachBacktestService`, `RollingVaRBacktestResult`
- `__init__.py`: public exports

## Public API

- `RollingVaRBreachBacktestService.run(portfolio_returns, confidence_level=0.95, window=250)`
- `RollingVaRBacktestResult`: immutable summary plus `backtest_data`

## Rolling VaR Breach Rules

- Use previous-window returns only: `portfolio_returns.shift(1).rolling(window).quantile(0.05)`.
- For 95% VaR, expected breach rate is `5%`.
- Breach means actual portfolio return is below rolling VaR cutoff.
- Count breaches and compare breach rate to expected rate.

## Boundaries

- Do not fetch prices here.
- Do not calculate portfolio returns here.
- Do not calculate unrelated VaR methods here.
