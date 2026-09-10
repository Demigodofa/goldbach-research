import unittest
from fractions import Fraction as F
from math import gcd

from prime_pointwise_band_gate import (classical_pointwise_exponent,
                                       diophantine_separation,
                                       pointwise_energy_budget,
                                       rational_separation_floor,
                                       source_pointwise_exponent)


class PrimePointwiseBandGateTests(unittest.TestCase):
    def test_source_exponent_uses_the_forced_diophantine_floor(self):
        self.assertEqual(rational_separation_floor(), F(41, 100))
        self.assertEqual(source_pointwise_exponent(), F(159, 200))
        self.assertEqual(classical_pointwise_exponent(), F(4, 5))

    def test_current_pointwise_energy_misses_by_companion_exponent(self):
        result = pointwise_energy_budget()
        self.assertEqual(result["active_frequency_count"], F(27, 25))
        self.assertEqual(result["pointwise_energy"], F(52, 25))
        self.assertEqual(result["all_frequency_variance"], F(159, 100))
        self.assertEqual(result["required_band_energy"], F(149, 100))
        self.assertEqual(result["gap"], F(59, 100))
        self.assertFalse(result["pointwise_route_closes"])
        self.assertFalse(result["averaged_type_I_II_estimate_proved"])

    def test_classical_pointwise_energy_misses_by_three_fifths(self):
        result = pointwise_energy_budget(classical_pointwise_exponent())
        self.assertEqual(result["pointwise_energy"], F(209, 100))
        self.assertEqual(result["gap"], F(3, 5))

    def test_only_square_root_pointwise_strength_reaches_the_energy_target(self):
        at_target = pointwise_energy_budget(F(1, 2))
        above_target = pointwise_energy_budget(F(1, 2) + F(1, 1000))
        self.assertTrue(at_target["pointwise_route_closes"])
        self.assertEqual(at_target["pointwise_energy"],
                         at_target["required_band_energy"])
        self.assertFalse(above_target["pointwise_route_closes"])

    def test_exact_rational_separation_exhaustively(self):
        for m in (11, 13, 17):
            for h in range(1, m):
                for q in range(1, m):
                    for a in range(q + 1):
                        if gcd(a, q) != 1 or F(a, q) == F(h, m):
                            continue
                        result = diophantine_separation(1000, h, m, a, q)
                        self.assertTrue(result["separation_holds"])
                        self.assertTrue(result["scaled_floor_holds"])


if __name__ == "__main__":
    unittest.main()
