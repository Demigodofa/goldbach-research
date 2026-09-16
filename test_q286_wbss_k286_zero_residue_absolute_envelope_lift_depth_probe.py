import json
import unittest
from pathlib import Path


class Q286WbssK286ZeroResidueAbsoluteEnvelopeLiftDepthProbeTests(
        unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/"
            "q286-wbss-k286-zero-residue-absolute-envelope-lift-depth-probe"
            ".json"
        ).read_text(encoding="utf-8"))

    def test_receipt_is_finite_probe_not_proof(self):
        receipt = self.load_receipt()

        self.assertEqual(
            receipt["status"],
            "PROBE_k286_zero_residue_absolute_envelope_payment_survives_"
            "lift_depth")
        self.assertFalse(receipt["k286_absolute_envelope_theorem_proved"])
        self.assertFalse(receipt["companion_adverse_drag_theorem_proved"])
        self.assertFalse(receipt["phase_cancellation_theorem_proved"])
        self.assertFalse(receipt["universal_pointwise_raw_bound_proved"])
        self.assertFalse(receipt["q286_threshold_theorem_proved"])
        self.assertFalse(receipt["strict_central_goldbach_theorem_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_lift_depth_targeting_and_counts_are_pinned(self):
        receipt = self.load_receipt()
        summary = receipt["finite_probe"]["summary"]
        targeting = receipt["targeting"]

        self.assertEqual(targeting["target_mod_286"], 0)
        self.assertEqual(targeting["period_residue_count"], 35)
        self.assertEqual(targeting["lift_count_per_period_residue"], 8)
        self.assertEqual(summary["row_count"], 280)
        self.assertEqual(summary["target_minimum"], 1156012)
        self.assertEqual(summary["target_maximum"], 1235806)
        self.assertEqual(
            summary["absolute_envelope_payment_positive_count"], 280)
        self.assertEqual(
            summary["absolute_envelope_payment_nonpositive_count"], 0)

    def test_payment_summaries_are_pinned(self):
        receipt = self.load_receipt()
        summary = receipt["finite_probe"]["summary"]

        margin = summary["absolute_envelope_margin_summary"]
        self.assertAlmostEqual(
            margin["minimum"], 0.1480214455719575, places=15)
        self.assertAlmostEqual(
            margin["mean"], 0.6780208445210824, places=15)
        self.assertAlmostEqual(
            margin["maximum"], 1.0951587951686008, places=15)

        ratio = summary["absolute_envelope_payment_ratio_summary"]
        self.assertAlmostEqual(
            ratio["minimum"], 0.1387055806478266, places=15)
        self.assertAlmostEqual(
            ratio["mean"], 0.32839648981729497, places=15)
        self.assertAlmostEqual(
            ratio["maximum"], 0.7926876143614664, places=15)

        cap = summary["k286_required_cancellation_cap_summary"]
        self.assertAlmostEqual(
            cap["minimum"], 1.2857788177846576, places=15)
        self.assertAlmostEqual(
            cap["mean"], 3.446371907120119, places=15)
        self.assertAlmostEqual(
            cap["maximum"], 7.688686822924483, places=15)

    def test_k286_envelope_and_observed_adverse_summaries_are_pinned(self):
        receipt = self.load_receipt()
        summary = receipt["finite_probe"]["summary"]

        envelope = summary["k286_absolute_phase_envelope_summary"]
        self.assertAlmostEqual(
            envelope["minimum"], 0.14007084949178422, places=15)
        self.assertAlmostEqual(
            envelope["mean"], 0.3015570812320769, places=15)
        self.assertAlmostEqual(
            envelope["maximum"], 0.5179580723281451, places=15)

        observed = summary["k286_signed_adverse_ratio_to_envelope_summary"]
        self.assertAlmostEqual(observed["minimum"], 0.0, places=15)
        self.assertAlmostEqual(
            observed["mean"], 0.11338319290255645, places=15)
        self.assertAlmostEqual(
            observed["maximum"], 0.6863544499659987, places=15)

        reconstruction = summary[
            "k286_pair_sum_reconstruction_error_summary"]
        self.assertAlmostEqual(
            reconstruction["maximum"], 5.551115123125783e-17,
            places=30)

    def test_tightest_payment_row_is_pinned(self):
        receipt = self.load_receipt()
        row = receipt["finite_probe"]["summary"][
            "tightest_absolute_envelope_payment_row"]

        self.assertEqual(row["target"], 1201486)
        self.assertEqual(row["target_residue"], 286)
        self.assertEqual(row["period_residue_index"], 1)
        self.assertEqual(row["lift_index"], 4)
        self.assertAlmostEqual(
            row["local_main"], 0.7140019401930244, places=15)
        self.assertAlmostEqual(
            row["other_moduli_adverse_drag"], 0.048022422292921904,
            places=15)
        self.assertAlmostEqual(
            row["k286_absolute_phase_envelope"], 0.5179580723281451,
            places=15)
        self.assertAlmostEqual(
            row["absolute_envelope_margin"], 0.1480214455719575,
            places=15)
        self.assertAlmostEqual(
            row["absolute_envelope_payment_ratio"],
            0.7926876143614664,
            places=15)

    def test_largest_observed_k286_adverse_row_is_pinned(self):
        receipt = self.load_receipt()
        row = receipt["finite_probe"]["summary"][
            "largest_observed_k286_signed_adverse_ratio_row"]

        self.assertEqual(row["target"], 1198626)
        self.assertEqual(row["target_residue"], 7436)
        self.assertEqual(row["period_residue_index"], 26)
        self.assertEqual(row["lift_index"], 4)
        self.assertAlmostEqual(
            row["k286_signed_adverse_ratio_to_envelope"],
            0.6863544499659987,
            places=15)
        self.assertAlmostEqual(
            row["absolute_envelope_margin"], 0.7439341864038584,
            places=15)

    def test_decision_preserves_finite_probe_boundary(self):
        receipt = self.load_receipt()

        self.assertIn("280-row finite lift-depth probe",
                      receipt["decision"])
        self.assertIn("M(N)-A_other(N)-H_286(N)",
                      receipt["finite_probe"]["definitions"][
                          "payment_margin"])
        self.assertIn("Finite zero-residue lift-depth",
                      receipt["status_boundary"])


if __name__ == "__main__":
    unittest.main()
