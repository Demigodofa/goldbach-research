import json
import unittest
from pathlib import Path


class Q286ResidualSupportOrderPointwiseTheoremTargetTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/q286-residual-support-order-pointwise-theorem-target.json"
        ).read_text(encoding="utf-8"))

    def test_receipt_demotes_finite_evidence(self):
        receipt = self.load_receipt()

        self.assertEqual(
            receipt["status"],
            "TARGET_pointwise_support_order_theorem_required")
        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["pointwise_analytic_estimate_proved"])
        self.assertFalse(receipt["one_period_threshold_theorem_proved"])
        self.assertFalse(receipt["acceptance_condition"][
            "finite_evidence_is_acceptance_condition"])

    def test_horizon_has_no_same_row_pointwise_failures(self):
        receipt = self.load_receipt()
        horizon = receipt["finite_calibration"]["horizon_lifts_1_to_32"]

        self.assertEqual(horizon["row_count"], 224)
        self.assertEqual(horizon["same_row_pointwise_fail_count"], 0)
        self.assertEqual(horizon["same_row_pointwise_failures"], [])
        self.assertTrue(horizon["disconnected_envelope_survives"])
        self.assertAlmostEqual(
            horizon["disconnected_envelope_margin"],
            0.22461870068431022)

    def test_tight_rows_are_preserved(self):
        receipt = self.load_receipt()
        horizon = receipt["finite_calibration"]["horizon_lifts_1_to_32"]
        tight = horizon["tight_pointwise_domination_row"]
        tight_base = horizon["tight_low_order_base_row"]
        worst_ratio = horizon["worst_high_order_adverse_to_base_ratio_row"]

        self.assertEqual(tight["target"], 255016)
        self.assertAlmostEqual(
            tight["pointwise_domination_margin"],
            0.27673704750570033)
        self.assertEqual(tight_base["target"], 255016)
        self.assertAlmostEqual(
            tight_base["low_order_base_action"],
            0.2943409774960611)
        self.assertEqual(worst_ratio["target"], 164926)
        self.assertAlmostEqual(worst_ratio["ratio"], 0.13266261119465184)

    def test_normalization_boundary_is_not_confirmed(self):
        receipt = self.load_receipt()
        boundary = receipt["normalization_and_zero_mass_boundary"]

        self.assertFalse(boundary["raw_unnormalized_pair_count_theorem_present"])
        self.assertFalse(boundary["zero_mass_check_transfers_from_l2_route"])
        self.assertEqual(
            boundary["raw_count_or_mass_fields_present_in_horizon_rows"], [])

    def test_l2_is_not_promoted_to_bridge(self):
        receipt = self.load_receipt()

        self.assertIn(
            "not confirmed",
            receipt["normalization_and_zero_mass_boundary"][
                "l2_status_short_answer"])
        self.assertIn(
            "unnormalized pointwise analytic estimate",
            receipt["decision"])


if __name__ == "__main__":
    unittest.main()
