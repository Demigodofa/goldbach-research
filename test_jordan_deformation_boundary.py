"""Exact arithmetic controls; no numerical parameter scan or asymptotic fit."""
from fractions import Fraction as F
from math import prod
import unittest

from complementary_divisor_correlation import central_interval
from jordan_deformation_boundary import (
    jordan_integer, jordan_linear_log_vector, local_pair_factor,
    pair_vanishing_order,
)
from major_arc_kernel import _factorization, _mobius_phi
from unexceptional_vaughan_gate import _divisors, mangoldt_log_vector


class JordanDeformationBoundaryTests(unittest.TestCase):
    def test_product_equals_full_divisor_sum(self):
        for n in range(1, 121):
            for k in (1, 2, 3):
                expected = sum(_mobius_phi(d)[0]*(n//d)**k for d in _divisors(n))
                self.assertEqual(jordan_integer(n, k), expected)
                self.assertGreater(jordan_integer(n, k), 0)
                self.assertLessEqual(jordan_integer(n, k), n**k)

    def test_exact_linear_coefficient_retains_proper_powers(self):
        for n in range(1, 241):
            self.assertEqual(jordan_linear_log_vector(n), mangoldt_log_vector(n))
        for n in (4, 8, 16, 64):
            self.assertEqual(jordan_linear_log_vector(n), ((2, 1),))
        for n in (6, 12, 30, 36, 60):
            self.assertEqual(jordan_linear_log_vector(n), ())

    def test_local_mean_by_independent_residue_enumeration(self):
        for p in (2, 3, 5, 7):
            for n in range(2*p):
                for t in (F(0), F(1, p), F(1, 2), F(1)):
                    mean = sum((1-t if a == 0 else 1)
                               *(1-t if (n-a) % p == 0 else 1)
                               for a in range(p))/F(p)
                    self.assertEqual(local_pair_factor(p, n, t), mean)

    def test_crt_product_for_actual_truncated_weights(self):
        primes = (2, 3, 5)
        period = prod(primes)
        for n in range(0, period, 2):
            mean = F(0)
            for a in range(period):
                left = prod(1-F(1, p) for p in primes if a % p == 0)
                right = prod(1-F(1, p) for p in primes if (n-a) % p == 0)
                mean += left*right*F(1, period)
            expected = prod(local_pair_factor(p, n, F(1, p)) for p in primes)
            self.assertEqual(mean, expected)

    def test_positive_tail_union_bound_without_per_prime_endpoint_loss(self):
        nmax, y = 120, 5
        primes = [p for p in range(2, nmax+1) if _factorization(p) == ((p, 1),)]
        tail = F(0)
        for n in range(1, nmax+1):
            full = F(jordan_integer(n, 1), n)
            short = prod(1-F(1, p) for p in primes if p <= y and n % p == 0)
            self.assertGreaterEqual(short, full)
            tail += short-full
        self.assertLessEqual(tail, nmax*sum(F(1, p*p) for p in primes if p > y))

    def test_deleted_family_has_no_quadratic_or_cubic_coefficient(self):
        self.assertEqual(pair_vanishing_order(60), 2)
        self.assertEqual(pair_vanishing_order(60, omit_prime_powers=True), 4)
        self.assertIsNone(pair_vanishing_order(6, omit_prime_powers=True))
        for target in range(6, 122, 2):
            order = pair_vanishing_order(target, omit_prime_powers=True)
            if order is not None:
                self.assertGreaterEqual(order, 4)
            for n in central_interval(target):
                if len(_factorization(n)) >= 2 and len(_factorization(target-n)) >= 2:
                    self.assertFalse(jordan_linear_log_vector(n))
                    self.assertFalse(jordan_linear_log_vector(target-n))

    def test_input_boundaries(self):
        for n in (True, 0, -1, 2.0):
            with self.assertRaises(ValueError):
                jordan_integer(n, 1)
            with self.assertRaises(ValueError):
                jordan_linear_log_vector(n)
        for k in (True, 0, -1, F(1), 1.0):
            with self.assertRaises(ValueError):
                jordan_integer(6, k)
        for p, n, t in ((4, 6, F(1, 2)), (True, 6, F(1, 2)),
                        (3, -1, F(1, 2)), (3, True, F(1, 2)),
                        (3, 6, 0.5), (3, 6, F(2))):
            with self.assertRaises(ValueError):
                local_pair_factor(p, n, t)
        with self.assertRaises(ValueError):
            pair_vanishing_order(60, omit_prime_powers=1)
        for n in (True, 4, 7, 6.0):
            with self.assertRaises(ValueError):
                pair_vanishing_order(n)


if __name__ == '__main__':
    unittest.main()
