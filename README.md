# Portfolio VaR Engine

Lean Python project for portfolio risk using daily stock prices.

## Notebook-First Run

```bash
python -m venv .venv
.venv/bin/pip install -r requirements.txt
```

Open and run:

```text
portfolio_var_analysis.ipynb
```

Use **Run All** to execute the full workflow cell by cell with tables and charts.

## CLI Check

`main.py` mirrors the notebook pipeline for quick verification:

```bash
.venv/bin/python main.py
```

## Flow

1. Fetch adjusted close prices from Yahoo Finance.
2. Calculate stock-wise daily returns.
3. Calculate weighted portfolio daily returns.
4. Calculate Historical VaR.
5. Calculate Parametric VaR.
6. Calculate Monte Carlo VaR.
7. Run stress scenarios.
8. Run rolling VaR breach backtest.
9. Explore outputs in notebook tables and charts.

## Structure

- `portfolio_var_analysis.ipynb`: primary exploratory workflow with tables and charts.
- `main.py`: CLI mirror of the notebook pipeline.
- `services/data_fetch/`: price data service.
- `services/returns/`: daily return and portfolio return service.
- `services/var/`: Historical, Parametric, and Monte Carlo VaR services.
- `services/scenarios/`: scenario interface and stress scenario implementations.
- `services/backtesting/`: rolling VaR breach backtest service.
- `codex.md`: design and navigation instructions for future agents.

Generated CSV files are ignored by git:

- `prices.csv`
- `returns.csv`
- `portfolio_returns.csv`
