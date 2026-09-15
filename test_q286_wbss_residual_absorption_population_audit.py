import json
import unittest
from pathlib import Path


class Q286WbssResidualAbsorptionPopulationAuditTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/q286-wbss-residual-absorption-population-audit.json"
        ).read_text(encoding="utf-8"))

    def test_receipt_preserves_boundaries(self):
        receipt = self.load_receipt()

        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["residual_absorption_theorem_proved"])
        self.assertFalse(receipt["fresh_holdout_claimed"])
        self.assertTrue(receipt["universal_bound_open"])
        self.assertIn("finite q286-WBSS full dual-edge population diagnostic",
                      receipt["status_boundary"])

    def test_population_counts_extend_post_discovery_fixture(self):
        receipt = self.load_receipt()
        summaries = receipt["summaries"]

        self.assertEqual(summaries["all_dual_edge_rows"]["row_count"], 230)
        self.assertEqual(summaries["discovery_rows"]["row_count"], 34)
        self.assertEqual(summaries["post_discovery_rows"]["row_count"], 196)
        self.assertEqual(
            summaries["all_dual_edge_rows"]["positive_pushback_row_count"],
            29)

    def test_threshold_results_match_expected_bucket_behavior(self):
        receipt = self.load_receipt()

        self.assertTrue(receipt["one_eighth_cap_falsified"])
        self.assertTrue(receipt[
            "point_126_cap_survives_full_dual_edge_population"])
        self.assertTrue(receipt[
            "point_13_cap_survives_full_dual_edge_population"])

    def test_worst_row_stays_in_post_discovery_bucket(self):
        receipt = self.load_receipt()
        all_worst = receipt["summaries"]["all_dual_edge_rows"]["worst_row"]
        discovery_worst = receipt["summaries"]["discovery_rows"]["worst_row"]

        self.assertEqual(all_worst["target"], 365578)
        self.assertEqual(all_worst["block_index_after_discovery"], 4)
        self.assertAlmostEqual(
            all_worst["pushback_to_main_drag_ratio"],
            0.12566677703853088,
            places=14)
        self.assertLess(
            discovery_worst["pushback_to_main_drag_ratio"],
            all_worst["pushback_to_main_drag_ratio"])

    def test_top20_drag_keeps_sign_on_full_population(self):
        receipt = self.load_receipt()
        self.assertEqual(
            receipt["summaries"]["all_dual_edge_rows"][
                "top20_nonnegative_count"],
            0)


if __name__ == "__main__":
    unittest.main()
