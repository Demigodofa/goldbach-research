import unittest

from joint_full_frame_cancellation import (
    joint_multiband_full_frame_probe,
    project_joint_full_frame_exponent_budget,
)
from multiband_full_frame_probe import multiband_full_frame_probe


class JointFullFrameCancellationTests(unittest.TestCase):
    def test_one_prime_one_row_matches_existing_probe(self):
        old = multiband_full_frame_probe(1009, 9, 8, 64)
        joint = joint_multiband_full_frame_probe(
            (1009,), 5, 9, 1, 8, 64)
        self.assertAlmostEqual(
            old["ideal_over_block_frame_min"],
            joint["ideal_over_frame_eigenvalue_min"], places=10)
        self.assertAlmostEqual(
            old["exact_over_block_frame_min"],
            joint["actual_exact_over_frame_eigenvalue_min"], places=10)

    def test_row_and_prime_aggregation_preserves_positive_exact_gram(self):
        receipt = joint_multiband_full_frame_probe(
            (1009, 1013, 1019), 5, 9, 4, 8, 48)
        self.assertGreater(receipt["actual_exact_over_frame_eigenvalue_min"], 0)
        self.assertGreater(receipt["ideal_over_frame_eigenvalue_min"], 0)
        self.assertLessEqual(
            receipt["proved_exact_over_frame_lower_via_weyl"],
            receipt["actual_exact_over_frame_eigenvalue_min"] + 1e-10)
        self.assertFalse(receipt["joint_full_frame_asymptotic_theorem"])

    def test_strict_combined_thresholds(self):
        below = project_joint_full_frame_exponent_budget(.326)
        active_edge = project_joint_full_frame_exponent_budget(49 / 150)
        full_edge = project_joint_full_frame_exponent_budget(109 / 300)
        self.assertTrue(below["joint_aggregate_components_power_saving"])
        self.assertFalse(below["all_lag_energy_transfer_proved"])
        self.assertFalse(below["previous_complete_assembly_supported"])
        self.assertFalse(active_edge["joint_active_endpoint_power_saving"])
        self.assertFalse(full_edge["joint_full_frame_power_saving"])
        self.assertAlmostEqual(
            below["joint_full_frame_worst_exponent"], -.084, places=12)

    def test_invalid_inputs_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "prime"):
            joint_multiband_full_frame_probe(
                (1001,), 5, 9, 1, 8, 64)
        with self.assertRaises(ValueError):
            project_joint_full_frame_exponent_budget(True)


if __name__ == "__main__":
    unittest.main()
