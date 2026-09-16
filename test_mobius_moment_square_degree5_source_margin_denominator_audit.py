import json
import unittest
from pathlib import Path


EVIDENCE = Path(
    "evidence/"
    "mobius-moment-square-degree5-source-margin-denominator-audit.json")


class MobiusMomentSquareDegree5SourceMarginDenominatorAuditTests(
        unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = json.loads(EVIDENCE.read_text(encoding="utf-8"))

    def test_receipt_preserves_boundaries(self):
        self.assertEqual(
            self.receipt["status"],
            "AUDIT_degree5_source_margin_denominator_decomposition")
        self.assertTrue(
            self.receipt["finite_denominator_decomposition_only"])
        self.assertTrue(self.receipt["finite_diagnostic_only"])
        self.assertFalse(self.receipt["goldbach_proved"])
        self.assertFalse(self.receipt["source_start_theorem_proved"])
        self.assertFalse(self.receipt["denominator_margin_theorem_proved"])

    def test_six_tight_prime_blocks_are_decomposed(self):
        self.assertEqual(self.receipt["scale_count"], 6)
        self.assertEqual(
            [(row["scale_modulus"], row["prime_modulus"])
             for row in self.receipt["scale_summaries"]],
            [(229, 379), (251, 379), (293, 461),
             (331, 599), (353, 599), (379, 599)])
        self.assertEqual(
            self.receipt["minimum_reduced_denominator_count"], 28)
        self.assertEqual(
            self.receipt["maximum_reduced_denominator_count"], 77)

    def test_adverse_denominator_share_is_small_on_checked_fixture(self):
        self.assertAlmostEqual(
            self.receipt["minimum_weakest_label_cancellation_ratio"],
            0.00034280843897457745)
        self.assertAlmostEqual(
            self.receipt["maximum_weakest_label_cancellation_ratio"],
            0.000878341064244336)
        self.assertLess(
            self.receipt["maximum_weakest_label_cancellation_ratio"],
            0.001)

    def test_m379_tight_block_denominator_ledger(self):
        row = self.receipt["scale_summaries"][-1]
        self.assertEqual(row["scale_modulus"], 379)
        self.assertEqual(row["prime_modulus"], 599)
        self.assertEqual(row["weakest_label"], "00,12")
        summary = row["weakest_label_denominator_summary"]
        self.assertAlmostEqual(
            summary["total_unnormalized_margin"],
            267181208856715.3)
        self.assertAlmostEqual(
            summary["cancellation_ratio_abs_negative_over_positive"],
            0.0005552064599450985)
        self.assertEqual(
            summary["largest_positive_denominator"]["reduced_denominator"],
            156009)
        self.assertEqual(
            summary["largest_negative_denominator"]["reduced_denominator"],
            52003)

    def test_candidate_subtarget_is_not_promoted(self):
        target = self.receipt["candidate_next_theorem_subtarget"]
        self.assertEqual(
            target["name"], "signed reduced-denominator margin ledger")
        self.assertEqual(target["novelty_label"], "new-to-this-task")
        self.assertIn("after grouping", target["mechanism"])
        self.assertIn("unstable denominator", target["falsifier"])


if __name__ == "__main__":
    unittest.main()
