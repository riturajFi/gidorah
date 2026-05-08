import unittest

import pandas as pd

from services.var import HistoricalVaRService


class HistoricalVaRServiceTest(unittest.TestCase):
    def setUp(self):
        self.service = HistoricalVaRService()
        self.portfolio_value = 1_000_000

    def test_calculate_var_with_negative_var_return(self):
        portfolio_returns = pd.Series([-0.10, -0.05, 0.00, 0.05, 0.10])

        result = self.service.calculate_var(
            portfolio_returns=portfolio_returns,
            portfolio_value=self.portfolio_value,
            confidence_level=0.95,
        )

        expected_var_return = portfolio_returns.quantile(0.05)
        self.assertEqual(result.confidence_level, 0.95)
        self.assertAlmostEqual(result.var_return, expected_var_return)
        self.assertAlmostEqual(
            result.var_dollar,
            -expected_var_return * self.portfolio_value,
        )

    def test_calculate_var_with_positive_var_return(self):
        portfolio_returns = pd.Series([0.01, 0.02, 0.03, 0.04, 0.05])

        result = self.service.calculate_var(
            portfolio_returns=portfolio_returns,
            portfolio_value=self.portfolio_value,
            confidence_level=0.95,
        )

        expected_var_return = portfolio_returns.quantile(0.05)
        self.assertGreater(expected_var_return, 0)
        self.assertEqual(result.confidence_level, 0.95)
        self.assertAlmostEqual(result.var_return, expected_var_return)
        self.assertEqual(result.var_dollar, 0.0)


if __name__ == "__main__":
    unittest.main()
