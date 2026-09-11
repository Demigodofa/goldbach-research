import unittest

from lcm_sawtooth_incomplete_frequency import _quadratic_support_data
from lcm_sawtooth_joint_phase_obstruction import (
    high_difference_modulus_witness,
    termwise_joint_phase_exponent_budget,
)


class LcmSawtoothJointPhaseObstructionTests(unittest.TestCase):
    def test_witness_is_on_actual_quadratic_conductor_support(self):
        receipt = high_difference_modulus_witness(5, 50)
        _, support = _quadratic_support_data(5, 50)
        polynomials = dict(support)
        for conductor, expected in zip(
                receipt["primitive_conductors"],
                receipt["structured_quadratic_coefficients"]):
            self.assertIn(conductor, polynomials)
            self.assertAlmostEqual(polynomials[conductor][0], expected)
        numerator, denominator = receipt[
            "reduced_frequency_difference"]
        self.assertGreater(numerator, 0)
        self.assertGreater(
            receipt["difference_denominator_over_B_fourth"], .1)
        self.assertTrue(
            receipt[
                "B_fourth_difference_denominator_witness_proved"])

    def test_maximum_denominator_bound_stops_at_one_quarter(self):
        self.assertTrue(termwise_joint_phase_exponent_budget(
            .245)["maximum_denominator_joint_bound_power_saving"])
        self.assertFalse(termwise_joint_phase_exponent_budget(
            .25)["maximum_denominator_joint_bound_power_saving"])
        receipt = termwise_joint_phase_exponent_budget(.32)
        self.assertAlmostEqual(
            receipt["difference_modulus_square_root_exponent"], .14)
        self.assertFalse(receipt["weighted_difference_modulus_bound_proved"])

    def test_invalid_ranges_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "four"):
            high_difference_modulus_witness(5, 10)
        with self.assertRaises(ValueError):
            termwise_joint_phase_exponent_budget(True)


if __name__ == "__main__":
    unittest.main()
