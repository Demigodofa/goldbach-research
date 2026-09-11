import unittest

from lcm_sawtooth_difference_modulus_mass import (
    difference_modulus_energy_mass_receipt,
)


class LcmSawtoothDifferenceModulusMassTests(unittest.TestCase):
    def test_pair_energy_fractions_are_ordered_probabilities(self):
        receipt = difference_modulus_energy_mass_receipt(
            101, 36, 24, 3, 12)
        for fractions in receipt[
                "large_lcm_pair_energy_fractions"].values():
            self.assertGreaterEqual(fractions[0], fractions[1])
            self.assertGreaterEqual(fractions[1], fractions[2])
            self.assertTrue(all(0 <= value <= 1 for value in fractions))
        self.assertTrue(receipt["finite_positive_pair_mass_measurement"])
        self.assertFalse(
            receipt["complete_energy_sparsity_above_MA_proved"])
        self.assertFalse(
            receipt["signed_difference_modulus_cancellation_proved"])

    def test_invalid_inputs_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "prime"):
            difference_modulus_energy_mass_receipt(100, 36, 24, 3, 12)


if __name__ == "__main__":
    unittest.main()
