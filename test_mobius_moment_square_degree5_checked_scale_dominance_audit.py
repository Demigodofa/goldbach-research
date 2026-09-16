import json
import unittest
from pathlib import Path

from tools.build_mobius_moment_square_degree5_checked_scale_dominance_audit import (
    dominance_row,
    flatten_rows,
    scale_summary,
)


EVIDENCE = Path(
    "evidence/mobius-moment-square-degree5-checked-scale-dominance-audit.json")


class MobiusMomentSquareDegree5CheckedScaleDominanceAuditTests(
        unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = json.loads(EVIDENCE.read_text(encoding="utf-8"))

    def test_dominance_row_translates_threshold(self):
        row = dominance_row(
            scale_modulus=127,
            prime_modulus=139,
            label="00,12",
            active=-8.0,
            full=-10.0,
            half=-3.0,
        )
        self.assertAlmostEqual(row["active_over_full_ratio"], 0.8)
        self.assertAlmostEqual(
            row["dominance_slack_above_one_half"], 0.3)
        self.assertTrue(row["dominates_one_half_signed_full"])

    def test_flatten_rows_keeps_components_and_totals(self):
        scale_results = [{
            "prime_rows": [{
                "component_rows": [{"label": "a"}, {"label": "b"}],
                "degree5_total_row": {"label": "TOTAL"},
            }]
        }]
        self.assertEqual(
            [row["label"] for row in flatten_rows(scale_results)],
            ["a", "b", "TOTAL"])
        self.assertEqual(
            [row["label"] for row in flatten_rows(
                scale_results, include_totals=False)],
            ["a", "b"])

    def test_scale_summary_identifies_weakest_row(self):
        scale_row = {
            "scale_modulus": 127,
            "prime_count": 1,
            "row_count": 10,
            "ell_freeze": 15,
            "divisor_range": [2, 5],
            "prime_rows": [{
                "component_rows": [
                    {
                        "label": "00,12",
                        "dominance_slack_above_one_half": 0.2,
                        "dominates_one_half_signed_full": True,
                    },
                    {
                        "label": "01,02",
                        "dominance_slack_above_one_half": 0.1,
                        "dominates_one_half_signed_full": True,
                    },
                ],
                "degree5_total_row": {
                    "label": "TOTAL",
                    "dominance_slack_above_one_half": 0.3,
                    "dominates_one_half_signed_full": True,
                },
            }],
        }
        summary = scale_summary(scale_row)
        self.assertEqual(summary["dominance_row_count"], 3)
        self.assertEqual(
            summary["dominance_slack_sign_counts"],
            {"positive": 3, "zero": 0, "negative": 0})
        self.assertEqual(summary["weakest_dominance_row"]["label"], "01,02")

    def test_receipt_preserves_boundaries(self):
        self.assertEqual(
            self.receipt["status"],
            "CHECK_degree5_checked_scale_primewise_dominance")
        self.assertTrue(
            self.receipt["finite_checked_scale_dominance_diagnostic_only"])
        self.assertTrue(self.receipt["finite_diagnostic_only"])
        self.assertFalse(self.receipt["goldbach_proved"])
        self.assertFalse(
            self.receipt["checked_scale_dominance_theorem_proved"])
        self.assertFalse(
            self.receipt["robust_margin_universal_theorem_proved"])

    def test_all_checked_scale_rows_dominate_one_half(self):
        self.assertEqual(
            self.receipt["scales"],
            [127, 149, 167, 191, 211, 227])
        self.assertEqual(self.receipt["prime_count_total"], 189)
        self.assertEqual(self.receipt["component_row_count"], 567)
        self.assertEqual(self.receipt["degree5_total_row_count"], 189)
        self.assertEqual(self.receipt["dominance_row_count"], 756)
        self.assertTrue(
            self.receipt["all_rows_dominate_one_half_signed_full"])
        self.assertEqual(
            self.receipt["all_dominance_slack_sign_counts"],
            {"positive": 756, "zero": 0, "negative": 0})

    def test_global_weakest_row_is_known_weak_block_component(self):
        weakest = self.receipt["weakest_dominance_row"]
        self.assertEqual(weakest["scale_modulus"], 167)
        self.assertEqual(weakest["prime_modulus"], 181)
        self.assertEqual(weakest["label"], "00,12")
        self.assertAlmostEqual(
            weakest["active_over_full_ratio"],
            0.5563677490893767)
        self.assertAlmostEqual(
            self.receipt["minimum_dominance_slack_above_one_half"],
            0.056367749089376695)

    def test_each_scale_summary_passes(self):
        self.assertEqual(len(self.receipt["scale_summaries"]), 6)
        for summary in self.receipt["scale_summaries"]:
            self.assertTrue(
                summary["all_rows_dominate_one_half_signed_full"])
            self.assertGreater(
                summary["minimum_dominance_slack_above_one_half"], 0.0)


if __name__ == "__main__":
    unittest.main()
