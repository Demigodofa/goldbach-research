import json
import unittest
from pathlib import Path


class Q286WbssFourierBurdenAuditTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/q286-wbss-fourier-burden-audit.json"
        ).read_text(encoding="utf-8"))

    def test_receipt_is_finite_diagnostic_not_proof(self):
        receipt = self.load_receipt()

        self.assertEqual(
            receipt["status"],
            "HOLD_fourier_burden_diffuse_high_conductor")
        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["signed_character_theorem_proved"])
        self.assertFalse(receipt["pointwise_adverse_drag_theorem_proved"])
        self.assertTrue(receipt["universal_bound_open"])

    def test_global_mode_burden_is_diffuse(self):
        receipt = self.load_receipt()
        summary = receipt["global_summary"]

        self.assertEqual(summary["nonprincipal_mode_count"], 636)
        self.assertAlmostEqual(summary["total_nonprincipal_energy"],
                               2965.516872883532,
                               places=9)
        self.assertEqual(
            summary["energy_cover_counts"]["0.9"]["mode_count"], 187)
        self.assertEqual(
            summary["energy_cover_counts"]["0.95"]["mode_count"], 232)
        self.assertEqual(
            summary["energy_cover_counts"]["0.99"]["mode_count"], 308)

    def test_modulus_286_dominates_energy_and_is_not_few_mode(self):
        receipt = self.load_receipt()
        fraction = receipt["global_summary"][
            "energy_fraction_by_modulus"]["286"]
        mod286 = receipt["per_modulus"]["286"]

        self.assertAlmostEqual(fraction, 0.8669957368249142, places=12)
        self.assertEqual(mod286["nonprincipal_mode_count"], 285)
        self.assertEqual(
            mod286["energy_cover_counts"]["0.9"]["mode_count"], 135)
        self.assertEqual(
            mod286["energy_cover_counts"]["0.99"]["mode_count"], 188)
        self.assertLess(
            mod286["effective_mode_count"]["largest_mode_fraction"], 0.013)

    def test_high_conductor_buckets_carry_modulus_286(self):
        receipt = self.load_receipt()
        conductor = receipt["per_modulus"]["286"]["conductor_energy"]

        self.assertAlmostEqual(conductor["143"]["energy_fraction"],
                               0.49994752357905275,
                               places=12)
        self.assertAlmostEqual(conductor["286"]["energy_fraction"],
                               0.49994752357905076,
                               places=12)
        self.assertLess(conductor["13"]["energy_fraction"], 0.00005)

    def test_decision_rejects_small_character_shortcut(self):
        receipt = self.load_receipt()

        self.assertIn("few-mode signed-character shortcut",
                      receipt["decision"])
        self.assertIn("broad high-conductor signed binary-prime",
                      receipt["decision"])
        self.assertIn("not a small character-mode lemma",
                      receipt["decision"])


if __name__ == "__main__":
    unittest.main()
