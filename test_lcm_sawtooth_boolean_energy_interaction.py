import unittest

import numpy as np

from lcm_sawtooth_boolean_energy_interaction import (
    boolean_energy_interaction_receipt,
    mixed_packet_high_q_obstruction_receipt,
)


class LcmSawtoothBooleanEnergyInteractionTests(unittest.TestCase):
    def test_complex_packet_expansion_and_cauchy_bound_are_exact(self):
        packets = (
            np.array((1 + 2j, -3 + 1j, 2 - 4j)),
            np.array((2 - 1j, 5 + 3j, -1 + 2j)),
            np.array((-4 + 2j, 1 - 5j, 3 + 1j)),
            np.array((3 + 4j, -2 + 2j, 1 - 3j)),
        )
        receipt = boolean_energy_interaction_receipt(*packets)
        self.assertAlmostEqual(receipt["identity_residual"], 0)
        self.assertGreaterEqual(
            receipt["boolean_energy_difference"],
            receipt["cauchy_lower_bound"] - 1e-12)
        self.assertTrue(receipt[
            "exact_boolean_energy_interaction_identity_proved"])
        self.assertFalse(receipt[
            "boolean_energy_interaction_nonnegative_proved"])
        self.assertFalse(receipt["signed_prime_correlation_proved"])

    def test_sign_is_unrestricted_without_a_mixed_packet(self):
        vector = np.array((1 + 2j, -3 + 4j))
        zero = np.zeros(2, dtype=complex)
        positive = boolean_energy_interaction_receipt(
            zero, vector, vector, zero)
        negative = boolean_energy_interaction_receipt(
            zero, vector, -vector, zero)
        self.assertAlmostEqual(
            positive["boolean_energy_difference"],
            2 * float(np.vdot(vector, vector).real))
        self.assertAlmostEqual(
            negative["boolean_energy_difference"],
            -2 * float(np.vdot(vector, vector).real))

    def test_guards_packet_shapes(self):
        with self.assertRaises(ValueError):
            boolean_energy_interaction_receipt([], [], [], [])
        with self.assertRaises(ValueError):
            boolean_energy_interaction_receipt(
                np.ones(2), np.ones(3), np.ones(2), np.ones(2))

    def test_m127_pair_has_no_direct_mixed_high_q_packet(self):
        receipt = mixed_packet_high_q_obstruction_receipt(77, 143, 127, 28)
        self.assertEqual(receipt["common_denominator"], 1001)
        self.assertEqual(receipt["high_q_threshold"], 3556)
        self.assertTrue(receipt[
            "mixed_packet_zero_in_high_q_signal_proved"])
        self.assertFalse(receipt["mixed_packet_presence_proved"])

    def test_mixed_packet_obstruction_guards_and_is_one_way(self):
        receipt = mixed_packet_high_q_obstruction_receipt(77, 143, 17, 1)
        self.assertFalse(receipt[
            "mixed_packet_zero_in_high_q_signal_proved"])
        self.assertFalse(receipt["mixed_packet_presence_proved"])
        with self.assertRaises(ValueError):
            mixed_packet_high_q_obstruction_receipt(1, 143, 127, 28)
        with self.assertRaises(ValueError):
            mixed_packet_high_q_obstruction_receipt(77, 77, 127, 28)


if __name__ == "__main__":
    unittest.main()
