"""Exact support and factor guards; these tests do not certify analytic errors."""
from fractions import Fraction as F
from itertools import combinations
from math import isqrt, prod
import unittest

from exceptional_character_model import character_values, pair_moments
from rare_factor_pruning import partner_factor_profile, sieve_index_split
from redistribution import trial_prime


def independent_support(cutoff, level):
    """Enumerate smooth squarefree d by subsets, without factoring indices."""
    small_primes = [p for p in range(2, cutoff+1) if trial_prime(p)]
    smooth = [prod(subset) for size in range(len(small_primes)+1)
              for subset in combinations(small_primes, size)]
    return [(q, d) for q in range(cutoff+1, isqrt(level)+1) if trial_prime(q)
            for d in smooth if q*d <= level]


class RareFactorPruningTests(unittest.TestCase):
    def test_complete_support_is_injective_including_square_root_boundary(self):
        for cutoff, level in ((2, 49), (5, 399), (5, 400), (5, 441), (5, 529)):
            support = independent_support(cutoff, level)
            indices = {q*d: (q, d) for q, d in support}
            self.assertEqual(len(indices), len(support))
            self.assertEqual({index: sieve_index_split(index, cutoff, level)
                              for index in range(1, level+1)
                              if sieve_index_split(index, cutoff, level) is not None},
                             indices)
        self.assertEqual(sieve_index_split(210, 5, 400), (7, 30))
        self.assertEqual(sieve_index_split(7, 2, 49), (7, 1))
        self.assertIsNone(sieve_index_split(7, 2, 48))
        self.assertEqual(sieve_index_split(23, 5, 529), (23, 1))
        self.assertIsNone(sieve_index_split(23, 5, 528))
        for index in (1, 5, 23, 49, 77, 401):
            self.assertIsNone(sieve_index_split(index, 5, 400))

    def test_remainder_budget_is_spent_once_across_all_q(self):
        level, cutoff = 400, 5
        support = independent_support(cutoff, level)
        errors = {index: F((index % 7)-3, index+1) for index in range(1, level+1)}
        by_q = {}
        coefficients = {}
        for q, d in support:
            weight = F(((q+2*d) % 5)-2, 2)
            self.assertLessEqual(abs(weight), 1)
            self.assertNotIn(q*d, coefficients)
            coefficients[q*d] = weight
            by_q[q] = by_q.get(q, F(0)) + weight*errors[q*d]
        weighted_norm = sum(abs(value) for value in by_q.values())
        support_norm = sum(abs(errors[index]) for index in coefficients)
        full_norm = sum(abs(value) for value in errors.values())
        self.assertGreater(len(by_q), 1)
        self.assertGreater(weighted_norm, 0)
        self.assertLessEqual(weighted_norm, support_norm)
        self.assertLessEqual(support_norm, full_norm)
        self.assertEqual(sum(by_q.values()),
                         sum(weight*errors[index] for index, weight in coefficients.items()))

    def test_factor_multiplicities_and_inclusive_pruning_boundary(self):
        self.assertEqual(partner_factor_profile(215, 31, 4, 10), (1, 1, (5,), ()))
        self.assertEqual(partner_factor_profile(209, 31, 4, 10), (1, 1, (), (19,)))
        self.assertEqual(partner_factor_profile(209, 31, 4, 19), (1, 1, (19,), ()))
        self.assertEqual(partner_factor_profile(1331, 31, 10, 50), (0, 3, (), ()))
        self.assertEqual(partner_factor_profile(19*11**3, 31, 4, 10),
                         (1, 3, (), (19,)))
        self.assertEqual(partner_factor_profile(5**3*11, 31, 4, 10),
                         (3, 1, (5,), ()))
        self.assertEqual(partner_factor_profile(11, 31, 4, 10), (0, 1, (), ()))

    def test_retained_composites_really_occur_with_prime_first_entries(self):
        chi = character_values(31)
        for prime, partner, cutoff, bound in ((349, 209, 4, 10),
                                              (1459, 1331, 10, 50)):
            self.assertTrue(trial_prime(prime))
            self.assertFalse(trial_prime(partner))
            self.assertEqual(chi[prime % 31], 1)
            target = prime+partner
            a, b, c = pair_moments(31, target)
            self.assertGreater(a, 0)
            self.assertEqual((b, c), (0, -a))
            positive, negative, small, large = partner_factor_profile(
                partner, 31, cutoff, bound)
            self.assertEqual(small, ())
            self.assertEqual(negative % 2, 1)
            if (positive+negative) % 2 == 0:
                self.assertTrue(large)
                for q in large:
                    self.assertGreater(q, bound)
                    self.assertLess(partner//q, F(partner, bound))
            else:
                self.assertEqual((positive, negative, large), (0, 3, ()))

    def test_invalid_inputs_and_out_of_support_are_distinct(self):
        for index, cutoff, level in ((True, 5, 400), (1.0, 5, 400), (0, 5, 400),
                                     (7, 1, 400), (7, 5.0, 400), (7, 5, 0),
                                     (7, 5, True)):
            with self.assertRaises(ValueError):
                sieve_index_split(index, cutoff, level)
        self.assertIsNone(sieve_index_split(49, 5, 400))
        for partner, conductor, cutoff, bound, sign in (
                (True, 31, 4, 10, 1), (209.0, 31, 4, 10, 1), (1, 31, 4, 10, 1),
                (209, 25, 4, 10, 1), (31, 31, 4, 10, 1), (121, 31, 4, 10, 1),
                (215, 31, 5, 10, 1), (209, 31, 4, 3, 1), (209, 31, 1, 10, 1),
                (209, True, 4, 10, 1), (209, 31, 4.0, 10, 1),
                (209, 31, 4, 10, True)):
            with self.assertRaises(ValueError):
                partner_factor_profile(partner, conductor, cutoff, bound, two_sign=sign)


if __name__ == "__main__":
    unittest.main()
