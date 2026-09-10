import unittest

from mobius_band_character_covariance import (
    active_nonzero_modes,
    character_box_sum,
    character_covariance_receipt,
    character_table,
    direct_box_sum,
)


class MobiusBandCharacterCovarianceTests(unittest.TestCase):
    def test_gauss_character_expansion_matches_direct_centered_box(self):
        alpha = {1: 2, 2: -1, 4: 3}
        beta = {1: 1, 3: -2, 5: 4}
        for prime in (7, 11, 13):
            for h in range(1, prime):
                self.assertAlmostEqual(
                    direct_box_sum(prime, h, alpha, beta).real,
                    character_box_sum(prime, h, alpha, beta).real,
                    places=9,
                )
                self.assertAlmostEqual(
                    direct_box_sum(prime, h, alpha, beta).imag,
                    character_box_sum(prime, h, alpha, beta).imag,
                    places=9,
                )

    def test_character_covariance_equals_direct_band_energy(self):
        alpha = {1: 1, 2: -1, 3: 2}
        beta = {2: 3, 4: -2, 5: 1}
        for prime, shift in ((101, 10), (103, 10)):
            result = character_covariance_receipt(prime, shift, alpha, beta)
            self.assertGreater(result["band_size"], 0)
            self.assertAlmostEqual(result["direct_energy"],
                                   result["covariance_energy"].real, places=7)
            self.assertAlmostEqual(result["covariance_energy"].imag, 0, places=7)
            self.assertAlmostEqual(result["direct_energy"],
                                   (result["diagonal"] + result["off_diagonal"]).real,
                                   places=7)

    def test_short_band_character_second_moment_is_exact(self):
        for prime, shift in ((101, 10), (103, 10), (109, 7)):
            modes = active_nonzero_modes(prime, shift)
            table = character_table(prime)
            moments = [abs(sum(chi[h] for h in modes)) ** 2 for chi in table]
            self.assertAlmostEqual(sum(moments), (prime - 1) * len(modes), places=7)
            self.assertAlmostEqual(sum(moments[1:]),
                                   (prime - 1) * len(modes) - len(modes) ** 2,
                                   places=7)


if __name__ == "__main__":
    unittest.main()
