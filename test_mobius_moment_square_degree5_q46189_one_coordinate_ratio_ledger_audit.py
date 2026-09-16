import json
import unittest
from pathlib import Path


EVIDENCE = Path(
    "evidence/"
    "mobius-moment-square-degree5-q46189-one-coordinate-ratio-ledger-audit.json")


class MobiusMomentSquareDegree5Q46189OneCoordinateLedgerAuditTests(
        unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = json.loads(EVIDENCE.read_text(encoding="utf-8"))

    def test_receipt_preserves_boundaries(self):
        self.assertEqual(
            self.receipt["status"],
            "AUDIT_q46189_one_coordinate_ratio_ledger")
        self.assertTrue(
            self.receipt["finite_one_coordinate_ratio_ledger_audit_only"])
        self.assertTrue(self.receipt["finite_diagnostic_only"])
        self.assertFalse(
            self.receipt[
                "symbolic_coordinate_00_energy_ratio_theorem_proved"])
        self.assertFalse(
            self.receipt["one_coordinate_active_full_ratio_theorem_proved"])
        self.assertFalse(self.receipt["goldbach_proved"])

    def test_q46189_exact_phase_removed_but_ratio_below_half(self):
        row = self.receipt["q46189_one_coordinate_row"]
        classification = self.receipt["classification"]

        self.assertEqual(row["reduced_denominator"], 46189)
        self.assertTrue(row["exact_log_pair_identity_verified"])
        self.assertLess(row["cross_ratio_reduction_abs_error"], 1e-15)
        self.assertAlmostEqual(
            row["ratio_minus_half"],
            -0.0026909627652296764)
        self.assertLess(
            row["scalar_cancelled_margin_full_over_2_minus_active"], 0.0)
        self.assertTrue(classification["q46189_exact_phase_removed"])
        self.assertTrue(
            classification["q46189_one_coordinate_ratio_below_half"])

    def test_replacements_pay_after_scalar_cancellation(self):
        summary = self.receipt["replacement_summary"]
        rows = self.receipt["replacement_one_coordinate_rows"]
        classification = self.receipt["classification"]

        self.assertEqual(summary["row_count"], 10)
        self.assertTrue(summary["all_rows_above_half"])
        self.assertTrue(summary["all_rows_positive_margin"])
        self.assertAlmostEqual(
            summary["minimum_ratio_minus_half"],
            0.0763534077069109)
        self.assertAlmostEqual(
            summary["payment_over_q46189_adverse"],
            1740.1304948166812)
        self.assertGreater(
            summary["minimum_individual_payment_over_defect"],
            36.0)
        self.assertTrue(
            classification[
                "replacement_family_pays_q46189_defect_after_scalar_cancel"])
        self.assertTrue(
            classification[
                "all_replacements_one_coordinate_ratio_above_half"])
        for row in rows:
            self.assertTrue(row["exact_log_pair_identity_verified"])
            self.assertGreater(row["ratio_minus_half"], 0.0)
            self.assertGreater(
                row["scalar_cancelled_margin_full_over_2_minus_active"],
                0.0)

    def test_each_omitted_high_prime_family_pays_after_scalar_cancel(self):
        families = self.receipt[
            "omitted_high_prime_family_one_coordinate_summaries"]
        classification = self.receipt["classification"]

        self.assertEqual(set(families), {"11", "13", "17", "19"})
        for summary in families.values():
            self.assertTrue(summary["all_rows_above_half"])
            self.assertTrue(summary["all_rows_positive_margin"])
            self.assertGreater(
                summary["payment_over_q46189_adverse"], 299.0)
        self.assertTrue(
            classification[
                "each_omitted_high_prime_family_pays_after_scalar_cancel"])

    def test_margin_formula_and_next_action_are_recorded(self):
        fixture = self.receipt["fixture"]
        action = self.receipt["candidate_next_action"]

        self.assertEqual(fixture["scale_modulus"], 229)
        self.assertEqual(fixture["prime_modulus"], 379)
        self.assertEqual(fixture["target_label"], "00,12")
        self.assertEqual(fixture["adverse_denominator"], 46189)
        self.assertIn("coordinate_00_full_energy",
                      fixture["common_margin_formula"])
        self.assertEqual(
            action["name"],
            "symbolic coordinate-00 energy ratio inequality")
        self.assertIn("Dirichlet-kernel", action["mechanism"])


if __name__ == "__main__":
    unittest.main()
