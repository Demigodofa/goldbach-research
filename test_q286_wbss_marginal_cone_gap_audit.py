import json
import unittest
from pathlib import Path


class Q286WbssMarginalConeGapAuditTests(unittest.TestCase):
    def test_receipt_preserves_boundaries(self):
        receipt = json.loads(Path(
            "evidence/q286-wbss-marginal-cone-gap-audit.json"
        ).read_text(encoding="utf-8"))

        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["marginal_cone_theorem_proved"])
        self.assertFalse(receipt["signed_discrepancy_theorem_proved"])
        self.assertIn("finite marginal-cone LP falsifier",
                      receipt["status_boundary"])

    def test_stress_selection_is_frozen_and_nonempty(self):
        receipt = json.loads(Path(
            "evidence/q286-wbss-marginal-cone-gap-audit.json"
        ).read_text(encoding="utf-8"))

        self.assertEqual(len(receipt["selected_targets"]), 24)
        self.assertIn(94856, receipt["selected_targets"])
        self.assertIn("top 12", receipt["selected_target_rule"])

    def test_weak_marginal_cones_allow_bad_synthetic_measures(self):
        receipt = json.loads(Path(
            "evidence/q286-wbss-marginal-cone-gap-audit.json"
        ).read_text(encoding="utf-8"))

        for family in ("full", "edge_beta"):
            for cone in (
                "support_reflection_only",
                "prime_factor_marginals",
                "q286_joint_marginal",
            ):
                summary = receipt["summary"][family][cone]
                self.assertEqual(summary["row_count"], 24)
                self.assertEqual(summary["bad_measure_feasible_count"], 24)
                self.assertEqual(summary["positive_forced_count"], 0)
                self.assertLess(
                    summary["minimum_signed_expectation_summary"]["maximum"],
                    0.0)

    def test_dominant_support_nearly_closes_but_fails_tight_rows(self):
        receipt = json.loads(Path(
            "evidence/q286-wbss-marginal-cone-gap-audit.json"
        ).read_text(encoding="utf-8"))

        for family in ("full", "edge_beta"):
            summary = receipt[
                "summary"][family]["dominant_coefficient_support_marginals"]
            self.assertEqual(summary["bad_measure_feasible_count"], 3)
            self.assertEqual(summary["positive_forced_count"], 21)
            bad_targets = {
                row["target"]
                for row in receipt[
                    "examples"][family][
                        "dominant_coefficient_support_marginals"][
                            "bad_measure_examples"]
            }
            self.assertIn(94856, bad_targets)

    def test_all_coefficient_support_marginals_force_positive_expectation(self):
        receipt = json.loads(Path(
            "evidence/q286-wbss-marginal-cone-gap-audit.json"
        ).read_text(encoding="utf-8"))

        for family in ("full", "edge_beta"):
            summary = receipt[
                "summary"][family]["all_coefficient_support_marginals"]
            self.assertEqual(summary["bad_measure_feasible_count"], 0)
            self.assertEqual(summary["positive_forced_count"], 24)
            self.assertGreater(
                summary["minimum_signed_expectation_summary"]["minimum"], 0.0)


if __name__ == "__main__":
    unittest.main()
