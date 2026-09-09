"""Exact source-domain, arithmetic regrouping and support-obstruction guards."""
from fractions import Fraction as F
import unittest

from factored_prime_ap_transfer import (
    balanced_factorizations, canonical_cofactor_split, canonical_factorization, selected_log_vector,
    selected_modulus_coefficients, source_exponent_margins, transfer_geometry,
    polynomial_gap_mass_bounds, small_factor_support_obstruction, two_prime_gap_geometry,
    gap_prime_divisor_counts, gap_variance_budget,
)
from major_arc_kernel import _mobius_phi, ramanujan
from ramanujan_type_i import progression_means


class FactoredPrimeAPTransferTests(unittest.TestCase):
    def test_source_inequalities_are_strict_and_exact(self):
        alphas, margins = source_exponent_margins(F(1, 2000), F(1, 40), F(41, 500))
        self.assertEqual(alphas, (F(787, 2000), F(1, 40), F(41, 500)))
        self.assertEqual(margins, (F(1, 200), F(43, 2000), F(1, 1000), F(1, 1000)))
        with self.assertRaises(ValueError):
            source_exponent_margins(F(1, 2000), F(1, 50), F(41, 500))
        with self.assertRaises(ValueError):
            source_exponent_margins(.0005, F(1, 40), F(41, 500))

    def test_endpoint_slack_preserves_a_real_beyond_half_range(self):
        caps, level, errors = transfer_geometry()
        self.assertEqual(caps, (F(1967, 5000), F(249, 10000), F(819, 10000)))
        self.assertEqual(level, F(2501, 5000))
        self.assertTrue(all(type(x) is F and x > 0 for x in errors))
        self.assertGreater(F(5, 24), F(3, 5)/3)
        for gamma in (F(5, 12), F(1, 2)):
            with self.assertRaises(ValueError):
                transfer_geometry(gamma=gamma)
        with self.assertRaises(ValueError):
            transfer_geometry(trim=F(1, 6000))  # exactly half, insufficient

    def test_canonical_split_never_counts_one_divisor_twice(self):
        self.assertEqual(canonical_factorization(6, 3, 3), (2, 3))
        self.assertIsNone(canonical_factorization(7, 3, 3))
        self.assertEqual(canonical_factorization(1, 3, 3), (1, 1))
        weights = (0, 1, -1, F(1, 2), 0, 0, F(1, 3))
        coefficients = selected_modulus_coefficients(11, 3, 3, weights)
        self.assertEqual(coefficients[42], (7, F(-1, 3)))
        self.assertEqual(coefficients[66], (11, F(-1, 3)))
        self.assertEqual(len(coefficients), 8)

    def test_progression_regrouping_keeps_actual_cofactor_signs(self):
        weights = (0, 1, -1, F(1, 2), 0, 0, F(1, 3))
        # n=462=7*11*6: for each p=7,11 the selected d are1,2,3,6.
        expected = -sum((F(1), F(-1), F(1, 2), F(1, 3)))
        self.assertEqual(selected_log_vector(462, 11, 3, 3, weights),
                         ((7, expected), (11, expected)))
        self.assertEqual(selected_log_vector(49, 11, 3, 3, weights), ((7, -1),))
        # Outside the physical support the c=1 compensation is REAL.
        self.assertEqual(selected_log_vector(7, 11, 3, 3, weights), ((7, -1),))

    def test_absorbing_a_cofactor_into_the_large_factor_retains_more_moduli(self):
        self.assertEqual(canonical_cofactor_split(7, 6, 14, 1, 3), (14, 1, 3))
        self.assertIsNone(canonical_cofactor_split(7, 6, 13, 1, 3))
        weights = (0, 1, -1, F(1, 2), 0, 0, F(1, 3))
        coefficients = selected_modulus_coefficients(23, 1, 1, weights)
        self.assertEqual(coefficients[14], (7, 1))
        self.assertEqual(coefficients[21], (7, F(-1, 2)))
        self.assertNotIn(42, coefficients)

    def test_nonreduced_complete_model_mean_is_zero(self):
        # Untruncated divisor means, including nonreduced and repeated moduli.
        for step in (6, 7, 12, 21):
            for target in (30, 32, 35):
                full = sum((F(_mobius_phi(q)[0]*ramanujan(q, target),
                              _mobius_phi(q)[1])
                            for q in range(1, step+1) if step % q == 0), F(0))
                from math import gcd
                expected = F(step, _mobius_phi(step)[1]) if gcd(step, target) == 1 else F(0)
                self.assertEqual(full, expected)
                self.assertEqual(progression_means(target, step, (0,)+(1,)*step)[0], full)

    def test_balanced_support_obstruction_includes_padded_levels(self):
        self.assertEqual(balanced_factorizations(77, 1000), ())  # prime11>10
        self.assertEqual(balanced_factorizations(77, 1330), ())  #11^3−1
        self.assertIn((1, 7, 11), balanced_factorizations(77, 1331))
        self.assertEqual(balanced_factorizations(14, 36, order=2), ())
        self.assertIn((2, 2, 3), balanced_factorizations(12, 27))

    def test_uncovered_prime_rectangle_is_inside_the_new_total_modulus_level(self):
        exponents, margins = two_prime_gap_geometry()
        a0, a1, b0, b1 = exponents
        self.assertEqual(a0+b0, F(5001, 10000))
        self.assertEqual(a1+b1, F(25007, 50000))
        self.assertTrue(all(type(x) is F and x > 0 for x in margins))
        self.assertLess(b1, F(5, 24))
        self.assertGreater(a0, F(1, 4))

    def test_positive_limit_mass_bounds_do_not_assume_a_numerical_onset(self):
        for nu in (F(21, 100), F(49, 200)):
            for degree in (9, 12):
                lower, upper = polynomial_gap_mass_bounds(nu, degree)
                self.assertGreater(lower, 0)
                self.assertLess(lower, upper)
                (a0, a1, b0, b1), _ = two_prime_gap_geometry(nu)
                middle = (b0+b1)/2
                midpoint_mass = (a1-a0)*(b1-b0)*(1-middle/nu)**degree/middle
                self.assertLess(lower, midpoint_mass)
                self.assertLess(midpoint_mass, upper)
        with self.assertRaises(ValueError):
            polynomial_gap_mass_bounds(F(1, 5))

    def test_rough_modulus_support_certificate_checks_all_finite_factor_splits(self):
        # Large-cap padding still cannot split a modulus having no small factors.
        for n, large, first, second in ((77, 50, 3, 5), (121, 100, 2, 7), (143, 100, 3, 5)):
            self.assertTrue(small_factor_support_obstruction(n, large, first, second))
            brute = [(q1, q2, q3) for q1 in range(1, large+1)
                     for q2 in range(1, first+1) for q3 in range(1, second+1)
                     if q1*q2*q3 == n]
            self.assertEqual(brute, [])
        self.assertFalse(small_factor_support_obstruction(77, 77, 3, 5))
        self.assertFalse(small_factor_support_obstruction(14, 10, 2, 3))
        # False is not an existence certificate:14 still has no split below(3,2,3).
        self.assertFalse(small_factor_support_obstruction(14, 3, 2, 3))

    def test_source_parameter_universal_large_factor_ceiling(self):
        for sigma, a2, a3 in ((F(1, 2000), F(1, 40), F(41, 500)),
                               (F(1, 10000), F(1, 50), F(21, 250))):
            (a1, _, _), margins = source_exponent_margins(sigma, a2, a3)
            self.assertEqual(F(2, 5)-a1, 11*sigma+margins[2])
            self.assertGreater(F(1, 20), a2)
            self.assertGreater(F(1, 10), a3)

    def test_intact_variance_target_has_room_for_the_actual_diagonal(self):
        constant, level, target_exponent = gap_variance_budget()
        self.assertGreater(constant, 0)
        self.assertEqual(level+target_exponent, 2)
        self.assertEqual(target_exponent, F(74993, 50000))
        self.assertGreater(target_exponent, 1)

    def test_prime_factor_counts_bound_diagonal_multiplicity_by_three(self):
        counts = gap_prime_divisor_counts()
        self.assertEqual(counts, ((1, 1), (1, 2), (1, 3), (2, 1)))
        self.assertEqual(max(s*t for s, t in counts), 3)
        (a0, _, b0, _), _ = two_prime_gap_geometry()
        self.assertGreater(2*a0+2*b0, 1)


if __name__ == '__main__':
    unittest.main()
