import unittest

from lcm_sawtooth_global_harmonic_bound import (
    global_complete_period_harmonic_bound_receipt,
    rectangular_lcm_harmonic_receipt,
)
from lcm_sawtooth_diagonal_bound import lcm_sawtooth_diagonal_probe


class LcmSawtoothGlobalHarmonicBoundTests(unittest.TestCase):
    def test_rectangular_lcm_harmonic_identity_and_bound(self):
        receipt = rectangular_lcm_harmonic_receipt(8, 11)
        self.assertAlmostEqual(
            receipt["direct_lcm_harmonic_sum"],
            receipt["gcd_expanded_lcm_harmonic_sum"])
        self.assertLessEqual(
            receipt["direct_lcm_harmonic_sum"],
            receipt["triple_harmonic_bound"] + 1e-12)
        self.assertTrue(
            receipt["rectangular_lcm_harmonic_identity_proved"])

    def test_global_bound_contains_exact_complete_energy(self):
        receipt = global_complete_period_harmonic_bound_receipt(
            101, 70, 4, 20)
        diagonal = lcm_sawtooth_diagonal_probe(101, 70, 4, 20)
        self.assertLessEqual(
            receipt["exact_complete_period_energy"],
            receipt["proved_global_harmonic_upper_bound"])
        self.assertAlmostEqual(
            receipt["reciprocal_lcm_pair_mass"],
            diagonal["reciprocal_lcm_pair_mass"], places=10)
        self.assertLessEqual(receipt["maximum_H_m_over_m_d"], 1)
        self.assertTrue(receipt["primitive_weight_bounded_by_F_verified"])
        self.assertTrue(
            receipt["global_complete_period_harmonic_bound_proved"])
        self.assertFalse(receipt["incomplete_row_covariance_bound_proved"])
        self.assertFalse(receipt["signed_prime_correlation_estimate_proved"])

    def test_invalid_limits_and_modulus_are_rejected(self):
        with self.assertRaises(ValueError):
            rectangular_lcm_harmonic_receipt(0, 2)
        with self.assertRaisesRegex(ValueError, "prime"):
            global_complete_period_harmonic_bound_receipt(100, 70, 4, 20)


if __name__ == "__main__":
    unittest.main()
