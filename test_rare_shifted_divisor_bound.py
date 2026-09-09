"""Independent finite algebra checks; no analytic prime estimate is tested."""
from fractions import Fraction as F
from math import gcd, prod
import unittest

from rare_shifted_divisor_bound import (hyperbola_orientations, reflection_weight,
                                       rough_log_form, shifted_local_factors)


def factors(n):
    result = {}
    p = 2
    while p*p <= n:
        while n % p == 0:
            result[p] = result.get(p, 0)+1
            n //= p
        p += 1
    if n > 1:
        result[n] = result.get(n, 0)+1
    return result


def legendre31(n):
    residue = pow(n, 15, 31)
    return -1 if residue == 30 else residue


def divisor_lambda(n):
    return sum(legendre31(d) for d in range(1, n+1) if n % d == 0)


class RareShiftedDivisorTests(unittest.TestCase):
    def test_hyperbola_against_full_divisor_sum_including_squares_and_nonunits(self):
        for n in range(1, 600):
            a, b = hyperbola_orientations(n, 31)
            self.assertEqual(a+b, divisor_lambda(n))
            self.assertGreaterEqual(a+b, 0)
        for d in range(1, 35):
            self.assertEqual(reflection_weight(d, d), F(1, 2))
            for k in range(1, 35):
                self.assertEqual(reflection_weight(d, k)+reflection_weight(k, d), 1)

    def test_four_orientations_against_product_without_absolute_values(self):
        saw_cancellation = False
        for n in range(2, 200):
            for h in (2, 6, 31, 62):
                a, b = hyperbola_orientations(n, 31)
                c, d = hyperbola_orientations(n+h, 31)
                terms = (a*c, a*d, b*c, b*d)
                self.assertEqual(sum(terms), divisor_lambda(n)*divisor_lambda(n+h))
                saw_cancellation |= sum(map(abs, terms)) > abs(sum(terms))
        self.assertTrue(saw_cancellation)

    def test_log_form_slope_and_prime_coefficients_with_empty_atom(self):
        for cutoff in (2, 7, 31, 43):
            limit = 150
            slope, constant = rough_log_form(limit, cutoff, 31)
            selected = [n for n in range(1, limit+1)
                        if all(p >= cutoff for p in factors(n))]
            self.assertEqual(slope, sum((F(legendre31(n), n) for n in selected), F(0)))
            # Independent rational assignments to formal log primes, testing
            # both the intercept and the exact cancellation at two log(y)'s.
            for log_y in (F(3, 7), F(17, 5)):
                direct = sum((F(legendre31(n), n)*(log_y-sum(
                    exponent*F(p+2, p+1) for p, exponent in factors(n).items()))
                              for n in selected), F(0))
                encoded = slope*log_y+sum(c*F(p+2, p+1) for p, c in constant)
                self.assertEqual(encoded, direct)
        self.assertEqual(rough_log_form(1, 43, 31), (F(1), ()))
        # Prime equal to the cutoff is retained, unlike <= cutoff conventions.
        self.assertEqual(rough_log_form(7, 7, 31)[0], 1+F(legendre31(7), 7))

    def test_local_conductor_restoration_and_positive_pair_count(self):
        for conductor in (4, 8, 12, 24, 31, 35, 40):
            for h in (1, 2, 6, conductor, 2*conductor):
                k, units, omitted, full = shifted_local_factors(conductor, h, 43)
                local_units = prod((F(p-(1 if h % p == 0 else 2), p)
                                    for p in factors(conductor)), start=F(1))
                self.assertEqual(units, local_units)
                self.assertEqual(units*omitted, full)
                self.assertGreaterEqual(k, 0)
                self.assertLessEqual(k, 4*units)
                if h % 2:
                    self.assertEqual(full, 0)
        k = shifted_local_factors(31, 62, 43)[0]
        self.assertEqual(k, F(4*sum(legendre31(a) == 1 for a in range(31)), 31))

    def test_forbidden_multiplier_substitution_and_domains(self):
        # chi31(3)=-1 and chi31(7)=+1. Multiplication kills the majorant.
        self.assertEqual((legendre31(3), legendre31(7)), (-1, 1))
        self.assertEqual(divisor_lambda(7), 2)
        self.assertEqual(divisor_lambda(3*7), 0)
        for bad in (True, 0, -1, 2.5):
            with self.assertRaises(ValueError):
                reflection_weight(bad, 1)
            with self.assertRaises(ValueError):
                rough_log_form(bad, 7, 31)
        with self.assertRaises(ValueError):
            shifted_local_factors(31, 2, 31)


if __name__ == "__main__":
    unittest.main()
