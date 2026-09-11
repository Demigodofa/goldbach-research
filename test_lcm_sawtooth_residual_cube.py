import math
import unittest

from lcm_sawtooth_residual_cube import (
    residual_cube_identity,
    truncated_residual_cube,
)


class LcmSawtoothResidualCubeTests(unittest.TestCase):
    def test_three_state_cube_matches_closed_form(self):
        for primes in ((), (2,), (2, 3), (2, 3, 5, 7)):
            receipt = residual_cube_identity(12.0, 11.0, primes)
            self.assertLess(abs(receipt["identity_error"]), 2e-12)
            self.assertEqual(
                receipt["three_state_assignment_count"], 3 ** len(primes))
            self.assertTrue(
                receipt["complete_residual_cube_identity_proved"])
            self.assertFalse(receipt["boundary_truncated_cube_control_proved"])

    def test_closed_form_detects_sign_margin(self):
        positive = residual_cube_identity(12.0, 11.0, (2, 3, 5))
        negative = residual_cube_identity(1.0, 1.0, (5,))
        self.assertTrue(positive["closed_form_positive"])
        self.assertFalse(negative["closed_form_positive"])

    def test_rejects_repeated_residual_primes(self):
        with self.assertRaises(ValueError):
            residual_cube_identity(3.0, 4.0, (2, 2))

    def test_untruncated_range_reconstructs_complete_cube(self):
        X, left, right, primes = 1_000_000, 7, 11, (2, 3, 5)
        truncated = truncated_residual_cube(
            X, left, right, 0, 1000, primes)
        complete = residual_cube_identity(
            math.log(X / left), math.log(X / right), primes)
        self.assertEqual(truncated["retained_assignment_count"], 27)
        self.assertAlmostEqual(
            truncated["truncated_cube_sum"], complete["closed_form"])
        self.assertFalse(truncated["uniform_truncated_cube_positivity_proved"])


if __name__ == "__main__":
    unittest.main()
