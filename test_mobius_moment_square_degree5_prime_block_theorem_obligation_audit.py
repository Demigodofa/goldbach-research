import json
import unittest
from pathlib import Path


EVIDENCE = Path(
    "evidence/"
    "mobius-moment-square-degree5-prime-block-theorem-obligation-audit.json")


class MobiusMomentSquareDegree5PrimeBlockTheoremObligationAuditTests(
        unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = json.loads(EVIDENCE.read_text(encoding="utf-8"))

    def test_receipt_preserves_boundaries(self):
        self.assertEqual(
            self.receipt["status"],
            "AUDIT_degree5_prime_block_theorem_obligation")
        self.assertTrue(self.receipt["finite_obligation_audit_only"])
        self.assertTrue(self.receipt["finite_diagnostic_only"])
        self.assertFalse(self.receipt["goldbach_proved"])
        self.assertFalse(self.receipt["source_start_theorem_proved"])
        self.assertFalse(self.receipt["prime_block_theorem_proved"])

    def test_six_scale_fixture_is_loaded(self):
        self.assertEqual(
            self.receipt["scales"], [229, 251, 293, 331, 353, 379])
        self.assertEqual(self.receipt["scale_count"], 6)
        self.assertEqual(self.receipt["checked_dominance_row_count"], 1188)

    def test_checked_pointwise_unnormalized_conditions_pass(self):
        self.assertTrue(
            self.receipt["all_checked_rows_have_negative_full_contribution"])
        self.assertTrue(
            self.receipt[
                "all_checked_rows_have_positive_unnormalized_half_frame_margin"
            ])
        self.assertGreater(
            self.receipt["minimum_checked_unnormalized_half_frame_margin"],
            0.0)
        self.assertAlmostEqual(
            self.receipt["minimum_checked_dominance_slack_above_one_half"],
            0.40189096624031384)

    def test_block_separation_warns_against_fixed_winner_theorem(self):
        self.assertAlmostEqual(
            self.receipt["minimum_top_to_second_block_slack_gap"],
            0.003258445243465413)
        self.assertEqual(
            self.receipt["tightest_prime_counts"],
            {"379": 2, "461": 1, "599": 3})
        self.assertLess(
            self.receipt["minimum_top_to_second_block_slack_gap"],
            0.004)

    def test_theorem_target_is_unnormalized_and_open(self):
        target = self.receipt["pointwise_unnormalized_theorem_target"]
        self.assertEqual(
            target["name"], "source-start prime-block lower-frame control")
        self.assertIn("full/2 - active > 0", target["statement_shape"])
        self.assertIn("equivalent", target["why_unnormalized"])
        for obligation in self.receipt["proof_obligations"]:
            self.assertEqual(obligation["theorem_status"], "open")


if __name__ == "__main__":
    unittest.main()
