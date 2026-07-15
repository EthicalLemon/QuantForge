"""Risk and performance metrics for periodic return series."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

import numpy as np


def _returns(values: Iterable[float]) -> np.ndarray:
    array = np.asarray(list(values), dtype=float)
    if array.ndim != 1:
        raise ValueError("returns must be one-dimensional")
    if array.size == 0:
        raise ValueError("returns cannot be empty")
    if not np.isfinite(array).all():
        raise ValueError("returns must contain only finite values")
    return array


@dataclass(frozen=True)
class CorrelationPair:
    """Pairwise correlation summary for two assets."""

    left: str
    right: str
    correlation: float


def _return_matrix(returns_by_asset: dict[str, Iterable[float]]) -> tuple[list[str], np.ndarray]:
    if len(returns_by_asset) < 2:
        raise ValueError("returns_by_asset must contain at least two assets")

    names = list(returns_by_asset)
    columns = [_returns(returns_by_asset[name]) for name in names]
    length = columns[0].size
    if length < 2:
        raise ValueError("each asset must contain at least two return observations")
    if any(column.size != length for column in columns[1:]):
        raise ValueError("all assets must have the same number of return observations")
    matrix = np.column_stack(columns)
    return names, matrix


def annualized_return(returns: Iterable[float], periods_per_year: int = 252) -> float:
    """Return the compounded annual growth rate implied by periodic returns."""
    r = _returns(returns)
    if periods_per_year <= 0:
        raise ValueError("periods_per_year must be positive")
    growth = float(np.prod(1.0 + r))
    if growth <= 0:
        return -1.0
    return growth ** (periods_per_year / r.size) - 1.0


def annualized_volatility(returns: Iterable[float], periods_per_year: int = 252) -> float:
    """Return sample standard deviation scaled to an annual horizon."""
    r = _returns(returns)
    if periods_per_year <= 0:
        raise ValueError("periods_per_year must be positive")
    if r.size < 2:
        return 0.0
    return float(np.std(r, ddof=1) * np.sqrt(periods_per_year))


def sharpe_ratio(
    returns: Iterable[float],
    risk_free_rate: float = 0.0,
    periods_per_year: int = 252,
) -> float:
    """Return annualized Sharpe ratio using a yearly risk-free rate."""
    r = _returns(returns)
    volatility = annualized_volatility(r, periods_per_year)
    if volatility == 0:
        return 0.0
    excess = annualized_return(r, periods_per_year) - risk_free_rate
    return float(excess / volatility)


def sortino_ratio(
    returns: Iterable[float],
    target_return: float = 0.0,
    periods_per_year: int = 252,
) -> float:
    """Return annualized Sortino ratio relative to an annual target return."""
    r = _returns(returns)
    periodic_target = (1.0 + target_return) ** (1.0 / periods_per_year) - 1.0
    downside = np.minimum(r - periodic_target, 0.0)
    downside_deviation = float(np.sqrt(np.mean(downside**2)) * np.sqrt(periods_per_year))
    if downside_deviation == 0:
        return 0.0
    return float((annualized_return(r, periods_per_year) - target_return) / downside_deviation)


def max_drawdown(returns: Iterable[float]) -> float:
    """Return maximum peak-to-trough loss as a negative decimal."""
    r = _returns(returns)
    wealth = np.cumprod(1.0 + r)
    peaks = np.maximum.accumulate(np.concatenate(([1.0], wealth)))
    drawdowns = np.concatenate(([1.0], wealth)) / peaks - 1.0
    return float(np.min(drawdowns))


def historical_var(returns: Iterable[float], confidence: float = 0.95) -> float:
    """Return positive historical Value at Risk at the requested confidence."""
    r = _returns(returns)
    if not 0.0 < confidence < 1.0:
        raise ValueError("confidence must be between 0 and 1")
    return float(max(0.0, -np.quantile(r, 1.0 - confidence)))


def historical_cvar(returns: Iterable[float], confidence: float = 0.95) -> float:
    """Return positive historical Conditional Value at Risk (expected shortfall)."""
    r = _returns(returns)
    var = historical_var(r, confidence)
    tail = r[r <= -var]
    if tail.size == 0:
        return var
    return float(max(0.0, -np.mean(tail)))


def covariance_matrix(
    returns_by_asset: dict[str, Iterable[float]],
    *,
    periods_per_year: int | None = None,
) -> np.ndarray:
    """Return the sample covariance matrix for aligned asset returns."""
    _, matrix = _return_matrix(returns_by_asset)
    covariance = np.cov(matrix, rowvar=False, ddof=1)
    if periods_per_year is None:
        return covariance
    if periods_per_year <= 0:
        raise ValueError("periods_per_year must be positive")
    return covariance * periods_per_year


def correlation_matrix(returns_by_asset: dict[str, Iterable[float]]) -> np.ndarray:
    """Return the correlation matrix for aligned asset returns."""
    _, matrix = _return_matrix(returns_by_asset)
    return np.corrcoef(matrix, rowvar=False)


def correlation_diagnostics(returns_by_asset: dict[str, Iterable[float]]) -> list[CorrelationPair]:
    """Return pairwise correlations sorted by absolute strength."""
    names, _ = _return_matrix(returns_by_asset)
    correlations = correlation_matrix(returns_by_asset)
    pairs: list[CorrelationPair] = []
    for left_index, left_name in enumerate(names[:-1]):
        for right_index in range(left_index + 1, len(names)):
            pairs.append(
                CorrelationPair(
                    left=left_name,
                    right=names[right_index],
                    correlation=float(correlations[left_index, right_index]),
                )
            )
    return sorted(pairs, key=lambda pair: abs(pair.correlation), reverse=True)
