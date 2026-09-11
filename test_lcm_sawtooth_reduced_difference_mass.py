import math
import unittest

import numpy as np

from lcm_sawtooth_reduced_difference_mass import (
    _reduced_difference_denominator,
    reduced_difference_mass_receipt,
)


class LcmSawtoothReducedDifferenceMassTests(unittest.TestCase):
    def test_reduced_denominator_divides_lcm_and_is_multiplier_invariant(self):
        left_d = np.array([6, 10, 15])
        left_k = np.array([1, 3, 2])
        right_d = np.array([10, 21, 14])
        right_k = np.array([1, 4, 3])
        reduced = _reduced_difference_denominator(
            left_d, left_k, right_d, right_k)
        common = np.lcm(left_d, right_d)
        self.assertTrue(np.all(common % reduced == 0))
        multiplier = 23
        multiplied = _reduced_difference_denominator(
            left_d, multiplier * left_k,
            right_d, multiplier * right_k)
        self.assertTrue(all(math.gcd(multiplier, int(x)) == 1 for x in common))
        np.testing.assert_array_equal(reduced, multiplied)

    def test_exact_positive_mass_is_normalized_and_parseval_matches(self):
        receipt = reduced_difference_mass_receipt(
            101, 36, 24, 3, 12, exact=True)
        q_fractions = receipt["reduced_Q_energy_fractions"]
        lcm_fractions = receipt["conductor_lcm_energy_fractions"]
        self.assertTrue(all(
            q_fractions[index] >= q_fractions[index + 1]
            for index in range(2)))
        self.assertTrue(all(
            0 <= q_fractions[index] <= lcm_fractions[index] <= 1
            for index in range(3)))
        self.assertLess(receipt["frequency_parseval_relative_error"], 1e-12)
        self.assertTrue(receipt["exact_enumeration"])
        self.assertFalse(
            receipt["positive_frequency_denominator_sparsity_proved"])
        self.assertFalse(
            receipt["signed_difference_modulus_cancellation_proved"])

    def test_invalid_inputs_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "prime"):
            reduced_difference_mass_receipt(100, 36, 24, 3, 12)


if __name__ == "__main__":
    unittest.main()
