import unittest

import numpy as np

from lcm_sawtooth_axial_invariant import (
    axial_distance_from_determinant,
    normalized_traceless_determinant,
    project_axial_invariant_receipt,
)


class LcmSawtoothAxialInvariantTests(unittest.TestCase):
    def test_extreme_traceless_spectra(self):
        axial = axial_distance_from_determinant(
            np.diag((2.0, -1.0, -1.0)))
        self.assertAlmostEqual(axial["normalized_absolute_determinant"], 1.0)
        self.assertAlmostEqual(axial["determinant_axial_distance"], 0.0)
        middle = axial_distance_from_determinant(
            np.diag((1.0, 0.0, -1.0)))
        self.assertAlmostEqual(middle["normalized_absolute_determinant"], 0.0)
        self.assertAlmostEqual(middle["determinant_axial_distance"], .5)

    def test_formula_matches_spectral_distance_after_rotation(self):
        eigenvalues = np.diag((1.8, -.7, -1.1))
        rotation, _ = np.linalg.qr(np.array((
            (1.0, 2.0, 3.0), (4.0, 1.0, -2.0), (2.0, -3.0, 1.0))))
        receipt = axial_distance_from_determinant(
            rotation.T @ eigenvalues @ rotation)
        self.assertLess(receipt["distance_identity_absolute_error"], 1e-14)
        self.assertTrue(
            receipt["traceless_axial_determinant_identity_proved"])

    def test_m127_response_has_near_extremal_determinant(self):
        receipt = project_axial_invariant_receipt(127)
        self.assertEqual(receipt["prime_count"], 24)
        self.assertAlmostEqual(
            receipt["normalized_absolute_determinant"],
            .9992599265347049)
        self.assertAlmostEqual(
            receipt["determinant_axial_distance"],
            .01282466536678671)
        self.assertLess(receipt["distance_identity_absolute_error"], 2e-14)
        self.assertFalse(receipt["uniform_determinant_lower_bound_proved"])
        self.assertFalse(receipt["uniform_active_full_lower_frame_proved"])
        self.assertFalse(receipt["signed_prime_correlation_proved"])

    def test_guards_invalid_matrices(self):
        with self.assertRaises(ValueError):
            normalized_traceless_determinant(np.eye(2))
        with self.assertRaises(ValueError):
            normalized_traceless_determinant(np.zeros((3, 3)))
        with self.assertRaises(ValueError):
            normalized_traceless_determinant(np.eye(3))
        with self.assertRaises(ValueError):
            normalized_traceless_determinant(np.array(
                ((1.0, 1.0, 0.0), (0.0, -1.0, 0.0), (0.0, 0.0, 0.0))))


if __name__ == "__main__":
    unittest.main()
