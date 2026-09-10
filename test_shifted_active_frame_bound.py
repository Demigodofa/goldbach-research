import math
import unittest

from shifted_active_frame_bound import (
    row_shifted_active_frame_bound,
    shifted_pair_error_bound,
)


class ShiftedActiveFrameBoundTests(unittest.TestCase):
    def test_pair_error_bound_dominates_every_signed_separation(self):
        modulus, ell_left, ell_right, left, right = 101, 5, 8, 6, 10
        radius = modulus - 1
        left_log = math.log(modulus * ell_left / left)
        right_log = math.log(modulus * ell_right / right)
        common = math.lcm(left, right)
        delta = ell_right - ell_left
        bound = shifted_pair_error_bound(
            modulus, ell_left, ell_right, left, right)
        for separation in range(-radius + 1, radius):
            exact = 0.0
            for x in range(1, modulus):
                y = x - separation
                if (1 <= y < modulus
                        and (modulus * ell_left + x) % left == 0
                        and (modulus * ell_right + y) % right == 0):
                    exact += (
                        math.log((modulus * ell_left + x) / left)
                        * math.log((modulus * ell_right + y) / right))
            model = 0.0
            if (separation - modulus * delta) % math.gcd(left, right) == 0:
                model = ((radius - abs(separation))
                         * left_log * right_log / common)
            self.assertLessEqual(abs(exact - model), bound + 1e-12)

    def test_combined_bound_dominates_exact_shifted_operator(self):
        receipt = row_shifted_active_frame_bound(
            1009, 5, 9, 12, 8, compare_exact=True)
        self.assertLessEqual(
            receipt["exact_shifted_active_frame_operator_norm"],
            receipt["proved_shifted_active_frame_operator_bound"])
        self.assertTrue(receipt["shifted_pair_active_frame_theorem"])
        self.assertFalse(receipt["dyadic_lag_sum_proved"])

    def test_composite_modulus_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "prime"):
            row_shifted_active_frame_bound(1001, 5, 9, 12, 8)


if __name__ == "__main__":
    unittest.main()
