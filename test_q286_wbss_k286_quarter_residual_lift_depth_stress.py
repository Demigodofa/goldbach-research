import json
import unittest
from pathlib import Path


class Q286WbssK286QuarterResidualLiftDepthStressTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/"
            "q286-wbss-k286-quarter-residual-lift-depth-stress.json"
        ).read_text(encoding="utf-8"))

    def test_receipt_is_finite_stress_not_proof(self):
        receipt = self.load_receipt()

        self.assertEqual(
            receipt["status"],
            "PROBE_k286_quarter_residual_survives_lift_depth_stress")
        self.assertFalse(receipt["quarter_residual_theorem_proved"])
        self.assertFalse(receipt["k286_absolute_envelope_theorem_proved"])
        self.assertFalse(receipt["companion_adverse_drag_theorem_proved"])
        self.assertFalse(receipt["same_row_tradeoff_theorem_proved"])
        self.assertFalse(receipt["universal_pointwise_raw_bound_proved"])
        self.assertFalse(receipt["q286_threshold_theorem_proved"])
        self.assertFalse(receipt["strict_central_goldbach_theorem_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_lift_depth_stress_counts_are_pinned(self):
        receipt = self.load_receipt()
        stress = receipt["finite_stress"]
        summary = stress["summary"]

        self.assertFalse(stress["finite_evidence_is_acceptance_condition"])
        self.assertEqual(receipt["targeting"]["lift_count_per_period_residue"],
                         16)
        self.assertEqual(summary["row_count"], 560)
        self.assertEqual(summary["target_minimum"], 1156012)
        self.assertEqual(summary["target_maximum"], 1315886)
        self.assertEqual(summary["quarter_residual_surviving_count"], 560)
        self.assertEqual(summary["quarter_residual_nonpositive_count"], 0)
        self.assertEqual(
            summary["residual_payment_route_surviving_count"], 560)
        self.assertEqual(summary["residual_payment_route_failed_count"], 0)

    def test_lift_depth_stress_summaries_are_pinned(self):
        receipt = self.load_receipt()
        summary = receipt["finite_stress"]["summary"]

        h_ratio = summary["k286_absolute_envelope_ratio_summary"]
        self.assertAlmostEqual(
            h_ratio["minimum"], 0.12870336618295997, places=15)
        self.assertAlmostEqual(
            h_ratio["mean"], 0.3101961131896782, places=15)
        self.assertAlmostEqual(
            h_ratio["maximum"], 0.7254295025978773, places=15)

        a_ratio = summary["other_moduli_adverse_ratio_summary"]
        self.assertAlmostEqual(a_ratio["minimum"], 0.0, places=15)
        self.assertAlmostEqual(
            a_ratio["mean"], 0.019030883364718643, places=15)
        self.assertAlmostEqual(
            a_ratio["maximum"], 0.10230465175850566, places=15)

        fraction = summary["companion_residual_fraction_summary"]
        self.assertAlmostEqual(fraction["minimum"], 0.0, places=15)
        self.assertAlmostEqual(
            fraction["mean"], 0.029198679142869433, places=15)
        self.assertAlmostEqual(
            fraction["maximum"], 0.24495753331096648, places=15)

        margin = summary[
            "quarter_residual_companion_margin_ratio_summary"]
        self.assertAlmostEqual(
            margin["minimum"], 0.0013845125869415692, places=15)
        self.assertAlmostEqual(
            margin["mean"], 0.1534200883378618, places=15)
        self.assertAlmostEqual(
            margin["maximum"], 0.21400834184099196, places=15)

    def test_deeper_stress_tight_row_is_pinned(self):
        receipt = self.load_receipt()
        row = receipt["finite_stress"]["summary"][
            "tightest_quarter_residual_margin_row"]

        self.assertEqual(row["target"], 1201486)
        self.assertEqual(row["target_residue"], 286)
        self.assertEqual(row["period_residue_index"], 1)
        self.assertEqual(row["lift_index"], 4)
        self.assertAlmostEqual(
            row["k286_absolute_envelope_ratio"],
            0.7254295025978773,
            places=15)
        self.assertAlmostEqual(
            row["other_moduli_adverse_ratio"],
            0.0672581117635891,
            places=15)
        self.assertAlmostEqual(
            row["companion_residual_fraction"],
            0.24495753331096648,
            places=15)
        self.assertAlmostEqual(
            row["quarter_residual_companion_margin_ratio"],
            0.0013845125869415692,
            places=15)

    def test_stress_boundary_and_falsifier_are_pinned(self):
        receipt = self.load_receipt()
        summary = receipt["finite_stress"]["summary"]

        self.assertIn("A_other(N) <= (1/4)(M(N)-H_286(N))",
                      receipt["finite_stress"]["tested_inequality"])
        self.assertAlmostEqual(
            summary["h286_other_ratio_pearson_correlation"],
            0.23923498609249583,
            places=15)
        self.assertIn("changed-condition falsifier probe",
                      receipt["finite_stress"]["role"])
        self.assertIn("No quarter-residual theorem",
                      receipt["status_boundary"])


if __name__ == "__main__":
    unittest.main()
