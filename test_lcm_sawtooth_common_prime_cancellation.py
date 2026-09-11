import unittest

from lcm_sawtooth_common_prime_cancellation import (
    common_prime_cancellation_probe,
    project_common_prime_cancellation_probe,
)
from lcm_sawtooth_residual_block_probe import dyadic_multi_residual_probe


class LcmSawtoothCommonPrimeCancellationTests(unittest.TestCase):
    def test_feature_split_reconstructs_exact_high_residual_quotient(self):
        receipt = common_prime_cancellation_probe(101, 70, 4, 20)
        dyadic = dyadic_multi_residual_probe(101, 70, 4, 20)
        self.assertLess(
            receipt["maximum_coefficient_reconstruction_error"], 1e-9)
        self.assertAlmostEqual(
            receipt["high_d"]["actual_residual_quotient"],
            dyadic["high_d_multi_residual_quotient"])
        for scope in (receipt["high_d"], receipt["dominant_block"]):
            self.assertAlmostEqual(scope["factorization_error"], 0.0)
            self.assertGreater(scope["coordinate_count"], 0)
            self.assertLessEqual(
                abs(scope["collapsed_feature_correlation"]), 1 + 1e-12)
            self.assertLessEqual(
                abs(scope["diagonal_feature_correlation"]), 1 + 1e-12)
            self.assertGreater(
                scope["common_sign_aligned_residual_quotient"], 0)
        self.assertTrue(
            receipt["common_prime_feature_decomposition_proved"])
        self.assertTrue(
            receipt["common_part_sign_counterfactual_measured"])
        self.assertFalse(
            receipt["common_prime_cancellation_mechanism_proved"])

    def test_invalid_ranges_are_rejected(self):
        with self.assertRaises(ValueError):
            common_prime_cancellation_probe(100, 70, 4, 20)
        with self.assertRaises(ValueError):
            common_prime_cancellation_probe(101, 70, 20, 4)

    def test_project_sampler_marks_measurement_as_finite(self):
        receipt = project_common_prime_cancellation_probe(101, 3)
        self.assertEqual(len(receipt["sampled_moduli"]), 3)
        self.assertTrue(
            receipt["finite_common_prime_interference_measurement"])
        self.assertIsInstance(
            receipt[
                "all_sampled_dominant_sign_alignment_increases_quotient"],
            bool)
        self.assertFalse(
            receipt["common_prime_cancellation_mechanism_proved"])


if __name__ == "__main__":
    unittest.main()
