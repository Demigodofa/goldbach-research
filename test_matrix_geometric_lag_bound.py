import unittest

import numpy as np

from matrix_geometric_lag_bound import (
    matrix_geometric_lag_probe,
    matrix_geometric_mean,
)


class MatrixGeometricLagBoundTests(unittest.TestCase):
    def test_geometric_mean_minorizes_scalar_geometric_energy(self):
        left_factor = np.array([[2.0, .3], [.4, 1.1]])
        right_factor = np.array([[1.2, -.2], [.7, 1.6]])
        left = left_factor.T @ left_factor
        right = right_factor.T @ right_factor
        geometric = matrix_geometric_mean(left, right)
        for vector in (
                np.array([.7, -.2]),
                np.array([.3 + .4j, -.8 + .1j])):
            lower = float(np.real(np.vdot(vector, geometric @ vector)))
            left_energy = float(np.real(np.vdot(vector, left @ vector)))
            right_energy = float(np.real(np.vdot(vector, right @ vector)))
            self.assertLessEqual(
                lower, np.sqrt(left_energy * right_energy) + 1e-12)

    def test_commuting_diagonal_case_is_entrywise_geometric_mean(self):
        left = np.diag([1.0, 4.0, 9.0])
        right = np.diag([16.0, 25.0, 36.0])
        self.assertTrue(np.allclose(
            matrix_geometric_mean(left, right),
            np.diag([4.0, 10.0, 18.0])))

    def test_finite_probe_returns_direct_lower_operator(self):
        receipt = matrix_geometric_lag_probe(
            (101, 103), 3, 5, 6, 3, 14, ((1, 2), (3, 6)),
            linearization_step=1e-4)
        self.assertTrue(
            receipt["matrix_geometric_scalar_minorization_proved"])
        self.assertFalse(receipt["asymptotic_all_lag_lower_frame_proved"])
        self.assertGreater(receipt["minimum_input_gram_eigenvalue"], 0)
        self.assertGreater(
            receipt["minimum_ideal_input_gram_eigenvalue"], 0)
        self.assertGreater(
            receipt["minimum_exact_single_row_over_frame"], 0)
        self.assertGreater(
            receipt["minimum_ideal_single_row_over_frame"], 0)
        self.assertEqual(len(receipt["minimum_exact_single_row_label"]), 2)
        self.assertGreater(
            receipt["exact_over_ideal_single_row_minimum_ratio"], 0)
        for block in receipt["lag_blocks"]:
            self.assertGreater(
                block[
                    "matrix_geometric_over_arithmetic_frame_minimum"], 0)
            self.assertTrue(
                block["measured_positive_generalized_eigenvalue"])
            self.assertGreater(
                block[
                    "ideal_matrix_geometric_over_arithmetic_frame_minimum"],
                0)
            self.assertGreater(
                block["exact_over_ideal_matrix_geometric_minimum_ratio"], 0)
            self.assertGreaterEqual(
                block["exact_minus_ideal_normalized_operator_norm"], 0)
            self.assertLessEqual(
                block["weyl_lower_certificate_from_ideal_and_difference"],
                block[
                    "matrix_geometric_over_arithmetic_frame_minimum"]
                + 1e-12)
            self.assertGreaterEqual(
                block["linearized_difference_normalized_operator_norm"], 0)
            self.assertGreaterEqual(
                block["nonlinear_remainder_normalized_operator_norm"], 0)

    def test_invalid_input_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "prime"):
            matrix_geometric_lag_probe(
                (105,), 3, 5, 6, 3, 14, ((1, 2),))
        with self.assertRaises(ValueError):
            matrix_geometric_mean(np.eye(2), np.eye(3))
        with self.assertRaises(ValueError):
            matrix_geometric_lag_probe(
                (101,), 3, 5, 6, 3, 14, ((1, 2),),
                linearization_step=-.1)


if __name__ == "__main__":
    unittest.main()
