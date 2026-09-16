import json
import unittest
from pathlib import Path


class Q286ResidualSupportOrderOnePeriodThresholdAuditTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/q286-residual-support-order-one-period-threshold-audit.json"
        ).read_text(encoding="utf-8"))

    def test_receipt_preserves_boundaries(self):
        receipt = self.load_receipt()

        self.assertEqual(
            receipt["status"],
            "CANDIDATE_one_period_threshold_removes_high_order_envelope_obstruction")
        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["eventual_threshold_theorem_proved"])
        self.assertFalse(receipt["low_order_base_theorem_proved"])
        self.assertFalse(
            receipt["high_order_tail_domination_theorem_proved"])
        self.assertFalse(receipt["q286_threshold_theorem_proved"])
        self.assertFalse(
            receipt["acceptance_condition"][
                "finite_evidence_is_acceptance_condition"])

    def test_fixture_fails_but_horizon_passes_envelope(self):
        receipt = self.load_receipt()
        summary = receipt["summary"]

        self.assertFalse(summary["fixture_envelope_survives"])
        self.assertTrue(summary["horizon_envelope_survives"])
        self.assertTrue(
            summary["one_period_threshold_candidate_survives_checked_horizon"])
        self.assertAlmostEqual(
            summary["fixture_envelope_margin"],
            -0.18097113020581837)
        self.assertAlmostEqual(
            summary["horizon_envelope_margin"],
            0.22461870068431022)

    def test_fixture_and_horizon_key_values_are_preserved(self):
        receipt = self.load_receipt()

        self.assertEqual(receipt["fixture"]["tight_positive_target"], 94856)
        self.assertAlmostEqual(
            receipt["fixture"]["tight_low_order_base"],
            0.05371090383605067)
        self.assertAlmostEqual(
            receipt["fixture"]["high_order_adverse_envelope"],
            0.23468203404186905)
        self.assertEqual(
            receipt["horizon"]["tight_low_order_base_target"], 255016)
        self.assertAlmostEqual(
            receipt["horizon"]["tight_low_order_base"],
            0.2943409774960611)
        self.assertAlmostEqual(
            receipt["horizon"]["high_order_adverse_envelope"],
            0.06972227681175086)

    def test_horizon_keeps_sign_structure(self):
        receipt = self.load_receipt()
        horizon = receipt["horizon"]

        self.assertEqual(horizon["row_count"], 224)
        self.assertEqual(horizon["actual_full_positive_count"], 224)
        self.assertEqual(horizon["low_order_base_positive_count"], 224)
        self.assertEqual(horizon["sign_mismatch_count"], 0)

    def test_contrast_factors_are_material(self):
        receipt = self.load_receipt()
        summary = receipt["summary"]

        self.assertGreater(summary["base_growth_factor_vs_fixture_tight"], 5.0)
        self.assertGreater(summary["adverse_ratio_drop_factor"], 5.0)


if __name__ == "__main__":
    unittest.main()
