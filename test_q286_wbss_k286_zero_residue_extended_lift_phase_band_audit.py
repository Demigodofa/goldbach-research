import json
import unittest
from pathlib import Path


class Q286WbssK286ZeroResidueExtendedLiftPhaseBandAuditTests(
        unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/"
            "q286-wbss-k286-zero-residue-extended-lift-phase-band-audit.json"
        ).read_text(encoding="utf-8"))

    def test_receipt_is_extended_lift_diagnostic_not_proof(self):
        receipt = self.load_receipt()

        self.assertEqual(
            receipt["status"],
            "DIAGNOSTIC_k286_small_phase_band_not_stable")
        self.assertFalse(receipt["moving_band_phase_theorem_proved"])
        self.assertFalse(receipt["phase_envelope_theorem_proved"])
        self.assertFalse(
            receipt["coefficient_direction_nonalignment_theorem_proved"])
        self.assertFalse(receipt["universal_pointwise_raw_bound_proved"])
        self.assertFalse(receipt["q286_threshold_theorem_proved"])
        self.assertFalse(receipt["strict_central_goldbach_theorem_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_extended_lift_counts_are_pinned(self):
        receipt = self.load_receipt()
        summary = receipt["finite_diagnostic"]["summary"]

        self.assertEqual(summary["extended_residue_count"], 4)
        self.assertEqual(summary["lift_count_per_residue"], 8)
        self.assertEqual(summary["row_count"], 32)
        self.assertEqual(summary["future_row_count_after_first_two"], 24)
        self.assertEqual(
            summary["future_top_abs_covered_by_first_two_count"], 3)
        self.assertEqual(
            summary["future_top_adverse_covered_by_first_two_count"], 5)
        self.assertEqual(
            summary["future_top_rescue_covered_by_first_two_count"], 4)

    def test_unique_top_pair_counts_are_pinned(self):
        receipt = self.load_receipt()
        summary = receipt["finite_diagnostic"]["summary"]

        self.assertEqual(summary["max_unique_top_abs_pair_count_by_residue"], 7)
        self.assertEqual(
            summary["max_unique_top_adverse_pair_count_by_residue"], 5)
        self.assertEqual(
            summary["max_unique_top_rescue_pair_count_by_residue"], 7)

    def test_top_fraction_and_cancellation_summaries_are_pinned(self):
        receipt = self.load_receipt()
        summary = receipt["finite_diagnostic"]["summary"]

        topfrac = summary["top_abs_pair_fraction_summary"]
        self.assertAlmostEqual(
            topfrac["minimum"], 0.08608537446205455, places=15)
        self.assertAlmostEqual(
            topfrac["mean"], 0.11641633995627859, places=15)
        self.assertAlmostEqual(
            topfrac["maximum"], 0.16050600038977816, places=15)

        cancellation = summary["pair_cancellation_ratio_summary"]
        self.assertAlmostEqual(
            cancellation["minimum"], 0.00047975281865278685, places=15)
        self.assertAlmostEqual(
            cancellation["mean"], 0.1837093859655672, places=15)
        self.assertAlmostEqual(
            cancellation["maximum"], 0.5134842560389142, places=15)

    def test_residue_specific_band_failures_are_pinned(self):
        receipt = self.load_receipt()
        records = {
            row["target_residue"]: row
            for row in receipt["finite_diagnostic"]["summary"][
                "residue_summaries"]
        }

        self.assertEqual(records[286]["unique_top_abs_pair_count"], 7)
        self.assertEqual(
            records[286]["later_top_abs_covered_by_first_two_count"], 1)

        self.assertEqual(records[3718]["unique_top_abs_pair_count"], 7)
        self.assertEqual(
            records[3718]["later_top_abs_covered_by_first_two_count"], 0)

        self.assertEqual(records[4576]["unique_top_abs_pair_count"], 6)
        self.assertEqual(
            records[4576]["later_top_abs_covered_by_first_two_count"], 0)
        self.assertEqual(records[4576]["first_two_top_abs_band"],
                         ["3,7|7,5"])

        self.assertEqual(records[7722]["unique_top_abs_pair_count"], 5)
        self.assertEqual(
            records[7722]["later_top_abs_covered_by_first_two_count"], 2)

    def test_decision_names_moving_band_not_fixed_labels(self):
        receipt = self.load_receipt()

        self.assertIn("small phase-band shortcut",
                      receipt["decision"])
        self.assertIn("envelope or concentration estimate",
                      receipt["decision"])
        self.assertIn("Finite extended-lift phase-band diagnostic only",
                      receipt["status_boundary"])


if __name__ == "__main__":
    unittest.main()
