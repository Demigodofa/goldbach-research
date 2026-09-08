"""Finite identity controls; these do not certify asymptotic error constants."""
from fractions import Fraction
from math import isqrt
import unittest

from exceptional_character_model import character_values
from redistribution import trial_prime
from rough_semiprime_character import factor_components


def is_rough_semiprime(n, cutoff):
    """Independent trial factorization, rather than an ordered product sum."""
    for d in range(2, isqrt(n)+1):
        if n % d == 0:
            return d > cutoff and trial_prime(d) and trial_prime(n//d)
    return False


class RoughSemiprimeCharacterTests(unittest.TestCase):
    def test_factor_identity_for_intervals_cutoffs_and_character_components(self):
        primes = [p for p in range(2, 201) if trial_prime(p)]
        # The last two periods are real and imaginary components of the
        # nonreal character mod5 with chi(2)=i. Each is rational-valued.
        periods = [(1,), character_values(5), character_values(24, two_sign=-1),
                   (0, 1, 0, 0, -1), (0, 0, 1, -1, 0)]
        for cutoff in (2, 3, 5, 7):
            for lower in (0, 24, 25, 48, 49, 120, 121):
                for upper in (lower, lower+1, min(lower+45, 200), 200):
                    for weights in periods:
                        actual, ordered, square = factor_components(
                            primes, cutoff, lower, upper, weights)
                        expected = sum(weights[n % len(weights)] for n in range(lower+1, upper+1)
                                       if is_rough_semiprime(n, cutoff))
                        self.assertEqual(actual, expected)
                        expected_squares = sum(weights[n % len(weights)] for n in range(lower+1, upper+1)
                                               if isqrt(n)**2 == n and isqrt(n) > cutoff
                                               and trial_prime(isqrt(n)))
                        self.assertEqual(square, expected_squares)
                        self.assertEqual(2*actual, ordered+square)

    def test_square_half_weight_and_strict_cutoff_boundaries(self):
        primes = [2, 3, 5, 7, 11, 13]
        self.assertEqual(factor_components(primes, 3, 24, 25, (1,)), (1, 1, 1))
        self.assertEqual(factor_components(primes, 5, 24, 25, (1,)), (0, 0, 0))
        self.assertEqual(factor_components(primes, 3, 34, 35, (1,)), (1, 2, 0))
        self.assertEqual(factor_components(primes, 3, 24, 25, (Fraction(-2, 3),)),
                         (Fraction(-2, 3), Fraction(-2, 3), Fraction(-2, 3)))

    def test_input_contract_does_not_claim_to_certify_prime_labels(self):
        for cutoff, lower, upper in ((True, 0, 25), (1, 0, 25), (3, -1, 25),
                                      (3, 26, 25), (3, 0, 25.0)):
            with self.assertRaises(ValueError):
                factor_components([2, 3, 5, 7], cutoff, lower, upper, (1,))
        for primes in ([2, 5, 3], [2, 3, 3], [True, 3], [1, 3]):
            with self.assertRaises(ValueError):
                factor_components(primes, 3, 0, 25, (1,))
        for weights in ((), (0.5,), (True,)):
            with self.assertRaises(ValueError):
                factor_components([2, 3, 5, 7], 3, 0, 25, weights)
        # Missing 5 is semantically untruthful input, not detectable by
        # ordering checks. The verifier must not advertise oracle validation.
        self.assertEqual(factor_components([2, 3, 7], 3, 24, 25, (1,)), (0, 0, 0))
        self.assertIn("do not certify", factor_components.__doc__)


if __name__ == "__main__":
    unittest.main()
