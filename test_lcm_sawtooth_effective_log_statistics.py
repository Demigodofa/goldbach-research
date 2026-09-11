import unittest

from lcm_sawtooth_effective_log_statistics import (
    project_effective_log_statistics,
)


class LcmSawtoothEffectiveLogStatisticsTests(unittest.TestCase):
    def test_m127_centroid_fails_while_largest_conductor_is_close(self):
        receipt = project_effective_log_statistics(
            127, .2795716513419446)
        self.assertEqual(receipt["prime_count"], 24)
        self.assertEqual(receipt["divisor_range"], (3, 13))
        self.assertAlmostEqual(
            receipt["leading_energy_weighted_vertex_mean"],
            .24027472035050035)
        self.assertFalse(
            receipt["weighted_vertex_mean_within_one_hundredth"])
        self.assertEqual(receipt["largest_quadratic_conductor"], 143)
        self.assertAlmostEqual(
            receipt["largest_conductor_midpoint_vertex"],
            .27792369242256126)
        self.assertTrue(
            receipt["largest_conductor_vertex_within_one_hundredth"])

    def test_m251_repeats_centroid_failure_and_endpoint_proximity(self):
        receipt = project_effective_log_statistics(
            251, .2809004167441096)
        self.assertEqual(receipt["prime_count"], 42)
        self.assertEqual(receipt["divisor_range"], (4, 20))
        self.assertAlmostEqual(
            receipt["leading_energy_weighted_vertex_mean"],
            .24589704609961716)
        self.assertFalse(
            receipt["weighted_vertex_mean_within_one_hundredth"])
        self.assertEqual(receipt["largest_quadratic_conductor"], 323)
        self.assertAlmostEqual(
            receipt["largest_conductor_midpoint_vertex"],
            .2858488159506599)
        self.assertTrue(
            receipt["largest_conductor_vertex_within_one_hundredth"])
        self.assertTrue(receipt["fitted_parameter_supplied_not_derived"])
        self.assertFalse(receipt["uniform_effective_log_formula_proved"])
        self.assertFalse(receipt["uniform_active_full_lower_frame_proved"])
        self.assertFalse(receipt["signed_prime_correlation_proved"])

    def test_guards_invalid_inputs(self):
        with self.assertRaises(ValueError):
            project_effective_log_statistics(16, .25)
        with self.assertRaises(ValueError):
            project_effective_log_statistics(127, float("nan"))


if __name__ == "__main__":
    unittest.main()
