import json
import unittest
from pathlib import Path

from tools.build_mobius_moment_square_degree5_source_admissible_window_audit import (
    contiguous_intervals,
    interval_containing,
)


EVIDENCE = Path(
    "evidence/mobius-moment-square-degree5-source-admissible-window-audit.json")


class MobiusMomentSquareDegree5SourceAdmissibleWindowAuditTests(
        unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = json.loads(EVIDENCE.read_text(encoding="utf-8"))

    def test_contiguous_interval_helpers(self):
        self.assertEqual(
            contiguous_intervals([0, 1, 3, 4, 7]),
            [
                {"start": 0, "stop": 1},
                {"start": 3, "stop": 4},
                {"start": 7, "stop": 7},
            ])
        intervals = contiguous_intervals([2, 3, 4])
        self.assertEqual(interval_containing(intervals, 3), {
            "start": 2,
            "stop": 4,
        })
        self.assertIsNone(interval_containing(intervals, 1))

    def test_receipt_preserves_boundaries(self):
        self.assertEqual(
            self.receipt["status"],
            "DERIVE_degree5_source_admissible_window_audit")
        self.assertTrue(
            self.receipt[
                "finite_source_admissible_window_diagnostic_only"])
        self.assertTrue(self.receipt["finite_diagnostic_only"])
        self.assertFalse(self.receipt["goldbach_proved"])
        self.assertFalse(
            self.receipt["source_admissible_window_theorem_proved"])
        self.assertFalse(
            self.receipt[
                "pointwise_universal_adverse_drag_estimate_proved"])

    def test_broad_failure_is_reinterpreted_as_translated_start_failure(self):
        self.assertEqual(self.receipt["scale_count"], 6)
        self.assertEqual(self.receipt["total_active_row_starts"], 440)
        self.assertEqual(self.receipt["failing_active_row_start_count"], 1)
        self.assertEqual(self.receipt["passing_active_row_start_count"], 439)
        self.assertEqual(self.receipt["failing_scale_count"], 1)
        self.assertEqual(self.receipt["broad_failure_row_count"], 1)
        failure = self.receipt["broad_failure_rows"][0]
        self.assertEqual(failure["scale_modulus"], 149)
        self.assertEqual(failure["prime_modulus"], 163)
        self.assertEqual(failure["active_row_start"], 1)
        self.assertEqual(failure["label"], "00,12")

    def test_all_canonical_source_starts_remain_inside_passing_intervals(self):
        self.assertTrue(self.receipt["all_source_starts_pass"])
        self.assertEqual(self.receipt["source_start_failure_count"], 0)
        for summary in self.receipt["scale_summaries"]:
            self.assertTrue(summary["source_start_passes"])
            interval = summary["source_connected_passing_interval"]
            self.assertLessEqual(
                interval["start"], summary["source_active_row_start"])
            self.assertGreaterEqual(
                interval["stop"], summary["source_active_row_start"])
            self.assertGreater(
                summary["source_start_minimum_canonical_slack"], 0.0)

    def test_m149_has_single_non_source_excluded_start(self):
        summary = [
            row for row in self.receipt["scale_summaries"]
            if row["scale_modulus"] == 149
        ][0]
        self.assertEqual(summary["row_count"], 32)
        self.assertEqual(summary["source_active_row_start"], 32)
        self.assertEqual(summary["failing_active_row_starts"], [1])
        self.assertEqual(
            summary["passing_active_row_start_intervals"],
            [{"start": 0, "stop": 0}, {"start": 2, "stop": 64}])
        self.assertEqual(
            summary["source_connected_passing_interval"],
            {"start": 2, "stop": 64})
        self.assertEqual(summary["source_connected_start_count"], 63)
        self.assertEqual(summary["source_start_distance_from_nearest_failure"], 31)
        self.assertAlmostEqual(
            summary["source_start_minimum_canonical_slack"],
            0.1905059738826077)

    def test_weakest_source_start_is_original_checked_scale_weak_row(self):
        self.assertAlmostEqual(
            self.receipt["minimum_source_start_canonical_slack"],
            0.056367749089376695)
        weakest = self.receipt["weakest_source_start_scale"]
        self.assertEqual(weakest["scale_modulus"], 167)
        row = weakest["source_start_weakest_canonical_row"]
        self.assertEqual(row["prime_modulus"], 181)
        self.assertEqual(row["label"], "00,12")


if __name__ == "__main__":
    unittest.main()
