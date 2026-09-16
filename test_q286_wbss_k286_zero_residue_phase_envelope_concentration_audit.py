import json
import unittest
from pathlib import Path


class Q286WbssK286ZeroResiduePhaseEnvelopeConcentrationAuditTests(
        unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/"
            "q286-wbss-k286-zero-residue-phase-envelope-concentration-audit"
            ".json"
        ).read_text(encoding="utf-8"))

    def test_receipt_is_concentration_diagnostic_not_proof(self):
        receipt = self.load_receipt()

        self.assertEqual(
            receipt["status"],
            "DIAGNOSTIC_k286_phase_envelope_broad")
        self.assertFalse(receipt["broad_phase_envelope_theorem_proved"])
        self.assertFalse(receipt["phase_cancellation_theorem_proved"])
        self.assertFalse(
            receipt["coefficient_direction_nonalignment_theorem_proved"])
        self.assertFalse(receipt["universal_pointwise_raw_bound_proved"])
        self.assertFalse(receipt["q286_threshold_theorem_proved"])
        self.assertFalse(receipt["strict_central_goldbach_theorem_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_phase_envelope_cover_counts_are_pinned(self):
        receipt = self.load_receipt()
        summary = receipt["finite_diagnostic"]["summary"]

        self.assertEqual(summary["row_count"], 32)
        self.assertEqual(summary["target_minimum"], 1158872)
        self.assertEqual(summary["target_maximum"], 1235806)
        self.assertEqual(summary["distinct_target_residue_count"], 4)

        pair_count = summary["pair_count_summary"]
        self.assertEqual(pair_count["minimum"], 30.0)
        self.assertEqual(pair_count["mean"], 30.0)
        self.assertEqual(pair_count["maximum"], 30.0)

        cover50 = summary["threshold_count_summaries"]["0.5"]
        self.assertEqual(cover50["minimum"], 5.0)
        self.assertEqual(cover50["mean"], 6.625)
        self.assertEqual(cover50["maximum"], 9.0)

        cover75 = summary["threshold_count_summaries"]["0.75"]
        self.assertEqual(cover75["minimum"], 10.0)
        self.assertEqual(cover75["mean"], 11.9375)
        self.assertEqual(cover75["maximum"], 15.0)

        cover90 = summary["threshold_count_summaries"]["0.9"]
        self.assertEqual(cover90["minimum"], 15.0)
        self.assertEqual(cover90["mean"], 16.875)
        self.assertEqual(cover90["maximum"], 19.0)

    def test_participation_and_cancellation_summaries_are_pinned(self):
        receipt = self.load_receipt()
        summary = receipt["finite_diagnostic"]["summary"]

        topfrac = summary["top_pair_fraction_summary"]
        self.assertAlmostEqual(
            topfrac["minimum"], 0.08608537446205455, places=15)
        self.assertAlmostEqual(
            topfrac["mean"], 0.11641633995627859, places=15)
        self.assertAlmostEqual(
            topfrac["maximum"], 0.16050600038977816, places=15)

        inverse_participation = summary[
            "inverse_participation_count_summary"]
        self.assertAlmostEqual(
            inverse_participation["minimum"], 13.618587347874957,
            places=15)
        self.assertAlmostEqual(
            inverse_participation["mean"], 16.20730306629838, places=15)
        self.assertAlmostEqual(
            inverse_participation["maximum"], 20.460843742095474,
            places=15)

        entropy_effective = summary["entropy_effective_count_summary"]
        self.assertAlmostEqual(
            entropy_effective["minimum"], 16.61009219301574, places=15)
        self.assertAlmostEqual(
            entropy_effective["mean"], 19.250858986362026, places=15)
        self.assertAlmostEqual(
            entropy_effective["maximum"], 22.437253748373113, places=15)

        cancellation = summary["pair_cancellation_ratio_summary"]
        self.assertAlmostEqual(
            cancellation["minimum"], 0.00047975281865278685, places=15)
        self.assertAlmostEqual(
            cancellation["mean"], 0.1837093859655672, places=15)
        self.assertAlmostEqual(
            cancellation["maximum"], 0.5134842560389142, places=15)

    def test_extreme_rows_are_pinned(self):
        receipt = self.load_receipt()
        summary = receipt["finite_diagnostic"]["summary"]

        largest90 = summary["largest_90pct_cover_count_row"]
        self.assertEqual(largest90["target"], 1201486)
        self.assertEqual(largest90["target_residue"], 286)
        self.assertEqual(largest90["lift_index"], 4)
        self.assertEqual(largest90["cover_counts"]["0.9"], 19)
        self.assertAlmostEqual(
            largest90["top_pair_fraction"], 0.08608537446205455,
            places=15)
        self.assertAlmostEqual(
            largest90["pair_real_cancellation_ratio"],
            0.1253111100394837,
            places=15)

        smallest90 = summary["smallest_90pct_cover_count_row"]
        self.assertEqual(smallest90["target"], 1158872)
        self.assertEqual(smallest90["target_residue"], 7722)
        self.assertEqual(smallest90["lift_index"], 0)
        self.assertEqual(smallest90["cover_counts"]["0.9"], 15)
        self.assertAlmostEqual(
            smallest90["pair_real_cancellation_ratio"],
            0.5134842560389142,
            places=15)

        largest_top = summary["largest_top_pair_fraction_row"]
        self.assertEqual(largest_top["target"], 1218932)
        self.assertEqual(largest_top["target_residue"], 7722)
        self.assertEqual(largest_top["lift_index"], 6)
        self.assertAlmostEqual(
            largest_top["top_pair_fraction"], 0.16050600038977816,
            places=15)

    def test_decision_names_broad_envelope_not_sparse_labels(self):
        receipt = self.load_receipt()

        self.assertIn("sparse K_286 phase-envelope concentration",
                      receipt["finite_diagnostic"]["role"])
        self.assertIn("broad phase cancellation",
                      receipt["decision"])
        self.assertIn("Finite phase-envelope concentration diagnostic only",
                      receipt["status_boundary"])


if __name__ == "__main__":
    unittest.main()
