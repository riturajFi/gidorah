from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class RollingVaRBacktestResult:
    confidence_level: float
    window: int
    observations: int
    breach_count: int
    breach_rate: float
    expected_breach_rate: float
    expected_breaches: float
    comment: str
    backtest_data: pd.DataFrame


class RollingVaRBreachBacktestService:
    def run(
        self,
        portfolio_returns: pd.Series,
        confidence_level: float = 0.95,
        window: int = 250,
    ) -> RollingVaRBacktestResult:
        if len(portfolio_returns) <= window:
            raise ValueError("Not enough portfolio returns for rolling VaR backtest.")

        expected_breach_rate = 1 - confidence_level
        rolling_var = (
            portfolio_returns.shift(1)
            .rolling(window=window)
            .quantile(expected_breach_rate)
        )
        backtest_data = pd.DataFrame(
            {
                "portfolio_return": portfolio_returns,
                "rolling_var": rolling_var,
            }
        ).dropna()
        backtest_data["breach"] = (
            backtest_data["portfolio_return"] < backtest_data["rolling_var"]
        )

        observations = len(backtest_data)
        breach_count = int(backtest_data["breach"].sum())
        breach_rate = breach_count / observations
        expected_breaches = observations * expected_breach_rate

        return RollingVaRBacktestResult(
            confidence_level=confidence_level,
            window=window,
            observations=observations,
            breach_count=breach_count,
            breach_rate=breach_rate,
            expected_breach_rate=expected_breach_rate,
            expected_breaches=expected_breaches,
            comment=self._build_comment(breach_rate, expected_breach_rate),
            backtest_data=backtest_data,
        )

    def _build_comment(
        self,
        breach_rate: float,
        expected_breach_rate: float,
    ) -> str:
        if breach_rate > expected_breach_rate * 1.5:
            return "Breach rate is above expected rate; VaR may underestimate tail risk."

        if breach_rate < expected_breach_rate * 0.5:
            return "Breach rate is below expected rate; VaR may be conservative."

        return "Breach rate is close to expected rate."
