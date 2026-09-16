import json
import unittest
from pathlib import Path


EVIDENCE = Path(
    "evidence/"
    "mobius-moment-square-degree5-q46189-50a60a-distance-profile-audit.json")


class MobiusMomentSquareDegree5Q4618950A60ADistanceProfileTests(
        unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = json.loads(EVIDENCE.read_text(encoding="utf-8"))

    def test_receipt_preserves_boundaries(self):
        self.assertEqual(
            self.receipt["status"],
            "AUDIT_q46189_50a60a_distance_profile")
        self.assertTrue(
            self.receipt["finite_50a60a_distance_profile_audit_only"])
        self.assertTrue(self.receipt["finite_diagnostic_only"])
        self.assertFalse(
            self.receipt["exact_distance_pointwise_theorem_proved"])
        self.assertFalse(
            self.receipt["short_block_positive_share_theorem_proved"])
        self.assertFalse(
            self.receipt["short_block_pressure_theorem_proved"])
        self.assertFalse(self.receipt["goldbach_proved"])

    def test_exact_distance_pointwise_envelope_fails(self):
        envelope = self.receipt["exact_distance_pointwise_envelope"]
        self.assertEqual(envelope["distance_count"], 430)
        self.assertEqual(envelope["pointwise_positive_gap_count"], 83)
        self.assertEqual(envelope["pointwise_nonpositive_gap_count"], 347)
        self.assertAlmostEqual(
            envelope["adverse_total_over_diagonal"],
            -0.08597078804878477,
            places=15)
        self.assertAlmostEqual(
            envelope["componentwise_min_replacement_total_over_diagonal"],
            -0.5389671631863593,
            places=15)
        self.assertAlmostEqual(
            envelope[
                "componentwise_min_replacement_minus_adverse_total_gap"],
            -0.4529963751375745,
            places=15)
        self.assertFalse(
            envelope["exact_distance_pointwise_separator_survives"])
        self.assertFalse(
            envelope["componentwise_exact_distance_envelope_survives"])

    def test_short_block_witness_survives(self):
        blocks = {
            row["block_name"]: row
            for row in self.receipt["contiguous_micro_block_summaries"]
        }
        block = blocks["56A_to_58A"]
        self.assertEqual(block["distance_range"], [2409, 2494])
        self.assertEqual(block["distance_count"], 86)
        self.assertAlmostEqual(
            block["adverse_positive_fraction"],
            0.26392574746028347,
            places=15)
        self.assertAlmostEqual(
            block["minimum_replacement_positive_fraction"],
            0.3055515148922263,
            places=15)
        self.assertEqual(
            block["minimum_replacement_positive_fraction_denominator"],
            40755)
        self.assertAlmostEqual(
            block["positive_fraction_gap"],
            0.04162576743194285,
            places=15)
        self.assertAlmostEqual(
            block["adverse_total_over_diagonal"],
            -0.057125505502661246,
            places=15)
        self.assertAlmostEqual(
            block["minimum_replacement_total_over_diagonal"],
            -0.023310151551005336,
            places=15)
        self.assertAlmostEqual(
            block["total_gap"],
            0.03381535395165591,
            places=15)
        self.assertTrue(block["separates_by_both_share_and_total"])

    def test_minimal_micro_slices_are_recorded(self):
        classification = self.receipt["classification"]
        self.assertTrue(
            classification["exact_distance_pointwise_theorem_target_falsified"])
        self.assertTrue(
            classification["componentwise_exact_distance_envelope_falsified"])
        self.assertEqual(
            classification["micro_slices_separating_by_both"],
            ["56A_to_57A", "57A_to_58A"])
        self.assertEqual(
            classification["minimal_width_separating_micro_blocks"],
            ["56A_to_57A", "57A_to_58A"])
        self.assertEqual(
            classification["two_a_witness_block"], "56A_to_58A")


if __name__ == "__main__":
    unittest.main()
