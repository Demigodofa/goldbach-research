import unittest

import numpy as np

from lcm_sawtooth_axial_schur_energy import (
    best_axial_approximation,
    project_axial_schur_energy_receipt,
    symmetric_matrix_coordinates,
)


class LcmSawtoothAxialSchurEnergyTests(unittest.TestCase):
    def test_exact_axial_tensor_is_unchanged(self):
        tensor = np.diag((2.0, -1.0, -1.0))
        approximation, _, axial = best_axial_approximation(tensor)
        np.testing.assert_allclose(approximation, tensor)
        self.assertAlmostEqual(
            axial["projective_axial_frobenius_distance"], 0.0)
        np.testing.assert_allclose(
            symmetric_matrix_coordinates(tensor),
            (2.0, 0.0, 0.0, -1.0, 0.0, -1.0))

    def test_m127_axial_error_is_below_but_comparable_to_margin(self):
        receipt = project_axial_schur_energy_receipt(127)
        self.assertEqual(receipt["prime_count"], 24)
        self.assertAlmostEqual(
            receipt["schur_response_projective_axial_distance"],
            .01282466536678671)
        self.assertAlmostEqual(receipt["schur_margin"], .005795730853614067)
        self.assertAlmostEqual(
            receipt["nonaxial_energy_error"], .005427450063227847)
        self.assertAlmostEqual(
            receipt["nonaxial_error_over_schur_margin"],
            .9364565402210543)
        self.assertAlmostEqual(
            receipt["nonaxial_error_over_axial_trial_value"],
            .4835928515669702)
        self.assertLess(receipt["completion_identity_absolute_error"], 1e-12)
        self.assertLess(receipt["nonaxial_error_over_schur_margin"], 1.0)
        self.assertFalse(receipt["uniform_axial_trial_lower_bound_proved"])
        self.assertFalse(receipt["uniform_nonaxial_energy_bound_proved"])
        self.assertFalse(receipt["uniform_active_full_lower_frame_proved"])
        self.assertFalse(receipt["signed_prime_correlation_proved"])

    def test_guards_coordinate_shape(self):
        with self.assertRaises(ValueError):
            symmetric_matrix_coordinates(np.eye(2))


if __name__ == "__main__":
    unittest.main()
