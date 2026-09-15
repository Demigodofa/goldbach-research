import json
import unittest
from pathlib import Path


class Q286WbssFourModulusMinimalityAuditTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/q286-wbss-four-modulus-minimality-audit.json"
        ).read_text(encoding="utf-8"))

    def test_receipt_preserves_boundaries(self):
        receipt = self.load_receipt()

        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["four_modulus_projection_theorem_proved"])
        self.assertFalse(receipt["signed_discrepancy_theorem_proved"])
        self.assertTrue(receipt["universal_bound_open"])
        self.assertIn("coefficient-span minimality audit",
                      receipt["status_boundary"])

    def test_enumerates_all_subfamilies(self):
        receipt = self.load_receipt()
        summary = receipt["holdout"]["summary"]

        self.assertEqual(receipt["target_moduli"], [70, 130, 154, 286])
        self.assertEqual(summary["family_count"], 16)
        self.assertEqual(summary["proper_family_count"], 15)
        self.assertEqual(len(receipt["holdout"]["families"]), 16)

    def test_no_proper_subfamily_is_exact(self):
        receipt = self.load_receipt()
        summary = receipt["holdout"]["summary"]

        self.assertTrue(receipt["no_smaller_projection_family_found"])
        self.assertEqual(summary["proper_exact_span_count"], 0)
        self.assertTrue(summary["full_four_modulus_exact_span"])
        self.assertLess(
            summary["full_four_modulus_family"]["relative_l2_residual"],
            1e-12)
        self.assertGreater(
            summary["best_proper_family"]["relative_l2_residual"],
            1e-3)

    def test_best_proper_family_is_recorded(self):
        receipt = self.load_receipt()
        best = receipt["holdout"]["summary"]["best_proper_family"]

        self.assertEqual(best["moduli"], [70, 154, 286])
        self.assertAlmostEqual(
            best["relative_l2_residual"],
            0.025284174723626925,
            places=12)
        self.assertGreater(best["max_abs_residual"], 0.25)


if __name__ == "__main__":
    unittest.main()
