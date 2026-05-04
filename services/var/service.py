from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class HistoricalVaRResult:
    confidence_level: float
    var_return: float
    var_dollar: float


class HistoricalVaRService:
    def calculate_var(
        self,
        portfolio_returns: pd.Series,
        portfolio_value: float,
        confidence_level: float,
    ) -> HistoricalVaRResult:
        tail_probability = 1 - confidence_level
        var_return = portfolio_returns.quantile(tail_probability)
        var_dollar = -var_return * portfolio_value

        return HistoricalVaRResult(
            confidence_level=confidence_level,
            var_return=var_return,
            var_dollar=var_dollar,
        )
