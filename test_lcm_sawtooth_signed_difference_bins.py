import unittest

from lcm_sawtooth_signed_difference_bins import (
    signed_difference_bin_receipt,
)


class LcmSawtoothSignedDifferenceBinTests(unittest.TestCase):
    def test_bins_reconstruct_boundary_and_respect_absolute_envelope(self):
        receipt = signed_difference_bin_receipt(101, 24, 24, 36, 3, 12)
        self.assertLess(
            receipt["bin_reconstruction_error_over_complete"], 1e-11)
        self.assertLess(
            receipt["ordered_pair_imaginary_error_over_complete"], 1e-11)
        for signed, absolute in zip(
                receipt["signed_boundary_bins_over_complete"],
                receipt["absolute_envelope_bins_over_complete"]):
            self.assertLessEqual(abs(signed), absolute + 1e-12)
        self.assertFalse(receipt["signed_boundary_asymptotic_bound_proved"])
        self.assertFalse(receipt["prime_averaged_cancellation_proved"])

    def test_high_Q_cancellation_is_measured_at_first_project_scale(self):
        receipt = signed_difference_bin_receipt(251, 46, 46, 69, 4, 20)
        self.assertGreater(receipt["high_Q_absolute_over_complete"], 4)
        self.assertLess(receipt["high_Q_net_over_absolute"], .01)

    def test_invalid_first_row_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "ell_first"):
            signed_difference_bin_receipt(101, 0, 24, 36, 3, 12)


if __name__ == "__main__":
    unittest.main()
