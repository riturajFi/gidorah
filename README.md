# Portfolio VaR Engine

Lean Python project for portfolio risk using daily stock prices.

## Run

```bash
python -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python main.py
```

## Flow

1. Fetch adjusted close prices from Yahoo Finance.
2. Calculate stock-wise daily returns.
3. Calculate weighted portfolio daily returns.
4. Calculate Historical VaR.
5. Calculate Parametric VaR.
6. Calculate Monte Carlo VaR.
7. Run correlation spike stress scenario.

## Structure

- `main.py`: orchestrates workflow.
- `services/data_fetch/`: price data service.
- `services/returns/`: daily return and portfolio return service.
- `services/var/`: Historical, Parametric, and Monte Carlo VaR services.
- `services/scenarios/`: stress scenario services.
- `codex.md`: design and navigation instructions for future agents.

Generated CSV files are ignored by git:

- `prices.csv`
- `returns.csv`
- `portfolio_returns.csv`
