import unittest

from tools.build_mobius_moment_square_degree5_primewise_dominance_audit import (
    build_receipt,
    dominance_row,
    total_dominance_row,
)


class MobiusMomentSquareDegree5PrimewiseDominanceAuditTests(
        unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = build_receipt()

    def test_dominance_row_translates_negative_half_frame(self):
        prime_row = {"prime_modulus": 17}
        contributor = {
            "left_label": "00",
            "right_label": "12",
            "active_contribution": -6.0,
            "full_contribution": -10.0,
            "half_frame_contribution": -1.0,
        }
        row = dominance_row(prime_row, contributor)
        self.assertAlmostEqual(row["active_over_full_ratio"], 0.6)
        self.assertAlmostEqual(
            row["dominance_slack_above_one_half"], 0.1)
        self.assertTrue(row["dominates_one_half_signed_full"])

    def test_total_dominance_row_sums_components(self):
        prime_row = {
            "prime_modulus": 19,
            "degree5_half_frame_total": -3.0,
            "contributors": [
                {
                    "active_contribution": -6.0,
                    "full_contribution": -10.0,
                },
                {
                    "active_contribution": -9.0,
                    "full_contribution": -12.0,
                },
            ],
        }
        row = total_dominance_row(prime_row)
        self.assertAlmostEqual(row["active_over_full_ratio"], 15 / 22)
        self.assertTrue(row["dominates_one_half_signed_full"])

    def test_receipt_preserves_boundaries(self):
        self.assertEqual(
            self.receipt["status"],
            "MEASURE_degree5_primewise_dominance_slack")
        self.assertTrue(
            self.receipt["finite_primewise_dominance_diagnostic_only"])
        self.assertTrue(self.receipt["finite_diagnostic_only"])
        self.assertFalse(self.receipt["goldbach_proved"])
        self.assertFalse(
            self.receipt["primewise_dominance_theorem_proved"])
        self.assertFalse(
            self.receipt["robust_margin_universal_theorem_proved"])

    def test_all_weak_block_ratios_exceed_one_half(self):
        self.assertEqual(self.receipt["scale_modulus"], 167)
        self.assertEqual(self.receipt["prime_count"], 29)
        self.assertTrue(
            self.receipt["all_component_ratios_exceed_one_half"])
        self.assertTrue(
            self.receipt["all_degree5_total_ratios_exceed_one_half"])
        self.assertEqual(
            self.receipt["component_dominance_slack_sign_counts"],
            {"positive": 87, "zero": 0, "negative": 0})
        self.assertEqual(
            self.receipt["degree5_total_dominance_slack_sign_counts"],
            {"positive": 29, "zero": 0, "negative": 0})

    def test_weakest_component_and_total_are_at_prime_181(self):
        weakest_component = self.receipt["weakest_component_dominance_row"]
        self.assertEqual(weakest_component["prime_modulus"], 181)
        self.assertEqual(weakest_component["left_label"], "00")
        self.assertEqual(weakest_component["right_label"], "12")
        self.assertAlmostEqual(
            weakest_component["active_over_full_ratio"],
            0.5563677490893767)
        self.assertAlmostEqual(
            self.receipt[
                "minimum_component_dominance_slack_above_one_half"],
            0.056367749089376695)

        weakest_total = self.receipt["weakest_degree5_total_dominance_row"]
        self.assertEqual(weakest_total["prime_modulus"], 181)
        self.assertAlmostEqual(
            weakest_total["active_over_full_ratio"],
            0.5696364991895461)
        self.assertAlmostEqual(
            self.receipt[
                "minimum_degree5_total_dominance_slack_above_one_half"],
            0.06963649918954606)

    def test_component_summaries_identify_three_degree5_pairs(self):
        self.assertEqual(
            set(self.receipt["component_summaries"]),
            {"00,12", "01,02", "01,11"})
        for summary in self.receipt["component_summaries"].values():
            self.assertEqual(summary["row_count"], 29)
            self.assertTrue(
                summary["all_rows_dominate_one_half_signed_full"])


if __name__ == "__main__":
    unittest.main()
