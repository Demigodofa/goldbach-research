import itertools
import math
import unittest

from mobius_covariance_lag_probe import _mobius_values
from mobius_lcm_coefficient_collapse import (
    complete_lcm_log_coefficient,
    mobius_lcm_collapse_probe,
)


class MobiusLcmCoefficientCollapseTests(unittest.TestCase):
    def test_complete_squarefree_divisor_cube_identity(self):
        X = 10000.0
        for q in (1, 2, 6, 30, 210):
            mobius = _mobius_values(q)
            divisors = [value for value in range(1, q + 1)
                        if q % value == 0]
            brute = sum(
                mobius[left] * mobius[right]
                * math.log(X / left) * math.log(X / right)
                for left, right in itertools.product(divisors, repeat=2)
                if math.lcm(left, right) == q)
            self.assertAlmostEqual(
                brute, complete_lcm_log_coefficient(q, X), places=10)

    def test_truncated_probe_preserves_pair_mass_accounting(self):
        receipt = mobius_lcm_collapse_probe(10000, 3, 30)
        self.assertAlmostEqual(
            receipt["grouped_lcm_l1"],
            receipt["grouped_low_lcm_l1"]
            + receipt["grouped_high_lcm_l1"])
        self.assertLessEqual(
            receipt["grouped_lcm_l1_over_raw_pair_l1"], 1 + 1e-12)
        self.assertGreater(receipt["distinct_lcm_count"], 0)
        self.assertGreater(
            receipt["grouped_lcm_l1_over_log_X_squared"], 0)
        self.assertFalse(receipt["mobius_lcm_collapse_asymptotic_proved"])

    def test_invalid_inputs_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "squarefree"):
            complete_lcm_log_coefficient(12, 100)
        with self.assertRaises(ValueError):
            mobius_lcm_collapse_probe(20, 3, 30)


if __name__ == "__main__":
    unittest.main()
