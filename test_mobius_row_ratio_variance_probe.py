import math
import unittest

import numpy as np

from divisor_active_full_gram import _full_collision_gram
from divisor_full_frame_probe import _totient
from mobius_covariance_lag_probe import _mobius_values
from mobius_row_ratio_variance_probe import (
    mobius_row_ratio_components,
    mobius_row_ratio_lag_graph_probe,
    mobius_row_ratio_variance_probe,
)
from near_cutoff_geometric_bound import _active_modes


class MobiusRowRatioVarianceTests(unittest.TestCase):
    def test_scalar_exact_ratio_matches_full_collision_matrix(self):
        modulus, ell, lower, upper = 101, 4, 3, 14
        receipt = mobius_row_ratio_components(
            modulus, ell, 2, lower, upper)
        mobius = _mobius_values(upper)
        divisors = tuple(a for a in range(lower + 1, upper + 1)
                         if mobius[a])
        coefficients = np.array([mobius[a] for a in divisors], dtype=float)
        matrix_value = float(
            coefficients @ _full_collision_gram(modulus, ell, divisors)
            @ coefficients)
        frame_value = modulus ** 2 * sum(
            _totient(a) * math.log(modulus * ell / a) ** 2 / a ** 2
            for a in divisors)
        rho = len(_active_modes(modulus, 2)) / (modulus - 1)
        recovered_frame = (receipt["vertex_weight"]
                           / (rho * modulus * math.log(modulus) ** 2)
                           * modulus ** 2)
        self.assertAlmostEqual(
            receipt["exact_row_ratio"],
            matrix_value / recovered_frame, places=11)
        self.assertAlmostEqual(recovered_frame, frame_value, places=11)

    def test_component_identity_and_weighted_variance(self):
        cell = mobius_row_ratio_components(101, 4, 2, 3, 14)
        self.assertAlmostEqual(cell["component_identity_error"], 0)
        self.assertGreaterEqual(cell["exact_row_ratio"], -1e-12)
        receipt = mobius_row_ratio_variance_probe(
            (101, 103), 2, 4, 2, 3, 14)
        self.assertEqual(receipt["cell_count"], 4)
        self.assertGreaterEqual(receipt["frame_weighted_exact_variance"], 0)
        self.assertFalse(receipt["mobius_row_ratio_variance_bound_proved"])

    def test_empty_active_band_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "nonempty active band"):
            mobius_row_ratio_components(101, 4, 100, 3, 14)
        with self.assertRaisesRegex(ValueError, "integer at least two"):
            mobius_row_ratio_components(101, 4, 0, 3, 14)
        with self.assertRaisesRegex(ValueError, "integer at least two"):
            mobius_row_ratio_components(101, 4, 2.5, 3, 14)

    def test_finite_lag_graph_certificate_uses_exact_rows(self):
        receipt = mobius_row_ratio_lag_graph_probe(
            (101, 103), 2, 4, 4, 3, 14, 2, 4)
        self.assertEqual(receipt["cell_count"], 8)
        self.assertEqual(receipt["edge_count"], 6)
        self.assertTrue(receipt["inequality_verified_numerically"])
        self.assertLessEqual(
            receipt["finite_fixed_mobius_lag_certificate"],
            receipt["weighted_edge_geometric_mean"] + 1e-12)
        self.assertFalse(
            receipt["asymptotic_fixed_mobius_lag_frame_proved"])
if __name__ == "__main__":
    unittest.main()
