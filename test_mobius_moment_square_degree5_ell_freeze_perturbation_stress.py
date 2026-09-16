import json
import unittest
from pathlib import Path

from tools.build_mobius_moment_square_degree5_ell_freeze_perturbation_stress import (
    ell_freeze_values,
)


EVIDENCE = Path(
    "evidence/mobius-moment-square-degree5-ell-freeze-perturbation-stress.json")


class MobiusMomentSquareDegree5EllFreezePerturbationStressTests(
        unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = json.loads(EVIDENCE.read_text(encoding="utf-8"))

    def test_ell_values_are_local_perturbation_of_weak_block_freeze(self):
        self.assertEqual(ell_freeze_values(), [50, 51, 52, 53, 54])
        self.assertEqual(self.receipt["scale_modulus"], 167)
        self.assertEqual(self.receipt["base_parameters"]["ell_freeze"], 52)
        self.assertEqual(self.receipt["ell_freezes"], [50, 51, 52, 53, 54])
        self.assertEqual(self.receipt["ell_offsets"], [-2, -1, 0, 1, 2])

    def test_receipt_preserves_boundaries(self):
        self.assertEqual(
            self.receipt["status"],
            "STRESS_degree5_ell_freeze_perturbation_dominance")
        self.assertTrue(
            self.receipt["finite_ell_freeze_perturbation_stress_only"])
        self.assertTrue(self.receipt["finite_diagnostic_only"])
        self.assertFalse(self.receipt["goldbach_proved"])
        self.assertFalse(
            self.receipt["ell_freeze_dominance_theorem_proved"])
        self.assertFalse(
            self.receipt["robust_margin_universal_theorem_proved"])

    def test_all_perturbed_rows_dominate_one_half(self):
        self.assertEqual(self.receipt["ell_count"], 5)
        self.assertEqual(self.receipt["prime_count_per_ell"], 29)
        self.assertEqual(self.receipt["component_row_count"], 435)
        self.assertEqual(self.receipt["degree5_total_row_count"], 145)
        self.assertEqual(self.receipt["dominance_row_count"], 580)
        self.assertEqual(self.receipt["failure_row_count"], 0)
        self.assertEqual(self.receipt["failure_rows"], [])
        self.assertTrue(
            self.receipt["all_rows_dominate_one_half_signed_full"])
        self.assertEqual(
            self.receipt["all_dominance_slack_sign_counts"],
            {"positive": 580, "zero": 0, "negative": 0})

    def test_each_ell_summary_passes(self):
        self.assertEqual(len(self.receipt["ell_summaries"]), 5)
        for summary in self.receipt["ell_summaries"]:
            self.assertEqual(summary["prime_count"], 29)
            self.assertEqual(summary["component_row_count"], 87)
            self.assertEqual(summary["degree5_total_row_count"], 29)
            self.assertEqual(summary["dominance_row_count"], 116)
            self.assertTrue(
                summary["all_rows_dominate_one_half_signed_full"])
            self.assertEqual(
                summary["dominance_slack_sign_counts"],
                {"positive": 116, "zero": 0, "negative": 0})

    def test_weakest_perturbed_row_is_recorded(self):
        weakest = self.receipt["weakest_dominance_row"]
        self.assertEqual(weakest["scale_modulus"], 167)
        self.assertEqual(weakest["ell_freeze"], 53)
        self.assertEqual(weakest["prime_modulus"], 181)
        self.assertEqual(weakest["label"], "00,12")
        self.assertAlmostEqual(
            weakest["active_over_full_ratio"],
            0.5563677490893759)
        self.assertAlmostEqual(
            self.receipt["minimum_dominance_slack_above_one_half"],
            0.05636774908937592)


if __name__ == "__main__":
    unittest.main()
