import json
import unittest
from pathlib import Path


class Q286ResidualSupportPacketRescueCoreAuditTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/q286-residual-support-packet-rescue-core-audit.json"
        ).read_text(encoding="utf-8"))

    def test_receipt_preserves_boundaries(self):
        receipt = self.load_receipt()

        self.assertEqual(
            receipt["status"],
            "HOLD_minimal_rescue_core_is_near_sharp_finite_fit")
        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["rescue_core_theorem_proved"])
        self.assertFalse(receipt["support_packet_theorem_proved"])
        self.assertFalse(
            receipt["signed_binary_prime_correlation_theorem_proved"])
        self.assertTrue(receipt["universal_bound_open"])
        self.assertIn("near-sharp", receipt["decision"])

    def test_minimal_core_is_size_five_and_unique_at_that_size(self):
        receipt = self.load_receipt()
        summary = receipt["summary"]

        self.assertEqual(summary["minimum_certifying_core_size"], 5)
        self.assertEqual(
            summary["minimal_certifying_core"],
            ["11x13", "5", "5x7", "5x7x13", "7"])
        self.assertEqual(
            summary["certifying_core_counts_through_size_5"],
            {"0": 0, "1": 0, "2": 0, "3": 0, "4": 0, "5": 1})

    def test_tight_row_margin_and_relative_budget_are_near_sharp(self):
        receipt = self.load_receipt()
        summary = receipt["summary"]

        self.assertEqual(summary["minimal_core_tight_target"], 94856)
        self.assertAlmostEqual(
            summary["minimal_core_minimum_margin"],
            0.0005798995134771445)
        self.assertAlmostEqual(
            summary["minimal_core_tight_relative_budget"],
            0.010227537717379533)
        self.assertLess(summary["minimal_core_tight_relative_budget"], 0.011)

    def test_minimal_core_certifies_all_positive_rows_only_with_fitted_tail(self):
        receipt = self.load_receipt()
        core = receipt["minimal_certifying_core"]

        self.assertTrue(core["all_positive_rows_certified"])
        self.assertEqual(core["certified_positive_row_count"], 5)
        self.assertEqual(core["tail_packet_count"], 10)
        self.assertAlmostEqual(
            core["tail_adverse_envelope"], 0.17016598888754483)
        margins = [
            row["rescue_core_margin"] for row in core["row_results"]]
        self.assertAlmostEqual(min(margins), 0.0005798995134771445)


if __name__ == "__main__":
    unittest.main()
