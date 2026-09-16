import json
import unittest
from pathlib import Path


EVIDENCE = Path(
    "evidence/"
    "mobius-moment-square-degree5-band-clearance-holdout.json")


class MobiusMomentSquareDegree5BandClearanceHoldoutTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = json.loads(EVIDENCE.read_text(encoding="utf-8"))

    def test_receipt_preserves_boundaries(self):
        self.assertEqual(
            self.receipt["status"],
            "HOLDOUT_degree5_band_clearance_family")
        self.assertTrue(self.receipt["finite_band_clearance_holdout_only"])
        self.assertTrue(self.receipt["finite_diagnostic_only"])
        self.assertFalse(self.receipt["goldbach_proved"])
        self.assertFalse(self.receipt["source_start_theorem_proved"])
        self.assertFalse(self.receipt["moving_prime_block_theorem_proved"])
        self.assertFalse(self.receipt["clearance_family_theorem_proved"])

    def test_four_sigma_band_minimum_blocks_are_checked(self):
        self.assertEqual(self.receipt["band_count"], 4)
        self.assertEqual(
            [(row["band"], row["scale_modulus"], row["prime_modulus"])
             for row in self.receipt["band_summaries"]],
            [
                ("sigma_1_00_1_25", 229, 283),
                ("sigma_1_25_1_50", 331, 479),
                ("sigma_1_50_1_75", 229, 379),
                ("sigma_1_75_2_00", 331, 599),
            ])

    def test_middle_far_dominates_near_leakage_in_every_band(self):
        self.assertTrue(
            self.receipt["all_middle_far_positive_dominates_near_negative"])
        self.assertTrue(
            self.receipt["all_middle_far_total_dominates_near_negative"])
        self.assertAlmostEqual(
            self.receipt["maximum_near_negative_over_middle_far_positive"],
            0.0016400172796714467)
        for row in self.receipt["band_summaries"]:
            self.assertGreater(
                row["middle_far_total_margin_sum"],
                row["near_negative_abs"])

    def test_all_negative_near_threshold_is_false_but_localized(self):
        self.assertFalse(
            self.receipt["all_negative_denominators_near_threshold"])
        self.assertEqual(
            self.receipt["negative_denominator_family_counts"],
            {"far_3_plus": 0, "middle_2_to_3": 1, "near_1_to_2": 17})
        exceptional = [
            row for row in self.receipt["band_summaries"]
            if not row["all_negative_denominators_near_threshold"]
        ]
        self.assertEqual(len(exceptional), 1)
        self.assertEqual(exceptional[0]["band"], "sigma_1_50_1_75")
        self.assertEqual(exceptional[0]["scale_modulus"], 229)
        self.assertEqual(exceptional[0]["prime_modulus"], 379)

    def test_low_sigma_band_is_ratio_worst(self):
        first = self.receipt["band_summaries"][0]
        self.assertEqual(first["band"], "sigma_1_00_1_25")
        self.assertAlmostEqual(
            first["near_negative_over_middle_far_positive"],
            0.0016400172796714467)
        self.assertEqual(
            first["family_summaries"]["near_1_to_2"]["negative_count"], 3)

    def test_replacement_target_is_sigma_banded_clearance_control(self):
        target = self.receipt["candidate_next_theorem_target"]
        self.assertEqual(
            target["name"],
            "sigma-banded clearance-family denominator control")
        self.assertIn("For each sigma band", target["mechanism"])
        self.assertEqual(target["novelty_label"], "new-to-this-task")


if __name__ == "__main__":
    unittest.main()
