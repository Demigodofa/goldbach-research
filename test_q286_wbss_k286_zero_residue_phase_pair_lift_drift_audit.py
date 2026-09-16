import json
import unittest
from pathlib import Path


class Q286WbssK286ZeroResiduePhasePairLiftDriftAuditTests(
        unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/"
            "q286-wbss-k286-zero-residue-phase-pair-lift-drift-audit.json"
        ).read_text(encoding="utf-8"))

    def test_receipt_is_lift_drift_diagnostic_not_proof(self):
        receipt = self.load_receipt()

        self.assertEqual(
            receipt["status"],
            "DIAGNOSTIC_k286_phase_pair_residue_only_rule_falsified")
        self.assertFalse(receipt["lift_dependent_phase_theorem_proved"])
        self.assertFalse(receipt["phase_band_theorem_proved"])
        self.assertFalse(
            receipt["coefficient_direction_nonalignment_theorem_proved"])
        self.assertFalse(receipt["universal_pointwise_raw_bound_proved"])
        self.assertFalse(receipt["q286_threshold_theorem_proved"])
        self.assertFalse(receipt["strict_central_goldbach_theorem_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_repeated_residue_counts_are_pinned(self):
        receipt = self.load_receipt()
        summary = receipt["finite_diagnostic"]["summary"]

        self.assertEqual(summary["violating_row_count"], 18)
        self.assertEqual(summary["distinct_target_residue_count"], 14)
        self.assertEqual(summary["repeated_target_residue_count"], 4)
        self.assertEqual(summary["singleton_target_residue_count"], 10)
        self.assertEqual(summary["repeated_target_residue_rows"], 8)
        self.assertEqual(
            summary["stable_top_adverse_pair_repeated_residue_count"], 1)
        self.assertEqual(
            summary["stable_top_rescue_pair_repeated_residue_count"], 0)
        self.assertEqual(
            summary["stable_top_abs_pair_repeated_residue_count"], 1)
        self.assertEqual(
            summary["stable_k286_component_sign_repeated_residue_count"], 2)

    def test_residue_only_rules_are_falsified_on_repeated_lifts(self):
        receipt = self.load_receipt()
        summary = receipt["finite_diagnostic"]["summary"]

        self.assertFalse(
            summary["target_residue_alone_explains_top_adverse_pairs"])
        self.assertFalse(
            summary["target_residue_alone_explains_top_rescue_pairs"])
        self.assertFalse(
            summary["target_residue_alone_explains_top_abs_pairs"])
        self.assertFalse(
            summary["target_residue_alone_explains_k286_component_sign"])

    def test_stable_and_unstable_residues_are_pinned(self):
        receipt = self.load_receipt()
        records = {
            row["target_residue"]: row
            for row in receipt["finite_diagnostic"]["summary"][
                "repeated_residue_records"]
        }

        self.assertEqual(set(records), {286, 3718, 4576, 7722})

        self.assertTrue(records[286]["stable_k286_component_sign"])
        self.assertFalse(records[286]["stable_top_adverse_pair"])
        self.assertFalse(records[286]["stable_top_abs_pair"])

        self.assertTrue(records[3718]["stable_k286_component_sign"])
        self.assertFalse(records[3718]["stable_top_rescue_pair"])

        self.assertFalse(records[4576]["stable_k286_component_sign"])
        self.assertTrue(records[4576]["stable_top_adverse_pair"])
        self.assertTrue(records[4576]["stable_top_abs_pair"])
        self.assertEqual(records[4576]["top_adverse_pairs"], ["3,7|7,5"])

        self.assertFalse(records[7722]["stable_k286_component_sign"])
        self.assertFalse(records[7722]["stable_top_adverse_pair"])
        self.assertFalse(records[7722]["stable_top_abs_pair"])

    def test_singleton_residues_are_pinned(self):
        receipt = self.load_receipt()
        summary = receipt["finite_diagnostic"]["summary"]

        self.assertEqual(
            summary["singleton_target_residues"],
            [2002, 2288, 3146, 5148, 5434,
             6292, 6864, 7436, 8866, 9724])

    def test_decision_names_lift_sensitive_next_target(self):
        receipt = self.load_receipt()

        self.assertIn("Target residue alone does not determine",
                      receipt["decision"])
        self.assertIn("lift-sensitive phase-band estimate",
                      receipt["decision"])
        self.assertIn("Finite repeated-lift phase-pair diagnostic only",
                      receipt["status_boundary"])


if __name__ == "__main__":
    unittest.main()
