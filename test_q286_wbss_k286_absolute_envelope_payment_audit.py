import json
import unittest
from pathlib import Path


class Q286WbssK286AbsoluteEnvelopePaymentAuditTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/q286-wbss-k286-absolute-envelope-payment-audit.json"
        ).read_text(encoding="utf-8"))

    def test_receipt_is_finite_diagnostic_not_proof(self):
        receipt = self.load_receipt()

        self.assertEqual(
            receipt["status"],
            "DIAGNOSTIC_k286_absolute_envelope_payment_survives")
        self.assertFalse(receipt["k286_absolute_envelope_theorem_proved"])
        self.assertFalse(receipt["companion_adverse_drag_theorem_proved"])
        self.assertFalse(receipt["phase_cancellation_theorem_proved"])
        self.assertFalse(receipt["universal_pointwise_raw_bound_proved"])
        self.assertFalse(receipt["q286_threshold_theorem_proved"])
        self.assertFalse(receipt["strict_central_goldbach_theorem_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_absolute_envelope_payment_counts_are_pinned(self):
        receipt = self.load_receipt()
        summary = receipt["finite_diagnostic"]["summary"]

        self.assertEqual(summary["row_count"], 32)
        self.assertEqual(summary["target_minimum"], 1158872)
        self.assertEqual(summary["target_maximum"], 1235806)
        self.assertEqual(
            summary["absolute_envelope_payment_positive_count"], 32)
        self.assertEqual(
            summary["absolute_envelope_payment_nonpositive_count"], 0)

    def test_payment_summaries_are_pinned(self):
        receipt = self.load_receipt()
        summary = receipt["finite_diagnostic"]["summary"]

        margin = summary["absolute_envelope_margin_summary"]
        self.assertAlmostEqual(
            margin["minimum"], 0.1480214455719575, places=15)
        self.assertAlmostEqual(
            margin["mean"], 0.49468209609724717, places=15)
        self.assertAlmostEqual(
            margin["maximum"], 0.6694413649537231, places=15)

        ratio = summary["absolute_envelope_payment_ratio_summary"]
        self.assertAlmostEqual(
            ratio["minimum"], 0.23855937004298816, places=15)
        self.assertAlmostEqual(
            ratio["mean"], 0.41306853497816054, places=15)
        self.assertAlmostEqual(
            ratio["maximum"], 0.7926876143614664, places=15)

        cap = summary["k286_required_cancellation_cap_summary"]
        self.assertAlmostEqual(
            cap["minimum"], 1.2857788177846576, places=15)
        self.assertAlmostEqual(
            cap["mean"], 2.636017528088691, places=15)
        self.assertAlmostEqual(
            cap["maximum"], 4.336313717289516, places=15)

    def test_k286_envelope_and_observed_adverse_summaries_are_pinned(self):
        receipt = self.load_receipt()
        summary = receipt["finite_diagnostic"]["summary"]

        envelope = summary["k286_absolute_phase_envelope_summary"]
        self.assertAlmostEqual(
            envelope["minimum"], 0.20065300258921384, places=15)
        self.assertAlmostEqual(
            envelope["mean"], 0.32482274937825234, places=15)
        self.assertAlmostEqual(
            envelope["maximum"], 0.5179580723281451, places=15)

        observed = summary["k286_signed_adverse_ratio_to_envelope_summary"]
        self.assertAlmostEqual(observed["minimum"], 0.0, places=15)
        self.assertAlmostEqual(
            observed["mean"], 0.13387156082256535, places=15)
        self.assertAlmostEqual(
            observed["maximum"], 0.5134842560389142, places=15)

        reconstruction = summary[
            "k286_pair_sum_reconstruction_error_summary"]
        self.assertAlmostEqual(
            reconstruction["maximum"], 5.551115123125783e-17,
            places=30)

    def test_tight_row_is_pinned(self):
        receipt = self.load_receipt()
        row = receipt["finite_diagnostic"]["summary"][
            "tightest_absolute_envelope_payment_row"]

        self.assertEqual(row["target"], 1201486)
        self.assertEqual(row["target_residue"], 286)
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

    def test_decision_demotes_delicate_phase_cancellation(self):
        receipt = self.load_receipt()

        self.assertIn("absolute-envelope-plus-companion-bounds",
                      receipt["decision"])
        self.assertIn("M(N)-A_other(N)-H_286(N)",
                      receipt["finite_diagnostic"]["definitions"][
                          "payment_margin"])
        self.assertIn("Finite absolute-envelope payment diagnostic only",
                      receipt["status_boundary"])


if __name__ == "__main__":
    unittest.main()
