import json
import unittest
from pathlib import Path


class Q286WbssMultiplicativeCharacterPaymentAuditTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/"
            "q286-wbss-multiplicative-character-payment-audit.json"
        ).read_text(encoding="utf-8"))

    def test_receipt_is_payment_hold_not_proof(self):
        receipt = self.load_receipt()

        self.assertEqual(
            receipt["status"],
            "HOLD_character_moment_payment_bound_required")
        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["character_moment_bound_proved"])
        self.assertFalse(receipt["pointwise_adverse_drag_theorem_proved"])
        self.assertTrue(receipt["universal_bound_open"])
        self.assertFalse(receipt["acceptance_condition"][
            "finite_evidence_is_acceptance_condition"])

    def test_character_payment_budget_values(self):
        receipt = self.load_receipt()
        budget = receipt["character_budget"]

        self.assertEqual(budget["active_character_count"], 122)
        self.assertEqual(budget["active_real_channel_count"], 64)
        self.assertEqual(budget["self_conjugate_channel_count"], 6)
        self.assertAlmostEqual(budget["total_character_l1"],
                               49.153988812629684,
                               places=12)
        self.assertAlmostEqual(budget["equal_character_moment_cap"],
                               0.012286599575574883,
                               places=14)
        self.assertAlmostEqual(
            budget["cap_relaxation_factor_vs_residue_cap"],
            7.58762434311955,
            places=12)

    def test_per_modulus_counts_and_bottleneck(self):
        receipt = self.load_receipt()
        per_modulus = receipt["character_budget"]["per_modulus"]

        self.assertEqual(per_modulus["70"]["active_character_count"], 11)
        self.assertEqual(per_modulus["130"]["active_character_count"], 23)
        self.assertEqual(per_modulus["154"]["active_character_count"], 29)
        self.assertEqual(per_modulus["286"]["active_character_count"], 59)
        self.assertAlmostEqual(per_modulus["286"]["character_l1"],
                               32.56739289271501,
                               places=12)
        self.assertAlmostEqual(
            per_modulus["286"]["equal_cap_if_this_modulus_paid_alone"],
            0.0185441733107891,
            places=14)

    def test_decision_keeps_universal_pointwise_boundary(self):
        receipt = self.load_receipt()

        self.assertIn("better analytic target", receipt["decision"])
        self.assertIn("universal pointwise", receipt["decision"])
        self.assertIn("not finite evidence", receipt["decision"])


if __name__ == "__main__":
    unittest.main()
