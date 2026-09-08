"""Independent arithmetic checks for the two-moment block certificate."""
from copy import deepcopy
from itertools import product
import unittest

from block_moments import (make_certificate, positive_count_bound, replay_certificate,
                           sufficient_bounded_moments, target_weight)
from redistribution import trial_prime


class BlockMomentTests(unittest.TestCase):
    def test_exhaustive_nonnegative_vectors_and_strict_zero_boundary(self):
        for length in range(1, 7):
            for values in product(range(4), repeat=length):
                S = sum(values)
                T = sum(x*x for x in values)
                lower = positive_count_bound(length, S, T)
                self.assertLessEqual(lower, sum(x>0 for x in values))
        self.assertEqual(positive_count_bound(3, 4, 8), 2)  # [0,2,2]
        self.assertEqual(positive_count_bound(3, 6, 12), 3)  # [2,2,2]
        self.assertEqual(positive_count_bound(3, 102, 10002), 2)  # [1,1,100]

    def test_weights_depend_on_distinct_odd_factors_and_stay_positive(self):
        self.assertEqual(target_weight(32, bits=3), 8)
        self.assertEqual(target_weight(30, bits=3), 3)
        self.assertEqual(target_weight(210, bits=3), 3)
        self.assertEqual(target_weight(900, bits=3), 3)
        for n in range(6, 2002, 2):
            self.assertGreaterEqual(target_weight(n, bits=1), 1)
            self.assertEqual(target_weight(n, mode="unit"), 1)

    def test_verified_bound_interface_and_invalid_moments(self):
        self.assertTrue(sufficient_bounded_moments(3, 3, 3))
        self.assertFalse(sufficient_bounded_moments(3, 2, 3))
        self.assertFalse(sufficient_bounded_moments(3, 0, 0))
        for args in [(True, 1, 1), (2, 0, 1), (2, 4, 1), (2, 1, 3), (2, -1, 0)]:
            with self.subTest(args=args), self.assertRaises(ValueError):
                positive_count_bound(*args)
        with self.assertRaises(ValueError):
            sufficient_bounded_moments(2, 4, 1)

    def test_canonical_receipts_and_tampering(self):
        for mode in ["unit", "singular"]:
            receipt = make_certificate(1000, 20, mode)
            self.assertTrue(replay_certificate(receipt))
            bad = deepcopy(receipt)
            bad["sum_weighted_counts"] += 1
            with self.assertRaises(ValueError):
                replay_certificate(bad)
            bad = deepcopy(receipt)
            bad["schema"] = True
            with self.assertRaises(ValueError):
                replay_certificate(bad)

    def test_receipt_moments_match_direct_trial_prime_counts(self):
        first, count = 1000, 20
        for mode in ["unit", "singular"]:
            values = []
            for N in range(first, first+2*count, 2):
                G = sum(trial_prime(a) and trial_prime(N-a)
                        for a in range(3, N-2, 2))
                values.append(target_weight(N, mode)*G)
            receipt = make_certificate(first, count, mode)
            self.assertEqual(receipt["sum_weighted_counts"], sum(values))
            self.assertEqual(receipt["sum_squared_weighted_counts"],
                             sum(x*x for x in values))

    def test_invalid_target_and_weight_parameters(self):
        for args in [(True, 1, "unit", 1), (5, 1, "unit", 1),
                     (6, 0, "unit", 1), (6, 1, "unknown", 1),
                     (6, 1, "singular", True), (6, 1, "singular", 0)]:
            with self.subTest(args=args), self.assertRaises(ValueError):
                make_certificate(*args)


if __name__ == "__main__":
    unittest.main()
