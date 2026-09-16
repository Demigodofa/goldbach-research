import json
import unittest
from pathlib import Path


EVIDENCE = Path(
    "evidence/"
    "mobius-moment-square-degree5-q46189-coordinate00-kernel-decomposition-audit.json")


class MobiusMomentSquareDegree5Q46189Coordinate00KernelTests(
        unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = json.loads(EVIDENCE.read_text(encoding="utf-8"))
        cls.rows = {
            row["role"]: row for row in cls.receipt["decomposition_rows"]
        }

    def test_receipt_preserves_boundaries(self):
        self.assertEqual(
            self.receipt["status"],
            "AUDIT_q46189_coordinate00_kernel_decomposition")
        self.assertTrue(
            self.receipt[
                "finite_coordinate00_kernel_decomposition_audit_only"])
        self.assertTrue(self.receipt["finite_diagnostic_only"])
        self.assertFalse(
            self.receipt["coordinate00_residue_gap_sign_theorem_proved"])
        self.assertFalse(
            self.receipt[
                "symbolic_coordinate_00_energy_ratio_theorem_proved"])
        self.assertFalse(self.receipt["goldbach_proved"])

    def test_q46189_negative_sign_is_off_diagonal_overpayment(self):
        row = self.rows["q46189_adverse"]
        classification = self.receipt["classification"]

        self.assertEqual(row["reduced_denominator"], 46189)
        self.assertTrue(row["finite_dirichlet_kernel_identity_verified"])
        self.assertAlmostEqual(
            row["component_half_margin_active_minus_half_full"],
            -112967899058.92188,
            delta=1.0)
        self.assertAlmostEqual(
            row["diagonal_half_contribution"],
            20990238237161.72,
            delta=1.0)
        self.assertAlmostEqual(
            row["off_diagonal_total_contribution"],
            -21103206136220.65,
            delta=1.0)
        self.assertLess(
            row["off_diagonal_total_contribution"],
            -row["diagonal_half_contribution"])
        self.assertTrue(
            classification[
                "q46189_negative_sign_from_off_diagonal_overpayment"])

    def test_weakest_replacement_survives_off_diagonal_drag(self):
        row = self.rows["weakest_positive_replacement"]
        classification = self.receipt["classification"]

        self.assertEqual(row["reduced_denominator"], 38038)
        self.assertTrue(row["finite_dirichlet_kernel_identity_verified"])
        self.assertAlmostEqual(
            row["ratio_minus_half"],
            0.07635340770691468)
        self.assertAlmostEqual(
            row["component_half_margin_active_minus_half_full"],
            4380137469743.5,
            delta=1.0)
        self.assertGreater(
            row["off_diagonal_total_contribution"],
            -row["diagonal_half_contribution"])
        self.assertTrue(
            classification["weakest_replacement_positive_after_off_diagonal"])

    def test_top_residue_gap_pairs_are_recorded(self):
        q_row = self.rows["q46189_adverse"]
        replacement = self.rows["weakest_positive_replacement"]

        self.assertEqual(
            q_row["top_negative_gap_pairs"][0]["circular_distance"], 245)
        self.assertEqual(
            q_row["top_positive_gap_pairs"][0]["circular_distance"], 134)
        self.assertLess(
            q_row["top_negative_gap_pairs"][0][
                "component_active_contribution"],
            0.0)
        self.assertGreater(
            q_row["top_positive_gap_pairs"][0][
                "component_active_contribution"],
            0.0)
        self.assertEqual(
            replacement["top_negative_gap_pairs"][0][
                "circular_distance"],
            68)
        self.assertEqual(
            replacement["top_positive_gap_pairs"][0][
                "circular_distance"],
            552)

    def test_bucket_and_next_action_are_recorded(self):
        row = self.rows["q46189_adverse"]
        action = self.receipt["candidate_next_action"]

        self.assertEqual(
            [bucket["bucket"]
             for bucket in row["distance_bucket_contributions"]],
            [
                "near_1_to_A",
                "middle_A_to_10A",
                "far_10A_to_100A",
                "tail_over_100A",
            ])
        self.assertEqual(
            action["name"],
            "coordinate-00 residue-gap sign theorem candidate")
        self.assertIn("off-diagonal Dirichlet-kernel total",
                      action["mechanism"])


if __name__ == "__main__":
    unittest.main()
