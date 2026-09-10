from fractions import Fraction as F

from core_vaughan_type_i import (CORE, balanced_cutoffs, identity_terms,
                                 term_sum, type_i_obstruction,
                                 type_ii_support_exponent, unbalanced_budget,
                                 no_plain_unbalanced_window)
from unexceptional_vaughan_gate import mangoldt_log_vector


def test_balanced_exact_type_ii_is_outside_core():
    gamma, u, v = balanced_cutoffs()
    assert gamma == F(499, 1000)
    assert u == v == F(499, 2000)
    assert u + v == gamma > CORE
    assert type_ii_support_exponent() > CORE


def test_vaughan_identity_keeps_free_convolution_and_is_exact():
    for n in range(1, 80):
        terms = identity_terms(n, 7, 5)
        assert term_sum(terms) == mangoldt_log_vector(n)


def test_reflected_type_i_modulus_misses_bv_and_leaves_two_primes():
    result = type_i_obstruction()
    assert result["type_ii_vanishes"]
    assert result["top_block_modulus_exponent"] == F(1679, 2000)
    assert result["BV_margin"] == F(-679, 2000)
    assert "hypothetical" in result["scope"]
    assert "simultaneous primality" in result["remaining_problem"]


def test_unbalancing_cannot_satisfy_plain_type_i_and_type_ii_requirements():
    # A deliberately unbalanced candidate creates Type-II support, but its
    # Type-I modulus still misses BV because the companion prime is long.
    budget = unbalanced_budget(F(1, 10), F(1, 10))
    assert budget["type_ii_can_survive"]
    assert not budget["type_i_bv_usable"]
    assert budget["type_i_bv_margin"] == F(-19, 100)
    assert no_plain_unbalanced_window()
