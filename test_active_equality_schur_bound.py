import math
import unittest

import numpy as np

from active_cross_component_probe import _row_components
from active_equality_schur_bound import (
    near_cutoff_equality_schur_bound,
    row_equality_schur_bound,
)
from divisor_full_frame_probe import _totient
from near_cutoff_geometric_bound import _active_modes


class ActiveEqualitySchurBoundTests(unittest.TestCase):
    def test_bound_dominates_exact_equality_row_sum(self):
        modulus, shift_length, ell, divisor_left = 1009, 5, 9, 8
        divisors = (10, 11, 13, 14, 15)
        equality, _, _, _ = _row_components(
            modulus, shift_length, ell, divisors)
        rho = len(_active_modes(modulus, shift_length)) / (modulus - 1)
        frame = np.array([
            rho * modulus ** 2 * math.log(modulus * ell / a) ** 2
            * _totient(a) / a ** 2 for a in divisors])
        normalized = ((1 - rho) * equality
                      / np.sqrt(frame[:, None] * frame[None, :]))
        exact_schur = float(np.max(np.sum(np.abs(normalized), axis=1)))
        receipt = row_equality_schur_bound(
            modulus, shift_length, ell, divisor_left)
        self.assertGreaterEqual(
            receipt["proved_equality_schur_bound"] + 1e-12, exact_schur)
        self.assertFalse(receipt["unequal_component_proved"])

    def test_project_range_receipt(self):
        receipt = near_cutoff_equality_schur_bound(32000)
        self.assertTrue(receipt["equality_component_N_epsilon_theorem"])
        self.assertGreater(receipt["uniform_proved_equality_schur_bound"], 0)


if __name__ == "__main__":
    unittest.main()
