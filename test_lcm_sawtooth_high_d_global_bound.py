import unittest

from lcm_sawtooth_high_d_global_bound import (
    high_conductor_global_bound_receipt,
)


class LcmSawtoothHighDGlobalBoundTests(unittest.TestCase):
    def test_separated_diagonal_returns_to_pair_cauchy_envelope(self):
        receipt = high_conductor_global_bound_receipt(101, 70, 4, 20)
        self.assertLessEqual(
            receipt["positive_separated_high_conductor_cell_majorant"],
            receipt["exact_diagonal_cauchy_envelope"] + 1e-10)
        self.assertAlmostEqual(
            receipt["exact_diagonal_cauchy_envelope"],
            receipt["existing_diagonal_probe_cauchy_envelope"])
        self.assertLessEqual(
            receipt["actual_complete_high_conductor_energy"],
            receipt["proved_complete_high_conductor_upper_bound"] + 1e-10)
        self.assertTrue(
            receipt["common_cells_partition_lcm_pairs_proved"])
        self.assertTrue(receipt["common_cell_partition_counts_verified"])
        self.assertTrue(
            receipt[
                "signed_cells_bounded_by_positive_cell_majorants_proved"])
        self.assertTrue(
            receipt["positive_separated_cell_majorant_bound_proved"])
        self.assertTrue(
            receipt["complete_high_conductor_pair_mass_bound_proved"])
        self.assertFalse(receipt["signed_prime_correlation_estimate_proved"])

    def test_project_range_has_active_high_conductors(self):
        receipt = high_conductor_global_bound_receipt(251, 69, 4, 20)
        self.assertGreater(receipt["active_high_conductor_count"], 0)
        self.assertGreater(
            receipt["uniform_high_conductor_collapse_factor"], 1)

    def test_invalid_inputs_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "prime"):
            high_conductor_global_bound_receipt(100, 70, 4, 20)


if __name__ == "__main__":
    unittest.main()
