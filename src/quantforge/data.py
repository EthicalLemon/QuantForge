"""Validated market-data containers used by analytics and research workflows."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

import numpy as np


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
