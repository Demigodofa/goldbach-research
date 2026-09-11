import unittest

import numpy as np

from lcm_sawtooth_lifted_endpoint_frame import (
    lifted_endpoint_residue_gram_receipt,
)
from lcm_sawtooth_rank_one_lower_frame import (
    _lifted_symmetric_matrix,
    _projective_rank_one_distance,
    _rank_one_lifts,
    rank_one_lower_frame_receipt,
)


class LcmSawtoothRankOneLowerFrameTests(unittest.TestCase):
    def test_lift_is_symmetric_rank_one_matrix(self):
        parameter = np.array((2.0, -3.0, 5.0))
        lift = _rank_one_lifts(parameter[None, :])[0]
        np.testing.assert_allclose(
            _lifted_symmetric_matrix(lift),
            np.outer(parameter, parameter))
        distance, _ = _projective_rank_one_distance(lift)
        self.assertAlmostEqual(distance, 0.0)
        distance, _ = _projective_rank_one_distance(-lift)
        self.assertAlmostEqual(distance, 0.0)

    def test_m151_relaxation_is_nearly_rank_one(self):
        receipt = rank_one_lower_frame_receipt(
            151, 28, 42, 3, 13, grid_size=100000)
        self.assertAlmostEqual(receipt["relaxed_minimum"], .5208139495)
        self.assertAlmostEqual(
            receipt["refined_minimum"], .521176, places=5)
        self.assertLess(
            receipt["projective_rank_one_frobenius_distance"], .15)
        self.assertLess(receipt["rank_one_over_relaxed_minimum"], 1.001)
        self.assertAlmostEqual(
            receipt["actual_selector_active_over_full"],
            .8591107437)
        base = lifted_endpoint_residue_gram_receipt(151, 28, 42, 3, 13)
        active = np.asarray(base["active_window_residue_energy_gram"])
        full = np.asarray(base["full_residue_energy_gram"])
        relaxed = np.asarray(receipt["relaxed_minimizer"])
        self.assertAlmostEqual(
            float(relaxed @ active @ relaxed)
            / float(relaxed @ full @ relaxed),
            receipt["relaxed_minimum"])
        parameter = np.asarray(receipt["minimizing_parameter"])
        lift = _rank_one_lifts(parameter[None, :])[0]
        self.assertAlmostEqual(
            float(lift @ active @ lift) / float(lift @ full @ lift),
            receipt["refined_minimum"])
        self.assertFalse(receipt["rank_one_global_minimum_proved"])
        self.assertFalse(receipt["uniform_lower_frame_proved"])


if __name__ == "__main__":
    unittest.main()
