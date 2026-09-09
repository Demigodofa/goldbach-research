"""Exact band and integer support checks, without a large prime-count run."""
from fractions import Fraction as F
from math import isqrt
import unittest

from balanced_semiprime_budget import (balanced_kernel_value, band_parameters,
                                       extended_sieve_index_split, sieve_level_certificate)
from rare_factor_pruning import sieve_index_split
from redistribution import trial_prime
from test_character_partner_weight import trial_factors


class BalancedSemiprimeBudgetTests(unittest.TestCase):
    def test_fixed_parameter_margins_and_reciprocal_main_coefficient(self):
        for epsilon in (F(1, 100), F(1, 1000), F(3, 10000), F(1, 100000)):
            kappa, lower, upper, bv, delta_cap = band_parameters(epsilon)
            self.assertEqual(kappa*epsilon, 1)
            self.assertEqual(bv-lower, epsilon)
            self.assertEqual((upper-lower)/2, 2*epsilon)
            self.assertGreaterEqual(lower, F(2, 5))
            self.assertLessEqual(upper, F(3, 5))
            # E/q has exponent at least epsilon-3delta/4, which exceeds
            # the original z^u exponent delta with room for integer floors.
            self.assertEqual(epsilon-3*delta_cap/4, 3*epsilon/4)
            self.assertGreater(epsilon-3*delta_cap/4, delta_cap)
            self.assertGreater((1+8*epsilon)**2, 1+16*epsilon)

    def test_positive_kernel_is_uniformly_bounded_in_the_remaining_band(self):
        for epsilon in (F(1, 100), F(1, 300), F(1, 10000)):
            kappa, lower, upper, _, _ = band_parameters(epsilon)
            self.assertEqual(balanced_kernel_value(epsilon, F(1, 2)), 1)
            for i in range(101):
                a = lower+(upper-lower)*F(i, 100)
                direct = 2*(1-a)-kappa*(1-a)*a*(2*a-1)
                value = balanced_kernel_value(epsilon, a)
                self.assertEqual(value, direct)
                self.assertLessEqual(value, 3)
                if a >= F(1, 2):
                    self.assertLessEqual(value, 1)
            self.assertLess(balanced_kernel_value(epsilon, upper), 0)
            for i in range(101):
                a = upper+(1-upper)*F(i, 100)
                self.assertLessEqual(balanced_kernel_value(epsilon, a), 0)
            # At the lower edge the coefficient stays bounded as kappa grows;
            # a generic (1+kappa)*W upper bound would lose the desired saving.
            self.assertGreater(balanced_kernel_value(epsilon, lower), 1)
            self.assertLess(balanced_kernel_value(epsilon, lower), F(5, 2))

    def test_complete_sieve_support_beyond_square_root_and_budget_injectivity(self):
        saw_beyond = False
        for level, limit, cutoff, ratio in ((1000, 100, 2, 3),
                                            (3000, 60, 5, 2),
                                            (1728, 64, 3, 3)):
            minimum = sieve_level_certificate(level, limit, cutoff, ratio)
            self.assertGreaterEqual(minimum, cutoff**ratio)
            independent = {}
            for q in range(cutoff+1, limit+1):
                if not trial_prime(q):
                    continue
                self.assertGreaterEqual(level//q, minimum)
                for d in range(1, level//q+1):
                    factors = trial_factors(d)
                    if any(p > cutoff or a != 1 for p, a in factors.items()):
                        continue
                    self.assertNotIn(q*d, independent)
                    independent[q*d] = (q, d)
                    saw_beyond |= q > isqrt(level)
            for index in range(1, level+2):
                actual = extended_sieve_index_split(index, cutoff, level, limit)
                self.assertEqual(actual, independent.get(index))
                older = sieve_index_split(index, cutoff, level)
                if actual is not None and actual[0] > isqrt(level):
                    self.assertIsNone(older)
                else:
                    self.assertEqual(actual, older)
        self.assertTrue(saw_beyond)
        self.assertEqual(extended_sieve_index_split(194, 2, 1000, 100), (97, 2))
        self.assertEqual(sieve_level_certificate(1728, 64, 3, 3), 27)
        with self.assertRaises(ValueError):
            sieve_level_certificate(1727, 64, 3, 3)
        # Two large factors and squareful smooth cofactors are not one index.
        self.assertIsNone(extended_sieve_index_split(7*11, 5, 1000, 100))
        self.assertIsNone(extended_sieve_index_split(97*4, 2, 1000, 100))

    def test_strict_domains_and_unsafe_levels(self):
        for epsilon in (True, 0.01, 0, F(0), F(-1, 100), F(1, 99)):
            with self.assertRaises(ValueError):
                band_parameters(epsilon)
        for share in (True, 0.5, 1, F(-1), F(2)):
            with self.assertRaises(ValueError):
                balanced_kernel_value(F(1, 100), share)
        for args in ((True, 100, 2, 3), (1000, 100.0, 2, 3), (100, 100, 2, 1),
                     (1000, 100, 1, 3), (1000, 100, 2, 0), (1000, 1001, 2, 3)):
            with self.assertRaises(ValueError):
                sieve_level_certificate(*args)
        for args in ((True, 2, 100, 10), (0, 2, 100, 10), (1, 1, 100, 10),
                     (1, 2, 100, 101), (1, 2, 100, 2), (1.0, 2, 100, 10)):
            with self.assertRaises(ValueError):
                extended_sieve_index_split(*args)


if __name__ == '__main__':
    unittest.main()
