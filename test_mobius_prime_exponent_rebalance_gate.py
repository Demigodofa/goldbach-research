import unittest
from fractions import Fraction as F

from mobius_prime_exponent_rebalance_gate import (
    UNPAID_COMPANION_FLOOR,
    WRIGHT_MODULUS_CEILING,
    prime_exponent_rebalance_budget,
    wright_factor_range,
)


class PrimeExponentRebalanceGateTests(unittest.TestCase):
    def test_current_exponent_keeps_type_i_but_misses_every_source_range(self):
        result = prime_exponent_rebalance_budget(F(59, 100))
        self.assertEqual(result["absolute_band_benchmark"], F(1499, 1000))
        self.assertEqual(result["u1_type_i"], F(749, 500))
        self.assertEqual(result["u1_type_i_margin"], F(1, 1000))
        self.assertTrue(result["in_unpaid_companion_range"])
        self.assertFalse(result["wright_possible_for_some_factor_scale"])
        self.assertFalse(result["classical_bv_with_small_divisor"])

    def test_wright_range_exists_exactly_below_seventeen_thirty_three(self):
        self.assertIsNone(wright_factor_range(WRIGHT_MODULUS_CEILING))
        below = WRIGHT_MODULUS_CEILING - F(1, 3300)
        interval = wright_factor_range(below)
        self.assertIsNotNone(interval)
        self.assertLess(interval[0], interval[1])
        above = WRIGHT_MODULUS_CEILING + F(1, 3300)
        self.assertIsNone(wright_factor_range(above))

    def test_no_wright_or_bv_range_intersects_unpaid_companions(self):
        self.assertGreater(UNPAID_COMPANION_FLOOR, WRIGHT_MODULUS_CEILING)
        self.assertFalse(prime_exponent_rebalance_budget(
            UNPAID_COMPANION_FLOOR)["in_unpaid_companion_range"])
        for tick in range(541, 592):
            result = prime_exponent_rebalance_budget(F(tick, 1000))
            self.assertTrue(result["in_unpaid_companion_range"])
            self.assertFalse(result["wright_possible_for_some_factor_scale"])
            self.assertFalse(result["classical_bv_with_small_divisor"])
            self.assertTrue(result["relative_balanced_interval_nonempty"])
            self.assertTrue(result["u1_type_i_fits"])

    def test_bv_requires_strict_exponent_margin(self):
        boundary = prime_exponent_rebalance_budget(F(491, 1000))
        self.assertFalse(boundary["classical_bv_with_small_divisor"])
        below = prime_exponent_rebalance_budget(F(490, 1000))
        self.assertTrue(below["classical_bv_with_small_divisor"])

    def test_balanced_factor_condition_reverses_wright_upper_condition(self):
        for mu_tick in range(501, 591):
            mu = F(mu_tick, 1000)
            for alpha_tick in range(1001-mu_tick, mu_tick):
                alpha = F(alpha_tick, 1000)
                longer = max(alpha, 1-alpha)
                self.assertLess(longer, mu)

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            prime_exponent_rebalance_budget(F(0))
        with self.assertRaises(ValueError):
            prime_exponent_rebalance_budget(0.59)


if __name__ == "__main__":
    unittest.main()
