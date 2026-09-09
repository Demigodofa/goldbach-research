"""Finite guards for the polynomial and corrected joint arithmetic bound."""
from fractions import Fraction as F
import unittest

from polynomial_joint_majorant import (
    affine_local_factor, affine_truncated_factor, joint_box_budget,
    mellin_euler_pair, mellin_majorant_constant, physical_cofactor_interval,
    polynomial_cofactor_samples, prime_power_majorant_lower_constant,
    summed_box_log_power,
)


class PolynomialJointMajorantTests(unittest.TestCase):
    def test_polynomial_share_differences_keep_support_and_degree(self):
        self.assertEqual(polynomial_cofactor_samples((), 9), 1)
        self.assertEqual(polynomial_cofactor_samples((F(1, 4),), 9), 1-F(3, 4)**9)
        self.assertEqual(polynomial_cofactor_samples((F(3, 2),), 9), 1)
        self.assertEqual(polynomial_cofactor_samples((F(1, 10),)*4, 3), 0)
        x, y = F(1, 5), F(1, 7)
        self.assertEqual(polynomial_cofactor_samples((x, y), 3), 6*x*y-3*x*x*y-3*x*y*y)
        # Truncation beyond the cutoff is real; no all-n polynomial identity.
        self.assertNotEqual(polynomial_cofactor_samples((F(3, 4), F(3, 4)), 1), 0)

    def test_mellin_finite_euler_product_is_radical_invariant(self):
        values = {2: F(2, 5), 3: F(3, 7)}
        for n in (6, 12, 36, 72):
            left, right = mellin_euler_pair(n, values)
            self.assertEqual(left, right)
            self.assertEqual(right, F(12, 35))
        self.assertEqual(mellin_euler_pair(1, {}), (1, 1))

    def test_kernel_order_and_prime_power_domination_constant(self):
        self.assertGreater(mellin_majorant_constant(9), 0)
        with self.assertRaises(ValueError):
            mellin_majorant_constant(8)
        self.assertEqual(prime_power_majorant_lower_constant(), F(511, 1152))

    def test_physical_interval_is_long_and_both_forms_stay_positive(self):
        for target in (150, 180, 210):
            for p in (7, 11, 17):
                left, right = physical_cofactor_interval(120, target, p)
                self.assertIs(type(left), F)
                self.assertIs(type(right), F)
                self.assertGreaterEqual(right-left, left/3)
                self.assertLessEqual(right-left, left)
                for c in (left, (left+right)/2, right):
                    self.assertTrue(60 <= p*c <= 120)
                    self.assertTrue(60 <= target-p*c <= 120)
        # The enclosure is not an exact (left,right] physical interval.
        for target, accepted in ((150, (False, False)), (180, (False, False)),
                                 (210, (True, True))):
            left, right = physical_cofactor_interval(120, target, 3)
            self.assertEqual(tuple(60 < 3*c <= 120 and 60 < target-3*c <= 120
                                   for c in (left, right)), accepted)

    def test_corrected_affine_root_and_local_divisor_factors(self):
        a, b = F(1, 2), F(3, 4)
        # Leading-prime, common-root, and distinct-root cases.
        for ell, expected in ((7, (1+a/7, 1)), (5, (1+a*b/5, 1)),
                              (11, (1+(a+b)/11, 2)), (2, (1+a*b/2, 1))):
            full, roots = affine_local_factor(ell, 30, 7, a, b)
            self.assertEqual((full, roots), expected)
            self.assertEqual(sum((r*(30-7*r)) % ell == 0 for r in range(ell)), roots)
            previous = F(1)
            for depth in (0, 1, 2):
                truncated = affine_truncated_factor(ell, 30, 7, a, b, depth)
                self.assertLessEqual(previous, truncated)
                self.assertLessEqual(truncated, full)
                previous = truncated
        self.assertEqual(affine_truncated_factor(7, 30, 7, a, b, 2), 1+a*(F(1, 7)-F(1, 7**3)))
        self.assertEqual(affine_truncated_factor(11, 30, 7, a, b, 2), 1+(a+b)*(F(1, 11)-F(1, 11**3)))

    def test_nonprimitive_form_is_not_sent_to_the_joint_theorem(self):
        with self.assertRaises(ValueError):
            affine_local_factor(7, 28, 7, 1, 1)
        with self.assertRaises(ValueError):
            affine_truncated_factor(7, 28, 7, 1, 1, 2)

    def test_uniform_exponent_and_source_class_margins_are_strict(self):
        budget = joint_box_budget(F(49, 100), F(1, 4800), F(3, 10), F(7, 10))
        self.assertTrue(all(value > 0 for value in budget.values()))
        self.assertEqual(budget['polynomial_norm_margin'], F(1, 20))
        self.assertEqual(budget['class_epsilon_margin'], F(1, 3000))
        for c0, c1 in ((F(1, 4), F(1, 2)), (F(1, 2), F(151, 200))):
            with self.assertRaises(ValueError):
                joint_box_budget(F(49, 100), F(1, 4800), c0, c1)

    def test_full_logarithmic_number_of_boxes_consumes_the_saving(self):
        self.assertEqual(summed_box_log_power(F(0)), -1)
        self.assertEqual(summed_box_log_power(F(1, 2)), F(-1, 2))
        self.assertEqual(summed_box_log_power(F(1)), 0)
        with self.assertRaises(ValueError):
            summed_box_log_power(0.5)


if __name__ == '__main__':
    unittest.main()
