import unittest

import numpy as np

from lcm_sawtooth_axial_schur_response import (
    project_axial_schur_response_receipt,
    projective_axial_distance,
)


class LcmSawtoothAxialSchurResponseTests(unittest.TestCase):
    def test_axial_distance_detects_exact_and_nonaxial_tensors(self):
        exact = projective_axial_distance(np.diag((2.0, -1.0, -1.0)))
        self.assertAlmostEqual(
            exact["projective_axial_frobenius_distance"], 0.0)
        nonaxial = projective_axial_distance(np.diag((1.0, 0.0, -1.0)))
        self.assertGreater(
            nonaxial["projective_axial_frobenius_distance"], .49)

    def test_axial_distance_is_rotation_invariant(self):
        matrix = np.diag((1.8, -.7, -1.1))
        rotation, _ = np.linalg.qr(np.array((
            (1.0, 2.0, 3.0), (4.0, 1.0, -2.0), (2.0, -3.0, 1.0))))
        first = projective_axial_distance(matrix)
        second = projective_axial_distance(rotation.T @ matrix @ rotation)
        self.assertAlmostEqual(
            first["projective_axial_frobenius_distance"],
            second["projective_axial_frobenius_distance"])

    def test_m127_schur_response_is_nearly_axial(self):
        receipt = project_axial_schur_response_receipt(127)
        self.assertEqual(receipt["prime_count"], 24)
        np.testing.assert_allclose(
            receipt["tensor_eigenvalues"],
            (-.56586236, -.54126770, 1.10713006), rtol=2e-8)
        self.assertAlmostEqual(
            receipt["projective_axial_frobenius_distance"],
            .01282466536678671)
        self.assertLess(
            receipt["projective_axial_frobenius_distance"], .1)
        self.assertFalse(receipt["uniform_axial_schur_response_proved"])
        self.assertFalse(
            receipt["axial_reduction_preserves_lower_frame_proved"])
        self.assertFalse(receipt["signed_prime_correlation_proved"])

    def test_guards_invalid_tensor(self):
        with self.assertRaises(ValueError):
            projective_axial_distance(np.eye(2))
        with self.assertRaises(ValueError):
            projective_axial_distance(np.zeros((3, 3)))
        with self.assertRaises(ValueError):
            projective_axial_distance(np.eye(3))


if __name__ == "__main__":
    unittest.main()
