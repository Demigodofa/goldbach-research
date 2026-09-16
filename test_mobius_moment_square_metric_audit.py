import unittest

import numpy as np

from mobius_moment_square_metric import (
    diagonal_equilibration_metric,
    moment_square_quadratic_quotient_minimum,
)
from mobius_moment_square_nullspace import moment_square_vector
from tools.build_mobius_moment_square_metric_audit import build_receipt


class MobiusMomentSquareMetricAuditTests(unittest.TestCase):
    def test_exact_diagonal_quadratic_minimum_is_recovered(self):
        target = .3
        curve = moment_square_vector(target)
        projector = np.eye(6) - np.outer(curve, curve) / float(curve @ curve)
        receipt = moment_square_quadratic_quotient_minimum(
            projector, np.eye(6))
        self.assertAlmostEqual(receipt["minimizing_parameter"], target)
        self.assertLess(receipt["minimum_value"], 1e-15)

    def test_diagonal_equilibration_metric_records_full_diagonal(self):
        full = np.diag((4.0, 9.0, 16.0, 25.0, 36.0, 49.0))
        metric, scale = diagonal_equilibration_metric(full)
        np.testing.assert_allclose(np.diag(metric), np.diag(full))
        np.testing.assert_allclose(scale, np.diag(full) ** -.5)

    def test_checked_scales_have_equilibrated_soft_direction(self):
        receipt = build_receipt()
        self.assertEqual(
            receipt["status"],
            "TARGET_metric_aware_moment_square_soft_direction")
        self.assertLess(
            receipt["maximum_equilibrated_moment_square_minimum"], 7e-11)
        self.assertGreater(
            receipt["minimum_raw_moment_square_minimum"], .9)
        self.assertLess(
            receipt["maximum_equilibrated_over_raw_minimum"], 1e-10)
        rows = {
            row["scale_modulus"]: row for row in receipt["scale_results"]}
        self.assertAlmostEqual(
            rows[167]["raw_moment_square_minimum"],
            0.9381026269590562)
        self.assertAlmostEqual(
            rows[167]["equilibrated_moment_square_minimum"],
            3.2957447749809375e-12)
        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["uniform_active_full_lower_frame_proved"])

    def test_guards_matrix_shape(self):
        with self.assertRaises(ValueError):
            moment_square_quadratic_quotient_minimum(np.eye(5), np.eye(5))
        with self.assertRaises(ValueError):
            diagonal_equilibration_metric(np.eye(5))


if __name__ == "__main__":
    unittest.main()
