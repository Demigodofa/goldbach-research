import json
import unittest
from pathlib import Path


class Q286WbssFourModulusVarianceScaleAuditTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/q286-wbss-four-modulus-variance-scale-audit.json"
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

    def test_variance_scale_exists_for_all_rows(self):
        receipt = self.load_receipt()
        summary = receipt["holdout"]["summary"]

        self.assertEqual(summary["row_count"], 116)
        self.assertEqual(summary["actual_positive_count"], 116)
        self.assertEqual(summary["actual_nonpositive_count"], 0)
        self.assertEqual(summary["variance_scale_positive_count"], 116)
        self.assertGreater(
            summary["local_phi_standard_deviation_summary"]["minimum"], 3.0)

    def test_adverse_load_is_finite_variance_sized(self):
        receipt = self.load_receipt()
        summary = receipt["holdout"]["summary"]

        self.assertAlmostEqual(
            summary["adverse_iid_z_score_summary"]["maximum"],
            2.696050693399999,
            places=12)
        self.assertLess(
            summary["adverse_iid_z_score_summary"]["maximum"], 3.0)
        self.assertEqual(summary["largest_adverse_z_row"]["target"], 992374)

    def test_tightest_row_is_recovered_but_not_largest_adverse_z(self):
        receipt = self.load_receipt()
        summary = receipt["holdout"]["summary"]

        self.assertEqual(summary["tightest_expectation_row"]["target"], 965362)
        self.assertEqual(summary["largest_lambda_row"]["target"], 965362)
        self.assertNotEqual(
            summary["largest_adverse_z_row"]["target"],
            summary["tightest_expectation_row"]["target"])
        self.assertAlmostEqual(
            summary["tightest_expectation_row"]["iid_z_score"],
            -2.318536356607163,
            places=12)

    def test_replays_decomposition_receipt(self):
        receipt = self.load_receipt()
        replay = receipt["holdout"]["decomposition_replay_check"]

        self.assertLess(
            replay["maximum_actual_expectation_abs_error"], 1e-12)
        self.assertLess(replay["maximum_lambda_phi_abs_error"], 1e-12)


if __name__ == "__main__":
    unittest.main()
