import json
import unittest
from pathlib import Path


EVIDENCE = Path(
    "evidence/"
    "mobius-moment-square-degree5-q46189-replacement-phase-profile-audit.json")


class MobiusMomentSquareDegree5Q46189ReplacementPhaseProfileAuditTests(
        unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = json.loads(EVIDENCE.read_text(encoding="utf-8"))

    def test_receipt_preserves_boundaries(self):
        self.assertEqual(
            self.receipt["status"],
            "AUDIT_q46189_replacement_phase_profile")
        self.assertTrue(self.receipt["finite_phase_profile_audit_only"])
        self.assertTrue(self.receipt["finite_diagnostic_only"])
        self.assertFalse(
            self.receipt["symbolic_replacement_ratio_theorem_proved"])
        self.assertFalse(
            self.receipt["replacement_family_payment_theorem_proved"])
        self.assertFalse(self.receipt["goldbach_proved"])

    def test_q46189_is_below_half_and_adverse(self):
        q_row = self.receipt["q46189_profile"]
        classification = self.receipt["classification"]

        self.assertEqual(q_row["reduced_denominator"], 46189)
        self.assertAlmostEqual(
            q_row["active_over_full_cross_ratio"],
            0.4973090372347702)
        self.assertAlmostEqual(
            q_row["ratio_minus_half"],
            -0.0026909627652297874)
        self.assertAlmostEqual(
            q_row["margin_full_over_2_minus_active"],
            -8444721229.472412)
        self.assertTrue(classification["q46189_ratio_below_half"])
        self.assertTrue(classification["q46189_margin_adverse"])

    def test_all_replacements_are_above_half_and_positive(self):
        summary = self.receipt["replacement_summary"]
        classification = self.receipt["classification"]

        self.assertEqual(summary["row_count"], 10)
        self.assertAlmostEqual(
            summary["minimum_ratio_minus_half"],
            0.07635340770691146)
        self.assertAlmostEqual(
            summary["maximum_ratio_minus_half"],
            0.5735414442150175)
        self.assertAlmostEqual(
            summary["positive_margin_sum"],
            14694916931621.637)
        self.assertAlmostEqual(
            summary["payment_over_q46189_adverse"],
            1740.1304948156007)
        self.assertTrue(classification["all_replacements_ratio_above_half"])
        self.assertTrue(classification["all_replacements_margin_positive"])
        self.assertTrue(
            classification["all_replacements_have_negative_full_cross"])

    def test_replacements_share_negative_real_scalar_alignment(self):
        summary = self.receipt["replacement_summary"]
        classification = self.receipt["classification"]

        self.assertLess(
            summary["maximum_relative_scalar_residual"],
            7e-16)
        self.assertTrue(
            classification["all_replacements_scalar_negative_real"])
        for row in self.receipt["replacement_profiles"]:
            self.assertLess(row["best_scalar_right_over_left_real"], 0)
            self.assertLess(
                abs(row["best_scalar_right_over_left_imag"]), 3e-18)
            self.assertLess(row["relative_scalar_residual"], 7e-16)

    def test_each_omitted_high_prime_family_stays_above_half(self):
        families = self.receipt[
            "omitted_high_prime_family_phase_summaries"]
        classification = self.receipt["classification"]

        self.assertEqual(set(families), {"11", "13", "17", "19"})
        self.assertTrue(
            classification[
                "all_omitted_high_prime_families_ratio_above_half"])
        self.assertAlmostEqual(
            families["17"]["minimum_ratio_minus_half"],
            0.07635340770691146)
        for summary in families.values():
            self.assertTrue(summary["all_rows_ratio_above_half"])
            self.assertTrue(summary["all_rows_margin_positive"])
            self.assertTrue(summary["all_rows_match_ratio_side"])

    def test_next_action_is_symbolic_ratio_inequality(self):
        action = self.receipt["candidate_next_action"]

        self.assertEqual(
            action["name"],
            "symbolic replacement ratio inequality")
        self.assertIn("one-half active/full ratio", action["mechanism"])
        self.assertIn("algebraic numerator forms",
                      action["smallest_next_test"])


if __name__ == "__main__":
    unittest.main()
