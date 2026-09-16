import json
import unittest
from pathlib import Path


EVIDENCE = Path(
    "evidence/"
    "mobius-moment-square-degree5-q46189-exact-log-polynomial-identity-audit.json")


class MobiusMomentSquareDegree5Q46189ExactLogIdentityAuditTests(
        unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = json.loads(EVIDENCE.read_text(encoding="utf-8"))

    def test_receipt_preserves_boundaries(self):
        self.assertEqual(
            self.receipt["status"],
            "AUDIT_q46189_exact_log_polynomial_identity")
        self.assertTrue(
            self.receipt["exact_log_polynomial_identity_proved_for_selected_family"])
        self.assertTrue(self.receipt["finite_selected_family_identity_only"])
        self.assertTrue(self.receipt["finite_diagnostic_only"])
        self.assertFalse(
            self.receipt[
                "universal_source_conductor_scalar_formula_theorem_proved"])
        self.assertFalse(
            self.receipt["one_coordinate_active_full_ratio_theorem_proved"])
        self.assertFalse(self.receipt["goldbach_proved"])

    def test_q46189_pair_formulas_are_exactly_equal(self):
        q_row = self.receipt["q46189_exact_log_identity_row"]
        classification = self.receipt["classification"]

        self.assertEqual(q_row["reduced_denominator"], 46189)
        self.assertEqual(
            q_row["common_log_numerator"],
            "-l11*l13*l17 - l11*l13*l19 - l11*l17*l19 - l13*l17*l19")
        self.assertEqual(
            q_row["common_log_numerator"],
            q_row["expected_common_log_numerator"])
        self.assertTrue(q_row["all_pair_scalar_expressions_equal"])
        self.assertTrue(q_row["common_log_numerator_equals_expected"])
        self.assertEqual(set(q_row["pair_difference_expressions"]), {"0"})
        self.assertAlmostEqual(
            q_row["exact_scalar_numeric_substitution"],
            -0.07475328212536136)
        self.assertEqual(q_row["numeric_substitution_minus_formula_scalar"], 0.0)
        self.assertTrue(
            classification["q46189_exact_log_identity_proved_for_checked_row"])

    def test_q46189_has_expected_ordered_source_pairs(self):
        q_row = self.receipt["q46189_exact_log_identity_row"]
        pairs = [
            (row["left_source_conductor"], row["right_source_conductor"])
            for row in q_row["ordered_source_conductor_pairs"]
        ]

        self.assertEqual(pairs, [
            (143, 323),
            (187, 247),
            (209, 221),
            (221, 209),
            (247, 187),
            (323, 143),
        ])

    def test_replacement_rows_have_exact_log_identity(self):
        rows = self.receipt["replacement_exact_log_identity_rows"]
        classification = self.receipt["classification"]

        self.assertEqual(len(rows), 10)
        self.assertTrue(
            classification[
                "all_replacements_exact_log_identity_proved_for_checked_rows"])
        self.assertTrue(
            classification[
                "all_numeric_substitutions_match_formula_checkpoint"])
        self.assertAlmostEqual(
            min(row["ratio_minus_half"] for row in rows),
            0.07635340770691146)
        self.assertLess(
            max(abs(row["numeric_substitution_minus_formula_scalar"])
                for row in rows),
            3e-17)
        for row in rows:
            self.assertTrue(row["all_pair_scalar_expressions_equal"])
            self.assertTrue(row["common_log_numerator_equals_expected"])
            self.assertEqual(set(row["pair_difference_expressions"]), {"0"})

    def test_formal_fixture_symbols_are_recorded(self):
        fixture = self.receipt["fixture"]

        self.assertEqual(fixture["scale_modulus"], 229)
        self.assertEqual(fixture["prime_modulus"], 379)
        self.assertEqual(fixture["adverse_denominator"], 46189)
        self.assertEqual(fixture["mobius_divisors"],
                         [5, 6, 7, 10, 11, 13, 14, 15, 17, 19])
        self.assertEqual(fixture["common_l_factor"], "L^-3")
        self.assertEqual(set(fixture["formal_prime_log_symbols"]), {
            "2", "3", "5", "7", "11", "13", "17", "19"})

    def test_next_action_is_one_coordinate_ratio_inequality(self):
        action = self.receipt["candidate_next_action"]

        self.assertEqual(
            action["name"],
            "one-coordinate active/full ratio inequality")
        self.assertIn("remove phase", action["mechanism"])
        self.assertIn("coordinate-00 active/full ratio gap",
                      action["smallest_next_test"])


if __name__ == "__main__":
    unittest.main()
