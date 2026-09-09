"""Exact new CRT and decoration-cost checks; no rerun of old kernel tests."""
from fractions import Fraction as F
import unittest

from decorated_prime_kernel import (
    periodic_transform_histogram, crt_transform_histogram, decoration_budget,
)


class DecoratedPrimeKernelTests(unittest.TestCase):
    def test_crt_with_joint_periodic_weights_and_zero_modes(self):
        for p, s, j in ((3, 1, 1), (5, 2, 1), (5, 1, 3),
                        (7, 2, 2), (5, 4, 2), (7, 3, 3), (5, 2, 4)):
            weight = tuple(tuple((-1)**(x*y+x+2*y) for y in range(j))
                           for x in range(j))
            for parameter in (0, 1, p, -2):
                for h, l in ((0, 0), (1, 0), (0, -1), (2, 3), (p, 2*p)):
                    self.assertEqual(
                        periodic_transform_histogram(p, s, j, parameter, h, l, weight),
                        crt_transform_histogram(p, s, j, parameter, h, l, weight))

    def test_nonunits_of_period_are_not_discarded(self):
        p, s, j = 5, 1, 3
        weight = ((1, 0, 0), (0, 0, 0), (0, 0, 0))
        direct = periodic_transform_histogram(p, s, j, 0, 0, 0, weight)
        self.assertEqual(direct[0], (p-1)**2)
        self.assertEqual(sum(direct), (p-1)**2)
        self.assertEqual(direct, crt_transform_histogram(p, s, j, 0, 0, 0, weight))

    def test_prime_argument_and_small_factor_can_share_period(self):
        for p, s, j in ((5, 2, 2), (7, 3, 3), (11, 4, 6)):
            for parameter, h, l in ((1, 2, 3), (-2, -3, 1)):
                factorized = (parameter*pow(s, -1, p)
                              * h*pow(s*j, -1, p)*l*pow(s*j, -1, p)) % p
                self.assertEqual(factorized,
                                 parameter*h*l*pow(s**3*j**2, -1, p) % p)

    def test_budget_includes_modulus_and_frequency_inflation(self):
        cap = F(1, 4096)
        for b in (F(1, 5), F(1, 3), F(12, 25)):
            plain = decoration_budget(b)
            self.assertEqual(plain.conservative_exponent, F(127, 128))
            budget = decoration_budget(b, cap, cap, cap)
            self.assertEqual(budget.conservative_exponent, F(4073, 4096))
            self.assertEqual(budget.remaining_triangle_margin, F(23, 4096))
            self.assertLess(budget.dual_cofactor, F(1, 2))
            self.assertLess(budget.grouped_frequency, F(1, 2))
            self.assertTrue(F(1, 8) < budget.source_product < F(5, 8))
            self.assertGreaterEqual(budget.short_saving, F(1, 100))
            self.assertGreaterEqual(budget.bulk_saving, F(1, 128))
            self.assertLess(budget.origin_and_bad_primes, F(3, 4))
            self.assertLess(budget.single_axes, F(3, 4))
        self.assertEqual(decoration_budget(F(1, 3), cap).conservative_exponent
                         - decoration_budget(F(1, 3)).conservative_exponent, 4*cap)

    def test_exact_domains_and_crt_coprimality(self):
        for p, s, j in ((4, 1, 1), (5, 5, 1), (5, 1, 5), (True, 1, 1), (5, 0, 1)):
            with self.assertRaises(ValueError):
                crt_transform_histogram(p, s, j, 1, 1, 1, ((1,),))
        with self.assertRaises(ValueError):
            periodic_transform_histogram(5, 1, 1, 1.0, 1, 1, ((1,),))
        with self.assertRaises(ValueError):
            crt_transform_histogram(5, 1, 2, 1, 1, 1, ((1,),))
        for args in ((0.2,), (True,), (F(1, 2),), (F(1, 3), F(1, 4000))):
            with self.assertRaises(ValueError):
                decoration_budget(*args)


if __name__ == "__main__":
    unittest.main()
