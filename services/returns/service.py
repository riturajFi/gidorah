import pandas as pd


class ReturnCalculatorService:
    def calculate_returns(self, prices: pd.DataFrame) -> pd.DataFrame:
        return prices.pct_change().dropna()

    def calculate_portfolio_returns(
        self,
        returns: pd.DataFrame,
        weights,
    ) -> pd.Series:
        portfolio_returns = returns @ weights
        portfolio_returns.name = "portfolio_return"
        return portfolio_returns

    def save_returns(self, returns: pd.DataFrame, path: str = "returns.csv") -> None:
        returns.to_csv(path)

    def save_portfolio_returns(
        self,
        portfolio_returns: pd.Series,
        path: str = "portfolio_returns.csv",
    ) -> None:
        portfolio_returns.to_csv(path, header=["portfolio_return"])

    def load_returns(self, path: str = "returns.csv") -> pd.DataFrame:
        return pd.read_csv(path, index_col=0, parse_dates=True)

    def load_portfolio_returns(
        self,
        path: str = "portfolio_returns.csv",
    ) -> pd.Series:
        return pd.read_csv(path, index_col=0, parse_dates=True)["portfolio_return"]
