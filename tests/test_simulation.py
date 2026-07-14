import numpy as np
import pytest

from quantforge.simulation import geometric_brownian_motion


def test_gbm_shape_and_starting_price():
    paths = geometric_brownian_motion(100, 0.08, 0.2, years=1, steps_per_year=12, paths=25)
    assert paths.shape == (13, 25)
    assert np.all(paths[0] == 100)


def test_gbm_is_reproducible_with_seed():
    first = geometric_brownian_motion(100, 0.08, 0.2, paths=5, seed=7)
    second = geometric_brownian_motion(100, 0.08, 0.2, paths=5, seed=7)
    assert np.array_equal(first, second)


def test_gbm_rejects_invalid_price():
    with pytest.raises(ValueError):
        geometric_brownian_motion(0, 0.08, 0.2)
