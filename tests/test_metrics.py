import numpy as np
import pytest

from quantforge.metrics import (
    correlation_diagnostics,
    correlation_matrix,
    covariance_matrix,
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


def test_covariance_matrix_matches_numpy_sample_covariance():
    returns_by_asset = {
        "SPY": [0.01, 0.02, -0.01, 0.015],
        "TLT": [0.005, -0.002, 0.004, 0.001],
    }

    covariance = covariance_matrix(returns_by_asset)

    expected = np.cov(np.column_stack(list(returns_by_asset.values())), rowvar=False, ddof=1)
    assert covariance == pytest.approx(expected)


def test_annualized_covariance_matrix_scales_by_periods_per_year():
    returns_by_asset = {
        "SPY": [0.01, 0.02, -0.01, 0.015],
        "TLT": [0.005, -0.002, 0.004, 0.001],
    }

    daily_covariance = covariance_matrix(returns_by_asset)
    annualized_covariance = covariance_matrix(returns_by_asset, periods_per_year=252)

    assert annualized_covariance == pytest.approx(daily_covariance * 252)


def test_correlation_matrix_reports_asset_alignment():
    returns_by_asset = {
        "A": [0.01, 0.02, 0.03, 0.04],
        "B": [0.01, 0.02, 0.03, 0.04],
        "C": [-0.01, -0.02, -0.03, -0.04],
    }

    correlation = correlation_matrix(returns_by_asset)

    assert np.diag(correlation) == pytest.approx([1.0, 1.0, 1.0])
    assert correlation[0, 1] == pytest.approx(1.0)
    assert correlation[0, 2] == pytest.approx(-1.0)


def test_correlation_diagnostics_sort_pairs_by_absolute_strength():
    returns_by_asset = {
        "A": [0.01, 0.02, 0.03, 0.04],
        "B": [0.011, 0.019, 0.031, 0.039],
        "C": [-0.01, -0.02, -0.01, -0.03],
    }

    diagnostics = correlation_diagnostics(returns_by_asset)

    assert (diagnostics[0].left, diagnostics[0].right) == ("A", "B")
    assert abs(diagnostics[0].correlation) >= abs(diagnostics[1].correlation)


def test_dependency_metrics_require_aligned_return_lengths():
    returns_by_asset = {
        "SPY": [0.01, 0.02, 0.03],
        "TLT": [0.01, 0.02],
    }

    with pytest.raises(ValueError, match="same number"):
        covariance_matrix(returns_by_asset)
