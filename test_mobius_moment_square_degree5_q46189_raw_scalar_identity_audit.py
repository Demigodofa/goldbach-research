import json
import unittest
from pathlib import Path


EVIDENCE = Path(
    "evidence/"
    "mobius-moment-square-degree5-q46189-raw-scalar-identity-audit.json")


class MobiusMomentSquareDegree5Q46189RawScalarIdentityAuditTests(
        unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = json.loads(EVIDENCE.read_text(encoding="utf-8"))

    def test_receipt_preserves_boundaries(self):
        self.assertEqual(
            self.receipt["status"],
            "AUDIT_q46189_raw_source_pair_scalar_identity")
        self.assertTrue(self.receipt["finite_raw_scalar_identity_audit_only"])
        self.assertTrue(self.receipt["finite_diagnostic_only"])
        self.assertFalse(
            self.receipt["raw_scalar_identity_theorem_proved"])
        self.assertFalse(
            self.receipt["exact_scalar_identity_theorem_proved"])
        self.assertFalse(self.receipt["goldbach_proved"])

    def test_q46189_raw_identity_holds_before_residue_grouping(self):
        q_row = self.receipt["q46189_raw_scalar_row"]
        classification = self.receipt["classification"]

        self.assertEqual(q_row["reduced_denominator"], 46189)
        self.assertEqual(q_row["ordered_source_conductor_pair_count"], 6)
        self.assertEqual(q_row["raw_frequency_pair_count"], 207360)
        self.assertEqual(q_row["raw_reduced_residue_count"], 34560)
        self.assertEqual(q_row["zero_left_raw_pair_count"], 0)
        self.assertAlmostEqual(
            q_row["raw_scalar_real"],
            -0.07475328212536138)
        self.assertEqual(q_row["raw_scalar_imag"], 0.0)
        self.assertLess(q_row["max_abs_raw_scalar_deviation"], 3e-17)
        self.assertTrue(q_row["raw_scalar_identity_holds_to_tolerance"])
        self.assertTrue(classification["q46189_raw_scalar_identity_holds"])

    def test_q46189_has_expected_six_source_conductor_pairs(self):
        q_row = self.receipt["q46189_raw_scalar_row"]
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
        for row in q_row["ordered_source_conductor_pairs"]:
            self.assertEqual(row["raw_frequency_pair_count"], 34560)

    def test_replacements_all_have_raw_scalar_identity(self):
        rows = self.receipt["replacement_raw_scalar_rows"]
        classification = self.receipt["classification"]

        self.assertEqual(len(rows), 10)
        self.assertTrue(
            classification["all_replacements_raw_scalar_identity_holds"])
        self.assertTrue(
            classification["all_rows_have_six_ordered_source_conductor_pairs"])
        self.assertTrue(
            classification["all_rows_have_no_zero_left_raw_pairs"])
        self.assertTrue(classification["all_replacements_ratio_above_half"])
        self.assertAlmostEqual(
            min(row["ratio_minus_half"] for row in rows),
            0.07635340770691146)
        self.assertLess(
            max(row["max_abs_raw_scalar_deviation"] for row in rows),
            3e-17)
        for row in rows:
            self.assertEqual(row["ordered_source_conductor_pair_count"], 6)
            self.assertTrue(row["raw_scalar_identity_holds_to_tolerance"])
            self.assertLess(row["raw_to_cellwise_scalar_abs_error"], 5e-17)

    def test_each_omitted_high_prime_family_has_raw_identity(self):
        families = self.receipt[
            "omitted_high_prime_family_raw_summaries"]

        self.assertEqual(set(families), {"11", "13", "17", "19"})
        self.assertAlmostEqual(
            families["17"]["minimum_ratio_minus_half"],
            0.07635340770691146)
        for summary in families.values():
            self.assertTrue(summary["all_rows_raw_scalar_identity"])
            self.assertEqual(
                summary["ordered_source_conductor_pair_counts"], [6])
            self.assertLess(
                summary["maximum_raw_scalar_deviation"], 3e-17)

    def test_next_action_is_symbolic_source_conductor_formula(self):
        action = self.receipt["candidate_next_action"]

        self.assertEqual(
            action["name"],
            "symbolic source-conductor scalar formula")
        self.assertIn("divisor-polynomial data", action["mechanism"])
        self.assertIn("without using floating aggregation",
                      action["smallest_next_test"])


if __name__ == "__main__":
    unittest.main()
