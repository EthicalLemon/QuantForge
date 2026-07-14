"""Deterministic Monte Carlo utilities for quantitative research."""

from __future__ import annotations

import numpy as np


def geometric_brownian_motion(
    initial_price: float,
    annual_drift: float,
    annual_volatility: float,
    years: float = 1.0,
    steps_per_year: int = 252,
    paths: int = 1_000,
    seed: int | None = 42,
) -> np.ndarray:
    """Simulate price paths under geometric Brownian motion.

    Returns an array shaped ``(steps + 1, paths)``. The seeded random number
    generator makes experiments reproducible by default.
    """
    if initial_price <= 0:
        raise ValueError("initial_price must be positive")
    if annual_volatility < 0:
        raise ValueError("annual_volatility cannot be negative")
    if years <= 0 or steps_per_year <= 0 or paths <= 0:
        raise ValueError("years, steps_per_year and paths must be positive")

    steps = max(1, int(round(years * steps_per_year)))
    dt = years / steps
    rng = np.random.default_rng(seed)
    shocks = rng.standard_normal((steps, paths))
    increments = (
        (annual_drift - 0.5 * annual_volatility**2) * dt
        + annual_volatility * np.sqrt(dt) * shocks
    )
    log_paths = np.vstack([np.zeros(paths), np.cumsum(increments, axis=0)])
    return initial_price * np.exp(log_paths)
