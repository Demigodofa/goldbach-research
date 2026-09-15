import json
import unittest
from pathlib import Path


class Q286WbssMultiplicativeCharacterL2PaymentAuditTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/"
            "q286-wbss-multiplicative-character-l2-payment-audit.json"
        ).read_text(encoding="utf-8"))

    def test_receipt_is_l2_payment_hold_not_proof(self):
        receipt = self.load_receipt()

        self.assertEqual(
            receipt["status"],
            "HOLD_aggregate_character_l2_bound_required")
        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["aggregate_character_l2_bound_proved"])
        self.assertFalse(receipt["pointwise_adverse_drag_theorem_proved"])
        self.assertTrue(receipt["universal_bound_open"])
        self.assertFalse(receipt["acceptance_condition"][
            "finite_evidence_is_acceptance_condition"])

    def test_aggregate_l2_payment_values(self):
        receipt = self.load_receipt()
        budget = receipt["character_l2_budget"]

        self.assertAlmostEqual(budget["aggregate_character_l2_square"],
                               30.52680126946419,
                               places=12)
        self.assertAlmostEqual(budget["aggregate_character_l2"],
                               5.525106448699807,
                               places=12)
        self.assertAlmostEqual(
            budget["aggregate_character_moment_l2_cap"],
            0.10930746469603118,
            places=14)
        self.assertAlmostEqual(
            budget["relaxation_factor_vs_character_linf_cap"],
            8.89647815277782,
            places=12)
        self.assertAlmostEqual(
            budget["relaxation_factor_vs_residue_linf_cap"],
            67.50313420004822,
            places=12)

    def test_modulus_286_remains_l2_bottleneck(self):
        receipt = self.load_receipt()
        budget = receipt["character_l2_budget"]

        self.assertAlmostEqual(
            budget["character_l2_by_modulus"]["286"],
            4.628792495952571,
            places=12)
        self.assertAlmostEqual(
            budget["single_modulus_l2_cap_if_paid_alone"]["286"],
            0.1304736340225126,
            places=14)

    def test_decision_names_missing_universal_theorem(self):
        receipt = self.load_receipt()

        self.assertIn("materially better", receipt["decision"])
        self.assertIn("universal pointwise aggregate", receipt["decision"])
        self.assertIn("no such theorem is proved", receipt["decision"])


if __name__ == "__main__":
    unittest.main()
