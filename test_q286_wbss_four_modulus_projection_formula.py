import json
import unittest
from pathlib import Path


class Q286WbssFourModulusProjectionFormulaTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/q286-wbss-four-modulus-projection-formula.json"
        ).read_text(encoding="utf-8"))

    def test_receipt_preserves_boundaries(self):
        receipt = self.load_receipt()

        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["four_modulus_projection_theorem_proved"])
        self.assertFalse(receipt["signed_discrepancy_theorem_proved"])
        self.assertIn("finite formula extraction only",
                      receipt["status_boundary"])

    def test_formula_reconstructs_unit_coefficient(self):
        receipt = self.load_receipt()
        fit = receipt["coefficient_fit"]

        self.assertEqual(receipt["unit_count"], 2880)
        self.assertLess(fit["relative_l2_residual"], 1e-12)
        self.assertLess(fit["max_abs_residual"], 1e-10)

    def test_local_uniform_main_terms_are_positive(self):
        receipt = self.load_receipt()
        summary = receipt["local_main_term_summary"]
        budget = receipt["projection_error_budget"]

        self.assertEqual(summary["row_count"], 5005)
        self.assertTrue(budget["all_even_residue_local_main_terms_positive"])
        self.assertGreater(
            summary["local_uniform_main_term_summary"]["minimum"], 0.0)
        self.assertLess(
            summary["formula_abs_error_summary"]["maximum"], 1e-10)

    def test_projection_error_budget_is_recorded(self):
        receipt = self.load_receipt()
        budget = receipt["projection_error_budget"]
        table = receipt["coefficient_table"]

        self.assertEqual(
            set(receipt["formula"]["moduli"]), {70, 130, 154, 286})
        self.assertGreater(table["total_nonconstant_l1_norm"], 0.0)
        self.assertGreater(
            budget["sufficient_uniform_projection_error_bound"], 0.0)
        self.assertEqual(
            budget["worst_local_uniform_row"]["target_residue"], 4124)


if __name__ == "__main__":
    unittest.main()
