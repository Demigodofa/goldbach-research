import unittest

from lcm_sawtooth_transition_core import transition_common_core_probe


class LcmSawtoothTransitionCoreTests(unittest.TestCase):
    def test_transition_split_reconstructs_energy(self):
        receipt = transition_common_core_probe(101, 70, 4, 20)
        self.assertAlmostEqual(receipt["component_reconstruction_error"], 0)
        self.assertAlmostEqual(
            receipt["assignment_split_total_energy"],
            receipt["transition_complete_energy"])
        self.assertAlmostEqual(
            receipt["assignment_split_reconstruction_error"], 0)
        self.assertGreater(
            receipt["positive_weight_transition_coordinate_count"], 0)
        self.assertTrue(receipt["transition_fixed_common_split_exact"])
        self.assertTrue(
            receipt["controlled_cells_have_fixed_common_polylog_bound"])
        self.assertAlmostEqual(sum(
            row[2] for row in receipt[
                "core_positive_diagonal_by_common"]), 1)
        self.assertTrue(
            receipt[
                "double_low_assignments_excluded_when_B_gt_V_squared"])
        self.assertTrue(
            receipt[
                "base_supported_assignments_have_polylog_residual_bound"])
        self.assertFalse(receipt["one_sided_assignment_bound_proved"])
        self.assertFalse(receipt["criterion_residual_core_bound_proved"])

    def test_invalid_modulus_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "prime"):
            transition_common_core_probe(100, 70, 4, 20)


if __name__ == "__main__":
    unittest.main()
