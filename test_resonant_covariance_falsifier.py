import cmath
import unittest
from math import pi

from mobius_band_character_covariance import active_nonzero_modes
from resonant_covariance_falsifier import resonant_covariance_receipt


class ResonantCovarianceFalsifierTests(unittest.TestCase):
    def test_closed_energy_formulas_match_direct_resonant_sum(self):
        prime, shift_length = 101, 3
        result = resonant_covariance_receipt(prime, shift_length)
        h0 = result["resonant_frequency"]
        alpha = {a: cmath.exp(2j * pi * h0 * a / prime)
                 for a in range(1, prime)}

        def value(h):
            return sum(alpha[a] * (
                cmath.exp(-2j * pi * h * a / prime) + 1 / (prime - 1)
            ) for a in alpha)

        full = sum(abs(value(h)) ** 2 for h in range(1, prime))
        band = sum(abs(value(h)) ** 2
                   for h in active_nonzero_modes(prime, shift_length))
        self.assertAlmostEqual(full, float(result["full_energy"]), places=8)
        self.assertAlmostEqual(band, float(result["band_energy"]), places=8)
        self.assertEqual(result["band_over_full"], result["closed_band_ratio"])
        self.assertEqual(result["off_over_full"], result["closed_off_ratio"])

    def test_resonance_reinforces_rather_than_cancels(self):
        result = resonant_covariance_receipt(1009, 5)
        self.assertGreater(result["band_over_full"], 0.99)
        self.assertGreater(result["off_over_full"], 0.9)
        self.assertGreater(result["off_diagonal_energy"], 0)


if __name__ == "__main__":
    unittest.main()
