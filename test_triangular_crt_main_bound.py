import unittest

from near_cutoff_geometric_bound import _active_modes
from triangular_crt_main_bound import (
    near_cutoff_triangular_main_bound,
    row_triangular_main_bound,
    triangular_kernel_sum_bound,
)
from triangular_crt_main_probe import (
    _triangular_kernel_fejer,
    triangular_crt_main_probe,
)


class TriangularCrtMainBoundTests(unittest.TestCase):
    def test_kernel_sum_bound_handles_both_gcd_ranges(self):
        modulus, shift_length = 1009, 5
        modes = _active_modes(modulus, shift_length)
        for gcd_value in (2, 5, 14):
            exact = sum(_triangular_kernel_fejer(
                modulus, gcd_value, mode).real for mode in modes)
            self.assertLessEqual(
                exact, triangular_kernel_sum_bound(
                    modulus, shift_length, gcd_value) + 1e-6)

    def test_schur_bound_dominates_exact_main(self):
        exact = triangular_crt_main_probe(1009, 5, 9, 1, 8)
        proved = row_triangular_main_bound(1009, 5, 8)
        self.assertLessEqual(
            exact["triangular_main_schur_row_sum"],
            proved["proved_triangular_main_schur_bound"])
        self.assertFalse(proved["discrepancy_theorem_proved"])

    def test_project_range_has_theorem_receipt(self):
        receipt = near_cutoff_triangular_main_bound(32000)
        self.assertTrue(receipt["triangular_main_N_epsilon_theorem"])

    def test_composite_modulus_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "prime"):
            row_triangular_main_bound(1001, 5, 8)


if __name__ == "__main__":
    unittest.main()
