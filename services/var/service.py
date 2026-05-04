from dataclasses import dataclass

import numpy as np
import pandas as pd
from scipy.stats import norm


@dataclass(frozen=True)
class HistoricalVaRResult:
    confidence_level: float
    var_return: float
    var_dollar: float


@dataclass(frozen=True)
class ParametricVaRResult:
    confidence_level: float
    portfolio_volatility: float
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


class ParametricVaRService:
    def calculate_var(
        self,
        returns: pd.DataFrame,
        weights,
        portfolio_value: float,
        confidence_level: float,
    ) -> ParametricVaRResult:
        cov_matrix = returns.cov()
        portfolio_variance = weights.T @ cov_matrix @ weights
        portfolio_volatility = np.sqrt(portfolio_variance)
        z_score = norm.ppf(confidence_level)
        var_dollar = z_score * portfolio_volatility * portfolio_value

        return ParametricVaRResult(
            confidence_level=confidence_level,
            portfolio_volatility=portfolio_volatility,
            var_dollar=var_dollar,
        )
