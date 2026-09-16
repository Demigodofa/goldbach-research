import json
import math
import unittest
from pathlib import Path


EVIDENCE = Path(
    "evidence/"
    "mobius-moment-square-degree5-q46189-phase-defect-audit.json")


class MobiusMomentSquareDegree5Q46189PhaseDefectAuditTests(
        unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = json.loads(EVIDENCE.read_text(encoding="utf-8"))

    def test_receipt_preserves_boundaries(self):
        self.assertEqual(
            self.receipt["status"],
            "FALSIFIER_q46189_per_denominator_nonadversity")
        self.assertTrue(self.receipt["finite_phase_defect_audit_only"])
        self.assertTrue(self.receipt["finite_diagnostic_only"])
        self.assertFalse(
            self.receipt["per_denominator_nonadversity_theorem_proved"])
        self.assertFalse(self.receipt["phase_defect_payment_theorem_proved"])
        self.assertFalse(self.receipt["goldbach_proved"])

    def test_target_coordinate_proportionality_is_pinned(self):
        target = self.receipt["target_pair_summary"]

        self.assertEqual(target["label"], "00,12")
        self.assertAlmostEqual(
            target["best_scalar_right_over_left_real"],
            -0.07475328212536138)
        self.assertAlmostEqual(
            target["best_scalar_right_over_left_imag"],
            0.0,
            places=17)
        self.assertLess(target["relative_scalar_residual"], 3e-16)
        self.assertAlmostEqual(target["best_scalar_phase"], math.pi)

    def test_target_energy_ratio_falsifies_per_denominator_nonadversity(self):
        target = self.receipt["target_pair_summary"]
        classification = self.receipt["classification"]

        self.assertAlmostEqual(
            target["active_over_full_cross_ratio"],
            0.49730903723477027)
        self.assertAlmostEqual(
            target["half_threshold_defect"],
            0.002690962765229732)
        self.assertFalse(target["per_denominator_nonadversity"])
        self.assertTrue(
            classification["per_denominator_nonadversity_falsified"])
        self.assertTrue(classification["group_payment_required"])

    def test_pair_summaries_record_all_three_adverse_components(self):
        rows = {
            row["label"]: row
            for row in self.receipt["pair_summaries"]
        }

        self.assertEqual(set(rows), {"00,12", "01,02", "01,11"})
        for row in rows.values():
            self.assertFalse(row["per_denominator_nonadversity"])
            self.assertGreater(row["half_threshold_defect"], 0)
        self.assertLess(rows["01,02"]["relative_scalar_residual"], 0.006)
        self.assertLess(rows["01,11"]["relative_scalar_residual"], 0.003)

    def test_next_action_is_group_payment(self):
        action = self.receipt["candidate_next_action"]

        self.assertEqual(action["name"], "q46189 group-payment phase defect")
        self.assertIn("missing small prime", action["prediction"])
        self.assertIn("without using total positivity",
                      action["smallest_next_test"])


if __name__ == "__main__":
    unittest.main()
