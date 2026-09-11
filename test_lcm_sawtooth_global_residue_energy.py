import unittest

from lcm_sawtooth_global_residue_energy import (
    global_residue_energy_receipt,
)


class LcmSawtoothGlobalResidueEnergyTests(unittest.TestCase):
    def test_packet_square_is_bounded_by_active_window_l2(self):
        receipt = global_residue_energy_receipt(101, 10, 10, 12, 3, 12)
        self.assertGreaterEqual(
            receipt["active_window_Q_weighted_l2_over_complete_squared"],
            receipt["packet_Q_weighted_square_over_complete_squared"])
        self.assertAlmostEqual(
            receipt["packet_square_over_active_window_l2"],
            receipt["packet_Q_weighted_square_over_complete_squared"]
            / receipt[
                "active_window_Q_weighted_l2_over_complete_squared"])
        self.assertAlmostEqual(
            receipt[
                "row_count_scaled_packet_square_over_active_window_l2"],
            10 * receipt["packet_square_over_active_window_l2"])
        self.assertLess(receipt["lag_expansion_reconstruction_error"], 1e-12)
        self.assertAlmostEqual(
            sum(value for _, value in receipt[
                "normalized_aggregate_lag_contributions"]),
            receipt[
                "row_count_scaled_packet_square_over_active_window_l2"] - 1)
        self.assertTrue(
            0 <= receipt["top_five_absolute_lag_mass_fraction"] <= 1)
        self.assertTrue(
            0 <= receipt["first_five_absolute_lag_mass_fraction"] <= 1)
        self.assertLess(
            receipt["row_gram_constant_direction_reconstruction_error"],
            1e-12)
        self.assertTrue(1 <= receipt["row_gram_effective_rank"] <= 10)
        self.assertEqual(receipt["rademacher_sign_probe_count"], 16384)
        lower, median, upper = receipt[
            "rademacher_sign_probe_central_95_interval"]
        self.assertLess(lower, median)
        self.assertLess(median, upper)
        self.assertTrue(
            0 < receipt["constant_direction_sign_probe_percentile"] <= 1)
        self.assertTrue(
            0 <= receipt["top_five_positive_packet_excess_fraction"] <= 1)
        self.assertLess(
            receipt["packet_excess_reconstruction_relative_error"], 1e-12)
        self.assertTrue(
            receipt["finite_global_residue_energy_measurement"])
        self.assertFalse(receipt["window_l2_equidistribution_bound_proved"])
        self.assertFalse(receipt["row_mean_cancellation_bound_proved"])

    def test_fixture_without_high_Q_packets_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "no high-Q"):
            global_residue_energy_receipt(101, 24, 24, 36, 3, 12)


if __name__ == "__main__":
    unittest.main()
