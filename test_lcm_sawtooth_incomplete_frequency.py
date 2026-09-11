import unittest

from lcm_sawtooth_incomplete_covariance import (
    lcm_sawtooth_incomplete_covariance_probe,
)
from lcm_sawtooth_incomplete_frequency import (
    primitive_conductor_operator_receipt,
    primitive_frequency_receipt,
)


class LcmSawtoothIncompleteFrequencyTests(unittest.TestCase):
    def test_primitive_frequency_factorization_is_exact(self):
        receipt = primitive_frequency_receipt(101, 47, 47, 70, 4, 14)
        covariance = lcm_sawtooth_incomplete_covariance_probe(
            101, 47, 47, 70, 4, 14)
        self.assertLess(receipt["maximum_row_reconstruction_error"], 1e-8)
        self.assertLess(receipt["maximum_primitive_parseval_error"], 1e-8)
        self.assertAlmostEqual(
            receipt["incomplete_frequency_energy"],
            covariance["frozen_incomplete_energy"], places=7)
        self.assertAlmostEqual(
            receipt["complete_primitive_energy"],
            covariance["complete_period_total_energy"], places=7)
        self.assertLess(receipt["pair_boundary_reconstruction_error"], 1e-7)
        self.assertTrue(
            receipt["exact_primitive_frequency_factorization_proved"])
        self.assertFalse(
            receipt["incomplete_boundary_asymptotic_bound_proved"])

    def test_conductor_operator_contains_actual_direction(self):
        receipt = primitive_conductor_operator_receipt(
            101, 47, 47, 70, 4, 14)
        covariance = lcm_sawtooth_incomplete_covariance_probe(
            101, 47, 47, 70, 4, 14)
        self.assertAlmostEqual(
            receipt["actual_mobius_conductor_ratio"],
            covariance["frozen_incomplete_energy"]
            / covariance["complete_period_total_energy"], places=8)
        self.assertLessEqual(
            receipt["actual_mobius_conductor_ratio"],
            receipt["sharp_arbitrary_conductor_ratio"] + 1e-12)
        self.assertLessEqual(
            receipt["actual_mobius_conductor_ratio"],
            receipt["sharp_quadratic_log_span_ratio"] + 1e-12)
        self.assertLessEqual(
            receipt["sharp_quadratic_log_span_ratio"],
            receipt["sharp_arbitrary_conductor_ratio"] + 1e-12)
        self.assertEqual(receipt["quadratic_log_conductor_span_rank"], 3)
        self.assertTrue(
            receipt[
                "largest_eigenvalue_dominates_trace_rank_bound_verified"])
        self.assertTrue(receipt["exact_conductor_packet_identity_proved"])
        self.assertFalse(
            receipt["uniform_conductor_operator_subpower_bound_proved"])

    def test_invalid_inputs_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "prime"):
            primitive_frequency_receipt(100, 10, 10, 10, 3, 9)
        with self.assertRaisesRegex(ValueError, "Boolean"):
            primitive_frequency_receipt(
                101, 10, 10, 10, 3, 9, decompose_pairs=1)


if __name__ == "__main__":
    unittest.main()
