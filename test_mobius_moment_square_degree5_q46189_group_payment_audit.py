import json
import unittest
from pathlib import Path


EVIDENCE = Path(
    "evidence/"
    "mobius-moment-square-degree5-q46189-group-payment-audit.json")


class MobiusMomentSquareDegree5Q46189GroupPaymentAuditTests(
        unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = json.loads(EVIDENCE.read_text(encoding="utf-8"))

    def test_receipt_preserves_boundaries(self):
        self.assertEqual(
            self.receipt["status"],
            "AUDIT_q46189_structured_group_payment")
        self.assertTrue(self.receipt["finite_group_payment_audit_only"])
        self.assertTrue(self.receipt["finite_diagnostic_only"])
        self.assertFalse(
            self.receipt["replacement_family_payment_theorem_proved"])
        self.assertFalse(self.receipt["phase_defect_payment_theorem_proved"])
        self.assertFalse(self.receipt["goldbach_proved"])

    def test_fixture_is_q46189_exception(self):
        fixture = self.receipt["fixture"]

        self.assertEqual(fixture["scale_modulus"], 229)
        self.assertEqual(fixture["prime_modulus"], 379)
        self.assertEqual(fixture["target_label"], "00,12")
        self.assertEqual(fixture["row_count_A"], 43)
        self.assertEqual(fixture["threshold_p_times_A"], 16297)
        self.assertEqual(fixture["adverse_denominator"], 46189)
        self.assertEqual(
            fixture["adverse_denominator_factorization"],
            {"11": 1, "13": 1, "17": 1, "19": 1})
        self.assertAlmostEqual(
            fixture["q46189_adverse_margin"],
            8444721229.472412)

    def test_replacement_family_pays_defect_without_total_positivity(self):
        summary = self.receipt["replacement_family_summary"]
        classification = self.receipt["classification"]

        self.assertEqual(summary["row_count"], 10)
        self.assertAlmostEqual(
            summary["positive_margin_sum"],
            14694916931621.637)
        self.assertAlmostEqual(
            summary["payment_over_q46189_adverse"],
            1740.1304948156007)
        self.assertGreater(
            summary["minimum_individual_payment_over_defect"], 36.0)
        self.assertTrue(classification["replacement_family_pays_defect"])
        self.assertTrue(
            classification["each_replacement_row_individually_pays_defect"])

    def test_each_omitted_high_prime_family_pays(self):
        families = self.receipt["omitted_high_prime_family_summaries"]
        classification = self.receipt["classification"]

        self.assertEqual(set(families), {"11", "13", "17", "19"})
        for summary in families.values():
            self.assertGreater(
                summary["payment_over_q46189_adverse"], 299.0)
            self.assertTrue(summary["all_rows_individually_pay_defect"])
        self.assertTrue(
            classification["each_omitted_high_prime_family_pays_defect"])

    def test_rows_are_three_of_four_high_prime_replacements(self):
        rows = self.receipt["replacement_family_rows"]

        self.assertEqual(len(rows), 10)
        for row in rows:
            self.assertEqual(len(row["high_prime_support"]), 3)
            self.assertEqual(len(row["missing_high_primes"]), 1)
            self.assertIn(row["clearance_family"], ("middle_2_to_3",
                                                    "far_3_plus"))
            self.assertGreater(row["margin"], 0)

    def test_next_action_is_replacement_family_theorem_target(self):
        action = self.receipt["candidate_next_action"]

        self.assertEqual(
            action["name"],
            "replacement-family phase-defect payment theorem")
        self.assertIn("omitted high prime", action["prediction"])
        self.assertIn("without total positivity",
                      action["smallest_next_test"])


if __name__ == "__main__":
    unittest.main()
