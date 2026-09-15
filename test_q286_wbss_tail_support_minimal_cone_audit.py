import json
import unittest
from pathlib import Path


class Q286WbssTailSupportMinimalConeAuditTests(unittest.TestCase):
    def test_receipt_preserves_boundaries(self):
        receipt = json.loads(Path(
            "evidence/q286-wbss-tail-support-minimal-cone-audit.json"
        ).read_text(encoding="utf-8"))

        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["tail_support_projection_theorem_proved"])
        self.assertFalse(receipt["signed_discrepancy_theorem_proved"])
        self.assertIn("finite tail-support minimal-cone LP audit",
                      receipt["status_boundary"])

    def test_single_modulus_130_is_the_unique_minimal_tail_closer(self):
        receipt = json.loads(Path(
            "evidence/q286-wbss-tail-support-minimal-cone-audit.json"
        ).read_text(encoding="utf-8"))

        self.assertEqual(
            receipt["minimum_tail_subset_size_for_both_families"], 1)
        self.assertEqual(
            [row["tail_subset"]
             for row in receipt["minimal_tail_subsets_for_both_families"]],
            [[130]],
        )
        self.assertEqual(
            receipt["minimal_tail_subsets_for_both_families"][0]["moduli"],
            [70, 130, 154, 286],
        )

    def test_dominant_only_fails_three_rows(self):
        receipt = json.loads(Path(
            "evidence/q286-wbss-tail-support-minimal-cone-audit.json"
        ).read_text(encoding="utf-8"))
        dominant = receipt["summary_by_tail_subset_size"]["0"]["best_subsets"][0]

        self.assertEqual(
            dominant["full_bad_targets"], [90644, 94856, 109178])
        self.assertEqual(
            dominant["edge_beta_bad_targets"], [90644, 94856, 109178])
        self.assertEqual(dominant["bad_measure_feasible_count_both_families"],
                         3)

    def test_modulus_130_projection_span_residual_is_tiny(self):
        receipt = json.loads(Path(
            "evidence/q286-wbss-tail-support-minimal-cone-audit.json"
        ).read_text(encoding="utf-8"))
        closer = receipt["minimal_tail_subsets_for_both_families"][0]

        self.assertLess(closer["full_span_l2_residual_max"], 1e-12)
        self.assertLess(closer["edge_beta_span_l2_residual_max"], 1e-12)

    def test_every_closing_subset_contains_130(self):
        receipt = json.loads(Path(
            "evidence/q286-wbss-tail-support-minimal-cone-audit.json"
        ).read_text(encoding="utf-8"))

        for row in receipt["all_subset_rows"]:
            if row["forces_both_families_positive"]:
                self.assertIn(130, row["tail_subset"])


if __name__ == "__main__":
    unittest.main()
