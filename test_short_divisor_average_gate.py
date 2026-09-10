import unittest
from fractions import Fraction as F

from short_divisor_average_gate import (divisor_average_budget,
                                        favorable_burgess_deficit,
                                        r_continuous_derivative_numerator)


class ShortDivisorAverageTests(unittest.TestCase):
    def test_r2_is_the_best_licensed_prime_component_parameter(self):
        # E_r-H=A+B/r+C/r^2 has positive derivative for all r>=1,
        # hence the licensed integers r>=2 are minimized at r=2.
        for r in range(1, 65):
            self.assertGreater(r_continuous_derivative_numerator(F(r)), 0)

    def test_favorable_deficit_is_exact(self):
        self.assertEqual(favorable_burgess_deficit(), F(97, 1600))

    def test_square_root_d_average_is_far_too_small(self):
        b = divisor_average_budget()
        self.assertEqual(b["square_root_d_gain"], F(9, 2000))
        self.assertEqual(b["residual_after_square_root"], F(449, 8000))

    def test_even_complete_d_cancellation_does_not_close(self):
        b = divisor_average_budget()
        self.assertEqual(b["residual_after_complete_d_cancellation"], F(413, 8000))
        self.assertFalse(b["d_average_alone_closes"])


if __name__ == "__main__":
    unittest.main()
