import unittest

from lcm_sawtooth_fixed_q_residue import fixed_q_residue_receipt
from lcm_sawtooth_signed_difference_bins import (
    signed_difference_bin_receipt,
)


class LcmSawtoothFixedQResidueTests(unittest.TestCase):
    def test_residue_packet_matches_ranked_exact_q_packet(self):
        signed = signed_difference_bin_receipt(101, 10, 10, 12, 3, 12)
        target, _, expected = signed["top_high_Q_packets"][0]
        receipt = fixed_q_residue_receipt(
            101, 10, 10, 12, 3, 12, (target,))
        packet = receipt["packets"][0]
        self.assertAlmostEqual(packet["packet_over_complete"], expected)
        self.assertLess(packet["ramanujan_kernel_identity_error"], 1e-10)
        self.assertLess(
            packet["packet_imaginary_error_over_complete"], 1e-12)
        for split in packet["crt_prime_split_metrics"]:
            self.assertTrue(
                0 <= split["leading_singular_energy_fraction"] <= 1)
            self.assertGreaterEqual(split["effective_singular_rank"], 1)
        self.assertTrue(receipt["exact_residue_packet_identity_proved"])
        self.assertFalse(receipt["constant_ramanujan_packet_bound_proved"])
        self.assertFalse(receipt["nonconstant_residue_bound_proved"])

    def test_invalid_target_family_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "target_denominators"):
            fixed_q_residue_receipt(101, 10, 10, 12, 3, 12, ())

    def test_prime_target_has_no_nontrivial_crt_split(self):
        receipt = fixed_q_residue_receipt(
            101, 10, 10, 12, 3, 12, (3,))
        self.assertEqual(
            receipt["packets"][0]["crt_prime_split_metrics"], ())


if __name__ == "__main__":
    unittest.main()
