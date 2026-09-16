import json
import unittest
from pathlib import Path


class Q286WbssK286QuarterResidualCompanionObligationTests(
        unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/"
            "q286-wbss-k286-quarter-residual-companion-obligation.json"
        ).read_text(encoding="utf-8"))

    def test_receipt_is_theorem_candidate_not_proof(self):
        receipt = self.load_receipt()

        self.assertEqual(
            receipt["status"],
            "TARGET_k286_quarter_residual_companion_theorem_candidate")
        self.assertFalse(receipt["quarter_residual_theorem_proved"])
        self.assertFalse(receipt["k286_absolute_envelope_theorem_proved"])
        self.assertFalse(receipt["companion_adverse_drag_theorem_proved"])
        self.assertFalse(receipt["same_row_tradeoff_theorem_proved"])
        self.assertFalse(receipt["universal_pointwise_raw_bound_proved"])
        self.assertFalse(receipt["q286_threshold_theorem_proved"])
        self.assertFalse(receipt["strict_central_goldbach_theorem_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_quarter_residual_counts_are_pinned(self):
        receipt = self.load_receipt()
        summary = receipt["finite_calibration"]["summary"]

        self.assertFalse(
            receipt["finite_calibration"][
                "finite_evidence_is_acceptance_condition"])
        self.assertEqual(summary["row_count"], 280)
        self.assertEqual(summary["target_minimum"], 1156012)
        self.assertEqual(summary["target_maximum"], 1235806)
        self.assertEqual(summary["quarter_residual_surviving_count"], 280)
        self.assertEqual(summary["quarter_residual_nonpositive_count"], 0)

    def test_quarter_residual_summaries_are_pinned(self):
        receipt = self.load_receipt()
        summary = receipt["finite_calibration"]["summary"]

        residual = summary["residual_after_h_ratio_summary"]
        self.assertAlmostEqual(
            residual["minimum"], 0.2745704974021227, places=15)
        self.assertAlmostEqual(
            residual["mean"], 0.692196021998406, places=15)
        self.assertAlmostEqual(
            residual["maximum"], 0.87129663381704, places=15)

        fraction = summary["companion_residual_fraction_summary"]
        self.assertAlmostEqual(fraction["minimum"], 0.0, places=15)
        self.assertAlmostEqual(
            fraction["mean"], 0.031684529803067824, places=15)
        self.assertAlmostEqual(
            fraction["maximum"], 0.24495753331096648, places=15)

        quarter_margin = summary[
            "quarter_residual_companion_margin_ratio_summary"]
        self.assertAlmostEqual(
            quarter_margin["minimum"], 0.0013845125869415692,
            places=15)
        self.assertAlmostEqual(
            quarter_margin["mean"], 0.1524564936839005, places=15)
        self.assertAlmostEqual(
            quarter_margin["maximum"], 0.21400834184099196, places=15)

    def test_tight_quarter_row_is_pinned(self):
        receipt = self.load_receipt()
        row = receipt["finite_calibration"]["summary"][
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
            row["residual_after_h_ratio"],
            0.2745704974021227,
            places=15)
        self.assertAlmostEqual(
            row["companion_residual_fraction"],
            0.24495753331096648,
            places=15)
        self.assertAlmostEqual(
            row["quarter_residual_companion_margin_ratio"],
            0.0013845125869415692,
            places=15)

    def test_theorem_obligation_and_boundary_are_pinned(self):
        receipt = self.load_receipt()
        obligation = receipt["theorem_obligation"]
        summary = receipt["finite_calibration"]["summary"]

        self.assertIn("H_286(N)<M(N)", obligation["k286_envelope_first"])
        self.assertIn("(1/4)(M(N)-H_286(N))",
                      obligation["quarter_residual_companion_bound"])
        self.assertAlmostEqual(
            summary["h286_other_ratio_pearson_correlation"],
            0.24407881205516213,
            places=15)
        self.assertIn("fragile finite candidate", receipt["decision"])
        self.assertIn("No quarter-residual theorem",
                      receipt["status_boundary"])


if __name__ == "__main__":
    unittest.main()
