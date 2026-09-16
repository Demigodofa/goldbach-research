import json
import unittest
from pathlib import Path


EVIDENCE = Path(
    "evidence/"
    "mobius-moment-square-degree5-source-margin-clearance-family-audit.json")


class MobiusMomentSquareDegree5SourceMarginClearanceFamilyAuditTests(
        unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = json.loads(EVIDENCE.read_text(encoding="utf-8"))

    def test_receipt_preserves_boundaries(self):
        self.assertEqual(
            self.receipt["status"],
            "AUDIT_degree5_source_margin_clearance_family")
        self.assertTrue(self.receipt["finite_clearance_family_audit_only"])
        self.assertTrue(self.receipt["finite_diagnostic_only"])
        self.assertFalse(self.receipt["goldbach_proved"])
        self.assertFalse(self.receipt["source_start_theorem_proved"])
        self.assertFalse(self.receipt["clearance_family_theorem_proved"])

    def test_six_tight_blocks_are_grouped_by_clearance(self):
        self.assertEqual(self.receipt["scale_count"], 6)
        self.assertEqual(
            [(row["scale_modulus"], row["prime_modulus"])
             for row in self.receipt["scale_summaries"]],
            [(229, 379), (251, 379), (293, 461),
             (331, 599), (353, 599), (379, 599)])
        self.assertEqual(
            self.receipt["clearance_families"]["near_1_to_2"],
            "p*A < Q < 2*p*A")

    def test_negative_mass_is_not_forced_entirely_near_threshold(self):
        self.assertFalse(
            self.receipt["all_negative_denominators_near_threshold"])
        self.assertEqual(
            self.receipt["negative_denominator_family_counts"],
            {"far_3_plus": 0, "middle_2_to_3": 1, "near_1_to_2": 17})
        self.assertAlmostEqual(
            self.receipt["near_threshold_negative_denominator_fraction"],
            0.9444444444444444)

    def test_higher_clearance_net_margin_dominates_low_clearance_leakage(self):
        self.assertTrue(
            self.receipt["all_middle_far_positive_dominates_near_negative"])
        self.assertTrue(
            self.receipt["all_middle_far_total_dominates_near_negative"])
        self.assertAlmostEqual(
            self.receipt["maximum_near_negative_over_middle_far_positive"],
            0.0009319007678001933)
        for row in self.receipt["scale_summaries"]:
            self.assertGreater(
                row["middle_far_total_margin_sum"],
                row["near_negative_abs"])

    def test_m229_records_the_only_middle_band_adverse_exception(self):
        first = self.receipt["scale_summaries"][0]
        self.assertEqual(first["scale_modulus"], 229)
        self.assertFalse(first["all_negative_denominators_near_threshold"])
        middle = first["family_summaries"]["middle_2_to_3"]
        self.assertEqual(middle["negative_count"], 1)
        self.assertEqual(
            middle["largest_negative"]["reduced_denominator"], 46189)
        self.assertAlmostEqual(
            middle["largest_negative"]["clearance_ratio_q_over_pA"],
            2.8342026139780327)

    def test_candidate_subtarget_is_not_promoted(self):
        target = self.receipt["candidate_next_theorem_subtarget"]
        self.assertEqual(
            target["name"],
            "near-threshold leakage versus higher-clearance dominance")
        self.assertEqual(target["novelty_label"], "new-to-this-task")
        self.assertIn("middle/far net margin", target["falsifier"])


if __name__ == "__main__":
    unittest.main()
