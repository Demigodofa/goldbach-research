import json
import unittest
from pathlib import Path


EVIDENCE = Path(
    "evidence/"
    "mobius-moment-square-degree5-q46189-source-conductor-scalar-formula-audit.json")


class MobiusMomentSquareDegree5Q46189SourceConductorFormulaAuditTests(
        unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = json.loads(EVIDENCE.read_text(encoding="utf-8"))

    def test_receipt_preserves_boundaries(self):
        self.assertEqual(
            self.receipt["status"],
            "AUDIT_q46189_source_conductor_scalar_formula")
        self.assertTrue(
            self.receipt["finite_source_conductor_formula_audit_only"])
        self.assertTrue(self.receipt["finite_diagnostic_only"])
        self.assertFalse(
            self.receipt["source_conductor_scalar_formula_theorem_proved"])
        self.assertFalse(
            self.receipt["exact_log_polynomial_identity_theorem_proved"])
        self.assertFalse(self.receipt["goldbach_proved"])

    def test_q46189_formula_reproduces_raw_scalar(self):
        q_row = self.receipt["q46189_formula_row"]
        classification = self.receipt["classification"]

        self.assertEqual(q_row["reduced_denominator"], 46189)
        self.assertEqual(q_row["ordered_source_conductor_pair_count"], 6)
        self.assertAlmostEqual(
            q_row["formula_scalar_mean"],
            -0.07475328212536136)
        self.assertAlmostEqual(
            q_row["raw_scalar"],
            -0.07475328212536138)
        self.assertLess(q_row["max_abs_formula_pair_deviation"], 3e-17)
        self.assertLess(q_row["max_abs_formula_minus_raw_scalar"], 3e-17)
        self.assertTrue(q_row["source_conductor_formula_verified_to_tolerance"])
        self.assertTrue(classification["q46189_formula_verified"])
        self.assertTrue(
            classification["coefficient_source_is_float_logarithmic"])

    def test_q46189_has_expected_formula_source_pairs(self):
        q_row = self.receipt["q46189_formula_row"]
        pairs = [
            (row["left_source_conductor"], row["right_source_conductor"])
            for row in q_row["ordered_source_conductor_formula_rows"]
        ]

        self.assertEqual(pairs, [
            (143, 323),
            (187, 247),
            (209, 221),
            (221, 209),
            (247, 187),
            (323, 143),
        ])
        for row in q_row["ordered_source_conductor_formula_rows"]:
            self.assertIn("left_polynomial_coefficients", row)
            self.assertIn("right_polynomial_coefficients", row)
            self.assertEqual(row["formula_pair_frequency_count"], 34560)
            self.assertAlmostEqual(
                row["formula_scalar"],
                row["formula_unscaled_scalar"])

    def test_replacements_all_have_source_conductor_formula(self):
        rows = self.receipt["replacement_formula_rows"]
        classification = self.receipt["classification"]

        self.assertEqual(len(rows), 10)
        self.assertTrue(
            classification["all_replacements_formula_verified"])
        self.assertTrue(classification["all_rows_have_six_formula_pairs"])
        self.assertTrue(classification["all_replacements_ratio_above_half"])
        self.assertAlmostEqual(
            min(row["ratio_minus_half"] for row in rows),
            0.07635340770691146)
        self.assertAlmostEqual(
            max(row["ratio_minus_half"] for row in rows),
            0.5735414442150175)
        self.assertLess(
            max(row["max_abs_formula_pair_deviation"] for row in rows),
            3e-17)
        self.assertLess(
            max(row["max_abs_formula_minus_raw_scalar"] for row in rows),
            3e-17)
        for row in rows:
            self.assertEqual(row["ordered_source_conductor_pair_count"], 6)
            self.assertTrue(
                row["source_conductor_formula_verified_to_tolerance"])

    def test_each_omitted_high_prime_family_has_formula(self):
        families = self.receipt[
            "omitted_high_prime_family_formula_summaries"]

        self.assertEqual(set(families), {"11", "13", "17", "19"})
        self.assertAlmostEqual(
            families["17"]["minimum_ratio_minus_half"],
            0.07635340770691146)
        for summary in families.values():
            self.assertTrue(summary["all_rows_formula_verified"])
            self.assertLess(
                summary["maximum_formula_pair_deviation"], 3e-17)
            self.assertLess(
                summary["maximum_formula_minus_raw_scalar"], 3e-17)

    def test_next_action_is_exact_log_polynomial_identity(self):
        formula = self.receipt["formula"]
        action = self.receipt["candidate_next_action"]

        self.assertEqual(
            formula["unscaled_scalar_formula"],
            "(b_d*c_e + c_d*b_e) / (a_d*a_e*L^3)")
        self.assertEqual(
            action["name"],
            "exact log-polynomial scalar equality")
        self.assertIn("symbolic expressions in logarithms",
                      action["smallest_next_test"])


if __name__ == "__main__":
    unittest.main()
