import unittest

from cross_divisor_band_probe import cross_divisor_band_probe
from shifted_active_frame_bound import row_shifted_active_frame_bound


class CrossDivisorBandProbeTests(unittest.TestCase):
    def test_same_band_matches_shifted_operator_probe(self):
        cross = cross_divisor_band_probe(1009, 5, 9, 12, 8, 8)
        same = row_shifted_active_frame_bound(
            1009, 5, 9, 12, 8, compare_exact=True)
        self.assertAlmostEqual(
            cross["largest_cross_band_singular_value"],
            same["exact_shifted_active_frame_operator_norm"], places=10)
        self.assertFalse(cross["cross_band_frame_bound_proved"])

    def test_transpose_and_row_swap_preserve_singular_value(self):
        forward = cross_divisor_band_probe(1009, 5, 9, 12, 8, 16)
        reverse = cross_divisor_band_probe(1009, 5, 12, 9, 16, 8)
        self.assertAlmostEqual(
            forward["largest_cross_band_singular_value"],
            reverse["largest_cross_band_singular_value"], places=10)

    def test_rejects_composite_modulus(self):
        with self.assertRaisesRegex(ValueError, "prime"):
            cross_divisor_band_probe(1001, 5, 9, 12, 8, 16)


if __name__ == "__main__":
    unittest.main()
