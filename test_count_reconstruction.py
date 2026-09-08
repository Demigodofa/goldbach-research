"""Finite checks for formal ordered-count square-root recovery."""
import unittest

from count_reconstruction import (ordered_count_prefix_from_binary_flags,
                                  recover_binary_flags)
from redistribution import trial_prime


class CountReconstructionTests(unittest.TestCase):
    def test_direct_trial_prime_counts_through_2004_recover_flags_through_2001(self):
        flags = [int(trial_prime(2 * k + 1)) for k in range(1, 1001)]
        counts = [sum(trial_prime(a) and trial_prime(target - a)
                      for a in range(3, target - 2, 2))
                  for target in range(6, 2005, 2)]
        self.assertEqual(counts, ordered_count_prefix_from_binary_flags(flags))
        self.assertEqual(counts[0], 1)
        self.assertEqual(recover_binary_flags(counts), flags)

    def test_single_g6_recovers_only_three(self):
        self.assertEqual(recover_binary_flags([1]), [1])

    def test_rejects_malformed_negative_noninteger_odd_and_nonbinary_inputs(self):
        cases = ([1, -1], [1, 1.0], [1, True], [1, 1], [1, 4], [], (1,))
        for counts in cases:
            with self.subTest(counts=counts):
                with self.assertRaises(ValueError):
                    recover_binary_flags(counts)
        for flags in ([], [0], [1, 2], [1, False], (1,)):
            with self.subTest(flags=flags):
                with self.assertRaises(ValueError):
                    ordered_count_prefix_from_binary_flags(flags)

    def test_toy_nonprime_binary_sequence_passes_algebra_but_is_not_prime_evidence(self):
        # The fourth flag labels 9, deliberately set to one despite 9 being composite.
        toy_flags = [1, 1, 0, 1, 0, 1]
        counts = ordered_count_prefix_from_binary_flags(toy_flags)
        self.assertEqual(recover_binary_flags(counts), toy_flags)
        self.assertFalse(trial_prime(9))

    def test_positivity_booleans_do_not_replace_exact_counts(self):
        left = ordered_count_prefix_from_binary_flags([1, 1, 0, 1])
        right = ordered_count_prefix_from_binary_flags([1, 1, 1, 0])
        self.assertNotEqual(left, right)
        self.assertEqual([count > 0 for count in left],
                         [count > 0 for count in right])
        self.assertNotEqual(recover_binary_flags(left), recover_binary_flags(right))


if __name__ == "__main__":
    unittest.main()
