import json
import unittest
from pathlib import Path


EVIDENCE = Path(
    "evidence/"
    "mobius-moment-square-degree5-q46189-source-matrix-margin-audit.json")


class MobiusMomentSquareDegree5Q46189SourceMatrixMarginTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = json.loads(EVIDENCE.read_text(encoding="utf-8"))

    def test_receipt_preserves_boundaries(self):
        self.assertEqual(
            self.receipt["status"], "AUDIT_q46189_source_matrix_margin")
        self.assertTrue(self.receipt["finite_diagnostic_only"])
        self.assertFalse(self.receipt["source_matrix_margin_theorem_proved"])
        self.assertFalse(
            self.receipt["source_block_interaction_sign_theorem_proved"])
        self.assertFalse(self.receipt["goldbach_proved"])

    def test_best_margin_correlations_are_weak(self):
        best = self.receipt[
            "best_feature_by_target"]["row_margin_above_failure"]
        best_matrix = self.receipt[
            "best_matrix_feature_by_target"]["row_margin_above_failure"]
        self.assertEqual(best["feature"], "missing_count")
        self.assertAlmostEqual(
            best["pearson"], 0.32654799306706145, places=15)
        self.assertEqual(best_matrix["feature"], "tension_sum")
        self.assertAlmostEqual(
            best_matrix["pearson"], -0.2169202637521853, places=15)
        self.assertFalse(
            self.receipt["classification"][
                "strong_input_feature_margin_correlation_found"])
        self.assertFalse(
            self.receipt["classification"][
                "strong_matrix_feature_margin_correlation_found"])

    def test_tightest_row_remains_q38038(self):
        tightest = self.receipt["tightest_rows_by_margin"][0]
        self.assertEqual(tightest["reduced_denominator"], 38038)
        self.assertAlmostEqual(
            tightest["row_margin_above_failure"],
            0.15270681541382948,
            places=15,
        )

    def test_next_action_returns_to_raw_q286(self):
        action = self.receipt["candidate_next_action"]
        self.assertEqual(action["name"],
                         "return to q286 raw adverse-envelope margin")
        self.assertIn("normalization-dependent", action["prediction"])
        self.assertIn("unknown prime-pair mass", action["falsifier"])


if __name__ == "__main__":
    unittest.main()
