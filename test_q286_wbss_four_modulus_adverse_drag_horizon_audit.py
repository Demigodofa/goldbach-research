import json
import unittest
from pathlib import Path


class Q286WbssFourModulusAdverseDragHorizonAuditTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/"
            "q286-wbss-four-modulus-adverse-drag-horizon-audit.json"
        ).read_text(encoding="utf-8"))

    def test_receipt_preserves_boundaries(self):
        receipt = self.load_receipt()

        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(
            receipt["one_sided_signed_concentration_theorem_proved"])
        self.assertFalse(
            receipt["fixed_modulus_equidistribution_theorem_proved"])
        self.assertFalse(receipt["universal_negative_drag_bound_proved"])
        self.assertTrue(receipt["universal_bound_open"])

    def test_adverse_drag_certificate_survives(self):
        receipt = self.load_receipt()
        summary = receipt["holdout"]["summary"]

        self.assertTrue(receipt["adverse_drag_certificate_survives_horizon"])
        self.assertEqual(summary["row_count"], 232)
        self.assertEqual(summary["actual_positive_count"], 232)
        self.assertEqual(summary["adverse_only_positive_count"], 232)
        self.assertEqual(summary["adverse_only_nonpositive_count"], 0)
        self.assertAlmostEqual(
            summary["negative_drag_ratio_summary"]["maximum"],
            0.18121406011311528,
            places=12)
        self.assertEqual(summary["largest_negative_drag_row"]["target"],
                         1059514)

    def test_subsets_and_single_moduli_are_not_essential(self):
        receipt = self.load_receipt()
        summary = receipt["holdout"]["summary"]

        self.assertTrue(receipt["all_projected_subsets_survive_horizon"])
        self.assertFalse(receipt["single_modulus_dependence_detected"])
        self.assertEqual(summary["all_projected_subsets_positive_count"], 232)
        self.assertEqual(summary["projected_subset_checks"], 232 * 15)
        self.assertEqual(
            summary["lowest_subset_expectation_row"][
                "minimum_projected_subset_expectation"]["moduli"],
            ["70", "130", "154", "286"],
        )

        for stats in receipt["holdout"]["modulus_summaries"].values():
            self.assertEqual(stats["removed_nonpositive_count"], 0)
            self.assertEqual(stats["only_nonpositive_count"], 0)

    def test_tightest_adverse_only_row_matches_lambda_row(self):
        receipt = self.load_receipt()
        summary = receipt["holdout"]["summary"]
        row = summary["tightest_adverse_only_row"]

        self.assertEqual(row["target"], 1059514)
        self.assertAlmostEqual(row["adverse_only_expectation"],
                               0.6096203823025632,
                               places=12)
        self.assertAlmostEqual(row["local_uniform_main_term"],
                               0.7445418302942308,
                               places=12)
        self.assertLess(
            summary["formula_reconstruction_error_summary"]["maximum"],
            1e-12)

    def test_horizon_range_is_preserved(self):
        receipt = self.load_receipt()
        holdout = receipt["holdout"]

        self.assertEqual(holdout["target_count"], 232)
        self.assertEqual(holdout["target_minimum"], 1036248)
        self.assertEqual(holdout["target_maximum"], 1115822)


if __name__ == "__main__":
    unittest.main()
