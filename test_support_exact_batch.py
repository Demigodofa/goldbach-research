"""Independent support/diagonal, coefficient-orientation and input-meaning checks."""
from itertools import product
import unittest
from unittest.mock import patch

from parity_bound_bootstrap import generate_prefix
from redistribution import trial_prime
from support_exact_batch import (_shape, reflected_counts, required_prefix_end,
                                  support_exact_batch)


class SupportExactTests(unittest.TestCase):
    def test_all_small_binary_correlations_include_zero_diagonal_and_edges(self):
        for slots in range(1, 5):
            arrays = [bytearray(bits) for bits in product((0, 1), repeat=slots)]
            for left in arrays:
                for right in arrays:
                    actual = reflected_counts(left, right, 6, slots)
                    expected = [sum(left[i]*right[k-i] for i in range(k+1))
                                for k in range(slots)]
                    self.assertEqual(actual, expected)
                    self.assertEqual(reflected_counts(left, right, 2*slots+4, 1), expected[-1:])

    def test_actual_counts_and_parities_on_complete_small_range(self):
        flags = [trial_prime(n) for n in range(501)]
        # Each target uses only its own shorter canonical parity prefix.
        for target in range(8, 501, 2):
            endpoint = required_prefix_end(target, 1)
            self.assertLess(endpoint, target)
            prefix = generate_prefix(endpoint)["lower_bounds"]
            result = support_exact_batch(prefix, target, 1)
            expected = sum(flags[p] and flags[target-p] for p in range(3, target-2, 2))
            self.assertEqual(result["counts"], [expected])
            self.assertEqual(expected % 2, flags[target//2])
        # The new exact output differs from the old cubic-cutoff lower bound.
        self.assertEqual(generate_prefix(24)["lower_bounds"][-1], 4)
        prefix = generate_prefix(required_prefix_end(24, 1))["lower_bounds"]
        self.assertEqual(support_exact_batch(prefix, 24, 1)["counts"], [6])

    def test_nontrivial_band_negative_input_and_no_prime_or_count_oracle(self):
        first, count = 220, 141  # crosses multiple old cube-root bands
        endpoint = required_prefix_end(first, count)
        prefix = generate_prefix(endpoint)["lower_bounds"]
        lowered = [value-100000 for value in prefix]
        with patch("packed_goldbach.build_prime_square", side_effect=AssertionError("full square")), \
                patch("redistribution.sieve", side_effect=AssertionError("ordinary sieve")), \
                patch("cubic_batch.build_chain", side_effect=AssertionError("count bootstrap")), \
                patch("count_reconstruction.recover_binary_flags", side_effect=AssertionError("exact counts")):
            normal = support_exact_batch(prefix, first, count)
            negative = support_exact_batch(lowered, first, count)
        self.assertEqual(normal["counts"], negative["counts"])
        self.assertGreater(normal["surviving_composites"], 0)
        for i, actual in enumerate(normal["counts"]):
            n = first+2*i
            expected = sum(trial_prime(p) and trial_prime(n-p) for p in range(3, n-2, 2))
            self.assertEqual(actual, expected)
        self.assertEqual(required_prefix_end(1002000, 1000), 2830)
        self.assertEqual(_shape(1002000, 1000), (1003998, 1003995, 708, 1415))

    def test_support_boundary_insufficient_input_and_malformed_values(self):
        # At equality C(121) can produce the diagonal121+121; strict support is required.
        self.assertEqual(_shape(240, 1, 10)[2], 10)
        with self.assertRaises(ValueError):
            _shape(242, 1, 10)
        self.assertEqual(_shape(242, 1)[2], 11)
        with self.assertRaises(ValueError):
            _shape(30, 1, 2)  # a triprime can survive
        for first, count in ((True, 1), (7, 1), (8, 0), (8, True), (8.0, 1)):
            with self.assertRaises(ValueError):
                required_prefix_end(first, count)
        with self.assertRaises(ValueError):
            required_prefix_end(6, 1)
        for cutoff in (True, 0, 4.0):
            with self.assertRaises(ValueError):
                _shape(30, 1, cutoff)
        with self.assertRaises(ValueError):
            support_exact_batch([1], 50, 1)
        with self.assertRaises(ValueError):
            support_exact_batch(generate_prefix(20)["lower_bounds"], 20, 1)
        for left, right, first, count in ((bytearray([2]), bytearray([0]), 6, 1),
                (bytearray(), bytearray(), 6, 1), (bytearray([1]), bytearray([1, 0]), 6, 1),
                (bytearray([1]), bytearray([1]), 8, 1),
                (bytearray([1]), bytearray([1]), True, 1),
                (bytearray([1]), bytearray([1]), 6, True)):
            with self.assertRaises(ValueError):
                reflected_counts(left, right, first, count)


if __name__ == "__main__":
    unittest.main()
