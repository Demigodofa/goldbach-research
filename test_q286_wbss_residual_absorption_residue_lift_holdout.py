import json
import unittest
from pathlib import Path


class Q286WbssResidualAbsorptionResidueLiftHoldoutTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/"
            "q286-wbss-residual-absorption-residue-lift-holdout.json"
        ).read_text(encoding="utf-8"))

    def test_receipt_preserves_boundaries(self):
        receipt = self.load_receipt()

        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["residual_absorption_theorem_proved"])
        self.assertFalse(receipt["signed_projection_theorem_proved"])
        self.assertTrue(receipt["fresh_holdout_claimed"])
        self.assertTrue(receipt["universal_bound_open"])
        self.assertIn("finite targeted q286-WBSS residue-lift holdout",
                      receipt["status_boundary"])

    def test_holdout_uses_positive_residual_source_residues(self):
        receipt = self.load_receipt()
        source = receipt["source_population"]
        holdout = receipt["holdout"]

        self.assertEqual(source["row_count"], 230)
        self.assertEqual(source["positive_pushback_row_count"], 29)
        self.assertEqual(holdout["lift_count_per_residue"], 4)
        self.assertEqual(
            holdout["target_count"],
            source["unique_positive_residue_count"] * 4)
        self.assertGreater(holdout["target_minimum"],
                           source["old_maximum_target"])

    def test_holdout_demotes_top20_sign_stability(self):
        receipt = self.load_receipt()

        self.assertTrue(receipt["top20_bandlimited_route_demoted_by_holdout"])
        self.assertEqual(receipt["holdout"]["summary"][
            "top20_nonnegative_count"], 70)
        self.assertFalse(receipt["point_126_cap_survives_holdout"])
        self.assertFalse(receipt["point_13_cap_survives_holdout"])

    def test_decimal_caps_are_explicit_finite_results(self):
        receipt = self.load_receipt()

        self.assertTrue(receipt["universal_bound_open"])
        self.assertIn("demotes the top-20 plus residual absorption route",
                      receipt["decision"])
        self.assertIsInstance(receipt["point_126_cap_survives_holdout"], bool)
        self.assertIsInstance(receipt["point_13_cap_survives_holdout"], bool)

    def test_ratio_cap_also_fails_where_ratio_is_defined(self):
        receipt = self.load_receipt()
        summary = receipt["holdout"]["summary"]

        self.assertGreater(
            summary["observed_minimum_passing_constant"], 1.0)
        self.assertEqual(summary["worst_row"]["target"], 971524)
        self.assertAlmostEqual(
            summary["worst_row"]["pushback_to_main_drag_ratio"],
            3.69343889977089,
            places=12)

    def test_all_lift_buckets_have_same_size(self):
        receipt = self.load_receipt()
        unique = receipt["source_population"]["unique_positive_residue_count"]

        for summary in receipt["holdout"]["summary_by_lift"].values():
            self.assertEqual(summary["row_count"], unique)


if __name__ == "__main__":
    unittest.main()
