"""Independent arithmetic checks of the smaller-input cubic block bound."""
from math import isqrt
import unittest
from unittest.mock import patch

from count_bootstrap import build_chain
from cubic_batch import batch_from_counts, canonical_batch
from cubic_sieve import cubic_sieve_count, exact_floor_cuberoot


def least_odd_factor(n: int) -> int:
    return next((p for p in range(3, isqrt(n) + 1, 2) if n % p == 0), n)


class CubicBatchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.counts = build_chain([26, 626])["ordered_counts"]

    def test_all_rows_match_event_masks_through_2000(self):
        first = 6
        while first <= 2000:
            z = exact_floor_cuberoot(first - 3)
            exclusive = (z + 1) ** 3 + 3
            last = min(2000, 2 * ((exclusive - 1) // 2))
            batch = batch_from_counts(self.counts, first, (last - first) // 2 + 1)
            for row in batch["rows"]:
                with self.subTest(target=row["target_even"]):
                    reference = cubic_sieve_count(row["target_even"])
                    self.assertEqual((row["M"], row["S1"], row["raw"]), (
                        reference["M_after_pre_sieve"], reference["S1"],
                        reference["union_bound_raw"]))
                    self.assertLessEqual(row["raw"], reference["result"])
            first = last + 2

    def test_same_factor_diagonal_and_distinct_factor_pairs_by_trial_division(self):
        batch = batch_from_counts(self.counts, 220, 63)
        rows = {row["target_even"]: row for row in batch["rows"]}
        for target in (242, 264, 290, 338):
            z = exact_floor_cuberoot(target - 3)
            expected_m = expected_ac = expected_same = 0
            for a in range(3, target - 2, 2):
                b = target - a
                q, r = least_odd_factor(a), least_odd_factor(b)
                if (q == a or q > z) and (r == b or r > z):
                    expected_m += 1
                    expected_ac += q != a
                    expected_same += q != a and r != b and q == r
            with self.subTest(target=target):
                row = rows[target]
                self.assertEqual((row["M"], row["AC"], row["same_factor"]),
                                 (expected_m, expected_ac, expected_same))
        self.assertGreaterEqual(rows[242]["same_factor"], 1)  # 121+121
        self.assertGreaterEqual(rows[264]["same_factor"], 2)  # 121+143 and reflection

    def test_band_edges_and_insufficient_prefix_are_rejected_before_convolution(self):
        for first, count in ((28, 2), (1000000, 3), (True, 1), (7, 1), (6, 0)):
            with self.subTest(first=first, count=count), self.assertRaises(ValueError):
                batch_from_counts(self.counts, first, count)
        with self.assertRaises(ValueError):
            batch_from_counts([1], 264, 1)

    def test_binary_consistency_is_required_but_not_mislabeled_as_primality(self):
        bad = self.counts.copy()
        bad[1] += 1
        with self.assertRaises(ValueError):
            batch_from_counts(bad, 264, 1)
        result = batch_from_counts(self.counts, 264, 1)
        self.assertIn("conditional", result["input_meaning"])

    def test_canonical_pipeline_uses_no_standard_sieve_event_masks_or_prime_square(self):
        def forbidden(*_args, **_kwargs):
            raise AssertionError("forbidden high-target oracle or reference route called")
        with patch("redistribution.sieve", forbidden), patch("cubic_sieve.sieve", forbidden), \
                patch("packed_goldbach.sieve", forbidden), \
                patch("packed_goldbach.build_prime_square", forbidden), \
                patch("cubic_sieve.event_masks", forbidden):
            result = canonical_batch([26, 100], 220, 63)
        self.assertEqual(result["input_prefix_end"], 100)
        self.assertEqual(result["target_count"], 63)
        self.assertIn("canonical", result["input_meaning"])
        self.assertGreaterEqual(result["seconds"]["complete_total"],
                                result["seconds"]["input_generation"])


if __name__ == "__main__":
    unittest.main()
