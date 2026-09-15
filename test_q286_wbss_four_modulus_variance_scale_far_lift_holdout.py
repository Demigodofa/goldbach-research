import json
import unittest
from pathlib import Path


class Q286WbssFourModulusVarianceScaleFarLiftHoldoutTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/"
            "q286-wbss-four-modulus-variance-scale-far-lift-holdout.json"
        ).read_text(encoding="utf-8"))

    def test_receipt_preserves_boundaries(self):
        receipt = self.load_receipt()

        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["independence_theorem_proved"])
        self.assertFalse(
            receipt["fixed_modulus_equidistribution_theorem_proved"])
        self.assertTrue(receipt["universal_bound_open"])
        self.assertTrue(
            receipt["residual_absorption_constants_fit_finite_data_only"])

    def test_far_lift_uses_same_source_residue_count(self):
        receipt = self.load_receipt()
        holdout = receipt["holdout"]
        previous = receipt["previous_holdout"]

        self.assertEqual(holdout["source_positive_residue_count"], 29)
        self.assertEqual(holdout["lift_count_per_residue"], 4)
        self.assertEqual(holdout["target_count"], 116)
        self.assertGreater(
            holdout["target_minimum"], previous["source_target_maximum"])

    def test_direct_witness_survives_far_lift(self):
        receipt = self.load_receipt()
        summary = receipt["holdout"]["summary"]

        self.assertTrue(receipt["direct_witness_survives_far_lift_holdout"])
        self.assertEqual(summary["actual_positive_count"], 116)
        self.assertEqual(summary["actual_nonpositive_count"], 0)
        self.assertEqual(summary["variance_scale_positive_count"], 116)

    def test_below_three_adverse_z_cap_is_falsified(self):
        receipt = self.load_receipt()
        summary = receipt["holdout"]["summary"]

        self.assertFalse(
            receipt["below_three_adverse_z_cap_survives_far_lift_holdout"])
        self.assertTrue(receipt["previous_max_adverse_z_exceeded"])
        self.assertAlmostEqual(
            summary["adverse_iid_z_score_summary"]["maximum"],
            3.5107558040930176,
            places=12)
        self.assertEqual(summary["largest_adverse_z_row"]["target"], 1002478)

    def test_tightest_and_largest_lambda_rows_are_recorded(self):
        receipt = self.load_receipt()
        summary = receipt["holdout"]["summary"]

        self.assertEqual(summary["tightest_expectation_row"]["target"],
                         1001554)
        self.assertEqual(summary["largest_lambda_row"]["target"], 1002478)
        self.assertTrue(receipt["previous_max_lambda_exceeded"])
        self.assertAlmostEqual(
            summary["lambda_phi_summary"]["maximum"],
            0.29444884696113977,
            places=12)

    def test_formula_reconstructs_direct_full_expectation(self):
        receipt = self.load_receipt()
        summary = receipt["holdout"]["summary"]

        self.assertLess(
            summary["formula_reconstruction_error_summary"]["maximum"],
            1e-12)


if __name__ == "__main__":
    unittest.main()
