import unittest

import numpy as np

from lcm_sawtooth_window_interference import (
    normalized_interval_kernel,
    window_packet_interference_receipt,
)


class LcmSawtoothWindowInterferenceTests(unittest.TestCase):
    def test_complex_packets_split_into_diagonal_and_off_diagonal(self):
        left = np.array((1 + 2j, -3 + 1j, 2 - 4j, 5 + 0j, -1 - 2j))
        right = np.array((2 - 1j, 4 + 3j, -2 + 2j, 1 - 5j, 3 + 1j))
        receipt = window_packet_interference_receipt(left, right, 3, 4)
        self.assertLess(abs(receipt["kernel_identity_residual"]), 1e-12)
        self.assertLess(
            abs(receipt["diagonal_off_diagonal_residual"]), 1e-12)
        self.assertLessEqual(
            receipt["maximum_interval_kernel_bound_error"], 1e-14)
        self.assertTrue(receipt[
            "exact_window_interference_decomposition_proved"])
        self.assertFalse(receipt["signed_prime_correlation_proved"])

    def test_complete_period_kills_off_diagonal_kernel(self):
        for difference in range(1, 7):
            self.assertLess(
                abs(normalized_interval_kernel(difference, 7, 5, 7)),
                1e-14)

    def test_guards_kernel_and_packet_inputs(self):
        with self.assertRaises(ValueError):
            normalized_interval_kernel(1, 1, 1, 1)
        with self.assertRaises(ValueError):
            normalized_interval_kernel(1, 7, 1, 0)
        with self.assertRaises(ValueError):
            window_packet_interference_receipt(
                np.ones(2), np.ones(3), 1, 1)


if __name__ == "__main__":
    unittest.main()
