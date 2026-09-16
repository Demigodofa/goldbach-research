import json
import unittest
from pathlib import Path

import numpy as np

from lcm_sawtooth_lifted_endpoint_frame import (
    lifted_endpoint_residue_gram_receipt,
)
from tools.build_mobius_moment_square_degree5_checked_scale_dominance_audit import (
    scale_parameters,
)
from tools.build_mobius_moment_square_degree5_checked_scale_phase_curve_sweep import (
    SCALES,
    active_row_start_sweep,
)


EVIDENCE = Path(
    "evidence/mobius-moment-square-degree5-checked-scale-phase-curve-sweep.json")


class MobiusMomentSquareDegree5CheckedScalePhaseCurveSweepTests(
        unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = json.loads(EVIDENCE.read_text(encoding="utf-8"))

    def test_sweeps_match_checked_scale_row_counts(self):
        self.assertEqual(list(SCALES), [127, 149, 167, 191, 211, 227])
        self.assertEqual(active_row_start_sweep(127), list(range(57)))
        self.assertEqual(active_row_start_sweep(227), list(range(87)))
        self.assertEqual(self.receipt["scale_count"], 6)
        self.assertEqual(self.receipt["prime_count_total"], 189)

    def test_receipt_preserves_boundaries(self):
        self.assertEqual(
            self.receipt["status"],
            "SWEEP_degree5_checked_scale_active_window_phase_curve")
        self.assertTrue(
            self.receipt["finite_checked_scale_phase_curve_sweep_only"])
        self.assertTrue(self.receipt["finite_diagnostic_only"])
        self.assertTrue(self.receipt["finite_falsifier_found"])
        self.assertTrue(
            self.receipt["broad_checked_scale_phase_curve_extension_falsified"])
        self.assertFalse(self.receipt["goldbach_proved"])
        self.assertFalse(self.receipt["phase_curve_theorem_proved"])
        self.assertFalse(
            self.receipt["robust_margin_universal_theorem_proved"])

    def test_broad_sweep_records_one_falsifying_row(self):
        self.assertEqual(self.receipt["component_row_count"], 42507)
        self.assertEqual(self.receipt["degree5_total_row_count"], 14169)
        self.assertEqual(self.receipt["dominance_row_count"], 56676)
        self.assertEqual(self.receipt["failure_row_count"], 1)
        self.assertFalse(
            self.receipt["all_rows_dominate_one_half_signed_full"])
        self.assertEqual(
            self.receipt["all_dominance_slack_sign_counts"],
            {"positive": 56675, "zero": 0, "negative": 1})
        self.assertEqual(
            self.receipt["failure_rows"],
            [self.receipt["weakest_dominance_row"]])

    def test_each_scale_summary_passes(self):
        expected_counts = {
            127: (24, 57, 5472),
            149: (28, 65, 7280),
            167: (29, 71, 8236),
            191: (33, 77, 10164),
            211: (36, 83, 11952),
            227: (39, 87, 13572),
        }
        self.assertEqual(len(self.receipt["scale_summaries"]), 6)
        for summary in self.receipt["scale_summaries"]:
            prime_count, start_count, row_count = expected_counts[
                summary["scale_modulus"]]
            self.assertEqual(summary["prime_count"], prime_count)
            self.assertEqual(summary["active_row_start_count"], start_count)
            self.assertEqual(summary["dominance_row_count"], row_count)
            if summary["scale_modulus"] == 149:
                self.assertFalse(
                    summary["all_rows_dominate_one_half_signed_full"])
                self.assertEqual(summary["failure_row_count"], 1)
                self.assertEqual(
                    summary["dominance_slack_sign_counts"],
                    {"positive": row_count - 1, "zero": 0, "negative": 1})
            else:
                self.assertTrue(
                    summary["all_rows_dominate_one_half_signed_full"])
                self.assertEqual(summary["failure_row_count"], 0)
                self.assertEqual(
                    summary["dominance_slack_sign_counts"],
                    {"positive": row_count, "zero": 0, "negative": 0})

    def test_weakest_checked_scale_phase_curve_row_is_recorded(self):
        weakest = self.receipt["weakest_dominance_row"]
        self.assertEqual(weakest["scale_modulus"], 149)
        self.assertEqual(weakest["prime_modulus"], 163)
        self.assertEqual(weakest["label"], "00,12")
        self.assertEqual(weakest["active_row_start"], 1)
        self.assertAlmostEqual(
            weakest["active_over_full_ratio"],
            0.4980466670754268)
        self.assertAlmostEqual(
            self.receipt["minimum_dominance_slack_above_one_half"],
            -0.0019533329245732256)

    def test_failure_row_matches_direct_lifted_receipt(self):
        parameters = scale_parameters(149)
        receipt = lifted_endpoint_residue_gram_receipt(
            163,
            parameters["row_count"],
            parameters["ell_freeze"],
            *parameters["divisor_range"],
            active_row_start=1)
        active = np.asarray(receipt["active_window_residue_energy_gram"])
        active = (active + active.T) / 2
        full = np.asarray(receipt["full_residue_energy_gram"])
        full = (full + full.T) / 2
        active_contribution = float(2 * active[0, 4])
        full_contribution = float(2 * full[0, 4])
        ratio = active_contribution / full_contribution
        self.assertAlmostEqual(ratio, 0.4980466670754268)
        self.assertLess(ratio, 0.5)


if __name__ == "__main__":
    unittest.main()
