"""QuantForge: compact, reproducible quantitative-finance research tools."""

from .data import PriceSeries, ReturnSeries, load_price_series_csv
from .metrics import (
    CorrelationPair,
    annualized_return,
    annualized_volatility,
    correlation_diagnostics,
    correlation_matrix,
    covariance_matrix,
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
    "load_price_series_csv",
    "CorrelationPair",
    "annualized_return",
    "annualized_volatility",
    "covariance_matrix",
    "correlation_matrix",
    "correlation_diagnostics",
    "historical_var",
    "historical_cvar",
    "max_drawdown",
    "sharpe_ratio",
    "sortino_ratio",
    "geometric_brownian_motion",
]

__version__ = "0.1.0"
