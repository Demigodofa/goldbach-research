import unittest

from lcm_sawtooth_fixed_q_residue import fixed_q_residue_receipt
from lcm_sawtooth_packet_conductor_channels import (
    packet_conductor_channel_receipt,
)
from lcm_sawtooth_signed_difference_bins import (
    signed_difference_bin_receipt,
)


class LcmSawtoothPacketConductorChannelTests(unittest.TestCase):
    def test_channels_reconstruct_named_exact_q_packet(self):
        signed = signed_difference_bin_receipt(101, 10, 10, 12, 3, 12)
        target = signed["top_high_Q_packets"][0][0]
        expected = fixed_q_residue_receipt(
            101, 10, 10, 12, 3, 12, (target,))["packets"][0]
        receipt = packet_conductor_channel_receipt(
            101, 10, 10, 12, 3, 12, target)
        self.assertAlmostEqual(
            receipt["packet_over_complete"],
            expected["packet_over_complete"])
        self.assertLess(
            receipt["packet_imaginary_error_over_complete"], 1e-12)
        self.assertAlmostEqual(
            sum(channel["absolute_channel_share"]
                for channel in receipt["channels"]),
            1)
        for channel in receipt["channels"]:
            self.assertTrue(
                0 <= channel["near_resonant_ordered_term_fraction"] <= 1)
            self.assertTrue(
                0 <= channel[
                    "near_resonant_absolute_envelope_fraction"] <= 1)
            self.assertTrue(
                isinstance(
                    channel["endpoint_mode_signed_channel_fraction"],
                    float))
            self.assertTrue(
                0 <= channel[
                    "top_five_term_absolute_envelope_fraction"] <= 1)
            self.assertLessEqual(
                len(channel["largest_ordered_terms"]), 10)
            for term in channel["largest_ordered_terms"]:
                self.assertLessEqual(
                    term["circular_reduced_numerator"],
                    receipt["target_denominator"] // 2)
        self.assertTrue(
            receipt["exact_conductor_channel_decomposition_proved"])
        self.assertFalse(receipt["uniform_channel_reinforcement_proved"])

    def test_absent_target_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "absent"):
            packet_conductor_channel_receipt(
                101, 10, 10, 12, 3, 12, 99991)


if __name__ == "__main__":
    unittest.main()
