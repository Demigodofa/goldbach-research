import json
import unittest
from pathlib import Path


class Q286ResidualSupportOrderPeriodLiftHoldoutTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/q286-residual-support-order-period-lift-holdout.json"
        ).read_text(encoding="utf-8"))

    def test_receipt_preserves_boundaries(self):
        receipt = self.load_receipt()

        self.assertEqual(
            receipt["status"],
            "CANDIDATE_period_lift_support_order_bridge_survives_holdout")
        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["eventual_threshold_theorem_proved"])
        self.assertFalse(receipt["low_order_base_theorem_proved"])
        self.assertFalse(
            receipt["high_order_tail_domination_theorem_proved"])
        self.assertTrue(receipt["universal_bound_open"])
        self.assertFalse(
            receipt["acceptance_condition"][
                "finite_evidence_is_acceptance_condition"])

    def test_all_lifted_rows_are_positive_with_matching_low_order_base(self):
        receipt = self.load_receipt()
        summary = receipt["summary"]

        self.assertEqual(summary["row_count"], 56)
        self.assertEqual(summary["actual_full_positive_count"], 56)
        self.assertEqual(summary["actual_full_nonpositive_count"], 0)
        self.assertEqual(summary["low_order_base_positive_count"], 56)
        self.assertEqual(summary["low_order_base_sign_mismatch_count"], 0)
        self.assertEqual(summary["low_order_base_sign_mismatch_targets"], [])

    def test_tight_lifted_base_is_much_larger_than_fixture_base(self):
        receipt = self.load_receipt()
        tight = receipt["summary"]["tight_low_order_base_row"]

        self.assertEqual(tight["target"], 124886)
        self.assertAlmostEqual(
            tight["low_order_base_action"], 0.3739719483114472)
        self.assertAlmostEqual(
            tight["actual_full_action"], 0.39426181470078336)

    def test_high_order_tail_domination_is_comfortable_on_holdout(self):
        receipt = self.load_receipt()
        summary = receipt["summary"]
        row = summary["maximum_high_order_adverse_to_base_ratio_row"]

        self.assertEqual(row["target"], 164926)
        self.assertAlmostEqual(
            summary["maximum_high_order_adverse_to_base_ratio"],
            0.13266261119465184)
        self.assertLess(
            summary["maximum_high_order_adverse_to_base_ratio"], 0.14)
        self.assertAlmostEqual(
            summary["maximum_high_order_abs_to_base_ratio"],
            0.13266261119465184)

    def test_holdout_high_order_adverse_envelope_survives_lifted_rows(self):
        receipt = self.load_receipt()
        summary = receipt["summary"]

        self.assertAlmostEqual(
            summary["holdout_high_order_adverse_envelope"],
            0.06972227681175086)
        self.assertAlmostEqual(
            summary["holdout_envelope_margin_at_tight_base"],
            0.30424967149969635)
        self.assertGreater(
            summary["holdout_envelope_margin_at_tight_base"], 0.0)

    def test_each_lift_batch_has_seven_rows_and_no_mismatch(self):
        receipt = self.load_receipt()

        self.assertEqual(len(receipt["summary_by_lift"]), 8)
        for row in receipt["summary_by_lift"]:
            self.assertEqual(row["row_count"], 7)
            self.assertEqual(row["actual_full_positive_count"], 7)
            self.assertEqual(row["low_order_base_positive_count"], 7)
            self.assertEqual(row["sign_mismatch_count"], 0)

    def test_reconstruction_is_exact_on_holdout(self):
        receipt = self.load_receipt()

        self.assertLess(
            receipt["summary"]["maximum_reconstruction_error"], 1e-9)


if __name__ == "__main__":
    unittest.main()
