"""Independent finite tests for asymmetric segmented packed certificates."""
from copy import deepcopy
import unittest

from redistribution import trial_prime
from segmented_packed import (_block_inputs, certify_block, output_document,
                              replay_certificate)


def restricted_count(target: int, cap: int, first_even: int) -> int:
    return sum(trial_prime(a) and trial_prime(target - a)
               for a in range(3, min(cap, first_even - 3) + 1, 2))


class SegmentedPackedTests(unittest.TestCase):
    def test_small_coefficients_exactly_match_restricted_pair_counts(self):
        receipt = certify_block(6, 100, 97, include_counts=True)
        for index, count in enumerate(receipt["restricted_ordered_counts"]):
            target = receipt["first_even"] + 2 * index
            self.assertEqual(count, restricted_count(target, 97, 6))
        self.assertEqual(receipt["restricted_ordered_counts"][:2], [1, 1])
        self.assertEqual(replay_certificate(receipt)["status"], "passed")

    def test_moderate_range_agrees_with_trial_primality_bounds_and_coverage(self):
        receipt = certify_block(50_000, 200, 1_000, include_counts=True)
        covered = []
        for index, count in enumerate(receipt["restricted_ordered_counts"]):
            target = 50_000 + 2 * index
            direct_restricted = restricted_count(target, 1_000, 50_000)
            self.assertEqual(count, direct_restricted)
            covered.append(count > 0)
        self.assertEqual(receipt["unresolved"],
                         [50_000 + 2 * i for i, value in enumerate(covered) if not value])

    def test_segment_bounds_have_odd_endpoints_and_nonprime_gaps(self):
        data = _block_inputs(124, 10, 31)
        self.assertEqual(data["segment_lo"] % 2, 1)
        self.assertEqual(data["segment_hi"] % 2, 1)
        self.assertNotIn(121, data["segment_primes"])
        self.assertNotIn(125, data["segment_primes"])
        self.assertNotIn(129, data["segment_primes"])

    def test_small_and_square_start_segments_preserve_real_primes(self):
        small = certify_block(6, 4, 1_000, include_counts=True)
        self.assertEqual(small["palette_min"], 3)
        self.assertEqual(small["palette_max"], 3)
        self.assertEqual(small["restricted_ordered_counts"][:2], [1, 1])
        square_start = _block_inputs(130, 1, 3)
        self.assertEqual((square_start["segment_lo"], square_start["segment_hi"]), (127, 127))
        self.assertEqual(square_start["segment_primes"], [127])

    def test_insufficient_palette_is_explicitly_unresolved_not_a_disproof(self):
        receipt = certify_block(510_510, 1, 17)
        self.assertFalse(receipt["all_positive"])
        self.assertEqual(receipt["unresolved"], [510_510])
        self.assertNotIn("restricted_ordered_counts", receipt)
        self.assertTrue(trial_prime(29))
        self.assertTrue(trial_prime(510_481))
        self.assertEqual(29 + 510_481, 510_510)

    def test_replay_rejects_tampering_and_bad_parameter_types(self):
        receipt = certify_block(100, 12, 29, include_counts=True)
        for key, value in (("first_even", 102), ("palette_prime_sha256", "0" * 64),
                           ("restricted_ordered_counts", [0] * 12),
                           ("all_positive", "yes")):
            tampered = deepcopy(receipt)
            tampered[key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                replay_certificate(tampered)
        for first, count, cap in ((True, 1, 3), (6, True, 3), (6, 1, True),
                                  (5, 1, 3), (6, 0, 3), (6, 1, 2)):
            with self.subTest(parameters=(first, count, cap)), self.assertRaises(ValueError):
                certify_block(first, count, cap)

    def test_exported_wrapper_keeps_nested_receipt_replayable(self):
        exported = output_document(100, 12, 29)
        self.assertEqual(replay_certificate(exported["receipt"])["status"], "passed")
        with self.assertRaises(ValueError):
            replay_certificate(exported)


if __name__ == "__main__":
    unittest.main()
