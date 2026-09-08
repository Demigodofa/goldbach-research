"""Independent arithmetic and prime-count checks of rigorous CRT errors."""
from fractions import Fraction
from math import isqrt
import unittest

from crt_error_bounds import central_crt_bound, odd_multiples
from redistribution import trial_prime


class CrtErrorTests(unittest.TestCase):
    def test_exact_odd_multiple_count_all_small_endpoints(self):
        for lo in range(1, 35):
            for hi in range(lo - 1, 45):
                for factor in (1, 3, 5, 7, 11):
                    expected = sum(a % 2 == 1 and a % factor == 0
                                   for a in range(lo, hi + 1))
                    self.assertEqual(odd_multiples(lo, hi, factor), expected)

    def test_bounds_and_exact_comparison_against_direct_divisibility(self):
        for target in range(6, 1001, 2):
            row = central_crt_bound(target, compare_exact=True)
            lo, hi = row["candidate_interval"]
            cutoff = row["cubic_cutoff"]
            primes = [p for p in range(3, isqrt(target - 3) + 1, 2)
                      if trial_prime(p)]
            base = [a for a in range(lo, hi + 1, 2)
                    if all(a % p and (target - a) % p
                           for p in primes if p <= cutoff)]
            S1 = sum((a >= p * p and a % p == 0) or
                     (target - a >= p * p and (target - a) % p == 0)
                     for p in primes if p > cutoff for a in base)
            G = sum(trial_prime(a) and trial_prime(target - a)
                    for a in range(lo, hi + 1, 2))
            with self.subTest(target=target):
                self.assertEqual(row["exact_diagnostic"]["M"], len(base))
                self.assertEqual(row["exact_diagnostic"]["S1"], S1)
                self.assertEqual(row["exact_diagnostic"]["G_ordered"], G)
                self.assertLessEqual(row["M_lower"], len(base))
                self.assertGreaterEqual(row["S1_upper"], S1)
                self.assertLessEqual(row["G_lower"], G)
                self.assertLessEqual(abs(len(base) - Fraction(row["M_main_term_exact"])),
                                     row["absolute_CRT_error_bound"])
                for branch in row["residual_branches"]:
                    prime = branch["prime"]
                    actual = sum(a >= prime * prime and a % prime == 0 for a in base)
                    self.assertLessEqual(actual, branch["presieved_arm_upper"])

    def test_large_error_is_not_silently_dropped(self):
        row = central_crt_bound(1_000_000)
        self.assertEqual(row["absolute_CRT_error_bound"], 2 * 3 ** 23 - 1)
        self.assertGreater(row["absolute_CRT_error_bound"], row["odd_candidate_slots"])
        self.assertEqual(row["M_lower"], 0)
        self.assertFalse(row["certifies_positive"])
        self.assertNotIn("exact_diagnostic", row)

    def test_input_contract_is_not_assert_dependent(self):
        for target in (4, 5, 9, True, 100.0, -2):
            with self.assertRaises(ValueError):
                central_crt_bound(target)
        for args in ((0, 4, 3), (1, 7, 2), (1, 7, True)):
            with self.assertRaises(ValueError):
                odd_multiples(*args)


if __name__ == "__main__":
    unittest.main()
