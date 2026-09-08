"""Independent checks of packed convolution and whole-block positivity."""
from copy import deepcopy
from itertools import product
import unittest

from packed_goldbach import (PrimeSquare, build_prime_square, certify_block, extend_prime_square,
                             positive_digit_mask, replay_certificate)
from redistribution import trial_prime


class PackedGoldbachTests(unittest.TestCase):
    def test_parallel_positive_mask_all_small_digit_patterns(self):
        for width, count in ((2, 8), (3, 5), (4, 3)):
            for digits in product(range(1 << (width - 1)), repeat=count):
                packed = sum(value << (width * i) for i, value in enumerate(digits))
                actual, all_bits = positive_digit_mask(packed, width, count)
                expected = sum(1 << (width * i + width - 1)
                               for i, value in enumerate(digits) if value > 0)
                self.assertEqual(actual, expected)
                self.assertEqual(actual == all_bits, all(value > 0 for value in digits))

    def test_sentinel_rejects_half_base_and_out_of_range(self):
        for value in (8, 128, 256):
            with self.assertRaises(ValueError):
                positive_digit_mask(value, 4, 2)

    def test_coefficients_match_independent_trial_prime_pair_counts(self):
        computed = build_prime_square(2004)
        mask = (1 << computed.digit_bits) - 1
        for target in range(6, 2005, 2):
            actual = (computed.packed_square >> (computed.digit_bits * (target // 2 - 1))) & mask
            expected = sum(trial_prime(a) and trial_prime(target - a)
                           for a in range(3, target - 2, 2))
            with self.subTest(target=target):
                self.assertEqual(actual, expected)
        receipt = certify_block(computed, 6, 1000)
        self.assertTrue(receipt["all_certified"])
        self.assertEqual(receipt["certified_target_count"], 1000)
        self.assertTrue(replay_certificate(receipt))

    def test_incremental_update_matches_fresh_square_and_keeps_old_counts(self):
        old = build_prime_square(2004, capacity_even=6004)
        updated = extend_prime_square(old, 4004)
        fresh = build_prime_square(4004, capacity_even=6004)
        self.assertEqual(updated, fresh)
        old_bits = old.digit_bits * (old.last_even // 2)
        self.assertEqual(updated.packed_square & ((1 << old_bits) - 1),
                         old.packed_square & ((1 << old_bits) - 1))
        self.assertTrue(certify_block(updated, 2006, 1000)["all_certified"])
        with self.assertRaises(ValueError):
            extend_prime_square(old, 6006)

    def test_receipt_tampering_fails_explicit_replay(self):
        receipt = certify_block(build_prime_square(100), 6, 48)
        for field, replacement in (("all_certified", False), ("target_count", 47),
                                   ("encoded_odd_prime_count", 0),
                                   ("prime_polynomial_sha256", "0" * 64)):
            altered = deepcopy(receipt)
            altered[field] = replacement
            with self.assertRaises(ValueError):
                replay_certificate(altered)

    def test_forged_internal_state_is_rejected_at_replay_gate(self):
        forged = PrimeSquare(14, 14, 8, 0, 0, sum(1 << (8 * k) for k in range(2, 7)))
        untrusted = certify_block(forged, 6, 5)
        self.assertTrue(untrusted["all_certified"])
        with self.assertRaises(ValueError):
            replay_certificate(untrusted)

    def test_target_and_block_input_contract(self):
        for value in (4, 5, 9, True, 100.0, -2):
            with self.assertRaises(ValueError):
                build_prime_square(value)
        computed = build_prime_square(100)
        for first, count in ((4, 1), (6, 49), (8, 0), (True, 2), (6, True)):
            with self.assertRaises(ValueError):
                certify_block(computed, first, count)


if __name__ == "__main__":
    unittest.main()
