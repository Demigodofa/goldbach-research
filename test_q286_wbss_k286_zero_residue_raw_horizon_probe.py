import json
import unittest
from pathlib import Path


class Q286WbssK286ZeroResidueRawHorizonProbeTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/q286-wbss-k286-zero-residue-raw-horizon-probe.json"
        ).read_text(encoding="utf-8"))

    def test_receipt_is_probe_not_proof(self):
        receipt = self.load_receipt()

        self.assertEqual(
            receipt["status"],
            "PROBE_zero_residue_raw_horizon_survives_finite_check_not_proof")
        self.assertFalse(
            receipt["zero_residue_raw_adverse_drag_theorem_proved"])
        self.assertFalse(receipt["universal_pointwise_raw_bound_proved"])
        self.assertFalse(receipt["binary_prime_moment_theorem_proved"])
        self.assertFalse(receipt["q286_threshold_theorem_proved"])
        self.assertFalse(receipt["strict_central_goldbach_theorem_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_probe_targets_all_period_residues_above_zero_mod_286(self):
        receipt = self.load_receipt()
        targeting = receipt["targeting"]
        summary = receipt["finite_probe"]["summary"]

        self.assertEqual(targeting["target_mod_286"], 0)
        self.assertEqual(targeting["period"], 10010)
        self.assertEqual(targeting["period_residue_count"], 35)
        self.assertEqual(targeting["lift_count_per_period_residue"], 2)
        self.assertEqual(len(targeting["period_residues_checked"]), 35)
        self.assertEqual(targeting["period_residues_checked"][0], 0)
        self.assertEqual(targeting["period_residues_checked"][-1], 9724)
        self.assertEqual(summary["row_count"], 70)
        self.assertEqual(summary["period_residue_count"], 35)
        self.assertEqual(summary["lift_count_per_period_residue"], 2)

    def test_zero_residue_probe_survives_finite_check(self):
        receipt = self.load_receipt()
        summary = receipt["finite_probe"]["summary"]

        self.assertEqual(summary["zero_pair_count_rows"], 0)
        self.assertEqual(summary["zero_total_weight_rows"], 0)
        self.assertEqual(summary["positive_raw_witness_count"], 70)
        self.assertEqual(summary["positive_raw_adverse_gate_gap_count"], 70)
        self.assertEqual(
            summary["raw_adverse_drag_below_raw_local_main_count"], 70)
        self.assertEqual(
            summary["raw_adverse_drag_not_below_raw_local_main_count"], 0)
        self.assertAlmostEqual(
            summary["raw_adverse_drag_ratio_summary"]["maximum"],
            0.22064948972651888,
            places=12)
        self.assertAlmostEqual(
            summary["raw_adverse_gate_gap_summary"]["minimum"],
            423543.19091507455,
            places=8)

    def test_tight_rows_and_prior_comparison_are_pinned(self):
        receipt = self.load_receipt()
        summary = receipt["finite_probe"]["summary"]
        compare = receipt["comparison_to_prior_raw_calibration"]

        self.assertEqual(
            summary["tightest_raw_gate_gap_row"]["target"], 1161446)
        self.assertEqual(
            summary["tightest_raw_gate_gap_row"]["target_residue"], 286)
        self.assertAlmostEqual(
            summary["tightest_raw_gate_gap_row"][
                "raw_adverse_gate_gap_over_target"],
            0.3646688618455568,
            places=12)
        self.assertEqual(
            summary["largest_raw_adverse_drag_ratio_row"]["target"], 1158872)
        self.assertEqual(
            summary["largest_raw_adverse_drag_ratio_row"][
                "target_residue"], 7722)
        self.assertAlmostEqual(
            compare["prior_largest_raw_adverse_drag_ratio"],
            0.23148438379145228,
            places=12)
        self.assertAlmostEqual(
            compare["probe_largest_raw_adverse_drag_ratio"],
            0.22064948972651888,
            places=12)
        self.assertIn("finite probe survives", receipt["decision"])
        self.assertIn("universal pointwise raw estimate",
                      receipt["status_boundary"])


if __name__ == "__main__":
    unittest.main()
