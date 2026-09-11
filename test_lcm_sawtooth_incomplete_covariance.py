import math
import unittest

from lcm_sawtooth_incomplete_covariance import (
    _cyclic_discrepancy,
    _evaluate_polynomial,
    _lcm_coefficient_polynomials,
    lcm_sawtooth_incomplete_covariance_probe,
    project_boundary_scale_probe,
)
from mobius_covariance_lag_probe import _mobius_values


class LcmSawtoothIncompleteCovarianceTests(unittest.TestCase):
    def test_polynomials_match_direct_pair_coefficients(self):
        mobius = _mobius_values(24)
        divisors = tuple(value for value in range(4, 25) if mobius[value])
        polynomials = _lcm_coefficient_polynomials(divisors, mobius)
        for X in (1009 * 9, 1009 * 17):
            logarithm = math.log(X)
            direct = {}
            for left in divisors:
                for right in divisors:
                    q = math.lcm(left, right)
                    direct[q] = direct.get(q, 0.0) + (
                        mobius[left] * mobius[right]
                        * math.log(X / left) * math.log(X / right))
            for q in direct:
                self.assertAlmostEqual(
                    direct[q], _evaluate_polynomial(
                        polynomials[q], logarithm), places=9)

    def test_full_global_period_has_zero_boundary_excess(self):
        # D={5,6,7}; every lcm period divides 210.
        receipt = lcm_sawtooth_incomplete_covariance_probe(
            101, 13, 210, 40, 3, 7)
        self.assertAlmostEqual(
            receipt["frozen_boundary_excess"], 0.0, places=8)
        self.assertAlmostEqual(
            receipt["frozen_incomplete_energy"],
            receipt["complete_period_total_energy"], places=8)

    def test_reported_decompositions_are_exact(self):
        receipt = lcm_sawtooth_incomplete_covariance_probe(
            101, 47, 47, 70, 4, 20)
        self.assertAlmostEqual(
            receipt["frozen_incomplete_energy"],
            receipt["complete_period_total_energy"]
            + receipt["frozen_boundary_excess"], places=9)
        self.assertAlmostEqual(
            receipt["varying_log_incomplete_energy"],
            receipt["frozen_incomplete_energy"]
            + receipt["varying_log_excess"], places=9)
        self.assertTrue(receipt["exact_finite_boundary_decomposition"])
        self.assertFalse(
            receipt["incomplete_boundary_asymptotic_bound_proved"])

    def test_cyclic_discrepancy_has_zero_complete_mean(self):
        for period in (6, 14, 21):
            self.assertAlmostEqual(sum(
                _cyclic_discrepancy(101, ell, period)
                for ell in range(period)), 0.0, places=12)

    def test_invalid_inputs_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "prime"):
            lcm_sawtooth_incomplete_covariance_probe(
                105, 10, 10, 10, 3, 24)
        with self.assertRaisesRegex(ValueError, "squarefree"):
            lcm_sawtooth_incomplete_covariance_probe(
                101, 10, 10, 10, 3, 4)
        with self.assertRaisesRegex(ValueError, "controls"):
            project_boundary_scale_probe(10, 1)

    def test_project_scale_sampler_has_distinct_ordered_primes(self):
        receipt = project_boundary_scale_probe(101, 3)
        self.assertEqual(len(receipt["sampled_moduli"]), 3)
        self.assertEqual(
            tuple(sorted(set(receipt["sampled_moduli"]))),
            receipt["sampled_moduli"])
        self.assertTrue(receipt["finite_project_boundary_measurement"])
        self.assertFalse(receipt["prime_averaged_boundary_bound_proved"])


if __name__ == "__main__":
    unittest.main()
