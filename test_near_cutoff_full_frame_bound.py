import math
import unittest

import numpy as np

from divisor_active_full_gram import _full_collision_gram
from divisor_full_frame_probe import _totient
from near_cutoff_full_frame_bound import (
    entry_error_bound,
    near_cutoff_lower_frame_bound,
    row_lower_frame_bound,
)


class NearCutoffFullFrameBoundTests(unittest.TestCase):
    def test_entry_bound_dominates_exact_error(self):
        modulus, ell = 1009, 9
        divisors = (10, 11, 13, 14, 15)
        exact = _full_collision_gram(modulus, ell, divisors)
        logs = np.log(modulus * ell / np.array(divisors))
        ideal = np.array([
            [modulus ** 2 * logs[i] * logs[j]
             * (math.gcd(a, b) - 1) / (a * b)
             for j, b in enumerate(divisors)]
            for i, a in enumerate(divisors)])
        for i, left in enumerate(divisors):
            for j, right in enumerate(divisors):
                self.assertLessEqual(
                    abs(exact[i, j] - ideal[i, j]),
                    entry_error_bound(modulus, ell, left, right) + 1e-8)

    def test_row_bound_proves_loewner_coefficient(self):
        modulus, ell, divisor_left = 1009, 9, 8
        receipt = row_lower_frame_bound(modulus, ell, divisor_left)
        divisors = (10, 11, 13, 14, 15)
        exact = _full_collision_gram(modulus, ell, divisors)
        frame = np.array([
            modulus ** 2 * math.log(modulus * ell / a) ** 2
            * _totient(a) / a ** 2 for a in divisors])
        actual_min = np.linalg.eigvalsh(
            exact / np.sqrt(frame[:, None] * frame[None, :]))[0]
        self.assertGreaterEqual(
            actual_min + 1e-10, receipt["proved_frame_coefficient"])
        self.assertTrue(receipt["positive_lower_frame_proved"])

    def test_project_near_cutoff_range_is_certified(self):
        receipt = near_cutoff_lower_frame_bound(32000)
        self.assertTrue(receipt["uniform_positive_lower_frame_proved"])
        self.assertLess(receipt["uniform_normalized_error_schur_bound"], 1)


if __name__ == "__main__":
    unittest.main()
