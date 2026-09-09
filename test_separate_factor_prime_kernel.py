"""Exact transform/budget guards; no numerical proof of an analytic bound."""
from fractions import Fraction as F
import unittest

from separate_factor_prime_kernel import (
    complete_transform, raw_kl3, separate_factor_budget,
)


class SeparateFactorPrimeKernelTests(unittest.TestCase):
    def test_off_axis_transform_exactly(self):
        for p in (2, 3, 5, 7, 11):
            kl = {t: raw_kl3(p, t) for t in range(1, p)}
            for t in range(1, p):
                for h in range(1, p):
                    for l in range(1, p):
                        self.assertEqual(complete_transform(p, t, h, l),
                                         kl[t*h*l % p])
        self.assertEqual(complete_transform(7, -2, 9, -3),
                         raw_kl3(7, (-2)*9*(-3)))

    def test_axes_and_zero_parameter_are_distinct(self):
        for p in (2, 3, 5, 7, 11, 13):
            def constant(value):
                return (value,)+(0,)*(p-2)
            for t in range(1, p):
                self.assertEqual(complete_transform(p, t, 0, 0), constant(1-p))
                for h in range(1, p):
                    self.assertEqual(complete_transform(p, t, h, 0), constant(1))
                    self.assertEqual(complete_transform(p, t, 0, h), constant(1))
            for h in range(p):
                for l in range(p):
                    expected = (p-1 if h == 0 else -1)*(p-1 if l == 0 else -1)
                    self.assertEqual(complete_transform(p, p, h, l),
                                     constant(expected))

    def test_source_normalization_and_uniform_saving(self):
        for b in (F(1, 5), F(1, 4), F(1, 3), F(2, 5), F(12, 25)):
            budget = separate_factor_budget(b)
            self.assertEqual(budget.dual_product, F(1, 2))
            self.assertEqual(budget.grouped_frequency, b)
            self.assertGreaterEqual(budget.short_variable_saving, F(1, 100))
            self.assertEqual(budget.saving, F(1, 128))
            self.assertEqual(budget.aggregate_exponent, F(127, 128))
            self.assertLessEqual(budget.origin_and_bad_moduli, F(37, 50))
            self.assertEqual(budget.pointwise_exponent, 1)
        for b in (0, F(1, 2)):
            self.assertEqual(separate_factor_budget(b).saving, 0)
        self.assertEqual(separate_factor_budget(F(49, 100)).saving, F(1, 200))

    def test_prime_and_exact_input_boundaries(self):
        for p in (True, 1, 4, 9, 15, 2.0):
            with self.assertRaises(ValueError):
                complete_transform(p, 1, 1, 1)
            with self.assertRaises(ValueError):
                raw_kl3(p, 1)
        for parameter in (0, 7, -14):
            with self.assertRaises(ValueError):
                raw_kl3(7, parameter)
        with self.assertRaises(ValueError):
            complete_transform(7, 1.0, 1, 1)
        for b in (True, 0.2, F(-1, 10), F(13, 25)):
            with self.assertRaises(ValueError):
                separate_factor_budget(b)


if __name__ == "__main__":
    unittest.main()
