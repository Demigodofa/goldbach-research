import unittest

from lcm_sawtooth_no_common_walsh import (
    dominant_no_common_walsh_probe,
    no_common_walsh_probe,
)


class LcmSawtoothNoCommonWalshTests(unittest.TestCase):
    def test_assignment_and_walsh_identities_match_direct_sum(self):
        for target in (30, 42, 70, 210):
            receipt = no_common_walsh_probe(101, 70, 4, 20, target)
            self.assertAlmostEqual(receipt["assignment_identity_error"], 0.0)
            self.assertAlmostEqual(receipt["walsh_identity_error"], 0.0)
            self.assertTrue(
                receipt["no_common_assignment_convolution_proved"])
            self.assertTrue(receipt["walsh_parity_square_identity_proved"])
            self.assertTrue(receipt["walsh_positive_majorant_proved"])
            self.assertFalse(
                receipt["walsh_parity_cancellation_bound_proved"])

    def test_dominant_probe_selects_and_reconstructs_coordinates(self):
        receipt = dominant_no_common_walsh_probe(101, 70, 4, 20, 3)
        self.assertGreater(receipt["selected_coordinate_count"], 0)
        self.assertLess(receipt["maximum_assignment_identity_error"], 1e-8)
        self.assertLess(receipt["maximum_walsh_identity_error"], 1e-8)
        self.assertGreater(
            receipt["selected_walsh_majorant_over_actual_energy"], 1)
        self.assertAlmostEqual(
            receipt["selected_walsh_majorant_over_no_common_diagonal"],
            receipt["selected_walsh_majorant_over_actual_energy"]
            * receipt["selected_no_common_actual_over_diagonal"])
        self.assertTrue(receipt["finite_dominant_walsh_measurement"])

    def test_nonsquarefree_target_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "squarefree"):
            no_common_walsh_probe(101, 70, 4, 20, 12)


if __name__ == "__main__":
    unittest.main()
