import json
import unittest
from pathlib import Path


class Q286WbssSignedDiscrepancyProblemTests(unittest.TestCase):
    def test_receipt_preserves_boundaries(self):
        receipt = json.loads(Path(
            "evidence/q286-wbss-signed-discrepancy-problem.json"
        ).read_text(encoding="utf-8"))

        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["signed_discrepancy_theorem_proved"])
        self.assertFalse(receipt["q286_threshold_theorem_proved"])
        self.assertIn("problem definition only", receipt["status_boundary"])
        self.assertIn("equivalent", receipt["bridge_boundary"])

    def test_signed_threshold_is_the_new_narrow_problem(self):
        receipt = json.loads(Path(
            "evidence/q286-wbss-signed-discrepancy-problem.json"
        ).read_text(encoding="utf-8"))

        for key in ("full", "edge_beta"):
            summary = receipt["families"][key]["summary"]
            self.assertEqual(summary["row_count"], 196)
            self.assertEqual(summary["signed_threshold_pass_count"], 196)
            self.assertEqual(summary["l1_budget_pass_count"], 0)
            self.assertLess(summary["lambda_phi_summary"]["maximum"], 1.0)
            self.assertGreater(
                summary["positivity_margin_ratio_summary"]["minimum"], 0.0)

    def test_l1_bridge_is_much_stronger_than_observed_anti_alignment(self):
        receipt = json.loads(Path(
            "evidence/q286-wbss-signed-discrepancy-problem.json"
        ).read_text(encoding="utf-8"))

        full = receipt["families"]["full"]["summary"]
        beta = receipt["families"]["edge_beta"]["summary"]

        self.assertGreater(
            full["l1_to_anti_alignment_ratio_summary"]["minimum"], 20.0)
        self.assertGreater(
            beta["l1_to_anti_alignment_ratio_summary"]["minimum"], 20.0)
        self.assertEqual(full["tightest_signed_row"]["target"], 94856)
        self.assertEqual(beta["tightest_signed_row"]["target"], 94856)

    def test_problem_statement_names_the_source_backed_gap(self):
        receipt = json.loads(Path(
            "evidence/q286-wbss-signed-discrepancy-problem.json"
        ).read_text(encoding="utf-8"))

        self.assertIn("lambda_phi(N)<=1-eta(N)",
                      receipt["problem_statement"])
        self.assertIn("source-backed estimate",
                      receipt["bridge_boundary"])


if __name__ == "__main__":
    unittest.main()
