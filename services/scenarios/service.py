from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Mapping

import numpy as np
import pandas as pd

from services.var import ParametricVaRService


@dataclass(frozen=True)
class ScenarioInput:
    returns: pd.DataFrame
    weights: np.ndarray
    portfolio_value: float


@dataclass(frozen=True)
class ScenarioResult:
    name: str
    metrics: dict[str, float]


class Scenario(ABC):
    name: str

    @abstractmethod
    def run(self, scenario_input: ScenarioInput) -> ScenarioResult:
        pass


class WeightedShockScenario(Scenario):
    def __init__(self, name: str, shocks: Mapping[str, float]):
        self.name = name
        self.shocks = shocks

    def run(self, scenario_input: ScenarioInput) -> ScenarioResult:
        shocks = pd.Series(self.shocks)
        missing_tickers = set(scenario_input.returns.columns) - set(shocks.index)
        if missing_tickers:
            raise ValueError(f"Missing shock values for tickers: {missing_tickers}")

        aligned_shocks = shocks.loc[scenario_input.returns.columns].to_numpy()
        portfolio_return = aligned_shocks @ scenario_input.weights
        portfolio_pnl = portfolio_return * scenario_input.portfolio_value
        portfolio_loss = -portfolio_pnl

        return ScenarioResult(
            name=self.name,
            metrics={
                "portfolio_return": portfolio_return,
                "portfolio_pnl_dollar": portfolio_pnl,
                "portfolio_loss_dollar": portfolio_loss,
            },
        )


class EquityShock2008Scenario(WeightedShockScenario):
    def __init__(self):
        super().__init__(
            name="2008-style Equity Shock",
            shocks={
                "AAPL": -0.08,
                "GOOGL": -0.07,
                "MSFT": -0.06,
            },
        )


class TechDrawdownScenario(WeightedShockScenario):
    def __init__(self):
        super().__init__(
            name="Tech Drawdown",
            shocks={
                "AAPL": -0.10,
                "GOOGL": -0.10,
                "MSFT": -0.10,
            },
        )


class CorrelationSpikeScenario(Scenario):
    name = "Correlation Spike Scenario"

    def __init__(
        self,
        parametric_var_service: ParametricVaRService | None = None,
        stressed_corr: float = 0.85,
    ):
        self.parametric_var_service = parametric_var_service or ParametricVaRService()
        self.stressed_corr = stressed_corr

    def run(self, scenario_input: ScenarioInput) -> ScenarioResult:
        spiked_cov_matrix = self._build_spiked_covariance(
            scenario_input.returns,
            self.stressed_corr,
        )
        var_95 = self.parametric_var_service.calculate_var_from_covariance(
            spiked_cov_matrix,
            scenario_input.weights,
            scenario_input.portfolio_value,
            confidence_level=0.95,
        )
        var_99 = self.parametric_var_service.calculate_var_from_covariance(
            spiked_cov_matrix,
            scenario_input.weights,
            scenario_input.portfolio_value,
            confidence_level=0.99,
        )

        return ScenarioResult(
            name=self.name,
            metrics={
                "stressed_corr": self.stressed_corr,
                "portfolio_vol": var_95.portfolio_volatility,
                "var_95_dollar": var_95.var_dollar,
                "var_99_dollar": var_99.var_dollar,
            },
        )

    def _build_spiked_covariance(
        self,
        returns: pd.DataFrame,
        correlation: float,
    ) -> pd.DataFrame:
        volatilities = returns.std()
        correlation_matrix = np.full(
            (len(volatilities), len(volatilities)),
            correlation,
        )
        np.fill_diagonal(correlation_matrix, 1.0)

        covariance_matrix = np.outer(volatilities, volatilities) * correlation_matrix
        return pd.DataFrame(
            covariance_matrix,
            index=returns.columns,
            columns=returns.columns,
        )
