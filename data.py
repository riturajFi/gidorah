from dataclasses import dataclass, field
from typing import Sequence

import pandas as pd
import yfinance as yf


DEFAULT_TICKERS = ("AAPL", "GOOGL", "MSFT")


@dataclass(frozen=True)
class PriceDataRequest:
    tickers: Sequence[str] = field(default_factory=lambda: DEFAULT_TICKERS)
    start_date: str = "2020-01-01"
    end_date: str | None = None


class PriceDataFetchService:
    """
    Fetch, validate, save, and load adjusted close price data.
    """

    def fetch_prices(self, request: PriceDataRequest | None = None) -> pd.DataFrame:
        if request is None:
            request = PriceDataRequest()

        tickers = list(request.tickers)
        raw = yf.download(
            tickers=tickers,
            start=request.start_date,
            end=request.end_date,
            interval="1d",
            auto_adjust=True,
            progress=False,
        )

        if raw.empty:
            raise ValueError("No data fetched. Check tickers/date range/internet.")

        prices = self._extract_close_prices(raw, tickers)
        prices = prices.dropna(how="any")

        if prices.empty:
            raise ValueError("Data became empty after dropping missing prices.")

        self.validate_prices(prices, tickers)
        return prices

    def validate_prices(
        self,
        prices: pd.DataFrame,
        tickers: Sequence[str] = DEFAULT_TICKERS,
    ) -> None:
        missing_cols = set(tickers) - set(prices.columns)
        if missing_cols:
            raise ValueError(f"Missing ticker columns: {missing_cols}")

        if prices.isnull().any().any():
            raise ValueError("Price data contains missing values.")

        if len(prices) < 252:
            raise ValueError("Less than 1 trading year of data. Use longer date range.")

        if (prices <= 0).any().any():
            raise ValueError("Price data contains zero/negative prices.")

    def save_prices(self, prices: pd.DataFrame, path: str = "prices.csv") -> None:
        prices.to_csv(path)

    def load_prices(self, path: str = "prices.csv") -> pd.DataFrame:
        return pd.read_csv(path, index_col=0, parse_dates=True)

    def _extract_close_prices(
        self,
        raw: pd.DataFrame,
        tickers: Sequence[str],
    ) -> pd.DataFrame:
        if isinstance(raw.columns, pd.MultiIndex):
            return raw["Close"].copy()

        prices = raw[["Close"]].copy()
        prices.columns = list(tickers)
        return prices


def fetch_price_data(
    tickers=None,
    start_date="2020-01-01",
    end_date=None,
) -> pd.DataFrame:
    request = PriceDataRequest(
        tickers=DEFAULT_TICKERS if tickers is None else tickers,
        start_date=start_date,
        end_date=end_date,
    )
    return PriceDataFetchService().fetch_prices(request)


def validate_price_data(prices: pd.DataFrame, tickers=None) -> None:
    PriceDataFetchService().validate_prices(
        prices,
        DEFAULT_TICKERS if tickers is None else tickers,
    )


def save_prices(prices: pd.DataFrame, path="prices.csv") -> None:
    PriceDataFetchService().save_prices(prices, path)


def load_prices(path="prices.csv") -> pd.DataFrame:
    return PriceDataFetchService().load_prices(path)
