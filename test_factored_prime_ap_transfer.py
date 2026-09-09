"""Exact source-domain, arithmetic regrouping and support-obstruction guards."""
from fractions import Fraction as F
import unittest

from factored_prime_ap_transfer import (
    balanced_factorizations, canonical_cofactor_split, canonical_factorization, selected_log_vector,
    selected_modulus_coefficients, source_exponent_margins, transfer_geometry,
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


if __name__ == '__main__':
    unittest.main()
