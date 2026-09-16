import json
import unittest
from pathlib import Path


class Q286WbssK286ZeroResidueDirectionalSlackAuditTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/q286-wbss-k286-zero-residue-directional-slack-audit.json"
        ).read_text(encoding="utf-8"))

    def test_receipt_is_directional_diagnostic_not_proof(self):
        receipt = self.load_receipt()

        self.assertEqual(
            receipt["status"],
            "DIAGNOSTIC_zero_residue_directional_slack_observed")
        self.assertFalse(
            receipt["coefficient_direction_nonalignment_theorem_proved"])
        self.assertFalse(receipt["signed_phase_character_theorem_proved"])
        self.assertFalse(receipt["universal_pointwise_raw_bound_proved"])
        self.assertFalse(receipt["q286_threshold_theorem_proved"])
        self.assertFalse(receipt["strict_central_goldbach_theorem_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_counts_are_pinned(self):
        receipt = self.load_receipt()
        summary = receipt["finite_diagnostic"]["summary"]

        self.assertEqual(summary["row_count"], 70)
        self.assertEqual(summary["local_l2_cap_exceeding_row_count"], 18)
        self.assertEqual(summary["local_l2_cap_nonexceeding_row_count"], 52)
        self.assertEqual(summary["positive_raw_adverse_count"], 68)
        self.assertEqual(summary["zero_raw_adverse_count"], 2)
        self.assertEqual(summary["positive_raw_adverse_gate_gap_count"], 70)

    def test_directional_efficiency_summaries_are_pinned(self):
        receipt = self.load_receipt()
        summary = receipt["finite_diagnostic"]["summary"]

        efficiency = summary["directional_efficiency_summary"]
        self.assertAlmostEqual(efficiency["minimum"], 0.0, places=15)
        self.assertAlmostEqual(
            efficiency["mean"], 0.05215378602893012, places=15)
        self.assertAlmostEqual(
            efficiency["maximum"], 0.21423128828054358, places=15)

        violating = summary[
            "violating_l2_cap_directional_efficiency_summary"]
        self.assertAlmostEqual(
            violating["minimum"], 0.0007566063462656461, places=15)
        self.assertAlmostEqual(
            violating["mean"], 0.05468085899942172, places=15)
        self.assertAlmostEqual(
            violating["maximum"], 0.19440538748390473, places=15)

    def test_largest_l2_threat_row_has_low_directional_efficiency(self):
        receipt = self.load_receipt()
        row = receipt["finite_diagnostic"]["summary"][
            "largest_l2_threat_violating_row"]

        self.assertEqual(row["target"], 1171456)
        self.assertEqual(row["target_residue"], 286)
        self.assertAlmostEqual(
            row["cauchy_l2_threat_ratio_to_local_main"],
            1.354153874306624,
            places=15)
        self.assertAlmostEqual(
            row["raw_adverse_drag_ratio_to_local_main"],
            0.024989313695990587,
            places=15)
        self.assertAlmostEqual(
            row["directional_efficiency_actual_over_cauchy"],
            0.018453821364123796,
            places=15)

    def test_largest_directional_efficiency_row_is_pinned(self):
        receipt = self.load_receipt()
        row = receipt["finite_diagnostic"]["summary"][
            "largest_directional_efficiency_row"]

        self.assertEqual(row["target"], 1157728)
        self.assertEqual(row["target_residue"], 6578)
        self.assertAlmostEqual(
            row["cauchy_l2_threat_ratio_to_local_main"],
            0.8961047462279278,
            places=15)
        self.assertAlmostEqual(
            row["raw_adverse_drag_ratio_to_local_main"],
            0.19197367421871855,
            places=15)
        self.assertAlmostEqual(
            row["directional_efficiency_actual_over_cauchy"],
            0.21423128828054358,
            places=15)

    def test_decision_names_nonalignment_as_candidate_not_theorem(self):
        receipt = self.load_receipt()

        self.assertIn(
            "coefficient-direction nonalignment estimate",
            receipt["decision"])
        self.assertIn(
            "not a universal bound",
            receipt["decision"])
        self.assertIn(
            "Finite directional-slack diagnostic only",
            receipt["status_boundary"])


if __name__ == "__main__":
    unittest.main()
