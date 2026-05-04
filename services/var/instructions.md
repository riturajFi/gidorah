# VaR Service Instructions

## Purpose

Calculate VaR using Historical Simulation and Parametric methods.

## Files

- `service.py`: historical and parametric VaR services/results
- `__init__.py`: public exports

## Public API

- `HistoricalVaRResult`: immutable result with `confidence_level`, `var_return`, `var_dollar`
- `HistoricalVaRService.calculate_var(portfolio_returns, portfolio_value, confidence_level)`
- `ParametricVaRResult`: immutable result with `confidence_level`, `portfolio_volatility`, `var_dollar`
- `ParametricVaRService.calculate_var(returns, weights, portfolio_value, confidence_level)`

## Historical VaR Rules

- Historical VaR uses bad-tail percentile.
- For 95% confidence, use `portfolio_returns.quantile(0.05)`.
- For 99% confidence, use `portfolio_returns.quantile(0.01)`.
- General formula: `tail_probability = 1 - confidence_level`.
- Dollar VaR formula: `-var_return * portfolio_value`.

## Parametric VaR Rules

- Parametric VaR assumes daily returns are roughly normally distributed.
- Use `returns.cov()` for covariance matrix.
- Use `weights.T @ cov_matrix @ weights` for portfolio variance.
- Use `np.sqrt(portfolio_variance)` for portfolio daily volatility.
- Use `norm.ppf(confidence_level)` for z-score.
- Dollar VaR formula: `z_score * portfolio_volatility * portfolio_value`.

## Boundaries

- Do not fetch prices here.
- Do not calculate daily returns here.
