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
        self.assertTrue(
            receipt["finite_global_residue_energy_measurement"])
        self.assertFalse(receipt["window_l2_equidistribution_bound_proved"])
        self.assertFalse(receipt["row_mean_cancellation_bound_proved"])

    def test_fixture_without_high_Q_packets_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "no high-Q"):
            global_residue_energy_receipt(101, 24, 24, 36, 3, 12)


if __name__ == "__main__":
    unittest.main()
