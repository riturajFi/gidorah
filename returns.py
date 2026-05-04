import pandas as pd


class ReturnCalculatorService:
    def calculate_returns(self, prices: pd.DataFrame) -> pd.DataFrame:
        return prices.pct_change().dropna()

    def save_returns(self, returns: pd.DataFrame, path: str = "returns.csv") -> None:
        returns.to_csv(path)

    def load_returns(self, path: str = "returns.csv") -> pd.DataFrame:
        return pd.read_csv(path, index_col=0, parse_dates=True)
