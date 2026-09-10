import unittest
from fractions import Fraction as F

from shift_fourier_energy_gate import (energy_gate_receipt,
                                       generic_large_sieve_improves,
                                       kernel_frequency_budget,
                                       required_prime_band_energy_ratio,
                                       resulting_correlation_gain)


class ShiftFourierEnergyTests(unittest.TestCase):
    def test_kernel_band_has_full_parseval_energy(self):
        b = kernel_frequency_budget()
        self.assertEqual(b["active_frequency_count"], F(499, 1000))
        self.assertEqual(b["coefficient_amplitude"], F(1, 10))
        self.assertEqual(b["kernel_square_energy"], F(699, 1000))
        self.assertEqual(b["kernel_square_energy"], b["parseval_expected_energy"])

    def test_needed_arithmetic_energy_gain_is_exactly_one_over_H(self):
        self.assertEqual(required_prime_band_energy_ratio(), F(-1, 10))
        self.assertEqual(resulting_correlation_gain(), F(-1, 20))

    def test_generic_large_sieve_is_conductor_dominated(self):
        self.assertFalse(generic_large_sieve_improves())

    def test_receipt_keeps_new_input_unproved(self):
        r = energy_gate_receipt()
        self.assertTrue(r["kernel_energy_matches_parseval"])
        self.assertFalse(r["generic_large_sieve_improves"])
        self.assertFalse(r["arithmetic_band_energy_proved"])
        self.assertFalse(r["mask_leakage_paid"])


if __name__ == "__main__":
    unittest.main()
