import json
import unittest
from pathlib import Path


EVIDENCE = Path("evidence/goldbach-three-candidate-synthesis-audit.json")


class GoldbachThreeCandidateSynthesisTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = json.loads(EVIDENCE.read_text(encoding="utf-8"))

    def test_preserves_boundaries(self):
        self.assertEqual(
            self.receipt["status"], "AUDIT_goldbach_three_candidate_synthesis")
        self.assertTrue(self.receipt["finite_synthesis_only"])
        self.assertTrue(self.receipt["new_to_this_task_candidate_synthesis"])
        self.assertFalse(self.receipt["universal_raw_pointwise_theorem_proved"])
        self.assertFalse(self.receipt["source_gap_curvature_theorem_proved"])
        self.assertFalse(self.receipt["goldbach_proved"])

    def test_three_attempts_are_recorded(self):
        attempts = self.receipt["attempts"]
        self.assertEqual(len(attempts), 3)
        self.assertEqual(attempts[0]["state"], "live_candidate_unproved")
        self.assertEqual(attempts[1]["state"],
                         "falsified_as_universal_sign_rule")
        self.assertEqual(attempts[2]["state"], "triage_statistic_only")

    def test_curvature_attempt_failed_globally(self):
        curvature = self.receipt["attempts"][1]["current_evidence"]
        self.assertEqual(curvature["checked_row_count"], 34)
        self.assertEqual(curvature["valid_prediction_count"], 32)
        self.assertEqual(curvature["match_count"], 13)
        self.assertEqual(curvature["mismatch_count"], 19)
        self.assertLess(curvature["match_count"], curvature["mismatch_count"])
        self.assertGreater(curvature["q38038"]["first_cross_non_middle"], 0)
        self.assertLess(curvature["q41990"]["first_cross_non_middle"], 0)

    def test_next_action_keeps_failed_baseline(self):
        self.assertIn("all-row source-block interaction sign audit",
                      self.receipt["candidate_next_action"])
        self.assertIn("failed single-feature baseline",
                      self.receipt["candidate_next_action"])


if __name__ == "__main__":
    unittest.main()
