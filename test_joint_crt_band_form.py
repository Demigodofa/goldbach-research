import unittest
from fractions import Fraction as F
from math import gcd

from joint_crt_band_form import (active_band_exponents,
                                 crt_additive_numerators,
                                 prime_component_gauss_status)


class JointCrtBandTests(unittest.TestCase):
    def test_crt_additive_phase_factorization_exactly(self):
        for d in range(2, 10):
            for m in (11, 13):
                if gcd(d, m) != 1:
                    continue
                for h in range(-8, 9):
                    for a in range(d * m):
                        self.assertEqual(*crt_additive_numerators(d, m, h, a))

    def test_nonzero_band_frequency_activates_prime_gauss_sum(self):
        for m in (11, 13, 17):
            for h in range(1, m):
                status = prime_component_gauss_status(m, h)
                self.assertFalse(status["zero"])
                self.assertEqual(status["magnitude_squared"], m)
            self.assertTrue(prime_component_gauss_status(m, m)["zero"])

    def test_actual_exponents_leave_prime_component_nonzero(self):
        result = active_band_exponents()
        self.assertEqual(result["q"], F(599, 1000))
        self.assertEqual(result["h"], F(499, 1000))
        self.assertEqual(result["h_below_m_margin"], F(91, 1000))
        self.assertEqual(result["prime_gauss_magnitude"], F(59, 200))

    def test_no_spectral_estimate_is_smuggled_in(self):
        result = active_band_exponents()
        self.assertFalse(result["d_gauss_component_paid"])
        self.assertTrue(result["target_phase_retained"])
        self.assertFalse(result["spectral_saving_proved"])


if __name__ == "__main__":
    unittest.main()
