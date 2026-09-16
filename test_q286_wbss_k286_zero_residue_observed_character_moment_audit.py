import json
import unittest
from pathlib import Path


class Q286WbssK286ZeroResidueObservedCharacterMomentAuditTests(
        unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/"
            "q286-wbss-k286-zero-residue-observed-character-moment-audit.json"
        ).read_text(encoding="utf-8"))

    def test_receipt_is_diagnostic_not_proof(self):
        receipt = self.load_receipt()

        self.assertEqual(
            receipt["status"],
            "DIAGNOSTIC_zero_residue_plain_character_l2_not_observed_bridge")
        self.assertFalse(
            receipt["zero_residue_raw_adverse_drag_theorem_proved"])
        self.assertFalse(receipt["aggregate_character_moment_theorem_proved"])
        self.assertFalse(receipt["signed_phase_character_theorem_proved"])
        self.assertFalse(receipt["universal_pointwise_raw_bound_proved"])
        self.assertFalse(receipt["q286_threshold_theorem_proved"])
        self.assertFalse(receipt["strict_central_goldbach_theorem_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_zero_mass_and_l2_cap_failure_counts_are_pinned(self):
        receipt = self.load_receipt()
        summary = receipt["finite_diagnostic"]["summary"]
        zero_mass = receipt["zero_mass_check"]

        self.assertEqual(summary["row_count"], 70)
        self.assertEqual(summary["target_minimum"], 1156012)
        self.assertEqual(summary["target_maximum"], 1175746)
        self.assertEqual(summary["zero_pair_count_rows"], 0)
        self.assertEqual(
            summary["nonpositive_raw_adverse_gate_gap_count"], 0)
        self.assertEqual(summary["local_l2_cap_exceeding_row_count"], 18)
        self.assertEqual(summary["global_l2_cap_exceeding_row_count"], 66)
        self.assertEqual(zero_mass["zero_pair_count_rows"], 0)
        self.assertEqual(
            zero_mass["nonpositive_raw_adverse_gate_gap_count"], 0)

    def test_observed_character_moment_summaries_are_pinned(self):
        receipt = self.load_receipt()
        summary = receipt["finite_diagnostic"]["summary"]

        aggregate = summary["aggregate_character_moment_l2_summary"]
        self.assertAlmostEqual(
            aggregate["minimum"], 0.09541894855503372, places=15)
        self.assertAlmostEqual(
            aggregate["mean"], 0.15214146088103925, places=15)
        self.assertAlmostEqual(
            aggregate["maximum"], 0.19292792994833513, places=15)

        ratio = summary["ratio_to_zero_residue_local_l2_cap_summary"]
        self.assertAlmostEqual(
            ratio["minimum"], 0.5008426004951454, places=15)
        self.assertAlmostEqual(
            ratio["mean"], 0.8570306512967532, places=15)
        self.assertAlmostEqual(
            ratio["maximum"], 1.354153874306624, places=15)

    def test_worst_l2_cap_violation_row_is_pinned(self):
        receipt = self.load_receipt()
        row = receipt["finite_diagnostic"]["summary"][
            "largest_local_l2_ratio_row"]

        self.assertEqual(row["target"], 1171456)
        self.assertEqual(row["target_residue"], 286)
        self.assertEqual(row["target_mod_286"], 0)
        self.assertAlmostEqual(
            row["aggregate_character_moment_l2"],
            0.17499545077585937,
            places=15)
        self.assertAlmostEqual(
            row["zero_residue_local_aggregate_l2_cap"],
            0.1292286305834065,
            places=15)
        self.assertAlmostEqual(
            row["ratio_to_zero_residue_local_l2_cap"],
            1.354153874306624,
            places=15)
        self.assertAlmostEqual(
            row["raw_adverse_drag_ratio"],
            0.024989313695990587,
            places=15)
        self.assertAlmostEqual(
            row["raw_adverse_gate_gap_over_target"],
            0.365687389609711,
            places=15)

    def test_decision_keeps_the_logical_bridge_open(self):
        receipt = self.load_receipt()

        self.assertIn(
            "plain aggregate active-character L2 does not explain",
            receipt["decision"])
        self.assertIn(
            "signed/phase-aware character moment estimate",
            receipt["decision"])
        self.assertIn(
            "Finite observed character-moment diagnostic only",
            receipt["status_boundary"])


if __name__ == "__main__":
    unittest.main()
