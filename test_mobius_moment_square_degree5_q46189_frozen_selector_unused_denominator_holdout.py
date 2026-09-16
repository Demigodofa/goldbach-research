import json
import unittest
from pathlib import Path


EVIDENCE = Path(
    "evidence/"
    "mobius-moment-square-degree5-q46189-frozen-selector-unused-denominator-holdout.json")


class MobiusMomentSquareDegree5Q46189FrozenSelectorHoldoutTests(
        unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = json.loads(EVIDENCE.read_text(encoding="utf-8"))

    def test_receipt_preserves_boundaries(self):
        self.assertEqual(
            self.receipt["status"],
            "AUDIT_q46189_frozen_selector_unused_denominator_holdout")
        self.assertTrue(
            self.receipt["finite_frozen_selector_holdout_audit_only"])
        self.assertTrue(self.receipt["finite_diagnostic_only"])
        self.assertFalse(self.receipt["natural_selector_theorem_proved"])
        self.assertFalse(self.receipt["fresh_conductor_holdout_proved"])
        self.assertFalse(
            self.receipt["distance_slice_positive_share_theorem_proved"])
        self.assertFalse(self.receipt["goldbach_proved"])

    def test_frozen_selector_fails_one_unused_same_source_denominator(self):
        classification = self.receipt["classification"]
        failures = self.receipt["failure_summary"]
        self.assertEqual(
            self.receipt["unused_same_source_denominator_count"], 24)
        self.assertFalse(
            classification[
                "frozen_selector_survives_all_unused_same_source_denominators"])
        self.assertTrue(
            classification[
                "frozen_selector_fails_at_least_one_unused_same_source_denominator"])
        self.assertEqual(failures["positive_fraction_failure_count"], 1)
        self.assertEqual(failures["total_pressure_failure_count"], 0)
        self.assertEqual(failures["both_test_failure_count"], 1)
        self.assertEqual(
            classification[
                "counterexample_denominator_to_too_broad_selector_claim"],
            16302,
        )

    def test_counterexample_values_are_stable(self):
        row = self.receipt["failure_summary"]["both_test_failures"][0]
        self.assertEqual(row["reduced_denominator"], 16302)
        self.assertEqual(
            row["factorization"],
            {"2": 1, "3": 1, "11": 1, "13": 1, "19": 1},
        )
        self.assertAlmostEqual(
            row["positive_fraction_gap_vs_q46189"],
            -0.07517830702507916,
            places=15,
        )
        self.assertAlmostEqual(
            row["total_gap_vs_q46189"],
            0.04221956863220733,
            places=15,
        )
        self.assertFalse(row["passes_positive_fraction_separator"])
        self.assertTrue(row["passes_total_pressure_separator"])
        self.assertFalse(row["passes_both_frozen_50A_to_60A_tests"])


if __name__ == "__main__":
    unittest.main()
