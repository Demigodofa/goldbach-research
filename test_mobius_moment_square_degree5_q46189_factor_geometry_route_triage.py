import json
import unittest
from pathlib import Path


EVIDENCE = Path(
    "evidence/"
    "mobius-moment-square-degree5-q46189-factor-geometry-route-triage.json")


class MobiusMomentSquareDegree5Q46189FactorGeometryRouteTriageTests(
        unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = json.loads(EVIDENCE.read_text(encoding="utf-8"))

    def test_receipt_preserves_boundaries(self):
        self.assertEqual(
            self.receipt["status"],
            "AUDIT_q46189_factor_geometry_route_triage")
        self.assertTrue(
            self.receipt["finite_factor_geometry_route_triage_only"])
        self.assertTrue(self.receipt["finite_diagnostic_only"])
        self.assertFalse(
            self.receipt["all_high_factor_separator_theorem_proved"])
        self.assertFalse(
            self.receipt["scalar_source_pair_coefficient_theorem_proved"])
        self.assertFalse(
            self.receipt["replacement_packet_compensation_theorem_proved"])
        self.assertFalse(self.receipt["goldbach_proved"])

    def test_all_high_no_small_is_finite_separator_only(self):
        separator = self.receipt["all_high_factor_separator"]
        classification = self.receipt["classification"]
        self.assertEqual(separator["all_high_no_small_row_count"], 1)
        self.assertEqual(
            separator["all_high_no_small_rows"][0]["reduced_denominator"],
            46189,
        )
        self.assertEqual(separator["replacement_row_count"], 34)
        self.assertTrue(separator["all_replacement_rows_keep_diagonal_surplus"])
        self.assertTrue(
            classification["all_high_no_small_finite_separator_observed"])
        self.assertTrue(
            classification["all_replacement_rows_keep_diagonal_surplus"])

    def test_scalar_source_pair_coefficient_is_refuted_as_boundary(self):
        scalar = self.receipt["scalar_source_pair_coefficient_test"]
        classification = self.receipt["classification"]
        self.assertFalse(scalar["scalar_threshold_explains_boundary"])
        self.assertEqual(scalar["false_positive_count"], 7)
        self.assertEqual(
            scalar["most_negative_raw_scalar_row"]["reduced_denominator"],
            67830,
        )
        self.assertAlmostEqual(
            scalar["most_negative_raw_scalar_row"]["raw_scalar_real"],
            -0.08346040426201057,
            places=15,
        )
        self.assertTrue(
            classification[
                "scalar_source_pair_coefficient_explanation_refuted"])

    def test_weakest_replacement_requires_compensation(self):
        comp = self.receipt["weakest_replacement_compensation"]
        classification = self.receipt["classification"]
        self.assertEqual(comp["denominator"], 38038)
        self.assertEqual(comp["missing_high_primes"], [17])
        self.assertEqual(comp["small_prime_support"], [2, 7])
        self.assertAlmostEqual(
            comp["total_off_diagonal_over_diagonal_half"],
            -0.8472931845861708,
            places=15,
        )
        self.assertLess(comp["middle_A_to_10A_contribution"], -0.9)
        self.assertGreater(comp["sum_of_other_buckets"], 0.0)
        self.assertAlmostEqual(
            comp["compensation_above_minus_one"],
            0.15270681541382922,
            places=15,
        )
        self.assertTrue(
            classification["weakest_replacement_needs_bucket_compensation"])

    def test_next_action_is_compensation_not_slice_rescue(self):
        action = self.receipt["candidate_next_action"]
        self.assertEqual(
            action["name"],
            "replacement-packet bucket compensation theorem target")
        self.assertIn("not a fitted distance selector", action["mechanism"])
        self.assertIn("q=38038", action["prediction"])


if __name__ == "__main__":
    unittest.main()
