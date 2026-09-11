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
        self.assertAlmostEqual(
            receipt["high_Q_net_over_absolute"],
            receipt["high_Q_within_Q_residual_over_pair_envelope"]
            * receipt["high_Q_across_Q_residual"])
        self.assertTrue(0 <= receipt["high_Q_across_Q_residual"] <= 1)
        self.assertTrue(
            0 <= receipt["high_Q_within_Q_residual_over_pair_envelope"] <= 1)
        shares = receipt["high_Q_top_1_5_10_20_packet_shares"]
        self.assertTrue(all(
            shares[index] <= shares[index + 1]
            for index in range(len(shares) - 1)))
        self.assertGreaterEqual(receipt["high_Q_half_mass_packet_count"], 1)
        self.assertGreaterEqual(
            receipt["high_Q_ninety_percent_mass_packet_count"],
            receipt["high_Q_half_mass_packet_count"])
        top_packets = receipt["top_high_Q_packets"]
        self.assertTrue(all(
            top_packets[index][1] >= top_packets[index + 1][1]
            for index in range(len(top_packets) - 1)))
        self.assertGreaterEqual(
            receipt["high_Q_weighted_cauchy_bound_over_complete"] + 1e-12,
            receipt["high_Q_fixed_Q_residual_over_complete"])
        self.assertGreaterEqual(
            receipt["high_Q_weighted_cauchy_slack_over_packet_sum"], 1)

    def test_conductor_sign_removal_preserves_energy_but_changes_boundary(self):
        actual = signed_difference_bin_receipt(101, 24, 24, 36, 3, 12)
        absolute = signed_difference_bin_receipt(
            101, 24, 24, 36, 3, 12, True)
        self.assertEqual(actual["conductor_coefficient_mode"], "actual")
        self.assertEqual(absolute["conductor_coefficient_mode"], "absolute")
        for actual_envelope, absolute_envelope in zip(
                actual["absolute_envelope_bins_over_complete"],
                absolute["absolute_envelope_bins_over_complete"]):
            self.assertAlmostEqual(actual_envelope, absolute_envelope)
        self.assertNotAlmostEqual(
            actual["total_boundary_over_complete"],
            absolute["total_boundary_over_complete"])

    def test_invalid_first_row_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "ell_first"):
            signed_difference_bin_receipt(101, 0, 24, 36, 3, 12)


if __name__ == "__main__":
    unittest.main()
