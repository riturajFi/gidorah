# Scenario Service Instructions

## Purpose

Run stress scenarios against existing return data.

## Files

- `service.py`: `CorrelationSpikeScenarioService`, `CorrelationSpikeScenarioResult`
- `__init__.py`: public exports

## Public API

- `CorrelationSpikeScenarioService.run(returns, weights, portfolio_value, correlation=0.85)`
- `CorrelationSpikeScenarioResult`: immutable result with `stressed_corr`, `portfolio_vol`, `var_95_dollar`, `var_99_dollar`

## Correlation Spike Rules

- Keep each stock volatility same.
- Force off-diagonal correlations to scenario value, default `0.85`.
- Keep diagonal correlations at `1.0`.
- Rebuild covariance matrix with `np.outer(volatilities, volatilities) * correlation_matrix`.
- Recompute Parametric VaR from spiked covariance matrix.

## Boundaries

- Do not fetch prices here.
- Do not calculate daily returns here.
- Do not own generic VaR formulas here; reuse VaR service where possible.
