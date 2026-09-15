import json
import unittest
from pathlib import Path


class Q286WbssFourModulusLambdaHorizonHoldoutTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/"
            "q286-wbss-four-modulus-lambda-horizon-holdout.json"
        ).read_text(encoding="utf-8"))

    def test_receipt_preserves_boundaries(self):
        receipt = self.load_receipt()

        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["signed_concentration_theorem_proved"])
        self.assertFalse(
            receipt["fixed_modulus_equidistribution_theorem_proved"])
        self.assertFalse(receipt["universal_lambda_bound_proved"])
        self.assertTrue(receipt["universal_bound_open"])
        self.assertTrue(
            receipt["residual_absorption_constants_fit_finite_data_only"])

    def test_horizon_starts_after_previous_far_lift(self):
        receipt = self.load_receipt()
        holdout = receipt["holdout"]
        previous = receipt["previous_holdout"]

        self.assertEqual(holdout["source_positive_residue_count"], 29)
        self.assertEqual(holdout["lift_count_per_residue"], 8)
        self.assertEqual(holdout["target_count"], 232)
        self.assertGreater(
            holdout["target_minimum"], previous["source_target_maximum"])
        self.assertEqual(holdout["target_minimum"], 1036248)
        self.assertEqual(holdout["target_maximum"], 1115822)

    def test_direct_witness_and_lambda_budget_survive(self):
        receipt = self.load_receipt()
        summary = receipt["holdout"]["summary"]

        self.assertTrue(receipt["direct_witness_survives_horizon_holdout"])
        self.assertTrue(receipt["lambda_budget_survives_horizon_holdout"])
        self.assertEqual(summary["actual_positive_count"], 232)
        self.assertEqual(summary["actual_nonpositive_count"], 0)
        self.assertEqual(summary["lambda_budget_failure_count"], 0)
        self.assertLess(summary["lambda_phi_summary"]["maximum"], 1.0)

    def test_horizon_does_not_exceed_prior_lambda_or_z_maxima(self):
        receipt = self.load_receipt()
        summary = receipt["holdout"]["summary"]

        self.assertFalse(receipt["previous_max_lambda_exceeded"])
        self.assertFalse(receipt["previous_max_adverse_z_exceeded"])
        self.assertAlmostEqual(
            summary["lambda_phi_summary"]["maximum"],
            0.18121406011311555,
            places=12)
        self.assertEqual(summary["largest_lambda_row"]["target"], 1059514)
        self.assertAlmostEqual(
            summary["adverse_iid_z_score_summary"]["maximum"],
            1.9123648886316162,
            places=12)
        self.assertEqual(summary["largest_adverse_z_row"]["target"], 1113078)

    def test_tightest_expectation_and_reconstruction_are_recorded(self):
        receipt = self.load_receipt()
        summary = receipt["holdout"]["summary"]

        self.assertEqual(summary["tightest_expectation_row"]["target"],
                         1059514)
        self.assertAlmostEqual(
            summary["tightest_expectation_row"]["actual_formula_expectation"],
            0.609620382302563,
            places=12)
        self.assertLess(
            summary["formula_reconstruction_error_summary"]["maximum"],
            1e-12)

    def test_each_lift_bucket_is_present(self):
        receipt = self.load_receipt()
        by_lift = receipt["holdout"]["summary"]["summary_by_lift_index"]

        self.assertEqual(set(by_lift), {str(i) for i in range(8)})
        for stats in by_lift.values():
            self.assertEqual(stats["row_count"], 29)
            self.assertEqual(stats["actual_positive_count"], 29)


if __name__ == "__main__":
    unittest.main()
