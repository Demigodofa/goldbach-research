import unittest

from lcm_sawtooth_cotangent_parity import (
    cotangent_parity_discriminator_receipt,
    cotangent_parity_source_receipt,
)


class CotangentParityTests(unittest.TestCase):
    def test_guards(self):
        with self.assertRaises(ValueError):
            cotangent_parity_source_receipt(lag=0)
        with self.assertRaises(ValueError):
            cotangent_parity_source_receipt(tolerance=-1)

    def test_q77_q143_discriminator(self):
        receipt = cotangent_parity_discriminator_receipt()
        self.assertEqual(receipt["strong_quotient"], 77)
        self.assertEqual(receipt["weak_quotient"], 143)
        self.assertTrue(receipt["both_reconstructions_pass"])
        self.assertAlmostEqual(
            receipt["strong_odd_shapley_loss_fraction"],
            .0013701429572540208, places=15)
        self.assertAlmostEqual(
            receipt["weak_odd_shapley_loss_fraction"],
            .004396551332287038, places=15)
        self.assertFalse(receipt["strong_odd_cotangent_gate_passes"])
        self.assertTrue(receipt["weak_odd_cotangent_gate_passes"])
        self.assertFalse(receipt["cotangent_parity_discriminator_passes"])
        strong = cotangent_parity_source_receipt(lag=130)
        weak = cotangent_parity_source_receipt(lag=70)
        self.assertAlmostEqual(
            strong["full_sector_recombination_loss"],
            3043.656249172302, places=9)
        self.assertAlmostEqual(
            weak["full_sector_recombination_loss"],
            1159.4346146954415, places=9)
        for row in (strong, weak):
            self.assertLess(
                row["maximum_source_parity_reconstruction_relative_error"],
                1e-12)
            self.assertTrue(row["cotangent_parity_reconstruction_passes"])


if __name__ == "__main__":
    unittest.main()
