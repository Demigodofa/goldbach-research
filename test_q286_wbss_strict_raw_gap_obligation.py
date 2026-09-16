import json
import unittest
from pathlib import Path


class Q286WbssStrictRawGapObligationTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/q286-wbss-strict-raw-gap-obligation.json"
        ).read_text(encoding="utf-8"))

    def test_receipt_preserves_boundaries(self):
        receipt = self.load_receipt()

        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["strict_raw_gap_theorem_proved"])
        self.assertFalse(receipt["raw_adverse_drag_theorem_proved"])
        self.assertFalse(receipt["positive_mass_theorem_proved"])
        self.assertTrue(receipt["universal_bound_open"])
        self.assertIn("finite rows calibrate",
                      receipt["status_boundary"])

    def test_homogeneous_ratio_boundary_is_explicit(self):
        receipt = self.load_receipt()
        definitions = receipt["definitions"]

        self.assertIn("zero-support row",
                      definitions["homogeneous_ratio_boundary"])
        self.assertIn("L_raw(N)=A_raw_-(N)=0",
                      definitions["homogeneous_ratio_boundary"])
        self.assertIn("G_raw(N)>0",
                      definitions["sufficient_strict_gap_theorem"])
        self.assertIn("positive eta",
                      receipt["candidate"]["smallest_next_theorem_target"])

    def test_finite_gap_calibration_is_positive(self):
        receipt = self.load_receipt()
        summary = receipt["finite_calibration"]["summary"]

        self.assertEqual(summary["row_count"], 348)
        self.assertEqual(summary["target_minimum"], 1036248)
        self.assertEqual(summary["target_maximum"], 1155862)
        self.assertEqual(summary["positive_strict_raw_gap_count"], 348)
        self.assertEqual(summary["nonpositive_strict_raw_gap_count"], 0)

    def test_stress_scales_are_pinned(self):
        receipt = self.load_receipt()
        summary = receipt["finite_calibration"]["summary"]

        tight = summary["tightest_strict_raw_gap_row"]
        over_n = summary["smallest_gap_over_target_row"]
        over_weight = summary["smallest_gap_over_total_weight_row"]

        self.assertEqual(tight["target"], 1059514)
        self.assertAlmostEqual(tight["strict_raw_gap"],
                               286929.1729900494,
                               places=6)
        self.assertEqual(over_n["target"], 1141274)
        self.assertAlmostEqual(over_n["strict_raw_gap_over_target"],
                               0.26310340793692394,
                               places=12)
        self.assertEqual(over_weight["target"], 1141274)
        self.assertAlmostEqual(over_weight[
            "strict_raw_gap_over_total_weight"],
            0.5992601478393073,
            places=12)


if __name__ == "__main__":
    unittest.main()
