import json
import unittest
from pathlib import Path


class Q286ResidualStructuralMaskSignedTailBridgeAuditTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/q286-residual-structural-mask-signed-tail-bridge-audit.json"
        ).read_text(encoding="utf-8"))

    def test_receipt_preserves_proof_boundaries(self):
        receipt = self.load_receipt()

        self.assertEqual(
            receipt["status"],
            "HOLD_signed_tail_bridge_requires_external_pointwise_theorem")
        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["signed_tail_theorem_proved"])
        self.assertFalse(receipt["structural_mask_theorem_proved"])
        self.assertFalse(receipt["non_circular_l2_bridge_confirmed"])
        self.assertFalse(receipt["pointwise_adverse_drag_theorem_proved"])
        self.assertTrue(receipt["universal_bound_open"])
        self.assertFalse(
            receipt["acceptance_condition"][
                "finite_evidence_is_acceptance_condition"])

    def test_zero_mass_check_is_clean_but_not_the_bridge(self):
        receipt = self.load_receipt()
        zero = receipt["zero_mass_check"]

        self.assertEqual(zero["row_count"], 348)
        self.assertEqual(zero["zero_pair_count"], 0)
        self.assertEqual(zero["zero_actual_mass_count"], 0)
        self.assertIn("does not confirm", zero["decision"])

    def test_two_subcube_signed_tail_budget_after_adverse_failure(self):
        receipt = self.load_receipt()
        summary = receipt["summary"]

        self.assertAlmostEqual(
            summary["two_subcube_all_row_adverse_tail_margin"],
            -0.3385081689657937)
        self.assertAlmostEqual(
            summary["two_subcube_signed_tail_budget"],
            0.07569390912763455)
        self.assertEqual(summary["two_subcube_tight_target"], 94856)
        self.assertAlmostEqual(
            summary["two_subcube_tight_tail_signed_action"],
            -0.16211735719392256)

    def test_support_size_two_has_looser_signed_tail_budget(self):
        receipt = self.load_receipt()
        summary = receipt["summary"]

        self.assertAlmostEqual(
            summary["support_size_le_2_all_row_adverse_tail_margin"],
            -0.18722458212180332)
        self.assertAlmostEqual(
            summary["support_size_le_2_signed_tail_budget"],
            0.24152101169573884)
        self.assertGreater(
            summary["support_size_le_2_signed_tail_budget"],
            summary["two_subcube_signed_tail_budget"])
        self.assertGreater(
            summary["support_size_le_2_signed_tail_budget"],
            summary["full_15_packet_signed_budget"])

    def test_signed_packet_reconstruction_is_exact_on_fixture(self):
        receipt = self.load_receipt()
        for mask_row in receipt["mask_rows"]:
            self.assertLess(
                mask_row["maximum_reconstruction_error"], 1e-9)


if __name__ == "__main__":
    unittest.main()
