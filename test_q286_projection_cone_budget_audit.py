import json
import unittest
from pathlib import Path


class Q286ProjectionConeBudgetAuditTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/q286-projection-cone-budget-audit.json"
        ).read_text(encoding="utf-8"))

    def test_receipt_preserves_boundaries(self):
        receipt = self.load_receipt()

        self.assertEqual(
            receipt["status"],
            "HOLD_projection_uniformity_sufficient_but_too_strong")
        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["projection_uniformity_theorem_proved"])
        self.assertFalse(
            receipt["signed_binary_prime_correlation_theorem_proved"])
        self.assertTrue(receipt["universal_bound_open"])
        self.assertIn("not only lower-dimensional AP", receipt["decision"])

    def test_prime_factor_marginals_are_too_weak(self):
        receipt = self.load_receipt()
        summary = receipt["summary"]

        self.assertEqual(summary["selected_target_count"], 7)
        self.assertEqual(
            summary["prime_factor_exact_marginal_bad_feasible_count"], 7)
        for row in receipt["target_rows"]:
            self.assertTrue(
                row["prime_factor_exact_marginal_cone"][
                    "bad_measure_feasible"])
            self.assertLessEqual(
                row["prime_factor_exact_marginal_cone"]["bad_first_three"],
                -0.3 + 1e-10)
            self.assertLessEqual(
                row["prime_factor_exact_marginal_cone"]["bad_full_action"],
                1e-10)

    def test_exact_q286_projection_uniformity_excludes_bad_branch(self):
        receipt = self.load_receipt()
        summary = receipt["summary"]

        self.assertEqual(
            summary["exact_q286_projection_uniform_bad_feasible_count"], 0)
        for row in receipt["target_rows"]:
            self.assertFalse(
                row["exact_q286_projection_uniform_cone"][
                    "bad_measure_feasible"])

    def test_projection_uniformity_budget_is_stronger_than_actual_rows(self):
        receipt = self.load_receipt()
        summary = receipt["summary"]

        self.assertEqual(summary["actual_tv_exceeds_minimum_bad_tv_count"], 7)
        self.assertEqual(
            summary["actual_linf_exceeds_minimum_bad_linf_count"], 7)
        self.assertLess(
            summary["minimum_bad_q286_projection_tv_summary"]["maximum"],
            summary["actual_q286_projection_tv_summary"]["minimum"])
        self.assertLess(
            summary["minimum_bad_q286_projection_linf_summary"]["maximum"],
            summary["actual_q286_projection_linf_summary"]["minimum"])

    def test_tightest_tv_row_is_recorded(self):
        receipt = self.load_receipt()
        tight = receipt["summary"]["tightest_minimum_bad_tv_row"]

        self.assertEqual(tight["target"], 1379072)
        self.assertAlmostEqual(
            tight["minimum_bad_q286_projection_l1"][
                "minimum_bad_projection_total_variation"],
            0.008069873564730923)
        self.assertGreater(
            tight["actual_q286_projection"][
                "actual_projection_total_variation"],
            0.06)


if __name__ == "__main__":
    unittest.main()
