import json
import unittest
from pathlib import Path


class Q286WbssCoefficientDiscrepancyBudgetHoldTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/q286-wbss-coefficient-discrepancy-budget-hold.json"
        ).read_text(encoding="utf-8"))

    def test_receipt_is_hold_not_proof(self):
        receipt = self.load_receipt()

        self.assertEqual(
            receipt["status"],
            "HOLD_for_pointwise_prime_pair_correlation_estimate")
        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["pointwise_adverse_drag_theorem_proved"])
        self.assertFalse(
            receipt[
                "fixed_modulus_binary_prime_discrepancy_theorem_proved"])
        self.assertTrue(receipt["universal_bound_open"])

    def test_exact_sufficient_inequalities_are_recorded(self):
        receipt = self.load_receipt()
        budget = receipt["coefficient_budget"]
        missing = receipt["missing_theorem"]

        self.assertEqual(budget["moduli"], ["70", "130", "154", "286"])
        self.assertIn(
            "sum_d L1_d*eta_d(N) < local_main(N)",
            budget["direct_sufficient_inequality"])
        self.assertIn(
            "sum_d max(0,B_d(N)) < local_main(N)",
            budget["component_bound_template"])
        self.assertIn(
            "sum_d L1_d*eta_d(N) < local_main(N)",
            missing["sufficient_eta_condition"])
        self.assertIn(
            "sum_d max(0,B_d(N)) < local_main(N)",
            missing["sufficient_one_sided_condition"])

    def test_budget_matches_four_modulus_formula_receipt(self):
        receipt = self.load_receipt()
        budget = receipt["coefficient_budget"]

        self.assertAlmostEqual(
            budget["minimum_local_main_over_even_residues"],
            0.6039353780830684,
            places=12)
        self.assertAlmostEqual(
            budget["total_l1_norm"],
            372.962002076135,
            places=12)
        self.assertAlmostEqual(
            budget["global_equal_residue_error_cap"],
            0.0016192946592982506,
            places=15)
        self.assertAlmostEqual(
            budget["global_equal_residue_error_cap"],
            budget["source_global_equal_residue_error_cap"],
            places=15)

    def test_finite_evidence_is_only_context(self):
        receipt = self.load_receipt()
        finite = receipt["finite_context"]

        self.assertFalse(
            receipt["acceptance_condition"][
                "finite_evidence_is_acceptance_condition"])
        self.assertFalse(finite["finite_evidence_is_acceptance_condition"])
        self.assertEqual(finite["checked_row_count"], 348)
        self.assertEqual(finite["checked_rows_with_adverse_drag_below_local_main"],
                         348)
        self.assertEqual(finite["tightest_known_adverse_drag_target"], 1124642)
        self.assertAlmostEqual(
            finite["tightest_known_adverse_drag_ratio"],
            0.23148438379145228,
            places=12)

    def test_frozen_constants_are_rejected_as_acceptance_substitute(self):
        receipt = self.load_receipt()
        finite = receipt["finite_context"]

        self.assertTrue(finite["frozen_component_constants_rejected"])
        self.assertEqual(finite["modulus_286_exceeding_row_count"], 2)
        self.assertIn(
            "frozen per-modulus adverse constants copied from checked rows",
            receipt["rejected_acceptance_substitutes"])
        self.assertIn(
            ".125, .126, or .13",
            receipt["acceptance_condition"]["normalization_boundary"])


if __name__ == "__main__":
    unittest.main()
