"""Exact switching orientation, exceptions, and coefficient boundary checks."""
from fractions import Fraction
from math import isqrt
import unittest

from cubic_batch import _build_survivors
from cubic_sieve import exact_floor_cuberoot
from factored_linear_barrier import log_enclosure
from redistribution import trial_prime
from switched_cubic_barrier import (switch_partition, switched_cubic_coefficient,
                                    switching_mass)


class SwitchedCubicTests(unittest.TestCase):
    def test_actual_partition_against_unique_prime_factors_and_true_counts(self):
        rows = {}
        for target in (6, 8, 12, 18, 24, 26, 28, 30, 50, 54, 66, 98,
                       124, 126, 128, 242, 264, 338, 500):
            high = target-3
            z = exact_floor_cuberoot(high)
            limit = max(z, high//(z+1))
            small = [p for p in range(3, limit+1, 2) if trial_prime(p)]
            a, c, _ = _build_survivors(small, z, high)
            t, distinct, square, g = switch_partition(target, a, c)
            direct_distinct = direct_square = 0
            switched = {}
            for q in small:
                if not z < q <= isqrt(high):
                    continue
                for r in small:
                    if r < q or q*r > high:
                        continue
                    complement = target-q*r
                    self.assertNotIn(complement, switched)
                    switched[complement] = (q, r)
                    if trial_prime(complement):
                        if q == r:
                            direct_square += 1
                        else:
                            direct_distinct += 1
            self.assertEqual((distinct, square), (direct_distinct, direct_square))
            true_g = sum(trial_prime(p) and trial_prime(target-p)
                         for p in range(3, target-2, 2))
            self.assertEqual(g, true_g)
            self.assertEqual(t, g+distinct+square)
            self.assertLessEqual(square, isqrt(target))
            small_prime_complements = sum(q < r and trial_prime(p) and p*p < target
                                          for p, (q, r) in switched.items())
            self.assertLessEqual(small_prime_complements, isqrt(target))
            rows[target] = (t, distinct, square, g, small_prime_complements)
        # q=r=3 with complement3 must be retained in the exact formula.
        self.assertEqual(rows[12][:4], (3, 0, 1, 2))
        # q=3,r=5 with complement3 is lost by a plain sqrt(18) sieve.
        self.assertEqual(rows[18][1], 1)
        self.assertEqual(rows[18][4], 1)
        # A composite at the center is not a prime/composite square term.
        self.assertEqual(rows[50][2], 0)

    def test_integral_mass_endpoints_and_partition_additivity(self):
        third, half = Fraction(1, 3), Fraction(1, 2)
        self.assertEqual(switching_mass(third, half), log_enclosure(2))
        self.assertEqual(switching_mass(third, third), (0, 0))
        endpoints = (third, Fraction(3, 8), Fraction(2, 5), half)
        parts = [switching_mass(a, b) for a, b in zip(endpoints, endpoints[1:])]
        full_low, full_high = switching_mass(third, half)
        self.assertLessEqual(sum(a for a, _ in parts), full_high)
        self.assertGreaterEqual(sum(b for _, b in parts), full_low)
        # Independently integrate after t=alpha/(1-alpha): the endpoint
        # ratios are6/5,10/9,3/2, whose product is2, with no factor2 in mass.
        for interval, ratio in zip(parts, (Fraction(6, 5), Fraction(10, 9), Fraction(3, 2))):
            self.assertEqual(interval, log_enclosure(ratio))
        self.assertEqual(Fraction(6, 5)*Fraction(10, 9)*Fraction(3, 2), 2)

    def test_negative_certificate_and_exact_limiting_balance(self):
        self.assertEqual(switched_cubic_coefficient(1, 1), (0, 0))
        for original in (Fraction(1, 2), Fraction(2, 3), Fraction(3, 4),
                         Fraction(9, 10), Fraction(999, 1000), 1):
            for switched in (Fraction(1, 2), Fraction(3, 4), Fraction(9, 10), 1):
                low, high = switched_cubic_coefficient(original, switched)
                self.assertLessEqual(low, high)
                if (original, switched) != (1, 1):
                    self.assertLess(high, 0)
                if original <= Fraction(2, 3):
                    a, b = log_enclosure(2)
                    self.assertEqual((low, high), (-2*b/switched, -2*a/switched))
        # For equal levels theta>2/3 the expression simplifies independently
        # to -(2/theta)*log(2/(3theta-1)).
        for theta in (Fraction(3, 4), Fraction(9, 10), 1):
            a, b = log_enclosure(Fraction(2, 3*theta-1))
            low, high = switched_cubic_coefficient(theta, theta)
            self.assertLessEqual(low, -2*a/theta)
            self.assertGreaterEqual(high, -2*b/theta)
        self.assertIn("NOT actual G/K or L/K", switched_cubic_coefficient.__doc__)

    def test_input_meanings_and_unsafe_ranges(self):
        for left, right in ((True, Fraction(1, 2)), (0.4, Fraction(1, 2)),
                            (Fraction(1, 4), Fraction(1, 2)),
                            (Fraction(1, 2), Fraction(1, 3)),
                            (Fraction(1, 3), Fraction(2, 3))):
            with self.assertRaises(ValueError):
                switching_mass(left, right)
        for original, switched in ((True, 1), (0.9, 1), (1, 0), (0, 1), (1, Fraction(11, 10))):
            with self.assertRaises(ValueError):
                switched_cubic_coefficient(original, switched)
        for terms in (True, 0, 129, 1.0):
            with self.assertRaises(ValueError):
                switched_cubic_coefficient(1, 1, terms)
        for target, a, c in ((True, bytearray([1]), bytearray([0])),
                             (6, bytearray([0]), bytearray([1])),
                             (8, bytearray([1]), bytearray([0]))):
            with self.assertRaises(ValueError):
                switch_partition(target, a, c)
        self.assertIn("do not establish primality", switch_partition.__doc__)


if __name__ == "__main__":
    unittest.main()
