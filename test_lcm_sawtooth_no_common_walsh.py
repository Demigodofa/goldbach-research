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
            self.assertTrue(receipt["paired_support_majorant_proved"])
            self.assertGreaterEqual(
                receipt["paired_support_positive_majorant"],
                abs(receipt["direct_no_common_collapsed_sum"]))
            self.assertLessEqual(
                receipt["paired_support_positive_majorant"],
                receipt["walsh_positive_majorant"])
            self.assertFalse(
                receipt["walsh_parity_cancellation_bound_proved"])

    def test_dominant_probe_selects_and_reconstructs_coordinates(self):
        receipt = dominant_no_common_walsh_probe(101, 70, 4, 20, 3)
        self.assertGreater(receipt["selected_coordinate_count"], 0)
        self.assertLess(receipt["maximum_assignment_identity_error"], 1e-8)
        self.assertLess(receipt["maximum_walsh_identity_error"], 1e-8)
        self.assertGreater(
            receipt["selected_walsh_majorant_over_actual_energy"], 1)
        self.assertGreaterEqual(
            receipt["selected_paired_majorant_over_actual_energy"], 1)
        self.assertLessEqual(
            receipt["selected_paired_majorant_over_no_common_diagonal"],
            receipt["selected_walsh_majorant_over_no_common_diagonal"])
        self.assertAlmostEqual(
            receipt["selected_walsh_majorant_over_no_common_diagonal"],
            receipt["selected_walsh_majorant_over_actual_energy"]
            * receipt["selected_no_common_actual_over_diagonal"])
        self.assertAlmostEqual(
            sum(receipt[
                "dyadic_common_divisor_majorant_attribution"].values()), 1)
        self.assertTrue(
            receipt[
                "common_divisor_majorant_attribution_identity_proved"])
        self.assertGreaterEqual(
            receipt["dyadic_cauchy_bound_over_no_common_diagonal"],
            receipt["selected_walsh_majorant_over_no_common_diagonal"])
        self.assertTrue(
            receipt["dyadic_common_divisor_cauchy_reduction_proved"])
        self.assertGreaterEqual(
            receipt["e1_maximum_coordinate_energy_over_diagonal"],
            receipt[
                "dyadic_common_divisor_square_energy_over_diagonal"][1])
        self.assertGreaterEqual(
            receipt["e1_bad_coordinate_energy_fraction"],
            receipt["e1_bad_coordinate_diagonal_fraction"])
        self.assertAlmostEqual(sum(
            group["diagonal_fraction"] for group in receipt[
                "e1_by_target_prime_factor_count"].values()), 1)
        self.assertAlmostEqual(sum(
            group["e1_energy_fraction"] for group in receipt[
                "e1_by_target_prime_factor_count"].values()), 1)
        self.assertTrue(receipt["finite_dominant_walsh_measurement"])

    def test_nonsquarefree_target_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "squarefree"):
            no_common_walsh_probe(101, 70, 4, 20, 12)


if __name__ == "__main__":
    unittest.main()
