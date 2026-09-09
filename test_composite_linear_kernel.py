"""New exact composite identities and evidence of the surviving budget gap."""
from fractions import Fraction as F
from itertools import product
from math import gcd
import unittest

from composite_linear_kernel import (
    periodic_linear_transform, periodic_kloosterman_prediction,
    restricted_axis_exact, restricted_axis_prediction, axis_triangle_budget,
    composite_linear_budget,
)
from major_arc_kernel import ramanujan


def tau(n):
    return sum(n % d == 0 for d in range(1, n+1))


class CompositeLinearKernelTests(unittest.TestCase):
    def test_general_periodic_transform_with_prime_powers_and_nonunits(self):
        for q, period in ((4, 1), (4, 2), (8, 4), (9, 3), (12, 4), (15, 6)):
            weight = tuple(tuple((a*a+a*b+2*b) % 3-1 for b in range(period))
                           for a in range(period))
            for parameter, h, dual in ((0, 0, 1), (1, 2, 1),
                                        (q//2, -2, -1), (q, q, q)):
                self.assertEqual(
                    periodic_linear_transform(q, period, parameter, h, dual, weight),
                    periodic_kloosterman_prediction(q, period, parameter, h, dual, weight))

    def test_period_nonunits_and_incompatible_lift_congruence(self):
        # M=2 mod4 is allowed when q=5. A unit restriction modJ would erase it.
        weight = tuple(tuple(int(a == 2) for b in range(4)) for a in range(4))
        direct = periodic_linear_transform(5, 4, 0, 0, 1, weight)
        prediction = periodic_kloosterman_prediction(5, 4, 0, 0, 1, weight)
        self.assertEqual(direct, prediction)
        self.assertEqual(direct[0], 4)
        self.assertTrue(all(v == 0 for v in direct[1:]))
        weight = ((1, -1), (0, 1))
        # gcd(q,J)=2 does not divide h=1: there are no terms in (4).
        result = periodic_linear_transform(8, 2, 3, 1, 1, weight)
        self.assertTrue(all(v == 0 for v in result))
        self.assertEqual(result, periodic_kloosterman_prediction(8, 2, 3, 1, 1, weight))

    def test_restricted_ramanujan_identity_and_zero_parameter(self):
        for q in (4, 8, 9, 12, 15, 18, 24, 30):
            for divisor in range(1, q+1):
                if q % divisor:
                    continue
                weights = tuple((r*r+r) % 3-1 for r in range(divisor))
                for parameter in (0, 1, -2, q//2, q):
                    self.assertEqual(
                        restricted_axis_exact(q, divisor, parameter, weights),
                        restricted_axis_prediction(q, divisor, parameter, weights))
                    self.assertLessEqual(axis_triangle_budget(q, divisor, parameter),
                                         divisor*tau(q)*gcd(q, parameter))
            for parameter in (0, 1, -2, q):
                result = restricted_axis_exact(q, 1, parameter, (1,))
                self.assertEqual(result[0], ramanujan(q, parameter))
                self.assertTrue(all(v == 0 for v in result[1:]))

    def test_modulus_gcd_average_including_divisors_above_interval(self):
        for length, n in product((2, 3, 7, 12, 20), (1, 8, 12, 49, 60, 121)):
            measured = sum(gcd(q, n) for q in range(length, 2*length+1))
            self.assertLessEqual(measured, 2*length*tau(n))

    def test_power_saving_region_and_balanced_failure_are_distinct(self):
        cap = F(1, 4096)
        for b, x in ((F(2, 5), F(31, 128)), (F(31, 128), F(3, 10))):
            budget = composite_linear_budget(b, x, F(1, 2), cap, cap)
            self.assertTrue(budget.active)
            self.assertTrue(budget.covered_by_fixed_margin)
            self.assertEqual(budget.total_exponent, F(4067, 4096))
            self.assertEqual(budget.saving, F(29, 4096))
        balanced = composite_linear_budget(F(1, 3), F(1, 3), F(1, 2))
        self.assertTrue(balanced.active)
        self.assertFalse(balanced.covered_by_fixed_margin)
        self.assertEqual(balanced.frequency_exponent, F(1, 6))
        self.assertEqual(balanced.total_exponent, F(13, 12))
        self.assertEqual(balanced.saving, -F(1, 12))
        self.assertFalse(composite_linear_budget(F(1, 5), 0, 0).active)
        # The family has min(b,x)<=1/3; this is the all-box low-modulus cutoff.
        low = composite_linear_budget(F(1, 3), F(1, 3), F(253, 576), cap, cap)
        self.assertTrue(low.covered_by_fixed_margin)
        self.assertEqual(low.total_exponent, F(4067, 4096))

    def test_strict_domains(self):
        for args in ((1, 1, 0, 0, 0, ((1,),)), (4, 0, 0, 0, 0, ()),
                     (4, 1, 0.0, 0, 0, ((1,),)), (4, 2, 0, 0, 0, ((1,),))):
            with self.assertRaises(ValueError):
                periodic_linear_transform(*args)
        for args in ((8, 3, 0, (1, 1, 1)), (8, 2, 0.0, (1, 1)),
                     (8, 2, 0, (1,))):
            with self.assertRaises(ValueError):
                restricted_axis_exact(*args)
        for args in ((0.2, 0, 0), (F(1, 5), F(1, 2), F(1, 2)),
                     (F(1, 3), F(1, 3), F(1, 2), F(1, 4000))):
            with self.assertRaises(ValueError):
                composite_linear_budget(*args)


if __name__ == "__main__":
    unittest.main()
