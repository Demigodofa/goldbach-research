import json
import unittest
from pathlib import Path


class Q286WbssFourModulusFactorAnovaAuditTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/q286-wbss-four-modulus-factor-anova-audit.json"
        ).read_text(encoding="utf-8"))

    def test_receipt_preserves_boundaries(self):
        receipt = self.load_receipt()

        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["four_modulus_projection_theorem_proved"])
        self.assertFalse(receipt["signed_discrepancy_theorem_proved"])
        self.assertTrue(receipt["universal_bound_open"])
        self.assertIn("factor-ANOVA coefficient audit",
                      receipt["status_boundary"])

    def test_anova_matches_span_minimality(self):
        receipt = self.load_receipt()
        summary = receipt["projection_family_summary"]

        self.assertTrue(receipt["anova_matches_span_minimality"])
        self.assertLess(summary["maximum_residual_match_abs_error"], 1e-9)
        self.assertTrue(receipt["no_smaller_projection_family_found"])
        self.assertEqual(summary["proper_exact_span_count"], 0)

    def test_nonzero_supports_are_four_modulus_edges(self):
        receipt = self.load_receipt()
        component_summary = receipt["component_summary"]

        self.assertEqual(component_summary["nonzero_support_keys"], [
            "empty", "5", "7", "11", "13",
            "5,7", "5,13", "7,11", "11,13",
        ])
        self.assertEqual(component_summary["nonzero_by_order"], {
            "0": 1,
            "1": 4,
            "2": 4,
            "3": 0,
            "4": 0,
        })

    def test_best_proper_family_misses_modulus_130_edge(self):
        receipt = self.load_receipt()
        best = receipt["projection_family_summary"]["best_proper_family"]

        self.assertEqual(best["moduli"], [70, 154, 286])
        self.assertEqual(
            [row["support_key"] for row in best["missing_nonzero_supports"]],
            ["5,13"],
        )
        self.assertAlmostEqual(
            best["anova_relative_l2_residual"],
            0.025284174723626925,
            places=12)
        self.assertAlmostEqual(
            best["span_relative_l2_residual"],
            0.025284174723626925,
            places=12)

    def test_full_family_has_no_missing_nonzero_supports(self):
        receipt = self.load_receipt()
        full = receipt["projection_family_summary"]["full_four_modulus_family"]

        self.assertEqual(full["moduli"], [70, 130, 154, 286])
        self.assertEqual(full["missing_nonzero_supports"], [])
        self.assertLess(full["anova_relative_l2_residual"], 1e-12)
        self.assertLess(full["span_relative_l2_residual"], 1e-12)


if __name__ == "__main__":
    unittest.main()
