import unittest

import numpy as np

from lcm_sawtooth_arithmetic_covariance_basis import (
    covariance_inverse_root,
    diagonally_equilibrated_spectrum,
    project_arithmetic_covariance_basis_receipt,
    weighted_coordinate_covariance,
)


class LcmSawtoothArithmeticCovarianceBasisTests(unittest.TestCase):
    def test_weighted_covariance_is_the_direct_quadratic_energy(self):
        coordinates = np.array(((1.0, 2.0, -1.0), (3.0, 0.0, 4.0)))
        weights = np.array((2.0, 5.0))
        covariance = weighted_coordinate_covariance(coordinates, weights)
        parameter = np.array((2.0, -3.0, 5.0))
        self.assertAlmostEqual(
            float(parameter @ covariance @ parameter),
            float(np.sum(weights * (coordinates @ parameter) ** 2)))

    def test_inverse_root_whitens_positive_definite_covariance(self):
        covariance = np.array(((5.0, 2.0), (2.0, 2.0)))
        transform, values = covariance_inverse_root(covariance)
        self.assertTrue(np.all(values > 0))
        np.testing.assert_allclose(
            transform.T @ covariance @ transform, np.eye(2), atol=1e-14)

    def test_m127_arithmetic_covariance_improves_but_does_not_certify(self):
        receipt = project_arithmetic_covariance_basis_receipt(127)
        self.assertEqual(receipt["prime_count"], 24)
        np.testing.assert_allclose(
            receipt["one_frequency_covariance_eigenvalues"],
            (3.48869376, 3598.63876, 1381803.33), rtol=2e-8)
        self.assertLess(receipt["covariance_whitening_max_error"], 3e-12)
        self.assertAlmostEqual(
            receipt["scaled_difference_gershgorin_lower_edge"],
            -.6764623181509886)
        self.assertGreater(
            receipt["scaled_difference_gershgorin_lower_edge"],
            receipt["raw_basis_gershgorin_lower_edge"])
        self.assertAlmostEqual(
            receipt["exact_smallest_generalized_eigenvalue"],
            .8768802946823542)
        self.assertGreater(
            receipt["raw_diagonally_equilibrated_full_condition_number"],
            5e11)
        self.assertLess(
            receipt[
                "arithmetic_diagonally_equilibrated_full_condition_number"],
            6000)
        self.assertGreater(
            receipt["raw_diagonally_equilibrated_full_condition_number"]
            / receipt[
                "arithmetic_diagonally_equilibrated_full_condition_number"],
            9e7)
        self.assertFalse(
            receipt["coordinate_scaled_gershgorin_certifies_candidate"])
        self.assertFalse(
            receipt["uniform_covariance_basis_comparison_proved"])
        self.assertFalse(receipt["signed_prime_correlation_proved"])

    def test_guards_invalid_covariances(self):
        with self.assertRaises(ValueError):
            weighted_coordinate_covariance(np.eye(2), np.ones(3))
        with self.assertRaises(ValueError):
            weighted_coordinate_covariance(np.eye(2), np.array((1.0, -1.0)))
        with self.assertRaises(ValueError):
            covariance_inverse_root(np.ones((2, 3)))
        with self.assertRaises(ValueError):
            covariance_inverse_root(np.ones((2, 2)))
        with self.assertRaises(ValueError):
            diagonally_equilibrated_spectrum(np.ones((2, 3)))
        with self.assertRaises(ValueError):
            diagonally_equilibrated_spectrum(np.array(((1.0, 0.0),
                                                       (0.0, 0.0))))


if __name__ == "__main__":
    unittest.main()
