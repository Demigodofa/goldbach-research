import unittest

import numpy as np

from crt_pair_discrepancy_bound import (
    dirichlet_residue_l1_bound,
    near_cutoff_crt_discrepancy_bound,
    row_crt_discrepancy_bound,
)
from near_cutoff_geometric_bound import _active_modes
from triangular_crt_main_probe import triangular_crt_main_probe


class CrtPairDiscrepancyBoundTests(unittest.TestCase):
    def test_dirichlet_l1_bound_dominates_exact_kernel(self):
        modulus, shift_length = 1009, 5
        indicator = np.zeros(modulus)
        indicator[list(_active_modes(modulus, shift_length))] = 1
        exact = float(np.sum(np.abs(np.fft.fft(indicator))))
        self.assertLessEqual(exact, dirichlet_residue_l1_bound(modulus))

    def test_schur_bound_dominates_exact_remainder(self):
        exact = triangular_crt_main_probe(1009, 5, 9, 1, 8)
        proved = row_crt_discrepancy_bound(1009, 5, 9, 8)
        self.assertLessEqual(
            exact["remainder_schur_row_sum"],
            proved["proved_discrepancy_schur_bound"])
        self.assertFalse(proved["centering_theorem_proved"])

    def test_project_range_has_theorem_receipt(self):
        receipt = near_cutoff_crt_discrepancy_bound(32000)
        self.assertTrue(receipt["crt_discrepancy_o_one_theorem"])


if __name__ == "__main__":
    unittest.main()
