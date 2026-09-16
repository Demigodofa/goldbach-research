import unittest

import numpy as np

from mobius_moment_square_nullspace import (
    moment_square_projective_fit,
    moment_square_vector,
    symmetric_matrix_rank_shape,
)
from tools.build_mobius_moment_square_nullspace_audit import build_receipt


class MobiusMomentSquareNullspaceAuditTests(unittest.TestCase):
    def test_exact_moment_square_vector_is_recovered(self):
        vector = moment_square_vector(.25)
        receipt = moment_square_projective_fit(vector)
        self.assertAlmostEqual(receipt["best_parameter"], .25)
        self.assertLess(receipt["projective_moment_square_distance"], 1e-12)
        self.assertFalse(receipt["infinite_parameter_selected"])

    def test_rank_one_shape_detects_symmetric_square(self):
        shape = symmetric_matrix_rank_shape(moment_square_vector(.2))
        self.assertTrue(shape["nearly_rank_one_positive_semidefinite"])
        self.assertLess(abs(shape["second_over_largest_eigenvalue"]), 1e-12)

    def test_m167_null_direction_is_near_moment_square(self):
        receipt = build_receipt()
        self.assertEqual(
            receipt["status"],
            "TARGET_moment_square_nullspace_support_activation")
        self.assertEqual(receipt["scale_modulus"], 167)
        self.assertAlmostEqual(
            receipt["best_parameter"], 0.26688993201398403)
        self.assertLess(
            receipt["projective_moment_square_distance"], 6e-5)
        self.assertGreater(
            receipt["projective_moment_square_correlation"],
            0.99999999)
        self.assertTrue(
            receipt["nearly_rank_one_positive_semidefinite"])
        self.assertLess(
            receipt["second_over_largest_eigenvalue"], 5e-5)
        self.assertAlmostEqual(
            receipt["active_positive_null_coupling_norm"],
            3.44675405351299e-08)
        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["uniform_active_full_lower_frame_proved"])

    def test_guards_invalid_fit_vector(self):
        with self.assertRaises(ValueError):
            moment_square_projective_fit(np.ones(5))
        with self.assertRaises(ValueError):
            moment_square_projective_fit(np.zeros(6))


if __name__ == "__main__":
    unittest.main()
