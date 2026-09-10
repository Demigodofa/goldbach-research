import math
import unittest

from near_cutoff_geometric_bound import (
    averaged_near_cutoff_receipt,
    exact_weighted_progression_energy,
    geometric_majorant_energy,
)


class NearCutoffGeometricBoundTests(unittest.TestCase):
    def test_explicit_bound_on_small_coprime_inputs(self):
        checked = 0
        for modulus in range(17, 100):
            for shift_length in range(2, 6):
                for divisor in range(shift_length, min(15, modulus)):
                    if math.gcd(divisor, modulus) != 1:
                        continue
                    receipt = geometric_majorant_energy(
                        modulus, shift_length, divisor)
                    self.assertLessEqual(receipt["energy"], receipt["bound"])
                    checked += 1
        self.assertGreater(checked, 2000)

    def test_exact_log_weighted_rows_fit_corollary(self):
        for arguments in ((32000, 457, 2, 5, 9),
                          (200000, 1361, 3, 7, 19)):
            receipt = exact_weighted_progression_energy(*arguments)
            self.assertLessEqual(receipt["energy"], receipt["bound"])
            self.assertFalse(receipt["cross_divisor_sum_proved"])

    def test_actual_average_retains_square_root_scale(self):
        receipt = averaged_near_cutoff_receipt(32000)
        self.assertLess(receipt["energy_over_square_root_scale"], 10)
        self.assertLess(receipt["energy_over_trivial_scale"], .02)
        self.assertFalse(receipt["cross_divisor_sum_proved"])


if __name__ == "__main__":
    unittest.main()
