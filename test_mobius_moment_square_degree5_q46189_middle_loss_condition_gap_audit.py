import json
import unittest
from pathlib import Path


EVIDENCE = Path(
    "evidence/"
    "mobius-moment-square-degree5-q46189-middle-loss-condition-gap-audit.json")


class MobiusMomentSquareDegree5Q46189MiddleLossGapTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = json.loads(EVIDENCE.read_text(encoding="utf-8"))
        cls.summary = cls.receipt["summary"]

    def test_receipt_preserves_boundaries(self):
        self.assertEqual(
            self.receipt["status"],
            "AUDIT_q46189_middle_loss_condition_gap")
        self.assertTrue(
            self.receipt["finite_middle_loss_condition_gap_audit_only"])
        self.assertTrue(self.receipt["finite_diagnostic_only"])
        self.assertFalse(
            self.receipt["middle_loss_compensation_theorem_proved"])
        self.assertFalse(
            self.receipt["source_factor_isolation_theorem_proved"])
        self.assertFalse(
            self.receipt["replacement_packet_compensation_theorem_proved"])
        self.assertFalse(self.receipt["goldbach_proved"])

    def test_q38038_is_uniquely_isolated_worst_middle_loss(self):
        worst = self.summary["worst_middle_loss_row"]
        second = self.summary["second_middle_loss_row"]
        self.assertEqual(worst["reduced_denominator"], 38038)
        self.assertEqual(second["reduced_denominator"], 41990)
        self.assertAlmostEqual(
            worst["middle_A_to_10A"],
            -0.939992990438763,
            places=15,
        )
        self.assertAlmostEqual(
            second["middle_A_to_10A"],
            -0.43222079205102754,
            places=15,
        )
        self.assertAlmostEqual(
            self.summary["middle_loss_isolation_gap"],
            0.5077721983877355,
            places=15,
        )

    def test_two_row_middle_loss_condition_is_refuted(self):
        failure = self.summary["smallest_middle_loss_prefix_failure"]
        self.assertEqual(failure["prefix_size"], 2)
        self.assertEqual(
            failure["nonpositive_non_middle_denominators"],
            [41990],
        )
        self.assertAlmostEqual(
            failure["minimum_non_middle_sum"],
            -0.10078449680431602,
            places=15,
        )
        classification = self.receipt["classification"]
        self.assertTrue(
            classification["middle_loss_threshold_compensation_singleton_only"])
        self.assertTrue(
            classification["any_two_row_middle_loss_condition_refuted"])
        self.assertTrue(
            classification["plain_middle_loss_monotonicity_refuted"])

    def test_factor_geometry_names_next_separator(self):
        worst = self.summary["worst_middle_loss_row"]["factor_geometry"]
        second = self.summary["second_middle_loss_row"]["factor_geometry"]
        self.assertEqual(worst["missing_high_primes"], [17])
        self.assertEqual(worst["small_prime_support"], [2, 7])
        self.assertEqual(second["missing_high_primes"], [11])
        self.assertEqual(second["small_prime_support"], [2, 5])
        action = self.receipt["candidate_next_action"]
        self.assertEqual(action["name"],
                         "source-factor isolation theorem target")
        self.assertIn("q=41990", action["prediction"])


if __name__ == "__main__":
    unittest.main()
