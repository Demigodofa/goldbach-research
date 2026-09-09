"""All-weight coefficient controls and finite weighted-loss identities."""
from fractions import Fraction as F
from math import isqrt
import unittest

from cubic_batch import _build_survivors
from cubic_sieve import exact_floor_cuberoot
from factored_linear_barrier import log_enclosure
from redistribution import trial_prime
from switched_cubic_barrier import (switched_cubic_coefficient, weight_kernel_integral,
                                    weighted_cubic_coefficient, weighted_switch_partition)


ZERO = ((F(1, 3), 0), (F(1, 2), 0))
TRIANGLE = ((F(1, 3), 0), (F(5, 12), 1), (F(1, 2), 0))
PROFILES = (ZERO, TRIANGLE,
            ((F(1, 3), 0), (F(3, 8), 1), (F(11, 24), 1), (F(1, 2), 0)),
            ((F(1, 3), 0), (F(3, 8), 1), (F(5, 12), F(1, 4)),
             (F(11, 24), F(1, 2)), (F(1, 2), 0)))


def actual_inputs(target):
    high = target-3
    z = exact_floor_cuberoot(high)
    small = [p for p in range(3, max(z, high//(z+1))+1, 2) if trial_prime(p)]
    a, c, _ = _build_survivors(small, z, high)
    return a, c, [p for p in small if z < p <= isqrt(high)]


def distinct_factors(n):
    factors = []
    p = 2
    while p*p <= n:
        if n % p == 0:
            factors.append(p)
            while n % p == 0:
                n //= p
        p += 1
    if n > 1:
        factors.append(n)
    return factors


class WeightedCubicTests(unittest.TestCase):
    def test_piecewise_integral_against_independent_log_products(self):
        for theta in (F(2, 3), F(3, 4), F(9, 10), 1):
            self.assertEqual(weight_kernel_integral(ZERO, theta), (0, 0))
            low, high = weight_kernel_integral(TRIANGLE, theta, 1)
            for terms in (2, 4, 8, 12):
                next_low, next_high = weight_kernel_integral(TRIANGLE, theta, terms)
                self.assertLessEqual(low, next_low)
                self.assertLessEqual(next_high, high)
                self.assertLessEqual(next_low, next_high)
                low, high = next_low, next_high
            half_profile = tuple((a, F(h, 2)) for a, h in TRIANGLE)
            self.assertEqual(weight_kernel_integral(half_profile, theta), (low/2, high/2))
        # Independent collected logarithm identities for this explicit triangle.
        ratio1 = F(8, 7)**8*F(6, 5)**6/(F(5, 4)**4*F(7, 6)**6)
        self.assertTrue(1 <= ratio1 <= 2)
        ref_low, ref_high = log_enclosure(ratio1)
        low, high = weight_kernel_integral(TRIANGLE, 1)
        self.assertLessEqual(low, ref_high)
        self.assertGreaterEqual(high, ref_low)
        # 3*I_(3/4)=log((5/4)^4*(6/5)^24/(4/3)^12).
        ratio3 = F(5, 4)**4*F(6, 5)**24/F(4, 3)**12
        self.assertTrue(1 <= ratio3/4 <= 2)
        a, b = log_enclosure(ratio3/4)
        c, d = log_enclosure(2)
        low, high = weight_kernel_integral(TRIANGLE, F(3, 4))
        self.assertLessEqual(low, (b+2*d)/3)
        self.assertGreaterEqual(high, (a+2*c)/3)

    def test_functional_ceiling_and_weights_can_improve_a_weaker_certificate(self):
        for profile in PROFILES:
            self.assertEqual(weighted_cubic_coefficient(profile, 1, 1), (0, 0))
            for original in (F(2, 3), F(3, 4), F(9, 10), F(99, 100), 1):
                ceiling = switched_cubic_coefficient(original, 1)
                for switched in (F(1, 2), F(3, 4), 1):
                    low, high = weighted_cubic_coefficient(profile, original, switched)
                    self.assertLessEqual(low, high)
                    self.assertLessEqual(high, ceiling[1])
                    if (original, switched) != (1, 1):
                        self.assertLess(high, 0)
                    if profile == ZERO:
                        self.assertEqual((low, high), switched_cubic_coefficient(original, switched))
        weighted = weighted_cubic_coefficient(TRIANGLE, F(3, 4), F(1, 2))
        unweighted = switched_cubic_coefficient(F(3, 4), F(1, 2))
        self.assertGreater(weighted[0], unweighted[1])
        self.assertLess(weighted[1], 0)
        # It cannot improve the optimistic comparison with switched level1.
        self.assertLess(weighted_cubic_coefficient(TRIANGLE, F(3, 4), 1)[1],
                        switched_cubic_coefficient(F(3, 4), 1)[0])

    def test_exact_prime_loss_negative_composite_loss_and_distinct_square_divisor(self):
        for target in (6, 8, 12, 14, 18, 30, 50, 54, 66, 98, 124, 126, 242, 500):
            a, c, residual = actual_inputs(target)
            for level in (0, F(1, 2), 1):
                weights = {p: level for p in residual}
                sigma1, sigma2, lower, prime_loss, negative_loss = weighted_switch_partition(target, a, c, weights)
                true_g = 0
                direct1 = direct2 = direct_prime_loss = direct_negative = F(0)
                for i, n in enumerate(range(3, target-2, 2)):
                    if not trial_prime(target-n):
                        continue
                    is_prime = trial_prime(n)
                    true_g += is_prime
                    w = 1-sum((weights.get(p, 0) for p in distinct_factors(n)), F(0))
                    direct1 += a[i]*w
                    direct2 += c[i]*max(w, 0)
                    direct_prime_loss += int(is_prime)*(1-w)
                    direct_negative += c[i]*max(-w, 0)
                self.assertEqual((sigma1, sigma2), (direct1, direct2))
                self.assertEqual((prime_loss, negative_loss), (direct_prime_loss, direct_negative))
                self.assertEqual(true_g-lower, prime_loss+negative_loss)
                self.assertLessEqual(lower, true_g)
        a, c, _ = actual_inputs(30)
        self.assertEqual(weighted_switch_partition(30, a, c, {5: F(3, 4)}),
                         (F(25, 4), F(1, 4), 6, 0, 0))
        a, c, _ = actual_inputs(66)
        result = weighted_switch_partition(66, a, c, {5: 1, 7: 1})
        self.assertEqual(result[3:], (2, 1))
        a, c, _ = actual_inputs(14)
        self.assertEqual(weighted_switch_partition(14, a, c, {3: F(1, 2)})[2:],
                         (F(5, 2), F(1, 2), 0))

    def test_profile_level_and_prime_weight_validation(self):
        for profile in (list(ZERO), (), ((F(1, 3), True), (F(1, 2), 0)),
                        ((1/3, 0), (F(1, 2), 0)),
                        ((F(1, 3), 0), (F(5, 12), 2), (F(1, 2), 0)),
                        ((F(1, 3), 0), (F(1, 3), 0), (F(1, 2), 0)),
                        ((F(1, 3), 1), (F(1, 2), 0))):
            with self.assertRaises(ValueError):
                weight_kernel_integral(profile, 1)
        for theta in (True, 1.0, F(1, 2), F(11, 10)):
            with self.assertRaises(ValueError):
                weight_kernel_integral(ZERO, theta)
        for original, switched in ((F(1, 2), 1), (1, 0), (True, 1), (1, 1.0)):
            with self.assertRaises(ValueError):
                weighted_cubic_coefficient(ZERO, original, switched)
        for terms in (True, 0, 129, 1.0):
            with self.assertRaises(ValueError):
                weighted_cubic_coefficient(ZERO, 1, 1, terms)
        a, c, _ = actual_inputs(30)
        for weights in ([], {True: 1}, {2: 1}, {3: 1}, {7: 1}, {5: True},
                        {5: 0.5}, {5: F(3, 2)}):
            with self.assertRaises(ValueError):
                weighted_switch_partition(30, a, c, weights)
        a, c, _ = actual_inputs(500)
        with self.assertRaises(ValueError):
            weighted_switch_partition(500, a, c, {9: 1})
        with self.assertRaises(ValueError):
            weighted_switch_partition(8, bytearray([1]), bytearray([0]), {})
        self.assertIn("NOT actual G/K", weighted_cubic_coefficient.__doc__)


if __name__ == "__main__":
    unittest.main()
