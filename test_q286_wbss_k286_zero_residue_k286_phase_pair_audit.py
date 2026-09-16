import json
import unittest
from pathlib import Path


class Q286WbssK286ZeroResidueK286PhasePairAuditTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/q286-wbss-k286-zero-residue-k286-phase-pair-audit.json"
        ).read_text(encoding="utf-8"))

    def test_receipt_is_phase_pair_diagnostic_not_proof(self):
        receipt = self.load_receipt()

        self.assertEqual(
            receipt["status"],
            "DIAGNOSTIC_k286_phase_pair_single_mode_falsified")
        self.assertFalse(receipt["phase_pair_theorem_proved"])
        self.assertFalse(
            receipt["target_residue_oscillation_theorem_proved"])
        self.assertFalse(
            receipt["coefficient_direction_nonalignment_theorem_proved"])
        self.assertFalse(receipt["universal_pointwise_raw_bound_proved"])
        self.assertFalse(receipt["q286_threshold_theorem_proved"])
        self.assertFalse(receipt["strict_central_goldbach_theorem_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_single_fixed_top_pair_counts_are_pinned(self):
        receipt = self.load_receipt()
        summary = receipt["finite_diagnostic"]["summary"]

        self.assertEqual(summary["violating_row_count"], 18)
        self.assertEqual(summary["k286_adverse_component_count"], 8)
        self.assertEqual(summary["k286_rescue_component_count"], 10)
        self.assertEqual(summary["top_adverse_pair_max_row_count"], 4)
        self.assertEqual(summary["top_rescue_pair_max_row_count"], 4)
        self.assertEqual(summary["top_abs_pair_max_row_count"], 3)
        self.assertFalse(summary["single_fixed_pair_dominates_top_adverse"])
        self.assertFalse(summary["single_fixed_pair_dominates_top_rescue"])
        self.assertFalse(summary["single_fixed_pair_dominates_top_abs"])

    def test_top_pair_histograms_are_pinned(self):
        receipt = self.load_receipt()
        summary = receipt["finite_diagnostic"]["summary"]

        self.assertEqual(
            summary["top_adverse_pair_counts"]["3,7|7,5"], 4)
        self.assertEqual(
            summary["top_rescue_pair_counts"]["3,5|7,7"], 4)
        self.assertEqual(
            summary["top_abs_pair_counts"]["3,5|7,7"], 3)
        self.assertEqual(
            len(summary["top_adverse_pair_counts"]), 11)
        self.assertEqual(
            len(summary["top_rescue_pair_counts"]), 10)
        self.assertEqual(
            len(summary["top_abs_pair_counts"]), 13)

    def test_pair_reconstruction_and_local_concentration_are_pinned(self):
        receipt = self.load_receipt()
        summary = receipt["finite_diagnostic"]["summary"]

        self.assertLess(
            summary["pair_reconstruction_error_summary"]["maximum"],
            5e-17)
        self.assertAlmostEqual(
            summary["pair_cancellation_ratio_summary"]["mean"],
            0.15132464895023304,
            places=15)
        self.assertAlmostEqual(
            summary["top_abs_pair_fraction_summary"]["minimum"],
            0.08285344480352641,
            places=15)
        self.assertAlmostEqual(
            summary["top_abs_pair_fraction_summary"]["mean"],
            0.11575000686804238,
            places=15)
        self.assertAlmostEqual(
            summary["top_abs_pair_fraction_summary"]["maximum"],
            0.16161053354457436,
            places=15)

    def test_extreme_rows_are_pinned(self):
        receipt = self.load_receipt()
        summary = receipt["finite_diagnostic"]["summary"]

        largest_fraction = summary["largest_top_abs_pair_fraction_row"]
        self.assertEqual(largest_fraction["target"], 1173172)
        self.assertEqual(largest_fraction["target_residue"], 2002)
        self.assertAlmostEqual(
            largest_fraction["top_abs_pair_fraction_of_envelope"],
            0.16161053354457436,
            places=15)

        smallest_cancel = summary["smallest_pair_cancellation_ratio_row"]
        self.assertEqual(smallest_cancel["target"], 1173458)
        self.assertEqual(smallest_cancel["target_residue"], 2288)
        self.assertAlmostEqual(
            smallest_cancel["pair_real_cancellation_ratio"],
            0.009089584046870686,
            places=15)

        largest_cancel = summary["largest_pair_cancellation_ratio_row"]
        self.assertEqual(largest_cancel["target"], 1158872)
        self.assertEqual(largest_cancel["target_residue"], 7722)
        self.assertAlmostEqual(
            largest_cancel["pair_real_cancellation_ratio"],
            0.5134842560389142,
            places=15)

    def test_decision_falsifies_single_mode_without_promotion(self):
        receipt = self.load_receipt()

        self.assertIn("single fixed conjugate phase-pair",
                      receipt["decision"])
        self.assertIn("target-residue-dependent oscillation",
                      receipt["decision"])
        self.assertIn("Finite K_286 conjugate phase-pair diagnostic only",
                      receipt["status_boundary"])


if __name__ == "__main__":
    unittest.main()
