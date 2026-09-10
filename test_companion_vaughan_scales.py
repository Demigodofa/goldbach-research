from fractions import Fraction as F

from companion_vaughan_scales import (BALANCED, CORE,
                                      balanced_companion_diagnostic,
                                      companion_range,
                                      linear_combined_range,
                                      type_ii_companion_range)


def test_reflection_forces_long_companion():
    assert companion_range() == F(59, 100)


def test_linear_term_becomes_a_triple_convolution_scale():
    r = linear_combined_range()
    assert r["min"] == F(41, 100)
    assert r["max"] == F(1319, 2000)
    assert r["free_factor_min"] == F(681, 2000)
    assert r["free_factor_max"] == F(59, 100)
    assert r["product_x_free"] == F(1)


def test_balanced_companion_type_ii_is_nonempty_but_short_factor_remains():
    r = type_ii_companion_range()
    assert r["nonempty"]
    assert r["a_min"] == r["b_min"] == BALANCED
    assert r["n_times_a_min"] == r["n_times_b_min"] == F(1319, 2000)


def test_diagnostic_does_not_claim_an_estimate():
    assert "no Type-II theorem" in balanced_companion_diagnostic()["scope"]
