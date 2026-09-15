import json
import unittest
from pathlib import Path


class Q286WbssFourModulusEdgeCharacterLoadAuditTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/q286-wbss-four-modulus-edge-character-load-audit.json"
        ).read_text(encoding="utf-8"))

    def test_receipt_preserves_boundaries(self):
        receipt = self.load_receipt()

        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["character_sum_bound_proved"])
        self.assertFalse(
            receipt["binary_prime_projection_control_theorem_proved"])
        self.assertFalse(receipt["signed_discrepancy_theorem_proved"])
        self.assertTrue(receipt["universal_bound_open"])
        self.assertIn("finite q286-WBSS edge-character row-load",
                      receipt["status_boundary"])
        self.assertIn("not universal bounds", receipt["status_boundary"])

    def test_edge_character_basis_counts_are_preserved(self):
        receipt = self.load_receipt()

        self.assertEqual(receipt["edge_character_obligation_counts"], {
            "5,7": 8,
            "5,13": 17,
            "7,11": 23,
            "11,13": 50,
        })
        self.assertEqual(
            sum(row["mode_count"]
                for row in receipt["edge_basis_summary"].values()),
            98,
        )
        self.assertEqual(
            sum(row["group_count"]
                for row in receipt["edge_basis_summary"].values()),
            50,
        )

    def test_character_group_reconstruction_is_verified(self):
        receipt = self.load_receipt()

        self.assertTrue(receipt["edge_translation_verified"])
        self.assertLess(
            receipt["summaries"]["all_dual_edge_rows"][
                "maximum_group_reconstruction_error"],
            1e-9,
        )
        self.assertLess(
            receipt["summaries"]["post_discovery_rows"][
                "maximum_group_reconstruction_error"],
            1e-9,
        )

    def test_post_discovery_rows_are_all_negative_and_11_13_dominant(self):
        receipt = self.load_receipt()
        post = receipt["summaries"]["post_discovery_rows"]

        self.assertEqual(post["row_count"], 196)
        self.assertEqual(
            post["edge_signed_contribution_sum"]["negative_count"], 196)
        self.assertEqual(
            post["edge_signed_contribution_sum"]["positive_count"], 0)
        self.assertEqual(post["dominant_abs_edge_counts"], {
            "5,7": 0,
            "5,13": 0,
            "7,11": 0,
            "11,13": 196,
        })

    def test_all_rows_still_do_not_support_tiny_group_shortcut(self):
        receipt = self.load_receipt()
        all_rows = receipt["summaries"]["all_dual_edge_rows"]
        ranking = receipt["finite_group_load_ranking"]["all_dual_edge_rows"]

        self.assertEqual(all_rows["row_count"], 230)
        self.assertEqual(
            all_rows["dominant_abs_edge_counts"]["11,13"], 227)
        self.assertEqual(
            all_rows["edge_signed_contribution_sum"]["negative_count"], 230)
        self.assertEqual(ranking["group_count_with_recorded_top_load"], 50)
        self.assertEqual(ranking["rank_needed_for_50pct_abs_load"], 16)
        self.assertGreater(ranking["rank_needed_for_80pct_abs_load"], 20)


if __name__ == "__main__":
    unittest.main()
