import json
import unittest
from pathlib import Path


EVIDENCE = Path(
    "evidence/"
    "mobius-moment-square-degree5-q46189-counterexample-reachability-audit.json")


class MobiusMomentSquareDegree5Q46189CounterexampleReachabilityTests(
        unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = json.loads(EVIDENCE.read_text(encoding="utf-8"))

    def test_receipt_preserves_boundaries(self):
        self.assertEqual(
            self.receipt["status"],
            "AUDIT_q46189_counterexample_reachability")
        self.assertTrue(
            self.receipt["finite_counterexample_reachability_audit_only"])
        self.assertTrue(self.receipt["finite_diagnostic_only"])
        self.assertFalse(self.receipt["natural_selector_theorem_proved"])
        self.assertFalse(self.receipt["fresh_conductor_holdout_proved"])
        self.assertFalse(
            self.receipt["raw_source_pair_admissibility_theorem_proved"])
        self.assertFalse(self.receipt["goldbach_proved"])

    def test_counterexample_is_reachable_by_six_pair_packet(self):
        packet = self.receipt["raw_source_pair_packet"]
        classification = self.receipt["classification"]
        self.assertTrue(
            classification[
                "counterexample_reachable_by_raw_source_pair_mechanism"])
        self.assertTrue(
            classification["counterexample_has_same_six_pair_packet_shape"])
        self.assertEqual(packet["ordered_source_conductor_pair_count"], 6)
        self.assertEqual(packet["raw_frequency_pair_count"], 25920)
        self.assertEqual(packet["raw_reduced_residue_count"], 4320)
        self.assertEqual(packet["zero_left_raw_pair_count"], 0)
        self.assertTrue(packet["raw_scalar_identity_holds_to_tolerance"])
        self.assertAlmostEqual(
            packet["raw_scalar_real"],
            -0.05374291102747207,
            places=15,
        )

    def test_exact_log_identity_matches_replacement_pattern(self):
        exact = self.receipt["exact_log_identity"]
        self.assertEqual(
            exact["factorization"],
            {"2": 1, "3": 1, "11": 1, "13": 1, "19": 1},
        )
        self.assertEqual(exact["missing_high_primes"], [17])
        self.assertEqual(exact["small_prime_support"], [2, 3])
        self.assertTrue(exact["all_pair_scalar_expressions_equal"])
        self.assertTrue(exact["common_log_numerator_equals_expected"])
        self.assertEqual(
            exact["pair_difference_expressions"],
            ["0", "0", "0", "0", "0", "0"],
        )
        self.assertAlmostEqual(
            exact["exact_scalar_minus_raw_scalar"],
            0.0,
            places=15,
        )

    def test_frozen_selector_failure_is_linked(self):
        failure = self.receipt["frozen_selector_failure_row"]
        self.assertEqual(failure["reduced_denominator"], 16302)
        self.assertAlmostEqual(
            failure["positive_fraction_gap_vs_q46189"],
            -0.07517830702507916,
            places=15,
        )
        self.assertFalse(failure["passes_positive_fraction_separator"])
        self.assertTrue(failure["passes_total_pressure_separator"])


if __name__ == "__main__":
    unittest.main()
