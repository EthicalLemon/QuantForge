"""Risk and performance metrics for periodic return series."""

from __future__ import annotations

from collections.abc import Iterable

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
