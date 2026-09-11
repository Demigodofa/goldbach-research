import unittest

from lcm_sawtooth_kloosterman_tensor_transfer import (
    _tensor_conditioned_difference_entry,
    kloosterman_tensor_transfer_receipt,
)


class KloostermanTensorTransferTests(unittest.TestCase):
    def test_forbidden_difference_is_zero(self):
        self.assertEqual(
            _tensor_conditioned_difference_entry(10010, 182, 1, 7), 0)

    def test_transfer_across_leading_lags(self):
        receipt = kloosterman_tensor_transfer_receipt()
        self.assertEqual(receipt["prime_factors"], (2, 5, 7, 11, 13))
        self.assertEqual(receipt["lags"], (140, 154, 156, 182, 240))
        self.assertEqual(receipt["tested_nonzero_kernel_entries"], 24528)
        self.assertLess(receipt["maximum_entry_relative_error"], 1e-12)
        self.assertTrue(receipt[
            "exact_finite_crt_kloosterman_tensor_identity_passes"])
        expected_degrees = {140: 99, 154: 33, 156: 135, 182: 27, 240: 495}
        for lag, degree in expected_degrees.items():
            row = receipt["rows"][lag]
            self.assertEqual(row["zero_quotient_frequency_degree"], degree)
            self.assertLessEqual(
                row["fully_nonresonant_to_zero_degree_ratio"], 1)
        self.assertFalse(receipt["uniform_source_sum_estimate_proved"])
        self.assertFalse(receipt["signed_prime_correlation_proved"])

    def test_guards(self):
        with self.assertRaises(ValueError):
            kloosterman_tensor_transfer_receipt(period=12)
        with self.assertRaises(ValueError):
            kloosterman_tensor_transfer_receipt(lags=(0,))


if __name__ == "__main__":
    unittest.main()
