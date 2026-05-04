# Historical VaR Service Instructions

## Purpose

Calculate Historical Simulation VaR from daily portfolio returns.

## Files

- `service.py`: `HistoricalVaRService`, `HistoricalVaRResult`
- `__init__.py`: public exports

## Public API

- `HistoricalVaRResult`: immutable result with `confidence_level`, `var_return`, `var_dollar`
- `HistoricalVaRService.calculate_var(portfolio_returns, portfolio_value, confidence_level)`

## Rules

- Historical VaR uses bad-tail percentile.
- For 95% confidence, use `portfolio_returns.quantile(0.05)`.
- For 99% confidence, use `portfolio_returns.quantile(0.01)`.
- General formula: `tail_probability = 1 - confidence_level`.
- Dollar VaR formula: `-var_return * portfolio_value`.
- Do not fetch prices here.
- Do not calculate daily returns here.
