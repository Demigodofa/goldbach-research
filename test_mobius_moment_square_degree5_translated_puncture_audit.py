import json
import unittest
from pathlib import Path


EVIDENCE = Path(
    "evidence/mobius-moment-square-degree5-translated-puncture-audit.json")


class MobiusMomentSquareDegree5TranslatedPunctureAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = json.loads(EVIDENCE.read_text(encoding="utf-8"))

    def test_receipt_preserves_boundaries(self):
        self.assertEqual(
            self.receipt["status"],
            "AUDIT_degree5_translated_puncture")
        self.assertTrue(
            self.receipt["finite_translated_puncture_audit_only"])
        self.assertTrue(self.receipt["finite_diagnostic_only"])
        self.assertFalse(self.receipt["goldbach_proved"])
        self.assertFalse(
            self.receipt["source_window_implication_theorem_proved"])
        self.assertFalse(
            self.receipt["source_admissible_window_theorem_proved"])

    def test_lone_failure_is_isolated_puncture(self):
        self.assertEqual(self.receipt["puncture_count"], 1)
        self.assertEqual(self.receipt["nonconvex_puncture_count"], 1)
        self.assertTrue(
            self.receipt["single_failure_nonconvex_puncture_detected"])
        puncture = self.receipt["puncture_summaries"][0]
        self.assertEqual(puncture["scale_modulus"], 149)
        self.assertEqual(puncture["prime_modulus"], 163)
        self.assertEqual(puncture["label"], "00,12")
        self.assertEqual(puncture["source_active_row_start"], 32)
        self.assertEqual(puncture["failing_active_row_starts"], [1])
        self.assertEqual(puncture["passing_active_row_start_intervals"], [
            {"start": 0, "stop": 0},
            {"start": 2, "stop": 64},
        ])

    def test_neighbors_and_source_start_pass(self):
        puncture = self.receipt["puncture_summaries"][0]
        self.assertTrue(puncture["left_far_edge_passes"])
        self.assertTrue(puncture["right_neighbor_passes"])
        self.assertTrue(puncture["source_start_passes"])
        self.assertTrue(puncture["puncture_is_not_left_edge"])
        self.assertTrue(puncture["nonconvex_pass_set_detected"])
        self.assertEqual(puncture["distance_to_source_at_failure"], 31)
        self.assertEqual(puncture["distance_to_source_at_left_far_edge"], 32)
        self.assertAlmostEqual(
            puncture["failure_row"]["dominance_slack_above_one_half"],
            -0.0019533329245732256)
        self.assertGreater(
            puncture["left_far_edge_row"][
                "dominance_slack_above_one_half"],
            0.0)
        self.assertGreater(
            puncture["neighbor_rows"][1][
                "dominance_slack_above_one_half"],
            0.0)
        self.assertGreater(puncture["source_start_slack"], 0.0)

    def test_decision_rejects_distance_only_translated_window_rule(self):
        self.assertIn("not a distance-only translated-window rule",
                      self.receipt["decision"])
        self.assertIn("source construction",
                      self.receipt["prediction"])


if __name__ == "__main__":
    unittest.main()
