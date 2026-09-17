"""Exact algebra, overlap and scope guards; not finite evidence for a rate."""

import unittest
from fractions import Fraction as F
from math import gcd, isqrt, lcm, prod

from complementary_divisor_correlation import central_interval
from cutoff_normalized_remainder import cutoff_log_vectors, singular_multiplier
from major_arc_kernel import _factorization, _mobius_phi
from squarefree_residual_localization import (
    complementary_cutoff_log_vector, excluded_pair_main_blocks,
    square_block_cutoff_vectors, square_block_parameters,
)
from unexceptional_vaughan_gate import _clean, _divisors


def value(vector):
    # Exact rational substitution tests identities only, not logarithmic bounds.
    return sum(p * coefficient for p, coefficient in vector)


def square_divisors(n):
    return [d for d in range(1, isqrt(n) + 1) if n % (d * d) == 0]


class SquarefreeResidualLocalizationTests(unittest.TestCase):
    def test_square_crt_compatibility_and_prime_support(self):
        self.assertIsNone(square_block_parameters(18, 2, 2))
        self.assertEqual(square_block_parameters(50, 2, 3), (36, 6, 2, 6))
        self.assertEqual(square_block_parameters(70, 3, 5), (225, 15, 15, 5))
        for target in (30, 50, 60, 70, 84):
            for d in (1, 2, 3, 5, 6):
                for e in (1, 2, 3, 5, 6):
                    parameters = square_block_parameters(target, d, e)
                    period = lcm(d * d, e * e)
                    residues = [n for n in range(period)
                                if n % (d * d) == 0 and (target - n) % (e * e) == 0]
                    self.assertEqual(len(residues), int(parameters is not None))
                    if parameters:
                        w, excluded, u, v = parameters
                        self.assertEqual(w, period)
                        self.assertEqual(gcd(residues[0], excluded), u)
                        self.assertEqual(gcd(target - residues[0], excluded), v)

    def test_alternating_cutoffs_equal_actual_short_sums(self):
        for target in (30, 50, 60, 84):
            for n in central_interval(target):
                for d in square_divisors(n):
                    for e in square_divisors(target - n):
                        if not _mobius_phi(d)[0] or not _mobius_phi(e)[0]:
                            continue
                        for cutoff in (3, 7, 11):
                            observed = square_block_cutoff_vectors(target, n, cutoff, d, e)
                            self.assertEqual(observed, (cutoff_log_vectors(n, cutoff)[0],
                                                       cutoff_log_vectors(target - n, cutoff)[0]))

    def test_excluded_euler_main_does_not_require_excluded_divides_target(self):
        for target in (15, 30, 50, 64, 70):
            for excluded in (1, 2, 6, 7, 15):
                self.assertEqual(sum(excluded_pair_main_blocks(target, excluded).values(), F(0)),
                                 F(excluded, _mobius_phi(excluded)[1])
                                 * singular_multiplier(target * excluded))
        self.assertNotEqual(30 % 7, 0)

    def test_crt_density_separates_square_period_from_excluded_pair(self):
        target, d, e, s, t = 50, 2, 3, 7, 5
        w, excluded, _, _ = square_block_parameters(target, d, e)
        def coefficients(cutoff):
            return {a: _mobius_phi(a)[0] * (value(_factorization(cutoff))
                    - value(_factorization(a))) for a in range(1, cutoff + 1)
                    if gcd(a, excluded) == 1}
        left, right = coefficients(s), coefficients(t)
        period = lcm(w, *left, *right)
        observed = F(sum(
            sum(c for a, c in left.items() if n % a == 0)
            * sum(c for b, c in right.items() if (target - n) % b == 0)
            for n in range(period) if n % (d * d) == 0 and (target - n) % (e * e) == 0
        ), period)
        expected = sum((F(c * b, w * lcm(a, k)) for a, c in left.items()
                        for k, b in right.items() if target % gcd(a, k) == 0), F(0))
        self.assertEqual(observed, expected)

    def test_every_nontrivial_square_block_main_cancels(self):
        for target in (30, 50, 60, 84):
            for d in (1, 2, 3, 5, 6):
                for e in (1, 2, 3, 5, 6):
                    parameters = square_block_parameters(target, d, e)
                    if parameters:
                        _, _, u, v = parameters
                        coefficient = prod(sum(_mobius_phi(h)[0] for h in _divisors(support))
                                           for support in (u, v))
                        self.assertEqual(coefficient, int(d == e == 1))

    def test_square_pair_multiplicity_has_convergent_euler_factor(self):
        divisors = _divisors(30)
        for power in (0, 2, 3):
            observed = sum((F(len(_divisors(lcm(d, e))) ** power, lcm(d, e) ** 2)
                            for d in divisors for e in divisors), F(0))
            expected = prod(1 + F(3 * 2 ** power, p * p) for p in (2, 3, 5))
            self.assertEqual(observed, expected)

    def test_two_sided_squarefree_projector_keeps_overlap(self):
        for n in range(1, 60):
            for m in (12, 18, 30, 31):
                projected = sum(_mobius_phi(d)[0] * _mobius_phi(e)[0]
                                for d in square_divisors(n) for e in square_divisors(m))
                self.assertEqual(projected, _mobius_phi(n)[0] ** 2 * _mobius_phi(m)[0] ** 2)
        self.assertEqual(1 - _mobius_phi(12)[0] ** 2 * _mobius_phi(18)[0] ** 2, 1)
        self.assertEqual((1 - _mobius_phi(12)[0] ** 2) + (1 - _mobius_phi(18)[0] ** 2), 2)

    def test_exact_signed_bad_union_matches_double_divisor_expansion(self):
        target, cutoff = 60, 7
        products = {n: value(cutoff_log_vectors(n, cutoff)[1])
                    * value(cutoff_log_vectors(target - n, cutoff)[1])
                    for n in central_interval(target)}
        direct = sum(c for n, c in products.items()
                     if not (_mobius_phi(n)[0] and _mobius_phi(target - n)[0]))
        expanded = -sum(c * _mobius_phi(d)[0] * _mobius_phi(e)[0]
                        for n, c in products.items() for d in square_divisors(n)
                        for e in square_divisors(target - n) if (d, e) != (1, 1))
        self.assertEqual(direct, expanded)

    def test_complementary_switch_is_exact_only_on_squarefree_support(self):
        for n in (2, 3, 6, 15, 30, 35, 70, 105):
            for cutoff in (1, 3, 7, 13, n):
                switched = _clean({p: -_mobius_phi(n)[0] * c
                                   for p, c in complementary_cutoff_log_vector(n, cutoff)})
                self.assertEqual(switched, cutoff_log_vectors(n, cutoff)[1])
        self.assertEqual(cutoff_log_vectors(12, 3)[1], ((2, -1),))
        self.assertEqual(_mobius_phi(12)[0], 0)

    def test_complementary_amplitude_need_not_be_positive(self):
        self.assertEqual(complementary_cutoff_log_vector(30, 3), ((2, -1),))
        self.assertEqual(complementary_cutoff_log_vector(15, 3), ((3, 1),))
        # R*k=n gives log(1)=0; strict and weak endpoint forms agree.
        self.assertEqual(complementary_cutoff_log_vector(7, 7), ())

    def test_validation(self):
        for args in ((0, 1, 1), (30, 4, 1), (30, 1, False)):
            with self.assertRaises(ValueError):
                square_block_parameters(*args)
        with self.assertRaises(ValueError):
            square_block_cutoff_vectors(30, 15, 7, 2, 1)
        for args in ((1, 3), (12, 0), (True, 3)):
            with self.assertRaises(ValueError):
                complementary_cutoff_log_vector(*args)


if __name__ == "__main__":
    unittest.main()
