import numpy as np
import pytest

from quantforge.data import PriceSeries, ReturnSeries, load_price_series_csv


def test_price_series_validates_positive_prices():
    prices = PriceSeries.from_prices([100, 101, 99], name="SPY")

    assert prices.name == "SPY"
    assert prices.values.tolist() == [100, 101, 99]


def test_price_series_rejects_non_positive_prices():
    with pytest.raises(ValueError, match="positive"):
        PriceSeries.from_prices([100, 0, 101])


def test_price_series_requires_two_observations():
    with pytest.raises(ValueError, match="at least two"):
        PriceSeries.from_prices([100])


def test_simple_returns_convert_adjacent_prices():
    prices = PriceSeries.from_prices([100, 110, 99], periods_per_year=12)
    returns = prices.simple_returns()

    assert isinstance(returns, ReturnSeries)
    assert returns.periods_per_year == 12
    assert returns.values.tolist() == pytest.approx([0.10, -0.10])


def test_log_returns_use_continuous_compounding():
    prices = PriceSeries.from_prices([100, 110])

    assert prices.log_returns().tolist() == pytest.approx([np.log(1.1)])


def test_return_series_wealth_index_includes_initial_value():
    returns = ReturnSeries.from_returns([0.10, -0.10])

    assert returns.wealth_index(initial_value=100).tolist() == pytest.approx([100, 110, 99])


def test_return_series_rejects_losses_below_total_loss():
    with pytest.raises(ValueError, match="-100%"):
        ReturnSeries.from_returns([-1.01])


def test_load_price_series_csv_reads_named_close_column(tmp_path):
    csv_path = tmp_path / "spy.csv"
    csv_path.write_text("date,close\n2026-01-01,100\n2026-01-02,101.5\n", encoding="utf-8")

    series = load_price_series_csv(csv_path, name="SPY")

    assert series.name == "SPY"
    assert series.values.tolist() == pytest.approx([100.0, 101.5])


def test_load_price_series_csv_can_drop_missing_rows(tmp_path):
    csv_path = tmp_path / "spy.csv"
    csv_path.write_text("close\n100\n\n101\n", encoding="utf-8")

    series = load_price_series_csv(csv_path, missing="drop")

    assert series.values.tolist() == pytest.approx([100.0, 101.0])


def test_load_price_series_csv_can_forward_fill_missing_rows(tmp_path):
    csv_path = tmp_path / "spy.csv"
    csv_path.write_text("close\n100\n\n101\n", encoding="utf-8")

    series = load_price_series_csv(csv_path, missing="ffill")

    assert series.values.tolist() == pytest.approx([100.0, 100.0, 101.0])


def test_load_price_series_csv_rejects_missing_values_by_default(tmp_path):
    csv_path = tmp_path / "spy.csv"
    csv_path.write_text("close\n100\n\n101\n", encoding="utf-8")

    with pytest.raises(ValueError, match="Missing value"):
        load_price_series_csv(csv_path)


def test_load_price_series_csv_requires_requested_column(tmp_path):
    csv_path = tmp_path / "spy.csv"
    csv_path.write_text("adjusted_close\n100\n101\n", encoding="utf-8")

    with pytest.raises(ValueError, match="close"):
        load_price_series_csv(csv_path)
