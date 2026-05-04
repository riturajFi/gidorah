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


@dataclass(frozen=True)
class MonteCarloVaRResult:
    var_95_return: float
    var_95_dollar: float
    var_99_return: float
    var_99_dollar: float
    num_simulations: int
    seed: int


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
        return self.calculate_var_from_covariance(
            cov_matrix,
            weights,
            portfolio_value,
            confidence_level,
        )

    def calculate_var_from_covariance(
        self,
        cov_matrix: pd.DataFrame,
        weights,
        portfolio_value: float,
        confidence_level: float,
    ) -> ParametricVaRResult:
        weights = np.asarray(weights)
        portfolio_variance = weights.T @ cov_matrix @ weights
        portfolio_volatility = np.sqrt(portfolio_variance)
        z_score = norm.ppf(confidence_level)
        var_dollar = z_score * portfolio_volatility * portfolio_value

        return ParametricVaRResult(
            confidence_level=confidence_level,
            portfolio_volatility=portfolio_volatility,
            var_dollar=var_dollar,
        )


class MonteCarloVaRService:
    def calculate_var(
        self,
        returns: pd.DataFrame,
        weights,
        portfolio_value: float = 1_000_000,
        num_simulations: int = 10_000,
        seed: int = 42,
    ) -> MonteCarloVaRResult:
        np.random.seed(seed)

        mean_returns = returns.mean()
        cov_matrix = returns.cov()

        simulated_stock_returns = np.random.multivariate_normal(
            mean=mean_returns,
            cov=cov_matrix,
            size=num_simulations,
        )
        simulated_portfolio_returns = simulated_stock_returns @ weights

        var_95_return = np.quantile(simulated_portfolio_returns, 0.05)
        var_99_return = np.quantile(simulated_portfolio_returns, 0.01)
        var_95_dollar = -var_95_return * portfolio_value
        var_99_dollar = -var_99_return * portfolio_value

        return MonteCarloVaRResult(
            var_95_return=var_95_return,
            var_95_dollar=var_95_dollar,
            var_99_return=var_99_return,
            var_99_dollar=var_99_dollar,
            num_simulations=num_simulations,
            seed=seed,
        )
