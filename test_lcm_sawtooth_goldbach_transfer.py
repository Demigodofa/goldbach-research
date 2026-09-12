import unittest

from lcm_sawtooth_goldbach_transfer import (
    all_even_residue_goldbach_main_receipt,
    all_residue_centered_outer_fiber_shadow_receipt,
    canonical_direct_resonant_goldbach_main_receipt,
    centered_outer_fiber_shadow_receipt,
    direct_source_fiber_average_receipt,
    even_even_goldbach_transfer_receipt,
    symbolic_centered_outer_fiber_shadow_receipt,
)


class EvenEvenGoldbachTransferTests(unittest.TestCase):
    def test_symbolic_centered_outer_fiber_shadow_identity(self):
        receipt = symbolic_centered_outer_fiber_shadow_receipt()
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["common_modulus"], 130)
        self.assertEqual(receipt["unit_group_order"], 48)
        self.assertEqual(receipt["fiber_size_over_U130"], 60)
        self.assertEqual(receipt["quotient77_divisor_row_count"], 4)
        self.assertEqual(receipt["quotient91_divisor_row_count"], 4)
        self.assertLess(
            receipt["quotient77_centered_fiber_shadow_relative_error"],
            1e-12)
        self.assertLess(
            receipt["quotient91_recombined_source_relative_l2"], 1e-12)
        self.assertEqual(receipt["central_unit_threshold"], 40)
        self.assertTrue(receipt[
            "quotient77_centered_coefficient_identity_proved"])
        self.assertTrue(receipt[
            "quotient91_recombined_source_cancels_symbolically"])
        self.assertTrue(receipt[
            "all_strict_central_targets_above_threshold_covered_by_identity"])
        self.assertFalse(receipt["endpoint_or_noncentral_terms_analyzed"])
        self.assertFalse(receipt["full_outer_assembly_identification_proved"])
        self.assertFalse(receipt["formal_signed_error_identification_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_all_residue_centered_outer_channel_samples(self):
        receipt = all_residue_centered_outer_fiber_shadow_receipt()
        self.assertEqual(receipt["selected_target_count"], 65)
        self.assertEqual(receipt["covered_even_residue_count"], 65)
        self.assertTrue(receipt["all_even_residue_classes_sampled"])
        self.assertEqual(receipt["maximum_bad_prime_terms_per_target"], 0)
        self.assertLess(
            receipt["base_receipt"][
                "maximum_fiber_shadow_centered_natural_scale_relative_error"],
            1e-12)
        self.assertLess(
            receipt["base_receipt"][
                "maximum_fiber_shadow_centered_relative_error"],
            1e-9)
        self.assertTrue(receipt[
            "all_residue_natural_scale_bridge_passes"])
        self.assertTrue(receipt[
            "all_residue_signed_scale_diagnostic_passes"])
        self.assertTrue(receipt[
            "quotient91_recombined_channel_cancels_on_samples"])
        self.assertFalse(receipt["full_outer_assembly_identification_proved"])
        self.assertFalse(receipt["formal_signed_error_identification_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_centered_outer_channel_is_lag130_fiber_shadow(self):
        receipt = centered_outer_fiber_shadow_receipt()
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["common_modulus"], 130)
        self.assertEqual(receipt["targets"], (1000, 1002))
        self.assertLess(
            receipt["maximum_fiber_shadow_centered_relative_error"],
            1e-12)
        self.assertLess(
            receipt["maximum_quotient91_direct_relative_to_natural_scale"],
            1e-12)
        for target, row in receipt["rows"].items():
            self.assertEqual(row["strict_central_interval"],
                             (target // 3, target - target // 3))
            self.assertFalse(row["nonunit_prime_pairs"])
            self.assertFalse(row["inadmissible_unit_pairs"])
            self.assertLess(
                row["fiber_shadow_centered_relative_error"], 1e-12)
            self.assertLess(
                row["constant_plus_shadow_reconstruction_relative_error"],
                1e-12)
        self.assertTrue(receipt[
            "quotient77_centered_channel_is_lag130_fiber_shadow"])
        self.assertTrue(receipt[
            "quotient91_recombined_channel_cancels_on_fixtures"])
        self.assertTrue(receipt[
            "constant_principal_channel_retained_separately"])
        self.assertFalse(receipt["full_outer_assembly_identification_proved"])
        self.assertFalse(receipt["formal_signed_error_identification_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_direct_lag_130_fiber_average_recovers_mod130_source(self):
        receipt = direct_source_fiber_average_receipt()
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["common_modulus"], 130)
        self.assertEqual(receipt["unit_group_order"], 48)
        self.assertEqual(receipt["fiber_size_over_U130"], 60)
        lag130 = receipt["lag_rows"][130]
        self.assertAlmostEqual(
            lag130["best_centered_fiber_sum_coefficient"].real, -1.0,
            places=12)
        self.assertAlmostEqual(
            lag130["best_centered_fiber_sum_coefficient"].imag, 0.0,
            places=12)
        self.assertLess(
            lag130[
                "negative_centered_fiber_sum_reconstruction_relative_error"],
            1e-12)
        self.assertLess(
            lag130[
                "negative_scaled_centered_fiber_average_relative_error"],
            1e-12)
        self.assertTrue(lag130[
            "reconstructs_recombined_centered_source"])
        lag110 = receipt["lag_rows"][110]
        self.assertGreater(
            lag110[
                "negative_centered_fiber_sum_reconstruction_relative_error"],
            .9)
        self.assertLess(
            lag110["centered_fiber_sum_correlation_with_G0"], .05)
        self.assertFalse(lag110[
            "reconstructs_recombined_centered_source"])
        self.assertTrue(receipt["lag_130_fiber_average_identifies_G0"])
        self.assertFalse(receipt["lag_110_fiber_average_identifies_G0"])
        self.assertTrue(receipt["quotient_source_fiber_shadow_identified"])
        self.assertFalse(receipt[
            "direct_source_pointwise_descent_to_mod130_proved"])
        self.assertFalse(receipt[
            "original_outer_assembly_identification_proved"])
        self.assertFalse(receipt["formal_signed_error_identification_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_actual_period_10010_resonant_sources(self):
        receipt = canonical_direct_resonant_goldbach_main_receipt()
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["unit_group_order"], 2880)
        self.assertEqual(receipt["even_target_residue_count"], 5005)
        self.assertEqual(tuple(receipt["lag_rows"]), (130, 110))
        expected = {
            130: (130, 77, (1, 131)),
            110: (110, 91, (1, 111)),
        }
        for lag, row in receipt["lag_rows"].items():
            common, quotient, witnesses = expected[lag]
            self.assertEqual(row["common_modulus"], common)
            self.assertEqual(row["quotient"], quotient)
            self.assertEqual(row["source_unit_count"], 2880)
            self.assertEqual(
                row["common_modulus_descent_witness_residues"], witnesses)
            self.assertGreater(row[
                "common_modulus_descent_witness_ratio"], .1)
            self.assertFalse(row["source_descends_to_common_modulus"])
            self.assertEqual(
                row["sampled_convolution_targets"], (0, 2, 72, 10008))
            self.assertLess(
                row["sampled_convolution_reconstruction_relative_error"],
                1e-12)
            self.assertEqual(row["even_target_residue_count"], 5005)
            self.assertGreater(min(
                target_row["admissible_residue_count"]
                for target_row in row["residue_rows"].values()), 0)
        lag130 = receipt["lag_rows"][130]
        self.assertLess(abs(
            lag130["common_modulus_descent_witness_values"][0]
            - complex(-336.7886448685408, -75.46799267074078)), 1e-8)
        lag110 = receipt["lag_rows"][110]
        self.assertLess(abs(
            lag110["common_modulus_descent_witness_values"][0]
            - complex(24531.634451810274, 0.0)), 1e-8)
        self.assertLess(
            receipt[
                "maximum_sampled_convolution_reconstruction_relative_error"],
            1e-12)
        self.assertTrue(receipt[
            "actual_unaveraged_periodic_sources_identified"])
        self.assertTrue(receipt["halupczok_modulus_10010_transfer_proved"])
        self.assertTrue(receipt[
            "all_even_target_l1_error_log_saving_proved"])
        self.assertTrue(receipt[
            "all_even_target_l2_error_log_saving_proved"])
        self.assertFalse(receipt["smaller_common_modulus_descent_proved"])
        self.assertFalse(receipt[
            "original_outer_assembly_identification_proved"])
        self.assertFalse(receipt[
            "pointwise_direct_resonant_correlation_estimate_proved"])
        self.assertFalse(receipt["formal_signed_error_identification_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_all_even_residue_singular_main_coefficients(self):
        receipt = all_even_residue_goldbach_main_receipt()
        self.assertEqual(receipt["common_modulus"], 130)
        self.assertEqual(receipt["unit_group_order"], 48)
        self.assertEqual(receipt["even_target_residue_count"], 65)
        self.assertEqual(tuple(receipt["rows"]), tuple(range(0, 130, 2)))
        self.assertLess(
            receipt["maximum_locally_centered_sum_relative_error"], 1e-12)
        self.assertLess(
            receipt["maximum_crt_inclusion_exclusion_relative_error"],
            1e-12)
        self.assertLess(receipt["maximum_local_source_bias_ratio"], .15)
        row72 = receipt["rows"][72]
        self.assertEqual(row72["admissible_residue_count"], 33)
        reconstructed_sum = (
            row72["central_singular_main_multiplier"] * 144)
        self.assertLess(
            abs(reconstructed_sum - row72["source_sum"])
            / max(1.0, abs(row72["source_sum"])), 1e-14)
        self.assertTrue(receipt[
            "all_even_residue_singular_main_coefficients_identified"])
        self.assertTrue(receipt[
            "all_even_residue_crt_inclusion_exclusion_identities_verified"])
        self.assertTrue(receipt[
            "local_uniform_channel_has_same_asymptotic_main"])
        self.assertTrue(receipt[
            "all_even_target_l1_error_log_saving_proved"])
        self.assertTrue(receipt[
            "all_even_target_l2_error_log_saving_proved"])
        self.assertFalse(receipt[
            "pointwise_signed_prime_correlation_estimate_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_exact_central_residue_and_character_transfers(self):
        receipt = even_even_goldbach_transfer_receipt(1700, 1800)
        self.assertEqual(receipt["common_modulus"], 130)
        self.assertEqual(receipt["target_residue"], 72)
        self.assertEqual(receipt["tested_target_count"], 1)
        self.assertEqual(tuple(receipt["rows"]), (1762,))
        self.assertEqual(len(receipt["admissible_residues"]), 33)
        self.assertEqual(len(receipt["dirichlet_character_labels"]), 48)
        self.assertFalse(receipt["nonunit_prime_pairs"])
        self.assertFalse(receipt["inadmissible_unit_prime_pairs"])
        self.assertLess(receipt["coefficient_sum_relative_error"], 1e-12)
        self.assertLess(
            receipt["maximum_reflection_coefficient_error"], 1e-12)
        self.assertLess(
            receipt["dirichlet_character_reconstruction_relative_error"],
            1e-12)
        self.assertLess(
            receipt["maximum_goldbach_transfer_identity_relative_error"],
            1e-12)
        self.assertTrue(receipt[
            "fixed_central_goldbach_residue_identity_proved_in_tested_range"])
        self.assertTrue(receipt[
            "fixed_dirichlet_character_expansion_verified"])
        self.assertTrue(receipt[
            "halupczok_theorem6_prime_only_weight_matches"])
        self.assertTrue(receipt[
            "moving_central_window_box_reduction_proved"])
        self.assertTrue(receipt[
            "applicable_mean_square_theorem_identified"])
        self.assertTrue(receipt[
            "almost_all_centered_correlation_estimate_proved"])
        self.assertFalse(receipt[
            "pointwise_centered_correlation_estimate_proved"])
        self.assertFalse(receipt["signed_prime_correlation_proved"])
        self.assertFalse(receipt["goldbach_proved"])


if __name__ == "__main__":
    unittest.main()
