import json
import unittest
from pathlib import Path


class Q286WbssMultiplicativeCharacterBurdenAuditTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/"
            "q286-wbss-multiplicative-character-burden-audit.json"
        ).read_text(encoding="utf-8"))

    def test_receipt_is_finite_diagnostic_not_proof(self):
        receipt = self.load_receipt()

        self.assertEqual(
            receipt["status"],
            "HOLD_multiplicative_character_burden_broad")
        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["multiplicative_character_theorem_proved"])
        self.assertFalse(
            receipt[
                "fixed_modulus_binary_prime_discrepancy_theorem_proved"])
        self.assertTrue(receipt["universal_bound_open"])

    def test_global_character_burden_is_broad_but_compressed(self):
        receipt = self.load_receipt()
        summary = receipt["global_summary"]

        self.assertEqual(summary["nonprincipal_character_count"], 248)
        self.assertAlmostEqual(summary["total_nonprincipal_energy"],
                               30.526801269464197,
                               places=12)
        self.assertEqual(
            summary["energy_cover_counts"]["0.9"]["character_count"], 60)
        self.assertEqual(
            summary["energy_cover_counts"]["0.99"]["character_count"], 77)
        self.assertEqual(
            receipt["comparison_to_additive_burden"][
                "additive_global_modes_for_99_percent"], 308)

    def test_modulus_286_still_dominates(self):
        receipt = self.load_receipt()
        fraction = receipt["global_summary"][
            "energy_fraction_by_modulus"]["286"]
        mod286 = receipt["per_modulus"]["286"]

        self.assertAlmostEqual(fraction, 0.7018658712866479, places=12)
        self.assertEqual(mod286["nonprincipal_character_count"], 119)
        self.assertEqual(
            mod286["energy_cover_counts"]["0.9"]["character_count"], 43)
        self.assertEqual(
            mod286["energy_cover_counts"]["0.99"]["character_count"], 50)
        self.assertLess(
            mod286["effective_character_count"]["largest_character_fraction"],
            0.032)

    def test_parseval_and_reconstruction_are_verified(self):
        receipt = self.load_receipt()

        for row in receipt["per_modulus"].values():
            self.assertLess(row["parseval_error"], 1e-12)
            self.assertLess(row["max_reconstruction_error"], 1e-12)

    def test_decision_keeps_broad_character_package_not_tiny_shortcut(self):
        receipt = self.load_receipt()

        self.assertIn("compress the burden", receipt["decision"])
        self.assertIn("broad multiplicative-character", receipt["decision"])
        self.assertIn("not a tiny signed-character shortcut",
                      receipt["decision"])


if __name__ == "__main__":
    unittest.main()
