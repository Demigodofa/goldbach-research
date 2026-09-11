import unittest

import numpy as np

from lcm_sawtooth_partner_doubling_transfer import (
    doubled_partner_geometric_receipt,
    classify_diagonal_multiplier_phase_bias,
    classify_multiplier_component_attribution,
    partner_packet_transfer_receipt,
    partner_doubling_transfer_receipt,
)


class PartnerDoublingTransferTests(unittest.TestCase):
    def test_multiplier_attribution_uses_three_packet_states(self):
        base = np.asarray((1, 0, 0, 0, 0), dtype=complex)
        right = np.asarray((0, 1, 0, 0, 0), dtype=complex)
        receipt = classify_multiplier_component_attribution(
            {17: (base, right, base, -right,
                  base, right, base, -right)}, 1, 1)
        self.assertEqual(
            receipt["minimum_explained_increment_fraction"], .75)
        self.assertIn(
            "aggregate_full_multiplier_increment", receipt)

    def test_phase_bias_classifier_applies_delta_mass_gate(self):
        actual_left = np.asarray((1, 0, 0, 0, 0), dtype=complex)
        actual_right = np.asarray((0, 1, 0, 0, 0), dtype=complex)
        neutral_left = actual_left.copy()
        neutral_right = -actual_right
        receipt = classify_diagonal_multiplier_phase_bias(
            {17: (actual_left, actual_right,
                  neutral_left, neutral_right)},
            1, 1, minimum_passing_channel_count=1)
        row = receipt["phase_bias_channel_rows"][0]
        self.assertIsNotNone(
            row["positive_phase_delta_absolute_mass_fraction"])
        self.assertEqual(receipt[
            "minimum_positive_phase_delta_absolute_mass_fraction"], .75)

    def test_project_packets_transfer_under_primitive_lift(self):
        receipt = partner_packet_transfer_receipt()
        self.assertEqual(receipt["prime_count"], 24)
        self.assertEqual(receipt["families"], ((77, 65, 1), (143, 35, 2)))
        self.assertEqual(
            receipt["unexpected_reduced_denominator_pair_count"], 0)
        self.assertEqual(receipt["nonodd_doubled_residue_pair_count"], 0)
        self.assertLess(
            receipt["maximum_packet_reconstruction_relative_error"], 1e-12)
        self.assertLess(
            receipt["maximum_packet_reconstruction_absolute_error"], 2e-15)
        self.assertLess(
            receipt["maximum_term_geometric_transfer_relative_error"],
            1e-12)
        self.assertLess(receipt[
            "maximum_endpoint_cosine_phase_factorization_relative_error"],
            1e-12)
        self.assertAlmostEqual(receipt[
            "maximum_direct_quotient_to_factored_multiplier_relative_error"],
            1.1764050738476914e-12, places=22)
        self.assertFalse(receipt[
            "direct_float_multiplier_factorization_test_passes"])
        self.assertTrue(receipt[
            "exact_multiplier_cosine_phase_factorization_proved"])
        empty_packets = {
            (row["prime_modulus"], row["conductor"])
            for row in receipt["packet_transfer_rows"]
            if row["nonzero_actual_packet_cell_count"] == 0}
        self.assertEqual(empty_packets, {(131, 77), (211, 143)})
        self.assertTrue(receipt[
            "exact_doubled_packet_diagonal_transfer_test_passes"])
        self.assertEqual(
            receipt["minimum_positive_phase_delta_absolute_mass_fraction"],
            .75)
        self.assertEqual(
            receipt["minimum_passing_phase_bias_channel_count"], 2)
        self.assertEqual(receipt["eligible_phase_bias_channel_count"], 22)
        self.assertEqual(receipt["phase_bias_passing_channel_count"], 3)
        self.assertEqual(
            receipt["phase_bias_passing_channels"], (139, 179, 233))
        self.assertTrue(receipt[
            "diagonal_multiplier_phase_bias_hypothesis_passes"])
        self.assertEqual(
            receipt["positive_signed_phase_delta_channel_count"], 10)
        self.assertAlmostEqual(
            receipt["aggregate_actual_near_lag_signed_sum"],
            .06574279317545717, places=10)
        self.assertAlmostEqual(
            receipt["aggregate_phase_neutral_near_lag_signed_sum"],
            .012887840697077239, places=10)
        self.assertAlmostEqual(
            receipt["aggregate_phase_delta_near_lag_signed_sum"],
            .052854952478380006, places=10)
        self.assertAlmostEqual(
            receipt[
                "aggregate_positive_phase_delta_absolute_mass_fraction"],
            .5053738213828133, places=10)
        phase_rows = {
            row["channel"]: row for row in receipt["phase_bias_channel_rows"]}
        self.assertAlmostEqual(
            phase_rows[179]["actual_near_lag_signed_sum"],
            .10502950751076004, places=10)
        self.assertAlmostEqual(
            phase_rows[179]["phase_neutral_near_lag_signed_sum"],
            -.22141963114248936, places=10)
        self.assertEqual(
            receipt["minimum_explained_increment_fraction"], .75)
        self.assertAlmostEqual(
            receipt["aggregate_sign_only_near_lag_signed_sum"],
            -.12483226301138946, places=10)
        self.assertAlmostEqual(
            receipt["aggregate_real_cosine_sign_increment"],
            -.13772010370847718, places=10)
        self.assertAlmostEqual(
            receipt["aggregate_additive_phase_increment"],
            .19057505618684667, places=10)
        self.assertAlmostEqual(
            receipt["aggregate_full_multiplier_increment"],
            .0528549524783695, places=10)
        self.assertLess(abs(receipt["shapley_reconstruction_error"]), 1e-12)
        self.assertAlmostEqual(
            receipt["aggregate_phase_only_near_lag_signed_sum"],
            -.25886661193381677, places=10)
        self.assertAlmostEqual(
            receipt["aggregate_phase_marginal_without_sign"],
            -.2717544526309045, places=10)
        self.assertAlmostEqual(
            receipt["aggregate_phase_marginal_with_sign"],
            .19057505618684667, places=10)
        self.assertAlmostEqual(
            receipt["real_sign_shapley_contribution"],
            .09344465070039841, places=10)
        self.assertAlmostEqual(
            receipt["additive_phase_shapley_contribution"],
            -.0405896982220289, places=10)
        self.assertFalse(receipt[
            "additive_phase_order_robust_shapley_hypothesis_passes"])
        self.assertFalse(receipt[
            "real_cosine_sign_meets_ordered_increment_gate"])
        self.assertTrue(receipt[
            "additive_phase_meets_ordered_increment_gate"])
        self.assertTrue(receipt[
            "some_multiplier_component_meets_ordered_increment_gate"])
        self.assertFalse(receipt["signed_prime_correlation_proved"])

    def test_half_interval_identity_and_primitive_lift(self):
        receipt = doubled_partner_geometric_receipt(17, 5)
        self.assertEqual(receipt["primitive_residue_count"], 4)
        self.assertTrue(receipt["primitive_odd_lift_is_bijection_proved"])
        self.assertLess(
            receipt["half_interval_factorization_maximum_relative_error"],
            1e-12)
        self.assertTrue(receipt[
            "exact_half_interval_geometric_identity_test_passes"])
        self.assertLess(
            receipt["diagonal_transfer_maximum_relative_error"], 1e-12)
        self.assertTrue(receipt[
            "exact_residue_diagonal_transfer_test_passes"])

    def test_project_fixture_applies_predeclared_scalar_gate(self):
        receipt = partner_doubling_transfer_receipt()
        self.assertEqual(receipt["odd_partners"], (35, 65))
        self.assertEqual(len(receipt["prime_moduli"]), 24)
        self.assertEqual(receipt["tolerance"], 1e-12)
        self.assertTrue(receipt[
            "exact_primitive_lift_half_interval_identity_proved"])
        self.assertTrue(receipt[
            "exact_residue_dependent_diagonal_transfer_proved"])
        self.assertLess(
            receipt["maximum_base_half_factorization_relative_error"],
            1e-12)
        self.assertLess(
            receipt["maximum_residue_diagonal_transfer_relative_error"],
            1e-12)
        self.assertLess(
            receipt["maximum_half_interval_factorization_relative_error"],
            1e-12)
        self.assertAlmostEqual(
            receipt[
                "minimum_nontrivial_full_geometric_transfer_relative_residual"],
            .6972166887783966, places=10)
        self.assertEqual(receipt["trivial_zero_geometric_channel_count"], 2)
        self.assertAlmostEqual(
            receipt[
                "maximum_nontrivial_full_geometric_transfer_relative_residual"],
            .9981053173424562, places=10)
        exact_zero_channels = {
            (row["prime_modulus"], row["odd_partner"])
            for row in receipt["geometric_transfer_rows"]
            if row["both_geometric_vectors_are_exactly_zero"]}
        self.assertEqual(exact_zero_channels, {(131, 65), (211, 35)})
        polynomial = {
            row["odd_partner"]: row
            for row in receipt["polynomial_transfer_rows"]}
        self.assertAlmostEqual(
            polynomial[35]["best_polynomial_transfer_relative_residual"],
            .2755577081330059, places=10)
        self.assertAlmostEqual(
            polynomial[65]["best_polynomial_transfer_relative_residual"],
            .29666696754607497, places=10)
        self.assertFalse(receipt[
            "single_scalar_geometric_transfer_all_channels_passes"])
        self.assertFalse(receipt[
            "single_scalar_polynomial_transfer_all_partners_passes"])
        self.assertFalse(receipt[
            "single_scalar_partner_doubling_transfer_hypothesis_passes"])
        self.assertFalse(receipt["signed_prime_correlation_proved"])

    def test_guards(self):
        with self.assertRaises(ValueError):
            doubled_partner_geometric_receipt(15, 5)
        with self.assertRaises(ValueError):
            doubled_partner_geometric_receipt(17, 6)
        with self.assertRaises(ValueError):
            partner_doubling_transfer_receipt(127, (35, 70))


if __name__ == "__main__":
    unittest.main()
