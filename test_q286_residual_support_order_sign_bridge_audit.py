import json
import unittest
from pathlib import Path


class Q286ResidualSupportOrderSignBridgeAuditTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/q286-residual-support-order-sign-bridge-audit.json"
        ).read_text(encoding="utf-8"))

    def test_receipt_preserves_boundaries(self):
        receipt = self.load_receipt()

        self.assertEqual(
            receipt["status"],
            "CANDIDATE_support_order_sign_bridge_survives_fixture")
        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["low_order_base_theorem_proved"])
        self.assertFalse(
            receipt["high_order_tail_domination_theorem_proved"])
        self.assertFalse(receipt["signed_packet_theorem_proved"])
        self.assertTrue(receipt["universal_bound_open"])
        self.assertFalse(
            receipt["acceptance_condition"][
                "finite_evidence_is_acceptance_condition"])

    def test_low_order_base_sign_matches_full_sign_on_fixture(self):
        receipt = self.load_receipt()
        summary = receipt["summary"]

        self.assertEqual(summary["row_count"], 7)
        self.assertEqual(summary["actual_full_positive_count"], 5)
        self.assertEqual(summary["low_order_base_positive_count"], 5)
        self.assertEqual(summary["low_order_base_sign_mismatch_count"], 0)
        self.assertEqual(summary["low_order_base_sign_mismatch_targets"], [])

    def test_tight_positive_row_is_94856(self):
        receipt = self.load_receipt()
        row = receipt["summary"]["tight_low_order_base_positive_row"]

        self.assertEqual(row["target"], 94856)
        self.assertAlmostEqual(
            row["low_order_base_action"], 0.05371090383605067)
        self.assertAlmostEqual(
            row["high_order_signed_tail"], -0.041134437542250886)
        self.assertAlmostEqual(
            row["actual_full_action"], 0.012576466293799767)

    def test_high_order_tail_domination_is_near_but_positive(self):
        receipt = self.load_receipt()
        summary = receipt["summary"]

        self.assertAlmostEqual(
            summary[
                "maximum_high_order_adverse_to_base_ratio_on_base_positive_rows"
            ],
            0.7658489171549095)
        self.assertLess(
            summary[
                "maximum_high_order_adverse_to_base_ratio_on_base_positive_rows"
            ],
            1.0)
        self.assertAlmostEqual(
            summary[
                "maximum_high_order_abs_to_base_ratio_on_base_positive_rows"
            ],
            0.9694853511961387)

    def test_all_row_high_order_adverse_envelope_still_fails(self):
        receipt = self.load_receipt()
        summary = receipt["summary"]

        self.assertAlmostEqual(
            summary["all_row_high_order_adverse_envelope"],
            0.23468203404186905)
        self.assertAlmostEqual(
            summary["all_row_high_order_envelope_margin_at_tight_positive_base"],
            -0.18097113020581839)
        self.assertLess(
            summary["all_row_high_order_envelope_margin_at_tight_positive_base"],
            0.0)

    def test_reconstruction_is_exact_on_fixture(self):
        receipt = self.load_receipt()

        self.assertLess(
            receipt["summary"]["maximum_reconstruction_error"], 1e-9)


if __name__ == "__main__":
    unittest.main()
