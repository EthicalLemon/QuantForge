"""Validated market-data containers used by analytics and research workflows."""

from __future__ import annotations

import csv
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

import numpy as np


MissingValuePolicy = Literal["raise", "drop", "ffill"]


def _array(values: Iterable[float], *, label: str) -> np.ndarray:
    result = np.asarray(list(values), dtype=float)
    if result.ndim != 1:
        raise ValueError(f"{label} must be one-dimensional")
    if result.size == 0:
        raise ValueError(f"{label} cannot be empty")
    if not np.isfinite(result).all():
        raise ValueError(f"{label} must contain only finite values")
    result.setflags(write=False)
    return result


def _is_missing(value: str | None) -> bool:
    if value is None:
        return True
    return value.strip().lower() in {"", "na", "nan", "null"}


def load_price_series_csv(
    path: str | Path,
    *,
    price_column: str = "close",
    name: str | None = None,
    periods_per_year: int = 252,
    missing: MissingValuePolicy = "raise",
) -> "PriceSeries":
    """Load a validated price series from a CSV file.

    Missing values can be rejected, dropped, or forward-filled before the
    resulting prices are validated.
    """
    if missing not in {"raise", "drop", "ffill"}:
        raise ValueError("missing must be one of: raise, drop, ffill")

    csv_path = Path(path)
    with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames or price_column not in reader.fieldnames:
            raise ValueError(f"CSV file must contain '{price_column}' column")

        prices: list[float] = []
        last_price: float | None = None
        for row_number, row in enumerate(reader, start=2):
            raw_value = row.get(price_column)
            if _is_missing(raw_value):
                if missing == "raise":
                    raise ValueError(
                        f"Missing value in column '{price_column}' at row {row_number}"
                    )
                if missing == "drop":
                    continue
                if last_price is None:
                    raise ValueError(
                        "Cannot forward-fill the first missing price observation"
                    )
                prices.append(last_price)
                continue

            try:
                price = float(raw_value)
            except (TypeError, ValueError) as exc:
                raise ValueError(
                    f"Invalid numeric value '{raw_value}' in column '{price_column}' "
                    f"at row {row_number}"
                ) from exc

            prices.append(price)
            last_price = price

    return PriceSeries.from_prices(
        prices,
        name=name or csv_path.stem,
        periods_per_year=periods_per_year,
    )


@dataclass(frozen=True)
class ReturnSeries:
    """Validated periodic returns for one asset or strategy."""

    values: np.ndarray
    name: str = "asset"
    periods_per_year: int = 252

    @classmethod
    def from_returns(
        cls,
        returns: Iterable[float],
        *,
        name: str = "asset",
        periods_per_year: int = 252,
    ) -> "ReturnSeries":
        """Create a return series from decimal periodic returns."""
        if periods_per_year <= 0:
            raise ValueError("periods_per_year must be positive")
        values = _array(returns, label="returns")
        if np.any(values < -1.0):
            raise ValueError("returns cannot be below -100%")
        return cls(values=values, name=name, periods_per_year=periods_per_year)

    def wealth_index(self, initial_value: float = 1.0) -> np.ndarray:
        """Return compounded wealth, including the initial value."""
        if initial_value <= 0:
            raise ValueError("initial_value must be positive")
        return initial_value * np.concatenate(([1.0], np.cumprod(1.0 + self.values)))


@dataclass(frozen=True)
class PriceSeries:
    """Validated positive price observations for one asset."""

    values: np.ndarray
    name: str = "asset"
    periods_per_year: int = 252

    @classmethod
    def from_prices(
        cls,
        prices: Iterable[float],
        *,
        name: str = "asset",
        periods_per_year: int = 252,
    ) -> "PriceSeries":
        """Create a price series from positive finite price observations."""
        if periods_per_year <= 0:
            raise ValueError("periods_per_year must be positive")
        values = _array(prices, label="prices")
        if values.size < 2:
            raise ValueError("prices must contain at least two observations")
        if np.any(values <= 0.0):
            raise ValueError("prices must be positive")
        return cls(values=values, name=name, periods_per_year=periods_per_year)

    def simple_returns(self) -> ReturnSeries:
        """Convert prices to decimal simple returns."""
        returns = self.values[1:] / self.values[:-1] - 1.0
        return ReturnSeries.from_returns(
            returns,
            name=self.name,
            periods_per_year=self.periods_per_year,
        )

    def log_returns(self) -> np.ndarray:
        """Return continuously compounded log returns."""
        return np.diff(np.log(self.values))
