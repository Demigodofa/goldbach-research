"""Finite exact guards for the endpoint and parity example, not asymptotics."""
from fractions import Fraction as F
import unittest

from major_arc_kernel import _factorization
from prime_factor_endpoint_gate import (
    factor_moment_vectors, liouville, liouville_square_pair, odd_prime_endpoint,
    parity_level_error, parity_multiples, prime_partner_moments,
)


def add_vectors(left, right):
    result = dict(left)
    for key, coefficient in right:
        result[key] = result.get(key, 0)+coefficient
    return tuple(sorted((key, coefficient) for key, coefficient in result.items() if coefficient))


class PrimeFactorEndpointGateTests(unittest.TestCase):
    def test_asymmetric_factor_compensation_keeps_internal_prime_powers(self):
        for cutoff in (2, 5, 10):
            for n in (11, 14, 27, 49, 81, 105, 121, 147, 231, 625):
                large, composite, prime, compensation = factor_moment_vectors(n, cutoff)
                self.assertEqual(large, compensation)
                self.assertEqual(large, add_vectors(composite, prime))
                self.assertEqual(bool(prime), _factorization(n) == ((n, 1),))
        self.assertEqual(factor_moment_vectors(27, 5)[0], ())
        self.assertEqual(factor_moment_vectors(49, 5)[0], ((7, 1),))
        with self.assertRaises(ValueError):
            factor_moment_vectors(5, 5)

    def test_prime_partner_moments_retain_exact_composite_deficit_and_endpoint(self):
        for y, target, cutoff in ((100, 150, 5), (200, 300, 13), (200, 288, 20)):
            total, composite, pairs, endpoint = prime_partner_moments(y, target, cutoff)
            self.assertEqual(total, add_vectors(composite, pairs))
            self.assertEqual(endpoint, pairs)
            direct = {}
            for n in range(y//2+1, y+1):
                q = target-n
                if (y < 2*q <= 2*y and _factorization(n) == ((n, 1),)
                        and _factorization(q) == ((q, 1),)):
                    key = tuple(sorted((n, q)))
                    direct[key] = direct.get(key, 0)+1
            self.assertEqual(pairs, tuple(sorted(direct.items())))
            self.assertTrue(composite)
            self.assertTrue(pairs)

    def test_odd_endpoint_is_exact_and_even_numbers_must_be_excluded(self):
        for n in (51, 53, 57, 63, 67, 77, 81, 91, 97, 99):
            self.assertEqual(odd_prime_endpoint(n, 100), _factorization(n) == ((n, 1),))
        # 94=2*47 would pass the largest-factor threshold while composite.
        self.assertGreater(3*47, 100)
        with self.assertRaises(ValueError):
            odd_prime_endpoint(94, 100)
        with self.assertRaises(ValueError):
            odd_prime_endpoint(49, 100)

    def test_fixed_power_witness_and_balanced_factor_log_coincidence(self):
        p, y = 101, 404
        n = 3*p
        self.assertEqual(_factorization(p), ((p, 1),))
        self.assertGreater(p**4, y**3)  # P+(n)>Y^(3/4), with exact integers.
        self.assertFalse(odd_prime_endpoint(n, y))
        self.assertNotEqual(_factorization(n), ((n, 1),))
        balanced = 101*103
        large, composite, prime, _ = factor_moment_vectors(balanced, 100)
        self.assertEqual(large, _factorization(balanced))  # exactly log(n)
        self.assertEqual(composite, large)
        self.assertFalse(prime)

    def test_liouville_uses_multiplicity_and_the_exact_square_convolution(self):
        for n in (1, 2, 4, 9, 12, 18, 36, 49, 72, 81, 105, 216):
            direct, convolution = liouville_square_pair(n)
            self.assertEqual(direct, convolution)
        self.assertEqual(liouville(9), 1)
        self.assertEqual(liouville(27), -1)
        for p in (2, 3, 5, 7, 11, 101):
            self.assertEqual(1+liouville(p), 0)

    def test_parity_multiple_formula_pays_the_liouville_divisor_sign(self):
        for x in (20, 37, 100):
            for divisor in (1, 2, 3, 4, 6, 9, 17, x+1):
                direct, formula = parity_multiples(x, divisor)
                self.assertEqual(direct, formula)
        self.assertEqual(sum(liouville(k) for k in range(1, 10)), -1)
        self.assertNotEqual(parity_multiples(18, 2)[0], 9+sum(liouville(k) for k in range(1, 10)))
        for level in (3, 15, 60):
            error, majorant = parity_level_error(60, level)
            self.assertLessEqual(error, majorant)

    def test_full_level_endpoint_contains_nonzero_prime_modulus_discrepancy(self):
        x = 100
        mass = sum(1+liouville(n) for n in range(1, x+1))
        primes = (53, 59, 61, 67, 71, 73, 79, 83, 89, 97)
        self.assertTrue(all(parity_multiples(x, p)[0] == 0 for p in primes))
        prime_error = sum((F(mass, p) for p in primes), F(0))
        self.assertGreater(prime_error, F(mass*len(primes), x))
        full_error, _ = parity_level_error(x, x)
        self.assertGreaterEqual(full_error, prime_error)
        with self.assertRaises(ValueError):
            parity_level_error(x, x+1)


if __name__ == '__main__':
    unittest.main()
