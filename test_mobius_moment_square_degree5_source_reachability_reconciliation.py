import json
import unittest
from pathlib import Path


EVIDENCE = Path(
    "evidence/"
    "mobius-moment-square-degree5-source-reachability-reconciliation.json")


class MobiusMomentSquareDegree5SourceReachabilityReconciliationTests(
        unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = json.loads(EVIDENCE.read_text(encoding="utf-8"))

    def test_receipt_preserves_boundaries(self):
        receipt = self.receipt

        self.assertEqual(
            receipt["status"],
            "RECONCILE_degree5_source_reachability_after_translated_puncture")
        self.assertTrue(receipt["finite_reconciliation_only"])
        self.assertTrue(receipt["finite_diagnostic_only"])
        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["source_window_theorem_proved"])
        self.assertFalse(
            receipt["source_admissible_window_theorem_proved"])

    def test_broad_failure_is_classified_unreachable(self):
        receipt = self.receipt

        self.assertTrue(receipt["broad_translated_quantifier_falsified"])
        self.assertEqual(receipt["broad_failure_count"], 1)
        self.assertEqual(receipt["reachable_source_failure_count"], 0)
        self.assertEqual(receipt["unreachable_translated_failure_count"], 1)
        self.assertEqual(receipt["unclassified_failure_count"], 0)
        self.assertTrue(receipt["all_broad_failures_are_unreachable"])

        failure = receipt["classified_broad_failures"][0]
        self.assertEqual(failure["scale_modulus"], 149)
        self.assertEqual(failure["prime_modulus"], 163)
        self.assertEqual(failure["label"], "00,12")
        self.assertEqual(failure["active_row_start"], 1)
        self.assertEqual(failure["reachability"], "UNREACHABLE")
        self.assertFalse(failure["reachable_from_original_source_mapping"])
        self.assertEqual(failure["source_active_row_start"], 32)

    def test_source_starts_survive_as_narrowed_target(self):
        receipt = self.receipt

        self.assertEqual(receipt["source_scale_count"], 6)
        self.assertTrue(receipt["all_source_starts_pass"])
        self.assertEqual(receipt["source_start_failure_count"], 0)
        self.assertAlmostEqual(
            receipt["minimum_source_start_canonical_slack"],
            0.056367749089376695)
        self.assertAlmostEqual(
            receipt["minimum_source_start_canonical_ratio"],
            0.5563677490893767)
        self.assertIn("canonical source-start",
                      receipt["candidate_next_theorem_target"]["name"])
        self.assertIn("unreachable translated starts",
                      receipt["decision"])


if __name__ == "__main__":
    unittest.main()
