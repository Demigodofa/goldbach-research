"""Finite mixture densities and the shared-character exclusion only."""
from fractions import Fraction as F
from math import gcd, lcm
import unittest

from exceptional_character_model import character_values
from wheel_mixture_obstruction import mixture_prime_defect, wheel_progression_means


class WheelMixtureTests(unittest.TestCase):
    def test_complete_joint_periods_include_signed_and_partial_coverage(self):
        for moduli, weights in (([6, 10, 14], [F(1, 3)]*3),
                                ([6, 10, 14], [2, -2, 1]),
                                ([6, 18, 30], [F(1, 2), F(-1, 2), 1])):
            for prime in (3, 5, 7, 11):
                period = lcm(*moduli, prime)
                phi = [sum(gcd(a, q) == 1 for a in range(q)) for q in moduli]
                model = sum(sum(F(w*q, ph) for q, ph, w in zip(moduli, phi, weights)
                                if gcd(a, q) == 1)
                            for a in range(period) if a % prime == 8 % prime)/period
                _, gap = mixture_prime_defect(moduli, weights, 8, prime)
                self.assertEqual(F(1, prime-1)-model, gap)
        # Every displayed prime occurs somewhere; coverage is nevertheless partial.
        for prime in (3, 5, 7):
            coverage, gap = mixture_prime_defect([6, 10, 14], [F(1, 3)]*3, 8, prime)
            self.assertEqual(coverage, F(1, 3))
            self.assertGreater(gap, 0)
        self.assertGreater(lcm(6, 10, 14), 10*max(6, 10, 14))

    def test_signed_defects_require_a_weighted_test(self):
        moduli, weights, primes = [6, 10, 14], [2, -2, 1], (3, 5, 7)
        data = [mixture_prime_defect(moduli, weights, 8, p) for p in primes]
        self.assertEqual([coverage for coverage, _ in data], [2, -2, 1])
        self.assertLess(data[0][1], 0)
        self.assertGreater(data[1][1], 0)
        self.assertEqual(data[2][1], 0)
        # Arbitrary rational test weights check the exact alignment identity;
        # they are not claimed to be enclosures for the logarithms in the proof.
        test = (F(1, 2), F(3, 4), F(1))
        scale = max(p*(p-1)*a for p, a in zip(primes, test))
        h = [p*(p-1)*a/scale for p, a in zip(primes, test)]
        self.assertTrue(all(0 <= a <= 1 for a in h))
        self.assertEqual(sum(a*gap for a, (_, gap) in zip(h, data)),
                         sum(a*(1-coverage) for a, (coverage, _) in zip(test, data))/scale)

    def test_progression_means_prime_powers_and_required_character_exclusion(self):
        for d, moduli, sign in ((31, (62, 186, 310), 1),
                                (40, (120, 200, 240), 1),
                                (40, (120, 200, 240), -1),
                                (33, (66, 330), 1)):
            chi = character_values(d, two_sign=sign)
            for q in moduli:
                for p in (3, 5, 7, 11, 31):
                    mean, twisted = wheel_progression_means(q, 8, p, conductor=d,
                                                            two_sign=sign)
                    expected = F(p, p-1) if q % p == 0 else F(1)
                    self.assertEqual(mean, expected)
                    self.assertEqual(twisted, expected*chi[8 % d] if d == p else 0)
        self.assertNotEqual(wheel_progression_means(62, 8, 31, conductor=31)[1], 0)
        self.assertEqual(wheel_progression_means(18, 8, 3), (F(3, 2), 0))

    def test_exact_types_normalization_and_nonzero_residue_premise(self):
        for moduli, weights, target, prime in (([], [], 8, 3), ([3], [1], 8, 5),
                                              ([True], [1], 8, 3), ([6], [0], 8, 5),
                                              ([6, 10], [1], 8, 3), ([6], [True], 8, 5),
                                              ([6], [1.0], 8, 5), ([6], [1], 6, 3),
                                              ([6], [1], 8, 9), ([6], [1], True, 3)):
            with self.assertRaises(ValueError):
                mixture_prime_defect(moduli, weights, target, prime)
        for q, d, sign in ((50, 25, 1), (62, 31, -1), (64, 31, 1),
                            (80, 40, True), (6, None, -1)):
            with self.assertRaises(ValueError):
                wheel_progression_means(q, 8, 7, conductor=d, two_sign=sign)
        self.assertIn("not an actual prime count", mixture_prime_defect.__doc__)


if __name__ == "__main__":
    unittest.main()
