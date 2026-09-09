"""Exact support, sign and rearrangement guards; no asymptotic experiment."""
from fractions import Fraction
import unittest

from factored_linear_barrier import log_enclosure
from major_arc_kernel import _factorization, _mobius_phi
from prime_factor_endpoint_gate import liouville
from redistribution import trial_prime
from rough_liouville_transfer_gate import (
    free_log_split, prime_partner_split, rough_divisor_split, rough_sign,
)


def combine(left, right, multiplier=1):
    result = dict(left)
    for key, value in right:
        result[key] = result.get(key, 0)+multiplier*value
    return tuple(sorted((k, v) for k, v in result.items() if v))


class RoughLiouvilleTransferTests(unittest.TestCase):
    def test_strict_cube_boundary_and_multiplicity(self):
        self.assertEqual(rough_sign(125, 125), 0)
        self.assertEqual(liouville(125), -1)  # would be a false prime signal
        self.assertEqual(rough_sign(49, 60), 1)
        self.assertEqual(_mobius_phi(49)[0], 0)  # Mobius cannot replace ell
        self.assertEqual(rough_sign(53, 60), -1)
        for y in (27, 60, 125, 200):
            for n in range(y//2+1, y+1):
                if rough_sign(n, y):
                    self.assertIn(sum(e for _, e in _factorization(n)), (1, 2))

    def test_signed_prime_partner_identity_with_nonconstant_rational_weights(self):
        for y, m in ((60, 102), (100, 150), (200, 300)):
            samples = {n: Fraction(n-y//2, y) for n in range(y//2+1, y+1)}
            a, c, g, q = prime_partner_split(y, m, samples)
            self.assertEqual(a, combine(c, g))
            self.assertEqual(q, combine(c, g, -1))
            direct = {}
            for n, w in samples.items():
                partner = m-n
                if y < 2*partner <= 2*y and trial_prime(n) and trial_prime(partner):
                    key = tuple(sorted((n, partner)))
                    direct[key] = direct.get(key, 0)+w
            self.assertEqual(g, tuple(sorted(direct.items())))
            self.assertTrue(g)
            self.assertTrue(c)

    def test_square_and_prime_samples_have_opposite_signed_mass(self):
        a, c, g, q = prime_partner_split(60, 102, {49: 1})
        self.assertEqual(a, (((7, 53), 2),))  # log49=2log7; unique square
        self.assertEqual((c, g, q), (a, (), a))
        a, c, g, q = prime_partner_split(100, 150, {53: 1})
        self.assertEqual((c, g), ((), a))
        self.assertEqual(q, (((53, 97), -1),))
        # The prime cube125 plus prime107 is physical, but excluded by R.
        self.assertEqual(prime_partner_split(125, 232, {125: 1}), ((), (), (), ()))

    def test_inclusion_exclusion_has_positive_outer_coefficients(self):
        for y in (27, 60, 125):
            for n in (1, 8, 12, 27, 30, 49, 60, 105, 125, 210):
                for cutoff in (1, 4, 20, y):
                    short, long = rough_divisor_split(n, y, cutoff)
                    direct = 0
                    for d in range(1, n+1):
                        if n % d == 0 and all(p**3 <= y for p, _ in _factorization(d)):
                            direct += _mobius_phi(d)[0]*liouville(n)
                    self.assertEqual(short+long, direct)
                    self.assertEqual(direct, rough_sign(n, y))
        self.assertEqual(rough_divisor_split(30, 125, 1), (-1, 1))
        self.assertEqual(rough_divisor_split(53, 125, 1), (-1, 0))

    def test_free_long_divisor_sum_is_not_a_subset_of_rough_integers(self):
        for y, cutoff in ((60, 1), (125, 4), (200, 10)):
            full, short, long = free_log_split(y, cutoff)
            self.assertEqual(full, combine(short, long))
            self.assertTrue(long)
            for n in range(y//2+1, y+1):
                if rough_sign(n, y):
                    self.assertEqual(rough_divisor_split(n, y, cutoff)[1], 0)
        # log2-1<0 is a certified coefficient, not a finite-size onset.
        low, high = log_enclosure(2)
        self.assertLess(high-1, Fraction(-1, 4))
        self.assertGreater(low-1, Fraction(-1, 3))

    def test_input_contract(self):
        for args in ((8, 12, None), (60, 101, None), (60, 102, {49: -1}),
                     (60, 102, {49: .5}), (60, 102, {1: 1})):
            with self.assertRaises(ValueError):
                prime_partner_split(*args)
        with self.assertRaises(ValueError):
            rough_divisor_split(30, 125, 0)


if __name__ == '__main__':
    unittest.main()
