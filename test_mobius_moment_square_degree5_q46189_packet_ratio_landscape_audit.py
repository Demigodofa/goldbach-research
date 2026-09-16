import json
import unittest
from pathlib import Path


EVIDENCE = Path(
    "evidence/"
    "mobius-moment-square-degree5-q46189-packet-ratio-landscape-audit.json")


class MobiusMomentSquareDegree5Q46189PacketRatioLandscapeTests(
        unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = json.loads(EVIDENCE.read_text(encoding="utf-8"))

    def test_receipt_preserves_boundaries(self):
        self.assertEqual(
            self.receipt["status"],
            "AUDIT_q46189_packet_ratio_landscape")
        self.assertTrue(
            self.receipt["finite_packet_ratio_landscape_audit_only"])
        self.assertTrue(self.receipt["finite_diagnostic_only"])
        self.assertFalse(
            self.receipt["one_coordinate_active_full_ratio_theorem_proved"])
        self.assertFalse(
            self.receipt["packet_landscape_ratio_theorem_proved"])
        self.assertFalse(self.receipt["goldbach_proved"])

    def test_q46189_is_unique_below_half_in_checked_landscape(self):
        summary = self.receipt["landscape_summary"]
        classification = self.receipt["classification"]
        self.assertEqual(summary["same_source_denominator_count"], 35)
        self.assertEqual(summary["nonadverse_denominator_count"], 34)
        self.assertEqual(summary["six_pair_packet_count"], 33)
        self.assertEqual(summary["raw_scalar_identity_count"], 33)
        self.assertEqual(summary["nonadverse_ratio_above_half_count"], 34)
        self.assertEqual(
            summary["nonadverse_ratio_below_or_equal_half_count"], 0)
        self.assertTrue(
            classification["q46189_unique_below_half_in_checked_landscape"])
        self.assertTrue(
            classification[
                "one_coordinate_ratio_landscape_survives_finite_check"])

    def test_tight_rows_are_stable(self):
        summary = self.receipt["landscape_summary"]
        qrow = self.receipt["q46189_row"]
        weakest = self.receipt["weakest_nonadverse_ratio_row"]
        self.assertEqual(qrow["reduced_denominator"], 46189)
        self.assertAlmostEqual(
            qrow["ratio_minus_half"],
            -0.0026909627652297874,
            places=15,
        )
        self.assertEqual(weakest["reduced_denominator"], 38038)
        self.assertAlmostEqual(
            weakest["ratio_minus_half"],
            0.0763534077069109,
            places=15,
        )
        self.assertEqual(
            summary["minimum_nonadverse_ratio_denominator"], 38038)

    def test_q16302_demotes_distance_selector_but_not_ratio_target(self):
        row = next(
            row for row in self.receipt["rows"]
            if row["reduced_denominator"] == 16302)
        self.assertGreater(row["ratio_minus_half"], 0)
        self.assertLess(
            row["frozen_50A_to_60A_positive_fraction_gap_vs_q46189"],
            0,
        )
        self.assertGreater(
            row["frozen_50A_to_60A_total_gap_vs_q46189"],
            0,
        )
        self.assertTrue(
            self.receipt["classification"][
                "q16302_distance_selector_failure_but_ratio_positive"])
        self.assertEqual(
            self.receipt["landscape_summary"][
                "frozen_50A_to_60A_positive_fraction_failures"],
            [16302],
        )


if __name__ == "__main__":
    unittest.main()
