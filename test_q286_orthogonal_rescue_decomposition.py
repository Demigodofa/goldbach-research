import json
import unittest
from pathlib import Path


class Q286OrthogonalRescueDecompositionTests(unittest.TestCase):
    def test_decomposition_is_narrow_residual_obligation(self):
        path = Path("evidence/q286-orthogonal-rescue-decomposition.json")
        receipt = json.loads(path.read_text(encoding="utf-8"))
        self.assertFalse(receipt["goldbach_proved"])
        self.assertIn("gamma_full_centered", receipt["definition"])
        self.assertIn("<nu_N,h_a>", receipt["prediction"])

        summary = receipt["summary"]
        self.assertEqual(summary["selected_target_count"], 7)
        self.assertEqual(summary["selected_residue_count"], 7)
        self.assertLess(
            summary["orthogonality_error_summary"]["maximum"], 1e-12)
        self.assertGreater(
            summary["projection_alpha_summary"]["minimum"], 0.99)
        self.assertLess(
            summary["projection_alpha_summary"]["maximum"], 1.03)
        self.assertEqual(summary["aligned_only_positive_target_count"], 7)
        self.assertEqual(summary["actual_full_positive_target_count"], 5)
        self.assertEqual(
            summary["orthogonal_residual_erases_aligned_margin_targets"],
            [14138, 14996])
        self.assertEqual(summary["actual_bad_branch_targets"], [14138, 14996])

        for row in receipt["target_rows"]:
            reconstructed = (
                row["aligned_only_full_action_to_principal"]
                + row["orthogonal_residual_action_to_principal"])
            self.assertAlmostEqual(
                reconstructed,
                row["actual_full_action_to_principal_ratio"])
            self.assertTrue(row["aligned_only_positive"])


if __name__ == "__main__":
    unittest.main()
