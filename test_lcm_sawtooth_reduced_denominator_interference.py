import unittest

from lcm_sawtooth_reduced_denominator_interference import (
    _require_no_mixed_high_q_packet,
    classify_shared_prime_denominator_mass,
    project_reduced_denominator_interference_receipt,
    shared_prime_high_q_support_obstruction,
)


class ReducedDenominatorInterferenceTests(unittest.TestCase):
    def test_mass_classifier_uses_absolute_contributions(self):
        rows = (
            {"reduced_denominator": 22,
             "off_diagonal_window_interference": 3.0},
            {"reduced_denominator": 35,
             "off_diagonal_window_interference": -1.0},
        )
        receipt = classify_shared_prime_denominator_mass(rows, 11, .75)
        self.assertEqual(receipt["absolute_off_diagonal_mass"], 4.0)
        self.assertEqual(receipt["shared_prime_absolute_mass_fraction"], .75)
        self.assertTrue(receipt[
            "shared_prime_denominator_mass_hypothesis_passes"])

    def test_actual_support_forces_shared_prime_on_high_q_packets(self):
        receipt = shared_prime_high_q_support_obstruction(
            127, 28, 3, 13, (77, 143), 11)
        self.assertEqual(receipt["maximum_nonshared_q_upper_bound"], 910)
        self.assertEqual(receipt["high_q_threshold"], 3556)
        self.assertTrue(receipt[
            "every_high_q_single_packet_denominator_has_shared_prime_proved"])

    def test_project_fixture_localizes_all_nonzero_mass(self):
        receipt = project_reduced_denominator_interference_receipt(127)
        self.assertEqual(receipt["prime_count"], 24)
        self.assertEqual(receipt["mixed_packet_high_q_pair_count"], 0)
        self.assertEqual(
            receipt["nonshared_single_packet_high_q_pair_count"], 0)
        self.assertEqual(
            receipt["nonzero_off_diagonal_denominators"],
            (5005, 6006, 10010))
        self.assertEqual(receipt["positive_nonzero_denominator_count"], 3)
        self.assertAlmostEqual(
            receipt["shared_prime_absolute_mass_fraction"], 1.0, places=12)
        self.assertAlmostEqual(
            receipt["active_window_boolean_cross_rayleigh"],
            .9755090695006173, places=8)
        self.assertAlmostEqual(
            receipt["full_residue_boolean_cross_rayleigh"],
            -.2370206674454969, places=8)
        self.assertAlmostEqual(
            receipt["off_diagonal_window_boolean_cross_rayleigh"],
            1.2125297369461143, places=8)
        self.assertLess(
            abs(receipt["active_matrix_reconstruction_residual"]), 2e-6)
        self.assertLess(
            abs(receipt["full_matrix_reconstruction_residual"]), 2e-6)
        self.assertTrue(receipt[
            "shared_prime_denominator_mass_hypothesis_passes"])
        self.assertFalse(receipt["signed_prime_correlation_proved"])

    def test_guards(self):
        with self.assertRaises(ValueError):
            classify_shared_prime_denominator_mass((), 11)
        with self.assertRaises(ValueError):
            classify_shared_prime_denominator_mass(({
                "reduced_denominator": 11,
                "off_diagonal_window_interference": 1.0},), 12)
        with self.assertRaises(ValueError):
            project_reduced_denominator_interference_receipt(
                127, (66, 78))
        with self.assertRaises(ArithmeticError):
            _require_no_mixed_high_q_packet(1)
        with self.assertRaises(ValueError):
            _require_no_mixed_high_q_packet(-1)


if __name__ == "__main__":
    unittest.main()
