from dataclasses import dataclass

import numpy as np
import pandas as pd

from services.var import ParametricVaRResult, ParametricVaRService


@dataclass(frozen=True)
class CorrelationSpikeScenarioResult:
    correlation: float
    var_95: ParametricVaRResult
    var_99: ParametricVaRResult


class CorrelationSpikeScenarioService:
    def __init__(self, parametric_var_service: ParametricVaRService | None = None):
        self.parametric_var_service = parametric_var_service or ParametricVaRService()

    def run(
        self,
        returns: pd.DataFrame,
        weights,
        portfolio_value: float,
        correlation: float = 0.85,
    ) -> CorrelationSpikeScenarioResult:
        spiked_cov_matrix = self._build_spiked_covariance(returns, correlation)

        return CorrelationSpikeScenarioResult(
            correlation=correlation,
            var_95=self.parametric_var_service.calculate_var_from_covariance(
                spiked_cov_matrix,
                weights,
                portfolio_value,
                confidence_level=0.95,
            ),
            var_99=self.parametric_var_service.calculate_var_from_covariance(
                spiked_cov_matrix,
                weights,
                portfolio_value,
                confidence_level=0.99,
            ),
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
