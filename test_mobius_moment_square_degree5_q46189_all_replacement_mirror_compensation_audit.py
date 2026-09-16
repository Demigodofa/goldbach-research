import json
import unittest
from pathlib import Path


EVIDENCE = Path(
    "evidence/"
    "mobius-moment-square-degree5-q46189-all-replacement-mirror-compensation-audit.json")


class MobiusMomentSquareDegree5Q46189AllReplacementMirrorTests(
        unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = json.loads(EVIDENCE.read_text(encoding="utf-8"))

    def test_receipt_preserves_boundaries(self):
        self.assertEqual(
            self.receipt["status"],
            "AUDIT_q46189_all_replacement_mirror_compensation")
        self.assertTrue(
            self.receipt[
                "finite_all_replacement_mirror_compensation_audit_only"])
        self.assertTrue(self.receipt["finite_diagnostic_only"])
        self.assertFalse(
            self.receipt[
                "universal_mirror_block_compensation_theorem_proved"])
        self.assertFalse(
            self.receipt["tight_middle_loss_compensation_theorem_proved"])
        self.assertFalse(self.receipt["goldbach_proved"])

    def test_broad_mirror_compensation_is_refuted(self):
        summary = self.receipt["summary"]
        classification = self.receipt["classification"]
        self.assertEqual(summary["replacement_denominator_count"], 34)
        self.assertEqual(summary["negative_non_middle_count"], 15)
        self.assertEqual(summary["nonpositive_best_mirror_count"], 7)
        self.assertTrue(
            classification[
                "universal_positive_non_middle_compensation_refuted"])
        self.assertTrue(
            classification[
                "universal_positive_best_mirror_block_refuted"])
        self.assertTrue(
            self.receipt[
                "universal_mirror_block_compensation_refuted_on_checked_rows"])

    def test_q38038_remains_tightest_total_and_middle_loss(self):
        summary = self.receipt["summary"]
        classification = self.receipt["classification"]
        q38038 = self.receipt["q38038_row"]
        self.assertEqual(summary["weakest_total_row"]["reduced_denominator"],
                         38038)
        self.assertEqual(summary["weakest_middle_row"]["reduced_denominator"],
                         38038)
        self.assertEqual(summary["q38038_ranks"]["off_diagonal_ascending"], 1)
        self.assertEqual(summary["q38038_ranks"]["middle_loss_ascending"], 1)
        self.assertAlmostEqual(
            q38038["off_diagonal_over_diagonal_half"],
            -0.8472931845861708,
            places=15,
        )
        self.assertAlmostEqual(
            q38038["middle_A_to_10A"],
            -0.939992990438763,
            places=15,
        )
        self.assertAlmostEqual(
            q38038["non_middle_sum"],
            0.09269980585259228,
            places=15,
        )
        self.assertTrue(
            classification["tight_middle_loss_condition_still_alive"])

    def test_q38038_mirror_block_is_not_universal_extreme(self):
        summary = self.receipt["summary"]
        q38038 = self.receipt["q38038_row"]
        self.assertEqual(summary["q38038_strongest_mirror_rank_descending"], 9)
        self.assertEqual(summary["q38038_ranks"]["non_middle_descending"], 13)
        self.assertAlmostEqual(
            q38038["strongest_non_middle_mirror_block"]["non_middle_sum"],
            0.07765412336759717,
            places=15,
        )

    def test_next_action_is_conditional_compensation(self):
        action = self.receipt["candidate_next_action"]
        self.assertEqual(
            action["name"],
            "tight-middle-loss conditional compensation target")
        self.assertIn("too broad", action["mechanism"])
        self.assertIn("severe middle-bucket loss", action["prediction"])


if __name__ == "__main__":
    unittest.main()
