# Scenario Service Instructions

## Purpose

Run stress scenarios against existing return data.

## Files

- `service.py`: scenario interface, inputs/results, scenario implementations
- `__init__.py`: public exports

## Public API

- `Scenario`: abstract interface every scenario implements
- `ScenarioInput`: immutable input with `returns`, `weights`, `portfolio_value`
- `ScenarioResult`: immutable output with `name`, `metrics`
- `WeightedShockScenario`: reusable base for direct return shocks
- `EquityShock2008Scenario`: AAPL -8%, GOOGL -7%, MSFT -6%
- `TechDrawdownScenario`: all tickers -10%
- `CorrelationSpikeScenario`: forces correlations to `0.85` and recomputes Parametric VaR

## Add New Scenario

1. Add new class in `service.py`.
2. Inherit from `Scenario`.
3. Implement `run(self, scenario_input: ScenarioInput) -> ScenarioResult`.
4. Return metrics as `dict[str, float]`.
5. Export class from `__init__.py`.
6. Add instance to `scenarios` list in `main.py`.

## Shock Scenario Rules

- Use `WeightedShockScenario` when scenario is direct per-ticker same-day shock.
- Shocks are decimal returns, e.g. `-0.10` means `-10%`.
- Align shocks to `scenario_input.returns.columns`.
- Portfolio return formula: `aligned_shocks @ weights`.
- Portfolio P&L formula: `portfolio_return * portfolio_value`.
- Portfolio loss formula: `-portfolio_pnl`.

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
- Keep all scenario implementations in this folder/file until file becomes too large.
