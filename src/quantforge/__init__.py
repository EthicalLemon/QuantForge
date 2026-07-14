"""QuantForge: compact, reproducible quantitative-finance research tools."""

from .data import PriceSeries, ReturnSeries
from .metrics import (
    annualized_return,
    annualized_volatility,
    historical_var,
    historical_cvar,
    max_drawdown,
    sharpe_ratio,
    sortino_ratio,
)
from .simulation import geometric_brownian_motion

__all__ = [
    "PriceSeries",
    "ReturnSeries",
    "annualized_return",
    "annualized_volatility",
    "historical_var",
    "historical_cvar",
    "max_drawdown",
    "sharpe_ratio",
    "sortino_ratio",
    "geometric_brownian_motion",
]

__version__ = "0.1.0"
