import unittest

from multiband_full_frame_probe import multiband_full_frame_probe


class MultibandFullFrameProbeTests(unittest.TestCase):
    def test_one_band_retains_unique_feature_lower_bound(self):
        receipt = multiband_full_frame_probe(1009, 9, 8, 16)
        self.assertGreaterEqual(
            receipt["ideal_over_block_frame_min"], 1 - 1e-10)
        self.assertFalse(receipt["multiband_lower_frame_proved"])

    def test_nested_union_is_numerically_positive(self):
        receipt = multiband_full_frame_probe(1009, 9, 8, 64)
        self.assertGreater(receipt["ideal_over_block_frame_min"], 0)
        self.assertGreater(receipt["exact_over_block_frame_min"], 0)

    def test_rejects_composite_modulus(self):
        with self.assertRaisesRegex(ValueError, "prime"):
            multiband_full_frame_probe(1001, 9, 8, 64)


if __name__ == "__main__":
    unittest.main()
