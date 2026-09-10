import unittest

import numpy as np

from all_lag_frame_transfer_probe import (
    _weighted_geometric_ratio_gradient,
    all_lag_frame_transfer_probe,
)


class AllLagFrameTransferProbeTests(unittest.TestCase):
    def test_analytic_gradient_matches_complex_directional_difference(self):
        rows = {
            0: (1.2, np.array([[3.0, .4], [.4, 1.7]]),
                np.array([2.0, 1.1])),
            1: (1.2, np.array([[2.2, -.2], [-.2, 2.6]]),
                np.array([1.8, 1.4])),
            2: (1.2, np.array([[1.9, .3], [.3, 3.1]]),
                np.array([1.6, 1.7])),
        }
        edges = ((0, 1), (1, 2))
        coefficients = np.array([.7 + .2j, -.3 + .5j])
        direction = np.array([.1 - .4j, .6 + .2j])
        value, gradient = _weighted_geometric_ratio_gradient(
            rows, edges, coefficients)
        step = 1e-6
        plus = _weighted_geometric_ratio_gradient(
            rows, edges, coefficients + step * direction)[0]
        minus = _weighted_geometric_ratio_gradient(
            rows, edges, coefficients - step * direction)[0]
        finite_difference = (plus - minus) / (2 * step)
        analytic = float(np.real(np.vdot(gradient, direction)))
        self.assertGreater(value, 0)
        self.assertAlmostEqual(finite_difference, analytic, places=7)

    def test_probe_includes_adversarial_candidates_and_open_scope(self):
        receipt = all_lag_frame_transfer_probe(
            (101, 103), 3, 5, 6, 3, 14,
            ((1, 2), (3, 6)), random_trials=8, random_seed=7)
        self.assertGreaterEqual(receipt["candidate_count"], 16)
        self.assertEqual(len(receipt["lag_blocks"]), 2)
        for block in receipt["lag_blocks"]:
            self.assertGreater(
                block["minimum_tested_exact_over_frame_lag_budget"], 0)
            self.assertGreater(block["candidate_aggregate_exact_over_frame"], 0)
        self.assertFalse(receipt["weighted_all_lag_lower_frame_proved"])

    def test_seeded_probe_is_reproducible(self):
        arguments = ((101,), 3, 5, 5, 3, 12, ((1, 3),))
        first = all_lag_frame_transfer_probe(
            *arguments, random_trials=4, random_seed=19)
        second = all_lag_frame_transfer_probe(
            *arguments, random_trials=4, random_seed=19)
        self.assertEqual(first["lag_blocks"], second["lag_blocks"])

    def test_nonlinear_refinement_cannot_worsen_sampled_minimum(self):
        receipt = all_lag_frame_transfer_probe(
            (101, 103), 3, 5, 6, 3, 14, ((1, 3),),
            random_trials=4, random_seed=11, gradient_steps=12)
        block = receipt["lag_blocks"][0]
        self.assertLessEqual(
            block["minimum_tested_exact_over_frame_lag_budget"],
            block["minimum_sampled_exact_over_frame_lag_budget"] + 1e-12)
        self.assertGreaterEqual(block["nonlinear_improvement"], -1e-12)

    def test_invalid_lag_and_modulus_are_rejected(self):
        with self.assertRaises(ValueError):
            all_lag_frame_transfer_probe(
                (101,), 3, 5, 6, 3, 14, ((0, 2),), random_trials=0)
        with self.assertRaisesRegex(ValueError, "prime"):
            all_lag_frame_transfer_probe(
                (105,), 3, 5, 6, 3, 14, ((1, 2),), random_trials=0)


if __name__ == "__main__":
    unittest.main()
