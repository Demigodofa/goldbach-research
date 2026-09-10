from fractions import Fraction as F

from core_vaughan_type_i import (CORE, balanced_cutoffs, identity_terms,
                                 term_sum, type_i_obstruction,
                                 type_ii_support_exponent)
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
    assert result["worst_modulus_exponent"] == F(1679, 2000)
    assert result["BV_margin"] == F(-679, 2000)
    assert "simultaneous primality" in result["remaining_problem"]
