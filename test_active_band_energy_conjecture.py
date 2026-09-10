import unittest
from fractions import Fraction as F

from active_band_energy_conjecture import (active_modes,
                                           critical_exponent_receipt,
                                           ramanujan_main_cancellation,
                                           resonant_energy_ratio,
                                           uniform_reduced_residue_output)


class ActiveBandEnergyConjectureTests(unittest.TestCase):
    def test_critical_exponents_and_conditional_margin(self):
        result = critical_exponent_receipt()
        self.assertEqual(result["modulus"], F(599, 1000))
        self.assertEqual(result["active_frequency"], F(499, 1000))
        self.assertEqual(result["frequency_below_companion"], F(91, 1000))
        self.assertEqual(result["conditional_net"], F(-1, 1000))
        self.assertFalse(result["prime_energy_inequality_proved"])

    def test_active_band_has_the_exact_angular_two_sided_normalization(self):
        self.assertEqual(active_modes(101, 10), (2, 3, 98, 99))
        self.assertEqual(active_modes(103, 10), (2, 3, 100, 101))

    def test_uniform_reduced_residue_main_is_annihilated(self):
        for d, m in ((1, 5), (2, 5), (3, 5), (4, 7), (5, 7)):
            self.assertTrue(all(value == 0
                                for value in uniform_reduced_residue_output(d, m)))

    def test_ramanujan_mains_cancel_even_when_h_and_d_are_not_coprime(self):
        for d, m in ((1, 13), (2, 13), (3, 13), (4, 13), (6, 13),
                     (10, 13), (12, 13)):
            for h in range(1, m):
                first, correction, total = ramanujan_main_cancellation(d, m, h)
                self.assertEqual(first, -correction)
                self.assertEqual(total, 0)

    def test_resonant_coefficients_put_almost_all_energy_in_one_mode(self):
        result = resonant_energy_ratio(101, 10, 2)
        self.assertEqual(result["single_mode_fraction"], F(99, 100))
        self.assertGreater(result["ratio"], F(99, 100))
        self.assertGreater(result["ratio"], result["uniform_H_inverse_target"])

    def test_falsifier_has_the_correct_scope(self):
        result = resonant_energy_ratio(101, 10)
        self.assertTrue(result["arbitrary_coefficient_extension_falsified"])
        self.assertFalse(result["actual_prime_log_inequality_falsified"])


if __name__ == "__main__":
    unittest.main()
