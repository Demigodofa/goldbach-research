import json
import unittest
from pathlib import Path


class Q286WbssK286AbsoluteEnvelopeTwoBudgetObligationTests(
        unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/"
            "q286-wbss-k286-absolute-envelope-two-budget-obligation.json"
        ).read_text(encoding="utf-8"))

    def test_receipt_is_theorem_obligation_not_proof(self):
        receipt = self.load_receipt()

        self.assertEqual(
            receipt["status"],
            "TARGET_k286_absolute_envelope_two_budget_theorem_required")
        self.assertFalse(receipt["k286_absolute_envelope_theorem_proved"])
        self.assertFalse(receipt["companion_adverse_drag_theorem_proved"])
        self.assertFalse(receipt["same_row_tradeoff_theorem_proved"])
        self.assertFalse(receipt["universal_pointwise_raw_bound_proved"])
        self.assertFalse(receipt["q286_threshold_theorem_proved"])
        self.assertFalse(receipt["strict_central_goldbach_theorem_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_budget_counts_are_pinned(self):
        receipt = self.load_receipt()
        summary = receipt["finite_calibration"]["summary"]

        self.assertFalse(
            receipt["finite_calibration"][
                "finite_evidence_is_acceptance_condition"])
        self.assertEqual(summary["row_count"], 280)
        self.assertEqual(summary["target_minimum"], 1156012)
        self.assertEqual(summary["target_maximum"], 1235806)
        self.assertEqual(summary["positive_two_budget_margin_count"], 280)
        self.assertEqual(summary["nonpositive_two_budget_margin_count"], 0)

    def test_budget_ratio_summaries_are_pinned(self):
        receipt = self.load_receipt()
        summary = receipt["finite_calibration"]["summary"]

        h_ratio = summary["k286_absolute_envelope_ratio_summary"]
        self.assertAlmostEqual(
            h_ratio["minimum"], 0.12870336618295997, places=15)
        self.assertAlmostEqual(
            h_ratio["mean"], 0.3078039780015939, places=15)
        self.assertAlmostEqual(
            h_ratio["maximum"], 0.7254295025978773, places=15)

        a_ratio = summary["other_moduli_adverse_ratio_summary"]
        self.assertAlmostEqual(a_ratio["minimum"], 0.0, places=15)
        self.assertAlmostEqual(
            a_ratio["mean"], 0.02059251181570102, places=15)
        self.assertAlmostEqual(
            a_ratio["maximum"], 0.09287286305792383, places=15)

        payment = summary["two_budget_payment_ratio_summary"]
        self.assertAlmostEqual(
            payment["minimum"], 0.13870558064782657, places=15)
        self.assertAlmostEqual(
            payment["mean"], 0.32839648981729497, places=15)
        self.assertAlmostEqual(
            payment["maximum"], 0.7926876143614664, places=15)

        margin = summary["two_budget_margin_ratio_summary"]
        self.assertAlmostEqual(
            margin["minimum"], 0.2073123856385336, places=15)
        self.assertAlmostEqual(
            margin["mean"], 0.671603510182705, places=15)
        self.assertAlmostEqual(
            margin["maximum"], 0.8612944193521734, places=15)

    def test_extreme_rows_are_pinned(self):
        receipt = self.load_receipt()
        summary = receipt["finite_calibration"]["summary"]

        max_h = summary["largest_k286_absolute_envelope_ratio_row"]
        self.assertEqual(max_h["target"], 1201486)
        self.assertEqual(max_h["target_residue"], 286)
        self.assertEqual(max_h["lift_index"], 4)
        self.assertAlmostEqual(
            max_h["k286_absolute_envelope_ratio"],
            0.7254295025978773,
            places=15)
        self.assertAlmostEqual(
            max_h["two_budget_payment_ratio"],
            0.7926876143614664,
            places=15)

        max_a = summary["largest_other_moduli_adverse_ratio_row"]
        self.assertEqual(max_a["target"], 1192048)
        self.assertEqual(max_a["target_residue"], 858)
        self.assertEqual(max_a["period_residue_index"], 3)
        self.assertEqual(max_a["lift_index"], 3)
        self.assertAlmostEqual(
            max_a["other_moduli_adverse_ratio"],
            0.09287286305792383,
            places=15)
        self.assertAlmostEqual(
            max_a["two_budget_payment_ratio"],
            0.4421364977305964,
            places=15)

    def test_theorem_obligation_and_warning_are_pinned(self):
        receipt = self.load_receipt()
        obligation = receipt["theorem_obligation"]
        warning = receipt["finite_ratio_warning"]

        self.assertIn("H_286(N) <= h(N) M(N)",
                      obligation["k286_absolute_envelope_bound"])
        self.assertIn("A_other(N) <= a(N) M(N)",
                      obligation["companion_adverse_drag_bound"])
        self.assertIn("h(N)+a(N)", obligation["strict_payment_condition"])
        self.assertFalse(warning["separate_maxima_do_not_pay"])
        self.assertAlmostEqual(
            warning["sum_of_separate_finite_maxima"],
            0.8183023656558012,
            places=15)
        self.assertIn("same-row sum", warning["reason"])


if __name__ == "__main__":
    unittest.main()
