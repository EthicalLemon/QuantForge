import numpy as np
import pytest

from quantforge.metrics import (
    annualized_return,
    annualized_volatility,
    historical_cvar,
    historical_var,
    max_drawdown,
    sharpe_ratio,
    sortino_ratio,
)


def test_constant_positive_returns_compound_correctly():
    returns = np.full(12, 0.01)
    assert annualized_return(returns, periods_per_year=12) == pytest.approx(0.01 * 0 + 1.01**12 - 1)


def test_annualized_volatility_is_zero_for_constant_series():
    assert annualized_volatility([0.01, 0.01, 0.01]) == pytest.approx(0.0)


def test_max_drawdown_tracks_peak_to_trough_loss():
    assert max_drawdown([0.10, -0.20, 0.05]) == pytest.approx(-0.20)


def test_var_and_cvar_are_positive_loss_numbers():
    returns = [-0.10, -0.05, 0.00, 0.02, 0.04]
    var = historical_var(returns, confidence=0.80)
    cvar = historical_cvar(returns, confidence=0.80)
    assert var >= 0
    assert cvar >= var


def test_ratios_are_finite():
    returns = [0.01, -0.005, 0.012, -0.002, 0.006]
    assert np.isfinite(sharpe_ratio(returns, periods_per_year=252))
    assert np.isfinite(sortino_ratio(returns, periods_per_year=252))


def test_empty_returns_are_rejected():
    with pytest.raises(ValueError):
        annualized_return([])
