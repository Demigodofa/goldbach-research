"""Exact guards for the restricted actual convolution; no new prime scan."""
from fractions import Fraction as F
from math import gcd, lcm
import unittest

from free_divisor_correlation import (
    free_correlation_budget, free_residue, free_solutions, product_log_vector, zero_density,
)
from major_arc_kernel import _factorization
from unexceptional_vaughan_gate import _divisors, vaughan_log_vectors


def sum_vectors(vectors):
    result = {}
    for vector in vectors:
        for prime, coefficient in vector:
            result[prime] = result.get(prime, 0)+coefficient
    return tuple((p, c) for p, c in sorted(result.items()) if c)


class FreeDivisorCorrelationTests(unittest.TestCase):
    def test_product_regrouping_preserves_free_factor_and_signed_coefficients(self):
        # New grouping is checked against the saved exact Type II term.
        for n in (1, 4, 12, 25, 30, 60, 81, 105):
            for u, v in ((1, 1), (2, 3), (5, 2)):
                total = sum_vectors(product_log_vector(r, u, v) for r in _divisors(n))
                self.assertEqual(total, vaughan_log_vectors(n, u, v)[3])
        self.assertEqual(product_log_vector(25, 2, 2), ((5, -1),))
        self.assertEqual(product_log_vector(30, 2, 2), ((3, 1), (5, 1)))
        self.assertEqual(sum_vectors(product_log_vector(r, 2, 2) for r in _divisors(30)), ())

    def test_grouped_coefficients_have_the_log_bound_and_small_support(self):
        for n in (12, 16, 25, 30, 60, 81, 105, 210):
            vector = dict(product_log_vector(n, 2, 3))
            full_log = dict(_factorization(n))
            self.assertTrue(all(abs(c) <= full_log[p] for p, c in vector.items()))
        for n in range(1, 26):
            self.assertEqual(product_log_vector(n, 5, 5), ())

    def test_reduced_progression_matches_direct_positive_solutions(self):
        for first, second, target in ((7, 11, 100), (6, 10, 100), (6, 10, 99),
                                       (5, 5, 40), (4, 12, 100), (12, 4, 100)):
            direct = tuple((k, l) for k in range(1, target//first+1)
                           for l in range(1, target//second+1) if first*k+second*l == target)
            self.assertEqual(free_solutions(first, second, target), direct)
        self.assertEqual(free_residue(6, 10, 100), (2, 5, 0))
        self.assertIsNone(free_residue(6, 10, 99))

    def test_poisson_phase_uses_the_reduced_target_and_positive_residue(self):
        # Finite phase identity, including negative frequencies and nontrivial gcd.
        for first, second, target in ((6, 10, 98), (7, 11, 100), (12, 4, 100)):
            g, v, residue = free_residue(first, second, target)
            self.assertEqual((first//g*residue-target//g) % v, 0)
            for k, _ in free_solutions(first, second, target):
                for h in (-3, -1, 1, 2):
                    self.assertEqual(F(h*k, v) % 1, F(h*residue, v) % 1)
        # Dividing only the modulus but not the target would give the wrong phase.
        self.assertEqual(free_residue(6, 10, 98)[2], 3)
        self.assertNotEqual((98*pow(3, -1, 5)) % 5, 3)

    def test_zero_mode_keeps_shared_factors_and_parity(self):
        for first, second, target in ((7, 11, 100), (6, 10, 98), (6, 10, 99), (5, 5, 40)):
            period = lcm(first, second)
            count = sum(n % first == 0 and (target-n) % second == 0 for n in range(period))
            self.assertEqual(zero_density(first, second, target), F(count, period))
        self.assertEqual(zero_density(6, 10, 98), F(1, 30))
        self.assertEqual(zero_density(6, 10, 99), 0)
        self.assertNotEqual(zero_density(6, 10, 98), F(1, 60))

    def test_both_source_terms_pass_with_all_gcd_costs(self):
        corner = free_correlation_budget(F(51, 100), F(51, 100))
        self.assertEqual((corner.first, corner.second), (F(1983, 2000), F(153, 160)))
        center = free_correlation_budget(F(1, 2), F(1, 2))
        self.assertEqual((center.first, center.second), (F(39, 40), F(15, 16)))
        for r, s, d in ((F(51, 100), F(51, 100), F(1, 100)),
                         (F(1, 2), F(51, 100), F(1, 100)),
                         (F(49, 100), F(51, 100), F(0))):
            budget = free_correlation_budget(r, s, d)
            self.assertEqual(budget.first, F(3, 20)+F(7, 10)*(r+s)+max(r, s)/4-F(9, 5)*d)
            self.assertEqual(budget.second, F(7, 8)*(r+s)+max(r, s)/8-F(15, 8)*d)
            self.assertLessEqual(max(budget.first, budget.second), corner.first)

    def test_range_boundary_does_not_erase_the_old_failed_geometry(self):
        edge = F(1, 2)+F(1, 66)
        self.assertEqual(free_correlation_budget(edge, edge).first, 1)
        old = free_correlation_budget(F(3, 5), F(1, 2))
        self.assertEqual((old.first, old.second), (F(107, 100), F(83, 80)))
        # A genuine k=1 term with a,d>W and nonzero mu(a)Lambda(d).
        self.assertEqual(product_log_vector(77, 3, 3), ((7, -1), (11, -1)))
        self.assertIn((1, 1), free_solutions(77, 83, 160))
        self.assertEqual(gcd(77, 83), 1)

    def test_invalid_inputs_and_negative_frequency_are_separate_cases(self):
        for args in ((0, 5, 40), (5, True, 40), (5, 5, -40)):
            with self.assertRaises(ValueError):
                free_residue(*args)
        for args in ((F(2, 5), F(1, 2)), (0.51, F(1, 2)),
                     (F(1, 2), F(1, 2), F(3, 5))):
            with self.assertRaises(ValueError):
                free_correlation_budget(*args)


if __name__ == '__main__':
    unittest.main()
