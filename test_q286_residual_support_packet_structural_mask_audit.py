import json
import unittest
from pathlib import Path


class Q286ResidualSupportPacketStructuralMaskAuditTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/q286-residual-support-packet-structural-mask-audit.json"
        ).read_text(encoding="utf-8"))

    def test_receipt_preserves_boundaries(self):
        receipt = self.load_receipt()

        self.assertEqual(
            receipt["status"],
            "CANDIDATE_two_subcube_structural_mask_survives_finitely")
        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["structural_mask_theorem_proved"])
        self.assertFalse(receipt["support_packet_theorem_proved"])
        self.assertFalse(
            receipt["signed_binary_prime_correlation_theorem_proved"])
        self.assertTrue(receipt["universal_bound_open"])
        self.assertIn("finitely", receipt["status"])

    def test_minimal_core_is_not_closure_natural(self):
        receipt = self.load_receipt()
        summary = receipt["summary"]

        self.assertEqual(summary["minimal_core_downward_violation_count"], 5)
        self.assertEqual(summary["minimal_core_upward_violation_count"], 16)
        self.assertAlmostEqual(
            summary["minimal_arbitrary_core_margin"],
            0.0005798995134771445)

    def test_one_subcube_has_no_nontrivial_certificate(self):
        receipt = self.load_receipt()
        one = receipt["dnf_scans"]["one_subcube"]

        self.assertEqual(one["certifying_mask_count"], 1)
        self.assertEqual(
            one["smallest_certifying_mask"]["mask_size"], 15)
        self.assertAlmostEqual(
            one["smallest_certifying_mask"]["minimum_margin"],
            0.012576466293799798)

    def test_two_subcube_structural_mask_certifies_with_larger_margin(self):
        receipt = self.load_receipt()
        mask = receipt["summary"]["smallest_two_subcube_certifying_mask"]

        self.assertEqual(mask["mask_size"], 7)
        self.assertEqual(set(mask["mask"]), {
            "11", "11x13", "5", "5x11", "5x11x13", "5x7", "7"})
        self.assertEqual(
            mask["rule"],
            "(7=0 and 11=1) OR (11=0 and 13=0)")
        self.assertAlmostEqual(mask["minimum_margin"], 0.005504640544899547)
        self.assertAlmostEqual(
            mask["tight_row"]["mask_relative_error_budget_with_tail_exact"],
            0.09076413199496625)

    def test_support_size_two_mask_also_certifies(self):
        receipt = self.load_receipt()
        mask = receipt["summary"]["support_size_le_2_mask"]

        self.assertTrue(mask["all_positive_rows_certified"])
        self.assertEqual(mask["mask_size"], 10)
        self.assertAlmostEqual(mask["minimum_margin"], 0.004018492886067315)
        self.assertAlmostEqual(
            mask["tight_row"]["mask_relative_error_budget_with_tail_exact"],
            0.022998983525494825)


if __name__ == "__main__":
    unittest.main()
