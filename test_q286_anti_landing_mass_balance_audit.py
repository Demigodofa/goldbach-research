import json
import unittest
from pathlib import Path


class Q286AntiLandingMassBalanceAuditTests(unittest.TestCase):
    def test_mass_balance_receipt_preserves_boundaries(self):
        receipt = json.loads(Path(
            "evidence/q286-anti-landing-mass-balance-audit.json"
        ).read_text(encoding="utf-8"))

        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["mass_balance_theorem_proved"])
        self.assertFalse(
            receipt["coefficient_weighted_anti_landing_theorem_proved"])
        self.assertTrue(receipt["mass_majority_candidate_falsified"])
        self.assertIn("finite anti-landing mass-balance diagnostic",
                      receipt["status_boundary"])

    def test_mass_majority_fails_but_weighted_landing_survives(self):
        receipt = json.loads(Path(
            "evidence/q286-anti-landing-mass-balance-audit.json"
        ).read_text(encoding="utf-8"))
        summary = receipt["summary"]
        post = summary["post_discovery_rows"]

        self.assertEqual(summary["target_row_count"], 230)
        self.assertEqual(summary["post_discovery_target_count"], 196)
        self.assertEqual(post["mass_majority_pass_count"], 178)
        self.assertEqual(post["mass_majority_fail_count"], 18)
        self.assertEqual(post["weighted_landing_pass_count"], 196)
        self.assertEqual(
            post["rescued_without_mass_majority_count"], 18)
        self.assertGreater(
            post["coefficient_lift_surplus_summary"]["minimum"], 0.0)
        self.assertLess(
            post["signed_part_identity_error_summary"]["maximum"], 1e-10)

    def test_examples_record_rows_rescued_without_mass_majority(self):
        receipt = json.loads(Path(
            "evidence/q286-anti-landing-mass-balance-audit.json"
        ).read_text(encoding="utf-8"))
        examples = receipt[
            "summary"]["post_discovery_rows_rescued_without_mass_majority"]
        targets = {row["target"] for row in examples}

        self.assertEqual(len(examples), 18)
        self.assertIn(91502, targets)
        self.assertIn(109178, targets)
        for row in examples:
            self.assertLess(row["mass_positive_minus_negative"], 0.0)
            self.assertGreater(row["coefficient_lift_surplus"], 0.0)
            self.assertTrue(row["weighted_landing_pass"])


if __name__ == "__main__":
    unittest.main()
