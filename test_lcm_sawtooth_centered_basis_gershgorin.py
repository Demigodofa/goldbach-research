import math
import unittest

import numpy as np

from lcm_sawtooth_centered_basis_gershgorin import (
    centered_degree_parameter_transform,
    project_centered_basis_gershgorin_receipt,
    symmetric_square_transform,
)


def _lift(parameter):
    first, second, third = parameter
    return np.array((
        first ** 2, first * second, first * third,
        second ** 2, second * third, third ** 2,
    ))


class LcmSawtoothCenteredBasisGershgorinTests(unittest.TestCase):
    def test_coefficient_transform_matches_centered_polynomial(self):
        center = 7.25
        scale = .4
        centered = np.array((2.0, -3.0, 5.0))
        original = centered_degree_parameter_transform(
            center, scale) @ centered
        for logarithm in (-2.0, center, 11.0):
            shifted = (logarithm - center) / scale
            self.assertAlmostEqual(
                centered @ np.array((shifted ** 2, shifted, 1.0)),
                original @ np.array((logarithm ** 2, logarithm, 1.0)))

    def test_symmetric_square_transform_is_covariant(self):
        transform = centered_degree_parameter_transform(8.0, .5)
        parameter = np.array((2.0, -3.0, 5.0))
        np.testing.assert_allclose(
            _lift(transform @ parameter),
            symmetric_square_transform(transform) @ _lift(parameter))

    def test_m127_centered_basis_does_not_certify_one_half(self):
        receipt = project_centered_basis_gershgorin_receipt(127)
        self.assertEqual(receipt["prime_count"], 24)
        self.assertAlmostEqual(
            receipt["center"], math.log(math.sqrt(2) * 127 * 42))
        self.assertAlmostEqual(receipt["scale"], math.log(2) / 2)
        self.assertAlmostEqual(
            receipt["scaled_difference_gershgorin_lower_edge"],
            -1.8664440043442379)
        self.assertLess(
            receipt["scaled_difference_gershgorin_lower_edge"],
            receipt["raw_basis_gershgorin_lower_edge"])
        self.assertAlmostEqual(
            receipt["exact_smallest_generalized_eigenvalue"],
            .8768802946823542)
        self.assertFalse(
            receipt["coordinate_scaled_gershgorin_certifies_candidate"])
        self.assertFalse(
            receipt["uniform_centered_basis_certificate_proved"])
        self.assertFalse(receipt["signed_prime_correlation_proved"])

    def test_guards_invalid_transform_inputs(self):
        with self.assertRaises(ValueError):
            centered_degree_parameter_transform(0.0, 0.0)
        with self.assertRaises(ValueError):
            centered_degree_parameter_transform(float("nan"), 1.0)
        with self.assertRaises(ValueError):
            symmetric_square_transform(np.eye(2))


if __name__ == "__main__":
    unittest.main()
