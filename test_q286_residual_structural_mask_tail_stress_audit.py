import json
import unittest
from pathlib import Path


class Q286ResidualStructuralMaskTailStressAuditTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/q286-residual-structural-mask-tail-stress-audit.json"
        ).read_text(encoding="utf-8"))

    def test_receipt_preserves_boundaries(self):
        receipt = self.load_receipt()

        self.assertEqual(
            receipt["status"],
            "HOLD_all_row_tail_envelope_breaks_structural_masks")
        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["structural_mask_theorem_proved"])
        self.assertFalse(receipt["tail_bound_theorem_proved"])
        self.assertFalse(
            receipt["signed_binary_prime_correlation_theorem_proved"])
        self.assertTrue(receipt["universal_bound_open"])
        self.assertIn("all-row adverse-tail", receipt["decision"])

    def test_two_subcube_mask_fails_all_row_tail_stress(self):
        receipt = self.load_receipt()
        summary = receipt["summary"]

        self.assertAlmostEqual(
            summary["two_subcube_positive_tail_margin"],
            0.005504640544899547)
        self.assertAlmostEqual(
            summary["two_subcube_all_tail_margin"],
            -0.3385081689657937)
        self.assertAlmostEqual(
            summary["two_subcube_positive_tail_envelope"],
            0.16918918294282279)
        self.assertAlmostEqual(
            summary["two_subcube_all_tail_envelope"],
            0.513201992453516)
        self.assertEqual(summary["two_subcube_tight_target"], 94856)

    def test_support_size_two_mask_also_fails_all_row_tail_stress(self):
        receipt = self.load_receipt()
        summary = receipt["summary"]

        self.assertAlmostEqual(
            summary["support_size_le_2_positive_tail_margin"],
            0.004018492886067315)
        self.assertAlmostEqual(
            summary["support_size_le_2_all_tail_margin"],
            -0.18722458212180332)
        self.assertLess(summary["support_size_le_2_all_tail_margin"], 0.0)

    def test_full_packet_control_is_not_a_tail_envelope_route(self):
        receipt = self.load_receipt()
        full = next(
            row for row in receipt["mask_rows"]
            if row["name"] == "full_15_packet")

        self.assertAlmostEqual(
            full["all_row_tail"]["tail_adverse_envelope"], 0.0)
        self.assertAlmostEqual(
            full["all_row_tail"]["minimum_margin"],
            0.012576466293799798)
        self.assertTrue(full["all_row_tail"]["all_positive_rows_certified"])


if __name__ == "__main__":
    unittest.main()
