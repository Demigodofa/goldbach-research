import unittest

from lcm_sawtooth_lifted_endpoint_frame import (
    project_prime_block_lifted_endpoint_scan,
)
from lcm_sawtooth_outer_weight_transfer import (
    UNIFORM_PROJECT_DISTORTION_BOUND,
    WEIGHT_MODES,
    _active_mode_count_formula,
    dyadic_outer_weight_distortion_receipt,
    project_outer_weights,
)


class LcmSawtoothOuterWeightTransferTests(unittest.TestCase):
    def test_active_mode_count_formula_matches_source_definition(self):
        from near_cutoff_geometric_bound import _active_modes

        for modulus in range(17, 300, 2):
            for shift_length in (1, 2, 3, 5):
                self.assertEqual(
                    _active_mode_count_formula(modulus, shift_length),
                    len(_active_modes(modulus, shift_length)))

    def test_established_weights_are_positive(self):
        weights = project_outer_weights(127, 251)
        self.assertEqual(tuple(weights), WEIGHT_MODES)
        self.assertTrue(all(value > 0 for value in weights.values()))

    def test_exact_distortions_obey_analytic_bounds(self):
        for scale in (17, 127, 251, 1009):
            receipt = dyadic_outer_weight_distortion_receipt(scale)
            for mode in WEIGHT_MODES:
                self.assertLessEqual(
                    receipt["exact_prime_block_distortion"][mode],
                    receipt["analytic_dyadic_distortion_bound"][mode])
                self.assertLessEqual(
                    receipt["analytic_dyadic_distortion_bound"][mode],
                    UNIFORM_PROJECT_DISTORTION_BOUND[mode])
            self.assertTrue(
                receipt["positive_weight_transfer_identity_proved"])
            self.assertFalse(receipt["unweighted_lifted_inequality_proved"])

    def test_measured_weighted_quotients_obey_transfer(self):
        scale = 127
        frame = project_prime_block_lifted_endpoint_scan(scale)
        distortion = dyadic_outer_weight_distortion_receipt(scale)[
            "exact_prime_block_distortion"]
        unweighted = frame["weighted_active_window_receipts"][
            "unweighted"]["largest_generalized_eigenvalue"]
        for mode, receipt in frame["weighted_active_window_receipts"].items():
            self.assertLessEqual(
                receipt["largest_generalized_eigenvalue"],
                distortion[mode] * unweighted * (1 + 1e-12))

    def test_input_guards(self):
        with self.assertRaises(ValueError):
            dyadic_outer_weight_distortion_receipt(16)
        with self.assertRaises(ValueError):
            project_outer_weights(127, 126)


if __name__ == "__main__":
    unittest.main()
