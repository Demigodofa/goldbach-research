import json
import unittest
from pathlib import Path


class Q286WbssDirectWitnessResidueLiftHoldoutTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/"
            "q286-wbss-direct-witness-residue-lift-holdout.json"
        ).read_text(encoding="utf-8"))

    def test_receipt_preserves_boundaries(self):
        receipt = self.load_receipt()

        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["wbss_theorem_proved"])
        self.assertFalse(receipt["signed_projection_theorem_proved"])
        self.assertTrue(receipt["universal_bound_open"])
        self.assertIn("finite targeted q286-WBSS direct-witness",
                      receipt["status_boundary"])

    def test_uses_same_lifted_denominator_as_residual_holdout(self):
        receipt = self.load_receipt()
        residual = json.loads(Path(
            "evidence/"
            "q286-wbss-residual-absorption-residue-lift-holdout.json"
        ).read_text(encoding="utf-8"))

        self.assertEqual(receipt["holdout"]["target_count"], 116)
        self.assertEqual(
            receipt["holdout"]["target_count"],
            residual["holdout"]["target_count"])
        self.assertEqual(
            receipt["holdout"]["target_minimum"],
            residual["holdout"]["target_minimum"])
        self.assertEqual(
            receipt["holdout"]["target_maximum"],
            residual["holdout"]["target_maximum"])

    def test_raw_witness_survives_when_top20_split_fails(self):
        receipt = self.load_receipt()
        summary = receipt["holdout"]["summary"]

        self.assertTrue(receipt["direct_witness_survives_holdout"])
        self.assertTrue(
            receipt["split_failure_interpreted_as_decomposition_failure"])
        self.assertEqual(summary["actual_positive_count"], 116)
        self.assertEqual(summary["actual_nonpositive_count"], 0)
        self.assertEqual(summary["top20_nonnegative_count"], 70)
        self.assertEqual(
            summary["top20_nonnegative_but_raw_positive_count"], 70)

    def test_tightest_direct_row_is_recorded(self):
        receipt = self.load_receipt()
        summary = receipt["holdout"]["summary"]

        self.assertEqual(summary["minimum_actual_expectation_row"]["target"],
                         965362)
        self.assertAlmostEqual(
            summary["actual_expectation_summary"]["minimum"],
            0.674072332014227,
            places=12)
        self.assertAlmostEqual(
            summary["lambda_phi_summary"]["maximum"],
            0.213151501463301,
            places=12)

    def test_direct_reconstruction_matches_optimized_filter(self):
        receipt = self.load_receipt()
        summary = receipt["holdout"]["summary"]

        self.assertLess(
            summary["maximum_full_reconstruction_error"], 1e-12)
        self.assertLess(
            summary["maximum_first_three_reconstruction_error"], 1e-12)


if __name__ == "__main__":
    unittest.main()
