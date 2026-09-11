import unittest

import numpy as np

from lcm_sawtooth_axial_moment_curve import (
    moment_curve_projective_fit,
    project_axial_moment_curve_receipt,
)


class LcmSawtoothAxialMomentCurveTests(unittest.TestCase):
    def test_exact_moment_curve_point_is_recovered(self):
        receipt = moment_curve_projective_fit(np.array((.09, .3, 1.0)))
        self.assertAlmostEqual(receipt["best_parameter"], .3)
        self.assertLess(receipt["projective_moment_curve_distance"], 2e-8)
        self.assertFalse(receipt["infinite_parameter_selected"])

    def test_infinite_curve_point_is_checked(self):
        receipt = moment_curve_projective_fit(np.array((1.0, 0.0, 0.0)))
        self.assertIsNone(receipt["best_parameter"])
        self.assertAlmostEqual(receipt["projective_moment_curve_distance"], 0)
        self.assertTrue(receipt["infinite_parameter_selected"])

    def test_m127_axis_is_on_effective_log_curve_not_actual_selector(self):
        receipt = project_axial_moment_curve_receipt(127)
        self.assertEqual(receipt["prime_count"], 24)
        self.assertAlmostEqual(receipt["best_parameter"], .2795716513419446)
        self.assertAlmostEqual(
            receipt["projective_moment_curve_distance"],
            4.166667001461609e-5)
        self.assertAlmostEqual(
            receipt["actual_selector_angle_degrees"], 60.912673267452014)
        self.assertLess(receipt["projective_moment_curve_distance"], .01)
        self.assertGreater(receipt["actual_selector_angle_degrees"], 15)
        self.assertTrue(
            receipt["moment_curve_selects_scaled_logarithm_proved"])
        self.assertFalse(receipt["uniform_moment_curve_alignment_proved"])
        self.assertFalse(receipt["effective_log_parameter_formula_proved"])
        self.assertFalse(receipt["uniform_active_full_lower_frame_proved"])
        self.assertFalse(receipt["signed_prime_correlation_proved"])

    def test_guards_invalid_vector(self):
        with self.assertRaises(ValueError):
            moment_curve_projective_fit(np.ones(2))
        with self.assertRaises(ValueError):
            moment_curve_projective_fit(np.zeros(3))


if __name__ == "__main__":
    unittest.main()
