import json
import unittest
from pathlib import Path


class Q286WbssResidualAbsorptionThresholdAuditTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/q286-wbss-residual-absorption-threshold-audit.json"
        ).read_text(encoding="utf-8"))

    def threshold(self, receipt, name):
        return {
            row["name"]: row
            for row in receipt["threshold_profiles"]
        }[name]

    def test_receipt_preserves_boundaries(self):
        receipt = self.load_receipt()

        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["residual_absorption_theorem_proved"])
        self.assertFalse(receipt["signed_projection_theorem_proved"])
        self.assertIn(
            "finite q286-WBSS residual absorption threshold diagnostic",
            receipt["status_boundary"])

    def test_one_eighth_fails_and_point_13_passes(self):
        receipt = self.load_receipt()

        self.assertTrue(receipt["one_eighth_cap_falsified"])
        self.assertFalse(self.threshold(receipt, "one_eighth")[
            "passes_all_rows"])
        self.assertEqual(self.threshold(receipt, "one_eighth")[
            "failing_row_count"], 1)
        self.assertTrue(receipt["point_13_cap_survives_fixture"])
        self.assertTrue(self.threshold(receipt, "decimal_0_13")[
            "passes_all_rows"])

    def test_observed_threshold_is_between_one_eighth_and_point_13(self):
        receipt = self.load_receipt()
        observed = receipt["row_summary"]["observed_minimum_passing_constant"]

        self.assertGreater(observed, 1.0 / 8.0)
        self.assertLess(observed, 0.126)
        self.assertEqual(receipt["row_summary"]["ceil_to_3_decimal_places"],
                         0.126)
        self.assertEqual(receipt["row_summary"]["ceil_to_2_decimal_places"],
                         0.13)

    def test_worst_row_is_the_known_threshold_obstruction(self):
        receipt = self.load_receipt()
        worst = receipt["row_summary"]["worst_row"]

        self.assertEqual(worst["target"], 365578)
        self.assertEqual(worst["target_mod_286"], 70)
        self.assertAlmostEqual(
            worst["pushback_to_main_drag_ratio"],
            0.12566677703853088,
            places=14)

    def test_all_recorded_rows_were_replayed(self):
        receipt = self.load_receipt()

        self.assertEqual(receipt["row_summary"]["row_count"], 196)
        self.assertEqual(receipt["row_summary"][
            "positive_pushback_row_count"], 24)
        self.assertEqual(self.threshold(receipt, "decimal_0_13")[
            "non_strict_pass_count"], 196)


if __name__ == "__main__":
    unittest.main()
