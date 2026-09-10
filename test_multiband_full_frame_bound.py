import unittest

from multiband_full_frame_bound import multiband_full_frame_bound


class MultibandFullFrameBoundTests(unittest.TestCase):
    def test_inversion_certificate_is_below_actual_ideal_eigenvalue(self):
        receipt = multiband_full_frame_bound(
            1009, 9, 8, 64, compare_exact=True)
        self.assertLessEqual(
            receipt["proved_ideal_over_block_frame_lower"],
            receipt["actual_ideal_over_block_frame_min"] + 1e-10)
        self.assertTrue(
            receipt["asymptotic_subpower_multiband_lower_frame_proved"])
        self.assertFalse(receipt["constant_lower_frame_proved"])

    def test_one_band_inversion_certificate_is_valid(self):
        receipt = multiband_full_frame_bound(
            1009, 9, 8, 16, compare_exact=True)
        self.assertLessEqual(
            receipt["proved_ideal_over_block_frame_lower"],
            receipt["actual_ideal_over_block_frame_min"] + 1e-10)

    def test_rejects_composite_modulus(self):
        with self.assertRaisesRegex(ValueError, "prime"):
            multiband_full_frame_bound(1001, 9, 8, 64)


if __name__ == "__main__":
    unittest.main()
