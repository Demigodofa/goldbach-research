import unittest
from fractions import Fraction as F

from active_frequency_spacing_gate import (critical_spacing_budget,
                                            distinct_prime_denominator_fractions,
                                            finite_cluster_receipt,
                                            safe_subband_modes)


class ActiveFrequencySpacingGateTests(unittest.TestCase):
    def test_exact_crowding_exponents(self):
        result = critical_spacing_budget()
        self.assertEqual(result["frequency_count"], F(27, 25))
        self.assertEqual(result["N_resolution_cells"], F(9, 10))
        self.assertEqual(result["forced_cluster"], F(9, 50))
        self.assertTrue(result["crowding_exceeds_desired_gain"])
        self.assertFalse(result["spacing_only_route_closes"])
        self.assertFalse(result["fixed_prime_energy_conjecture_falsified"])

    def test_safe_rational_subband_uses_strict_integer_inequalities(self):
        modes = safe_subband_modes(101, 10)
        self.assertEqual(modes, (2,))
        for h in modes:
            self.assertGreater(F(h, 101), F(1, 60))
            self.assertLess(F(h, 101), F(1, 40))

    def test_distinct_prime_denominators_have_no_exact_collision(self):
        for m, other_m in ((101, 103), (101, 107), (103, 109)):
            for h in safe_subband_modes(m, 3):
                for other_h in safe_subband_modes(other_m, 3):
                    self.assertTrue(distinct_prime_denominator_fractions(
                        m, h, other_m, other_h))

    def test_finite_actual_prime_moduli_have_a_near_collision_cluster(self):
        result = finite_cluster_receipt()
        self.assertEqual(result["frequency_count"], 5414)
        self.assertEqual(result["distinct_count"], 5414)
        self.assertEqual(result["largest_cluster"], 10)
        self.assertEqual(result["cell_width"], F(1, 120000))


if __name__ == "__main__":
    unittest.main()
