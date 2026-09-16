import json
import unittest
from pathlib import Path


EVIDENCE = Path(
    "evidence/"
    "mobius-moment-square-degree5-q46189-replacement-kernel-family-audit.json")


class MobiusMomentSquareDegree5Q46189ReplacementKernelFamilyAuditTests(
        unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = json.loads(EVIDENCE.read_text(encoding="utf-8"))
        cls.rows = cls.receipt["replacement_kernel_rows"]

    def test_receipt_preserves_boundaries(self):
        self.assertEqual(
            self.receipt["status"],
            "AUDIT_q46189_replacement_kernel_family")
        self.assertTrue(
            self.receipt["finite_replacement_kernel_family_audit_only"])
        self.assertTrue(self.receipt["finite_diagnostic_only"])
        self.assertFalse(
            self.receipt["replacement_residue_gap_bound_theorem_proved"])
        self.assertFalse(
            self.receipt["coordinate00_residue_gap_sign_theorem_proved"])
        self.assertFalse(self.receipt["goldbach_proved"])

    def test_q38038_is_the_finite_weakest_replacement(self):
        self.assertEqual(len(self.rows), 10)
        self.assertEqual(
            self.receipt["weakest_by_ratio_gap"]["reduced_denominator"],
            38038)
        self.assertEqual(
            self.receipt["weakest_by_half_margin"]["reduced_denominator"],
            38038)
        self.assertEqual(
            self.receipt[
                "weakest_by_off_diagonal_pressure"][
                    "reduced_denominator"],
            38038)
        self.assertTrue(
            self.receipt["classification"][
                "q38038_is_weakest_by_ratio_margin_and_offdiag_pressure"])

    def test_summary_values_are_pinned(self):
        summary = self.receipt["summary"]
        self.assertAlmostEqual(
            summary["minimum_ratio_minus_half"],
            0.07635340770691468,
            places=15)
        self.assertAlmostEqual(
            summary["minimum_half_margin"],
            4380137469743.5,
            delta=1.0)
        self.assertAlmostEqual(
            summary["minimum_off_diagonal_over_diagonal_half"],
            -0.8472931845861708,
            places=15)
        self.assertAlmostEqual(
            summary["maximum_active_reconstruction_abs_error"],
            0.6484375,
            places=7)
        self.assertAlmostEqual(
            summary["maximum_ledger_active_energy_abs_error"],
            1.0859375,
            places=7)
        self.assertLess(summary["maximum_relative_energy_error"], 1e-12)

    def test_all_replacements_survive_with_roundoff_distinction(self):
        summary = self.receipt["summary"]
        self.assertTrue(
            summary["all_replacements_positive_after_off_diagonal"])
        self.assertTrue(
            summary["all_kernel_identities_verified_with_roundoff"])
        self.assertFalse(
            summary["all_strict_abs_lt_1_pair_builder_flags"])

        strict_failures = [
            row for row in self.rows
            if not row[
                "finite_dirichlet_kernel_identity_verified_strict_abs_lt_1"]
        ]
        self.assertEqual(
            [row["reduced_denominator"] for row in strict_failures],
            [62985])
        self.assertTrue(all(
            row["finite_dirichlet_kernel_identity_verified_with_roundoff"]
            for row in self.rows))

    def test_family_keys_and_next_action_are_recorded(self):
        self.assertEqual(
            set(self.receipt[
                "omitted_high_prime_family_kernel_summaries"].keys()),
            {"11", "13", "17", "19"})
        self.assertTrue(all(
            family["all_rows_positive_after_off_diagonal"]
            for family in self.receipt[
                "omitted_high_prime_family_kernel_summaries"].values()))
        self.assertEqual(
            self.receipt["candidate_next_action"]["name"],
            "replacement residue-gap bound pattern")


if __name__ == "__main__":
    unittest.main()
