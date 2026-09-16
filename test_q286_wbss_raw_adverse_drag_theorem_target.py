import json
import unittest
from pathlib import Path


class Q286WbssRawAdverseDragTheoremTargetTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/q286-wbss-raw-adverse-drag-theorem-target.json"
        ).read_text(encoding="utf-8"))

    def test_receipt_preserves_theorem_boundaries(self):
        receipt = self.load_receipt()

        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["raw_adverse_drag_theorem_proved"])
        self.assertFalse(receipt["raw_witness_theorem_proved"])
        self.assertFalse(receipt["positive_mass_theorem_proved"])
        self.assertTrue(receipt["universal_bound_open"])
        self.assertFalse(
            receipt["acceptance_condition"][
                "finite_evidence_is_acceptance_condition"])

    def test_raw_inequality_is_non_circular(self):
        receipt = self.load_receipt()
        definitions = receipt["definitions"]

        self.assertIn("A_raw_-(N)<L_raw(N)",
                      definitions["sufficient_pointwise_inequality"])
        self.assertIn("T_N=0", definitions["zero_support_boundary"])
        self.assertIn("strict inequality cannot hold",
                      definitions["zero_support_boundary"])
        self.assertIn(
            "A_raw_-(N) < L_raw(N)",
            receipt["acceptance_condition"]["required_universal_statement"])

    def test_finite_calibration_survives_raw_gate(self):
        receipt = self.load_receipt()
        summary = receipt["finite_calibration"]["summary"]

        self.assertEqual(summary["row_count"], 348)
        self.assertEqual(summary["target_minimum"], 1036248)
        self.assertEqual(summary["target_maximum"], 1155862)
        self.assertEqual(summary["positive_total_weight_count"], 348)
        self.assertEqual(summary["zero_total_weight_count"], 0)
        self.assertEqual(
            summary["raw_adverse_drag_below_raw_local_main_count"], 348)
        self.assertEqual(
            summary["raw_adverse_drag_not_below_raw_local_main_count"], 0)
        self.assertEqual(summary["positive_raw_gate_gap_count"], 348)

    def test_stress_rows_are_pinned(self):
        receipt = self.load_receipt()
        summary = receipt["finite_calibration"]["summary"]

        tight = summary["tightest_raw_gate_gap_row"]
        largest_ratio = summary["largest_raw_adverse_drag_ratio_row"]
        min_main = summary["minimum_raw_local_main_row"]

        self.assertEqual(tight["target"], 1059514)
        self.assertAlmostEqual(tight["raw_adverse_gate_gap"],
                               286929.1729900494,
                               places=6)
        self.assertEqual(largest_ratio["target"], 1124642)
        self.assertAlmostEqual(largest_ratio["raw_adverse_drag_ratio"],
                               0.23148438379145228,
                               places=12)
        self.assertEqual(min_main["target"], 1038176)
        self.assertAlmostEqual(min_main["raw_local_main"],
                               323194.9984858959,
                               places=6)


if __name__ == "__main__":
    unittest.main()
