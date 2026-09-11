import unittest

import numpy as np

from lcm_sawtooth_trace_traceless_block_frame import (
    project_trace_traceless_block_receipt,
    trace_traceless_transform,
    two_block_gershgorin_receipt,
)


class LcmSawtoothTraceTracelessBlockFrameTests(unittest.TestCase):
    def test_trace_traceless_basis_is_orthonormal_and_correctly_split(self):
        transform = trace_traceless_transform()
        np.testing.assert_allclose(
            transform.T @ transform, np.eye(6), atol=1e-15)
        traces = transform[0] + transform[3] + transform[5]
        self.assertGreater(abs(traces[0]), 0)
        np.testing.assert_allclose(traces[1:], np.zeros(5), atol=1e-15)

    def test_two_block_diagonal_fixture_is_exact(self):
        matrix = np.diag((2.0, 3.0, 5.0))
        receipt = two_block_gershgorin_receipt(matrix, 1)
        self.assertAlmostEqual(
            receipt["left_block_smallest_eigenvalue"], 2.0)
        self.assertAlmostEqual(
            receipt["right_block_smallest_eigenvalue"], 3.0)
        self.assertAlmostEqual(receipt["cross_block_operator_norm"], 0.0)
        self.assertAlmostEqual(
            receipt["two_block_gershgorin_lower_bound"], 2.0)
        self.assertTrue(
            receipt["two_block_positive_semidefinite_certified"])

    def test_m127_trace_traceless_block_bound_fails_but_matrix_is_positive(self):
        receipt = project_trace_traceless_block_receipt(127)
        self.assertEqual(receipt["prime_count"], 24)
        self.assertAlmostEqual(
            receipt["left_block_smallest_eigenvalue"], .471397947622108)
        self.assertAlmostEqual(
            receipt["right_block_smallest_eigenvalue"], .013920013451368894)
        self.assertAlmostEqual(
            receipt["cross_block_operator_norm"], .5729586673404257)
        self.assertAlmostEqual(
            receipt["two_block_gershgorin_lower_bound"],
            -.5590386538890568)
        self.assertFalse(
            receipt["two_block_positive_semidefinite_certified"])
        self.assertGreater(receipt["trace_schur_complement"], 3.8e-4)
        self.assertGreater(
            receipt["exact_scaled_difference_smallest_eigenvalue"], 1.5e-4)
        self.assertFalse(
            receipt["uniform_trace_traceless_interaction_bound_proved"])
        self.assertFalse(receipt["uniform_active_full_lower_frame_proved"])
        self.assertFalse(receipt["signed_prime_correlation_proved"])

    def test_guards_invalid_split(self):
        with self.assertRaises(ValueError):
            two_block_gershgorin_receipt(np.eye(3), 0)
        with self.assertRaises(ValueError):
            two_block_gershgorin_receipt(np.eye(3), 3)
        with self.assertRaises(ValueError):
            two_block_gershgorin_receipt(np.ones((2, 3)), 1)


if __name__ == "__main__":
    unittest.main()
