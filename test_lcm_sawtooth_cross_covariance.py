import math
import unittest

from lcm_sawtooth_cross_covariance import (
    cyclic_sawtooth_covariance,
    mobius_lcm_complete_covariance_probe,
)


def _discrepancy(modulus, period, ell):
    X = modulus * ell
    return ((X + modulus - 1) // period - X // period
            - (modulus - 1) / period)


class LcmSawtoothCrossCovarianceTests(unittest.TestCase):
    def test_crt_formula_matches_complete_period(self):
        for modulus, left, right in ((101, 14, 21), (103, 12, 25),
                                     (107, 18, 30), (109, 8, 8)):
            period = math.lcm(left, right)
            direct = sum(
                _discrepancy(modulus, left, ell)
                * _discrepancy(modulus, right, ell)
                for ell in range(period)) / period
            receipt = cyclic_sawtooth_covariance(modulus, left, right)
            self.assertAlmostEqual(direct, receipt["covariance"], places=12)
            self.assertLessEqual(
                abs(receipt["covariance"]),
                receipt["gcd_covariance_bound"] + 1e-12)
            self.assertLessEqual(
                abs(receipt["covariance"]),
                receipt["cauchy_covariance_bound"] + 1e-12)

    def test_coprime_periods_are_exactly_uncorrelated(self):
        receipt = cyclic_sawtooth_covariance(101, 14, 25)
        self.assertEqual(receipt["gcd"], 1)
        self.assertEqual(receipt["covariance"], 0)
        self.assertTrue(receipt["coprime_covariance_zero"])

    def test_gcd_bound_exhaustive_small_ranges(self):
        for modulus in (101, 103):
            for left in range(2, 25):
                for right in range(2, 25):
                    receipt = cyclic_sawtooth_covariance(
                        modulus, left, right)
                    self.assertLessEqual(
                        abs(receipt["covariance"]),
                        receipt["gcd_covariance_bound"] + 1e-12)

    def test_actual_coefficient_energy_is_nonnegative(self):
        receipt = mobius_lcm_complete_covariance_probe(101, 101, 3, 24)
        self.assertGreater(receipt["complete_period_diagonal_energy"], 0)
        self.assertGreaterEqual(
            receipt["complete_period_total_energy"], -1e-9)
        self.assertLessEqual(
            abs(receipt["complete_period_off_diagonal_energy"]),
            receipt["absolute_off_diagonal_gcd_bound"] + 1e-9)
        self.assertTrue(
            receipt["complete_period_cross_covariance_identity_proved"])
        self.assertFalse(
            receipt["incomplete_prime_row_covariance_bound_proved"])

    def test_invalid_inputs_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "coprime"):
            cyclic_sawtooth_covariance(10, 14, 21)
        with self.assertRaisesRegex(ValueError, "prime"):
            mobius_lcm_complete_covariance_probe(105, 10, 3, 24)
        with self.assertRaisesRegex(ValueError, "squarefree"):
            mobius_lcm_complete_covariance_probe(101, 10, 3, 4)


if __name__ == "__main__":
    unittest.main()
