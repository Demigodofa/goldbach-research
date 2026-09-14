import math
import unittest

from lcm_sawtooth_goldbach_transfer import (
    all_even_residue_goldbach_main_receipt,
    all_residue_centered_outer_fiber_shadow_receipt,
    canonical_direct_resonant_goldbach_main_receipt,
    combined_coefficient_admissible_main_receipt,
    combined_coefficient_character_spectrum_receipt,
    combined_coefficient_character_support_receipt,
    combined_coefficient_centered_error_envelope_receipt,
    combined_coefficient_lower_modulus_deviation_receipt,
    combined_coefficient_pairwise_gram_receipt,
    combined_coefficient_negative_residue_lift_receipt,
    combined_coefficient_prime_correlation_diagnostic_receipt,
    combined_coefficient_period_cycle_envelope_receipt,
    combined_coefficient_support_contribution_receipt,
    combined_coefficient_support_cycle_envelope_receipt,
    combined_coefficient_support_descent_receipt,
    combined_coefficient_uniform_residue_margin_receipt,
    combined_fixed_strict_central_coefficient_receipt,
    count_four_outer_holdout_sector_receipt,
    dominant_support_singular_tail_scan_receipt,
    dominant_support_character_matrix_structure_receipt,
    exact_projected_pairwise_gram_receipt,
    holdout_full_projected_prime_coefficient_receipt,
    holdout_lag_fiber_shadow_candidate_receipt,
    holdout_original_projected_action_audit_receipt,
    holdout_q65_dual_prime_target_sum_receipt,
    holdout_q65_active_row_bridge_receipt,
    holdout_q65_naive_spatial_prime_coefficient_receipt,
    holdout_q65_projected_spatial_fiber_bridge_receipt,
    holdout_q55_projected_principal_channel_receipt,
    q286_character_imbalance_receipt,
    q286_character_matrix_structure_receipt,
    q286_leading_mode_cycle_profile_receipt,
    q286_leading_mode_lift_decay_receipt,
    q286_leading_mode_period_envelope_receipt,
    q286_leading_mode_character_shape_receipt,
    q286_leading_singular_mode_contribution_receipt,
    q286_first_three_ap_discrepancy_proxy_receipt,
    q286_first_three_character_mixture_norm_receipt,
    q286_first_three_character_mode_coordinate_receipt,
    q286_first_two_mode_sign_window_receipt,
    q286_first_two_mode_subcone_magnitude_window_receipt,
    q286_first_two_mode_subcone_complement_window_receipt,
    q286_first_three_full_negative_driver_receipt,
    q286_driver_residue_lift_occupancy_receipt,
    q286_first_two_mode_lower_tail_receipt,
    q286_boundary_complement_support_split_receipt,
    q286_first_three_removed_support_envelope_receipt,
    q286_subcone_lower_support_package_receipt,
    q286_lower_support_package_support_only_obstruction_receipt,
    q286_lower_support_package_local_discrepancy_receipt,
    q286_lower_support_package_component_local_discrepancy_receipt,
    _q286_lower_support_component_data,
    _q286_first_two_mode_lower_tail_selected_cached,
    q286_lower_support_component_pair_tail_window_receipt,
    q286_lower_support_component_pair_coefficient_geometry_receipt,
    q286_lower_support_component_pair_cone_projection_receipt,
    q286_lower_support_component_pair_support_geometry_obstruction_receipt,
    q286_lower_support_component_pair_reflection_support_geometry_obstruction_receipt,
    q286_lower_support_component_pair_character_mixture_receipt,
    q286_lower_support_component_pair_real_channel_receipt,
    q286_lower_support_component_pair_real_channel_action_receipt,
    q286_lower_support_component_pair_real_channel_rescue_margin_receipt,
    q286_lower_support_component_pair_real_channel_bound_budget_receipt,
    q286_lower_support_component_pair_conditional_norm_closure_receipt,
    q286_lower_support_component_pair_floor_stability_decomposition_receipt,
    q286_lower_support_component_pair_floor_identity_receipt,
    q286_lower_support_component_pair_combined_driver_channel_closure_receipt,
    q286_lower_support_component_pair_action_identity_receipt,
    q286_lower_support_component_pair_closure_margin_profile_receipt,
    q286_lower_support_component_pair_channel_pressure_profile_receipt,
    q286_lower_support_component_pair_channel_conductor_profile_receipt,
    q286_lower_support_component_pair_fixed_conductor_reduction_receipt,
    q286_lower_support_component_pair_fixed_conductor_residue_pressure_receipt,
    q286_lower_support_component_pair_fixed_conductor_character_cancellation_receipt,
    q286_lower_support_component_pair_fixed_conductor_reflection_orbit_receipt,
    q286_lower_support_component_pair_fixed_conductor_residual_orbit_cancellation_receipt,
    q286_lower_support_component_pair_fixed_conductor_orbit_polygon_receipt,
    q286_lower_support_component_pair_fixed_conductor_orbit_phase_profile_receipt,
    q286_lower_support_component_pair_fixed_conductor_phase_bin_compression_receipt,
    q286_lower_support_component_pair_fixed_conductor_phase_antipodal_compression_receipt,
    q286_lower_support_component_pair_fixed_conductor_phase_antipodal_pair_balance_receipt,
    q286_lower_support_component_pair_fixed_conductor_phase_antipodal_threshold_envelope_receipt,
    q286_lower_support_component_pair_fixed_conductor_phase_antipodal_thin_exception_receipt,
    q286_lower_support_component_pair_fixed_conductor_phase_antipodal_exception_budget_receipt,
    q286_lower_support_component_pair_fixed_conductor_phase_antipodal_nonthin_ratio_receipt,
    q286_lower_support_component_pair_fixed_conductor_phase_antipodal_sector_geometry_receipt,
    q286_lower_support_component_pair_fixed_conductor_phase_antipodal_thin_large_side_budget_receipt,
    q286_lower_support_component_pair_fixed_conductor_phase_antipodal_thin_large_side_edge_support_receipt,
    q286_lower_support_component_pair_fixed_conductor_phase_antipodal_thin_large_side_support_receipt,
    q286_lower_support_component_pair_fixed_inequality_stress_receipt,
    q286_lower_support_component_pair_fixed_inequality_target_census_receipt,
    q286_lower_support_component_pair_tail_selector_grid_receipt,
    q286_active_lane_strict_closure_margin_census_receipt,
    q286_first_three_removed_support_gram_receipt,
    q286_first_three_removed_vector_stress_receipt,
    q286_first_three_removed_low_tail_lift_receipt,
    q286_first_three_removed_low_tail_auto_lift_receipt,
    q286_first_three_removed_low_tail_multi_period_receipt,
    q286_first_three_removed_complement_threshold_horizon_receipt,
    q286_first_three_tail_threshold_horizon_receipt,
    q286_first_three_tail_mode_only_horizon_receipt,
    q286_first_three_tail_mode_only_fast_horizon_receipt,
    q286_first_three_weighted_discrepancy_norm_receipt,
    q286_first_three_reflection_support_obstruction_receipt,
    q286_first_three_reflection_orbit_cap_receipt,
    q286_first_three_reflection_orbit_signed_cancellation_receipt,
    q286_first_three_reflection_orbit_ratio_certificate_receipt,
    q286_first_three_reflection_orbit_ratio_cycle_horizon_receipt,
    q286_first_three_reflection_orbit_dual_rectangle_receipt,
    q286_first_three_positive_orbit_landing_profile_receipt,
    q286_first_three_positive_mass_threshold_falsifier_receipt,
    q286_selected_first_three_alignment_receipt,
    q286_first_three_tail_alignment_window_receipt,
    q286_selected_alignment_complement_certificate_receipt,
    q286_first_three_tail_alignment_complement_window_receipt,
    q286_first_three_tail_hit_residue_profile_receipt,
    q286_active_selector_necessary_condition_scout_receipt,
    q286_first_three_tail_threshold_ladder_receipt,
    q286_first_three_complement_cooccurrence_receipt,
    q286_nonrescued_first_three_tail_classification_receipt,
    q286_first_three_filter_order_audit_receipt,
    q286_nonrescued_first_three_tail_cycle_horizon_receipt,
    q286_first_three_tail_rescue_profile_receipt,
    q286_first_three_tail_rescue_floor_candidate_receipt,
    q286_residue_discrepancy_profile_receipt,
    q286_separable_mode_coefficient_receipt,
    q286_separable_mode_local_bias_receipt,
    q286_significant_lift_envelope_receipt,
    q286_singular_mode_approximation_receipt,
    q286_singular_mode_cycle_scan_receipt,
    q286_singular_mode_lower_tail_stress_receipt,
    reduced_full_lower_envelope_cycle_scan_receipt,
    reduced_full_lower_envelope_receipt,
    centered_outer_fiber_shadow_receipt,
    direct_source_fiber_average_receipt,
    even_even_goldbach_transfer_receipt,
    q77_original_strict_central_action_receipt,
    symbolic_q65_dual_prime_coefficient_receipt,
    symbolic_centered_outer_fiber_shadow_receipt,
    symbolic_principal_plus_centered_channel_receipt,
)


class EvenEvenGoldbachTransferTests(unittest.TestCase):
    def test_count_four_outer_holdout_sector_receipt(self):
        receipt = count_four_outer_holdout_sector_receipt()
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(
            receipt["all_count_four_quotients"],
            (35, 55, 65, 77, 91, 143))
        self.assertEqual(receipt["linked_prime_slice_quotients"], (77, 91))
        self.assertEqual(receipt["strict_central_principal_plus_shadow_quotient"], 77)
        self.assertEqual(receipt["linked_slice_cancelling_quotient"], 91)
        self.assertEqual(receipt["holdout_quotients"], (35, 55, 65, 143))
        self.assertEqual(receipt["live_holdout_quotients"], (35, 55, 65, 143))
        expected_fourier = {
            35: .010906884721340548,
            55: .024560020667301303,
            65: .0005487547365190931,
            143: .006101857449924944,
        }
        expected_count_four = {
            35: .16118908808873234,
            55: .3024507788824479,
            65: .014327564985042195,
            143: .09820822341044044,
        }
        for quotient, expected in expected_fourier.items():
            self.assertAlmostEqual(
                receipt["holdout_rows"][quotient][
                    "fourier_cancellation_quotient"],
                expected, places=14)
        for quotient, expected in expected_count_four.items():
            self.assertAlmostEqual(
                receipt["holdout_rows"][quotient][
                    "count_four_recombination_quotient"],
                expected, places=14)
        self.assertTrue(receipt["all_projected_fourier_identities_pass"])
        self.assertTrue(receipt["all_holdout_count_four_sectors_are_live"])
        self.assertTrue(receipt["endpoint_only_residual_hypothesis_falsified"])
        self.assertTrue(receipt["full_outer_assembly_needs_holdout_sector_bridge"])
        self.assertFalse(receipt["full_outer_assembly_identification_proved"])
        self.assertFalse(receipt["formal_signed_error_identification_proved"])
        self.assertFalse(receipt[
            "pointwise_signed_prime_correlation_estimate_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_holdout_lag_fiber_shadow_candidate(self):
        receipt = holdout_lag_fiber_shadow_candidate_receipt()
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["quotient"], 65)
        self.assertEqual(receipt["lag"], 154)
        self.assertEqual(receipt["common_modulus"], 154)
        self.assertEqual(receipt["unit_group_order"], 60)
        self.assertEqual(receipt["fiber_size_over_common_modulus"], 48)
        self.assertAlmostEqual(
            receipt["fiber_sum_mean"].real, -1127.8833333333703,
            places=9)
        self.assertAlmostEqual(
            receipt["fiber_sum_mean"].imag,
            -3.036385957481495e-13, places=9)
        self.assertAlmostEqual(
            receipt["centered_fiber_sum_l2"], 86071.18524618556,
            places=8)
        self.assertAlmostEqual(
            receipt["centered_to_total_fiber_l2_ratio"],
            .9948879642115595, places=14)
        self.assertAlmostEqual(
            receipt["maximum_internal_fiber_point_spread"],
            28401.117801547734, places=8)
        self.assertFalse(
            receipt["direct_source_pointwise_descends_to_common_modulus"])
        self.assertTrue(receipt["nonzero_fiber_shadow_candidate_available"])
        self.assertEqual(receipt["central_unit_threshold"], 34)
        self.assertFalse(receipt["linked_prime_or_outer_row_bridge_proved"])
        self.assertFalse(receipt["full_outer_assembly_identification_proved"])
        self.assertFalse(receipt["formal_signed_error_identification_proved"])
        self.assertFalse(receipt[
            "pointwise_signed_prime_correlation_estimate_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_holdout_q65_active_row_bridge_fails(self):
        receipt = holdout_q65_active_row_bridge_receipt()
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["quotient"], 65)
        self.assertEqual(receipt["lag"], 154)
        self.assertEqual(receipt["common_modulus"], 154)
        self.assertEqual(receipt["targets"], (1000, 1002))
        self.assertEqual(receipt["active_divisors"], (1, 5, 13, 65))
        self.assertEqual(receipt["unit_group_order"], 60)
        self.assertLess(receipt["recombined_active_source_l2"], 1e-10)
        self.assertEqual(
            receipt["active_source_cancellation_tolerance"], 1e-10)
        self.assertAlmostEqual(
            receipt["fiber_shadow_l2"], 86071.18524618556,
            places=8)
        self.assertLess(
            receipt["active_source_to_fiber_shadow_l2_ratio"], 1e-12)
        self.assertGreater(
            receipt["same_sign_shadow_match_relative_error"], .999999)
        self.assertGreater(
            receipt["opposite_sign_shadow_match_relative_error"], .999999)
        self.assertLess(
            abs(receipt["best_scalar_to_fiber_shadow"]), 1e-12)
        self.assertEqual(receipt["maximum_target_source_vector_spread"], 0.0)
        self.assertTrue(receipt["active_recombined_source_cancels"])
        self.assertFalse(
            receipt["active_row_bridge_matches_nonzero_fiber_shadow"])
        self.assertTrue(receipt["q65_active_linked_row_bridge_falsified"])
        self.assertFalse(
            receipt["alternative_count_four_sector_bridge_ruled_out"])
        self.assertFalse(receipt["full_outer_assembly_identification_proved"])
        self.assertFalse(receipt["formal_signed_error_identification_proved"])
        self.assertFalse(receipt[
            "pointwise_signed_prime_correlation_estimate_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_holdout_q65_projected_spatial_fiber_bridge(self):
        receipt = holdout_q65_projected_spatial_fiber_bridge_receipt()
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["quotient"], 65)
        self.assertEqual(receipt["lag"], 154)
        self.assertEqual(receipt["common_modulus"], 154)
        self.assertEqual(receipt["spatial_frequency_count"], 3900)
        self.assertEqual(receipt["unit_group_order"], 60)
        self.assertAlmostEqual(
            receipt["projected_signed_total"], -67673.0, places=6)
        self.assertAlmostEqual(
            receipt["projected_absolute_mass"], 123321031.23021583,
            places=5)
        self.assertAlmostEqual(
            receipt["projected_cancellation_quotient"],
            .0005487547365190946, places=14)
        self.assertAlmostEqual(
            receipt["grouped_centered_spatial_l2"],
            86071.18524618637, places=8)
        self.assertAlmostEqual(
            receipt["fiber_shadow_l2"], 86071.18524618556,
            places=8)
        self.assertGreater(
            receipt["same_sign_fiber_shadow_relative_error"], 1.999999)
        self.assertLess(
            receipt["opposite_sign_fiber_shadow_relative_error"], 1e-12)
        self.assertAlmostEqual(
            receipt["best_scalar_to_fiber_shadow"].real, -1.0,
            places=12)
        self.assertLess(
            abs(receipt["best_scalar_to_fiber_shadow"].imag), 1e-12)
        self.assertTrue(receipt[
            "projected_spatial_grouping_equals_negative_fiber_shadow"])
        self.assertTrue(receipt["active_linked_row_bridge_was_wrong_layer"])
        self.assertFalse(
            receipt["linked_prime_or_target_prime_pair_bridge_proved"])
        self.assertFalse(receipt["full_outer_assembly_identification_proved"])
        self.assertFalse(receipt["formal_signed_error_identification_proved"])
        self.assertFalse(receipt[
            "pointwise_signed_prime_correlation_estimate_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_holdout_q65_naive_spatial_prime_coefficient_fails(self):
        receipt = holdout_q65_naive_spatial_prime_coefficient_receipt()
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["quotient"], 65)
        self.assertEqual(receipt["lag"], 154)
        self.assertEqual(receipt["common_modulus"], 154)
        self.assertEqual(receipt["unit_group_order"], 60)
        self.assertAlmostEqual(
            receipt["naive_spatial_prime_coefficient_l2"],
            86071.18524618637, places=8)
        self.assertGreater(
            receipt["fourier_dual_prime_coefficient_l2"],
            receipt["naive_spatial_prime_coefficient_l2"])
        self.assertGreater(receipt["same_index_relative_error"], .99)
        self.assertGreater(receipt["opposite_index_relative_error"], .95)
        self.assertGreater(
            receipt["best_scalar_dual_to_naive_relative_error"], .9)
        self.assertFalse(
            receipt["naive_spatial_is_fourier_dual_prime_coefficient"])
        self.assertTrue(
            receipt["naive_same_index_prime_coefficient_falsified"])
        self.assertFalse(receipt["target_prime_pair_bridge_proved"])
        self.assertFalse(receipt["full_outer_assembly_identification_proved"])
        self.assertFalse(receipt["formal_signed_error_identification_proved"])
        self.assertFalse(receipt[
            "pointwise_signed_prime_correlation_estimate_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_holdout_q65_dual_prime_target_sum(self):
        receipt = holdout_q65_dual_prime_target_sum_receipt()
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["quotient"], 65)
        self.assertEqual(receipt["lag"], 154)
        self.assertEqual(receipt["common_modulus"], 154)
        self.assertEqual(receipt["targets"], (1000, 1002))
        self.assertEqual(receipt["unit_group_order"], 60)
        self.assertLess(
            receipt["maximum_spatial_dual_relative_error"], 1e-12)
        self.assertGreater(
            receipt["minimum_naive_dual_relative_error"], .1)
        self.assertFalse(receipt["nonunit_prime_pairs"])
        for row in receipt["rows"].values():
            self.assertGreater(row["ordered_central_prime_pair_count"], 0)
            self.assertLess(row["spatial_dual_relative_error"], 1e-12)
            self.assertGreater(row["naive_dual_relative_error"], .1)
        self.assertTrue(
            receipt["spatial_to_dual_target_transfer_verified_on_targets"])
        self.assertTrue(receipt["naive_same_index_target_transfer_falsified"])
        self.assertFalse(receipt["target_prime_pair_bridge_proved_symbolically"])
        self.assertFalse(receipt["full_outer_assembly_identification_proved"])
        self.assertFalse(receipt["formal_signed_error_identification_proved"])
        self.assertFalse(receipt[
            "pointwise_signed_prime_correlation_estimate_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_symbolic_q65_dual_prime_coefficient(self):
        receipt = symbolic_q65_dual_prime_coefficient_receipt()
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["quotient"], 65)
        self.assertEqual(receipt["lag"], 154)
        self.assertEqual(receipt["common_modulus"], 154)
        self.assertEqual(receipt["unit_group_order"], 60)
        self.assertEqual(receipt["central_unit_threshold"], 34)
        self.assertAlmostEqual(
            receipt["spatial_source_l2"], 86071.18524618637,
            places=8)
        self.assertAlmostEqual(
            receipt["fourier_dual_prime_coefficient_l2"],
            751779.5321027868, places=7)
        self.assertLess(
            receipt["maximum_dual_coefficient_imaginary_part"], 1e-8)
        self.assertEqual(len(receipt["coefficient_by_unit_residue"]), 60)
        self.assertFalse(receipt["coefficient_depends_on_target_residue"])
        self.assertFalse(receipt[
            "nonunit_central_prime_pair_correction_needed_for_N_ge_34"])
        self.assertTrue(receipt[
            "symbolic_q65_dual_coefficient_transfer_proved"])
        self.assertTrue(receipt["q65_source_layer_bridge_proved"])
        self.assertFalse(receipt["q65_positive_or_signed_estimate_proved"])
        self.assertFalse(receipt["full_outer_assembly_identification_proved"])
        self.assertFalse(receipt["formal_signed_error_identification_proved"])
        self.assertFalse(receipt[
            "pointwise_signed_prime_correlation_estimate_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_holdout_q55_projected_principal_channel(self):
        receipt = holdout_q55_projected_principal_channel_receipt()
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["quotient"], 55)
        self.assertEqual(receipt["lag"], 182)
        self.assertEqual(receipt["common_modulus"], 182)
        self.assertEqual(receipt["unit_group_order"], 72)
        self.assertEqual(receipt["spatial_frequency_count"], 3960)
        self.assertAlmostEqual(
            receipt["projected_signed_total"], -3644424.0,
            places=6)
        self.assertAlmostEqual(
            receipt["projected_absolute_mass"], 148388474.47926253,
            places=5)
        self.assertAlmostEqual(
            receipt["projected_cancellation_quotient"],
            .024560020667301303, places=14)
        self.assertAlmostEqual(
            receipt["constant_grouped_spatial_value"], -50617.0,
            places=6)
        self.assertLess(
            receipt["maximum_centered_grouped_spatial_absolute_value"],
            1e-9)
        self.assertLess(receipt["centered_grouped_spatial_l2"], 1e-9)
        self.assertEqual(receipt["ramanujan_unit_value"], -1)
        self.assertAlmostEqual(
            receipt["principal_prime_residue_coefficient"], 50617.0,
            places=6)
        self.assertEqual(receipt["central_unit_threshold"], 40)
        self.assertLess(receipt["maximum_target_relative_error"], 1e-9)
        self.assertFalse(receipt["nonunit_prime_pairs"])
        self.assertTrue(receipt["q55_centered_shadow_cancels"])
        self.assertTrue(receipt["q55_principal_channel_identified"])
        self.assertFalse(receipt["target_prime_pair_bridge_proved_symbolically"])
        self.assertFalse(receipt["full_outer_assembly_identification_proved"])
        self.assertFalse(receipt["formal_signed_error_identification_proved"])
        self.assertFalse(receipt[
            "pointwise_signed_prime_correlation_estimate_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_holdout_full_projected_prime_coefficients(self):
        expected = {
            35: {
                "lag": 286,
                "common": 286,
                "units": 120,
                "threshold": 40,
                "mean": 21442.808333333334,
                "principal": -21442.808333333334,
                "centered_l2": 188155.56923352455,
                "dual_l2": 2232674.8772659665,
                "full_l2": 2244997.1917757513,
            },
            65: {
                "lag": 154,
                "common": 154,
                "units": 60,
                "threshold": 34,
                "mean": -1127.8833333333334,
                "principal": 1127.8833333333334,
                "centered_l2": 86071.18524618639,
                "dual_l2": 751779.5321027868,
                "full_l2": 751830.2947723654,
            },
            143: {
                "lag": 70,
                "common": 70,
                "units": 24,
                "threshold": 22,
                "mean": -13896.875,
                "principal": 13896.875,
                "centered_l2": 77398.42936794648,
                "dual_l2": 443487.86788549845,
                "full_l2": 448683.0108172142,
            },
        }
        for quotient, row in expected.items():
            receipt = holdout_full_projected_prime_coefficient_receipt(
                quotient=quotient)
            self.assertEqual(receipt["quotient"], quotient)
            self.assertEqual(receipt["lag"], row["lag"])
            self.assertEqual(receipt["common_modulus"], row["common"])
            self.assertEqual(receipt["unit_group_order"], row["units"])
            self.assertEqual(receipt["central_unit_threshold"], row["threshold"])
            self.assertAlmostEqual(
                receipt["grouped_spatial_mean"], row["mean"], places=9)
            self.assertAlmostEqual(
                receipt["principal_prime_residue_coefficient"],
                row["principal"], places=9)
            self.assertAlmostEqual(
                receipt["centered_spatial_l2"], row["centered_l2"], places=7)
            self.assertAlmostEqual(
                receipt["centered_dual_coefficient_l2"],
                row["dual_l2"], places=6)
            self.assertAlmostEqual(
                receipt["full_prime_residue_coefficient_l2"],
                row["full_l2"], places=6)
            self.assertLess(
                receipt["maximum_target_relative_error"], 1e-9)
            self.assertLess(
                receipt["maximum_full_coefficient_imaginary_part"], 1e-7)
            self.assertFalse(receipt["nonunit_prime_pairs"])
            self.assertTrue(receipt[
                "full_projected_spatial_target_transfer_verified_on_targets"])
            self.assertFalse(receipt["coefficient_depends_on_target_residue"])
            self.assertFalse(receipt["positive_or_signed_estimate_proved"])
            self.assertFalse(receipt["full_outer_assembly_identification_proved"])
            self.assertFalse(receipt["formal_signed_error_identification_proved"])
            self.assertFalse(receipt[
                "pointwise_signed_prime_correlation_estimate_proved"])
            self.assertFalse(receipt["goldbach_proved"])

    def test_combined_fixed_strict_central_coefficient_family(self):
        receipt = combined_fixed_strict_central_coefficient_receipt()
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["unit_group_order"], 2880)
        self.assertEqual(
            receipt["assembled_quotients"], (35, 55, 65, 77, 143))
        self.assertAlmostEqual(
            receipt["aggregate_principal_mean"].real,
            44002.512499999146, places=7)
        self.assertLess(
            abs(receipt["aggregate_principal_mean"].imag), 1e-8)
        self.assertAlmostEqual(
            receipt["expected_principal_mean"].real, 44002.5125,
            places=7)
        self.assertLess(receipt["principal_mean_relative_error"], 1e-12)
        expected_l2 = {
            77: 339622.7115252295,
            35: 10937828.421665356,
            55: 1.835792019507675e-09,
            65: 5208481.3827695325,
            143: 4858166.184415171,
        }
        for quotient, expected in expected_l2.items():
            self.assertAlmostEqual(
                receipt["component_centered_l2"][quotient],
                expected, places=5)
        self.assertAlmostEqual(
            receipt["sum_component_centered_l2"],
            21344098.70037529, places=5)
        self.assertAlmostEqual(
            receipt["aggregate_centered_l2"],
            13056020.079597872, places=5)
        self.assertAlmostEqual(
            receipt["centered_cancellation_ratio"],
            .6116922650553668, places=14)
        self.assertLess(
            receipt["maximum_holdout_fixture_transfer_error"], 1e-12)
        self.assertEqual(
            len(receipt["aggregate_coefficient_by_unit_residue"]), 2880)
        self.assertTrue(receipt["fixed_coefficient_family_assembled"])
        self.assertTrue(receipt["all_components_are_fixed_before_target"])
        self.assertFalse(receipt["signed_prime_correlation_estimate_proved"])
        self.assertFalse(receipt["full_outer_assembly_identification_proved"])
        self.assertFalse(receipt["formal_signed_error_identification_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_combined_coefficient_character_spectrum_is_broad(self):
        receipt = combined_coefficient_character_spectrum_receipt()
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["unit_group_order"], 2880)
        self.assertEqual(
            receipt["assembled_quotients"], (35, 55, 65, 77, 143))
        self.assertLess(
            receipt["character_reconstruction_relative_error"], 1e-12)
        self.assertAlmostEqual(
            receipt["total_character_energy"],
            59187382055.160706, places=3)
        self.assertAlmostEqual(
            receipt["parseval_centered_l2_squared_over_phi"],
            59187382055.1607, places=3)
        self.assertEqual(receipt["top_count"], 12)
        self.assertAlmostEqual(
            receipt["top_character_cumulative_energy_fraction"],
            .2525547318628327, places=14)
        self.assertAlmostEqual(
            receipt["character_energy_participation_ratio"],
            66.02126503332039, places=12)
        self.assertEqual(
            receipt["nontrivial_character_count_at_tolerance"], 110)
        self.assertEqual(
            receipt["top_character_rows"][0]["label"], (1, 3, 0, 0))
        self.assertAlmostEqual(
            receipt["top_character_rows"][0]["energy_fraction"],
            .023772825073655336, places=14)
        self.assertFalse(receipt["small_character_support_diagnostic_passes"])
        self.assertTrue(receipt["broad_character_support_observed"])
        self.assertTrue(receipt["character_spectrum_measured"])
        self.assertFalse(receipt["signed_prime_correlation_estimate_proved"])
        self.assertFalse(receipt["formal_signed_error_identification_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_combined_coefficient_character_support_is_low_dimensional(self):
        receipt = combined_coefficient_character_support_receipt()
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["unit_group_order"], 2880)
        self.assertEqual(receipt["factor_primes"], (5, 7, 11, 13))
        self.assertAlmostEqual(
            receipt["full_support_energy_fraction"],
            2.6819396744968046e-31, places=30)
        self.assertAlmostEqual(
            receipt["lower_support_energy_fraction"], 1.0, places=14)
        self.assertEqual(receipt["leading_support"], (11, 13))
        self.assertAlmostEqual(
            receipt["leading_support_energy_fraction"],
            .70082890257693, places=14)
        self.assertFalse(receipt["full_support_dominates"])
        self.assertTrue(receipt["low_dimensional_support_diagnostic_passes"])
        self.assertTrue(receipt["character_support_grouping_measured"])
        self.assertFalse(receipt["signed_prime_correlation_estimate_proved"])
        self.assertFalse(receipt["formal_signed_error_identification_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_combined_coefficient_pairwise_gram_has_only_tiny_net_cancellation(self):
        receipt = combined_coefficient_pairwise_gram_receipt()
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["unit_group_order"], 2880)
        self.assertEqual(receipt["quotients"], (77, 35, 55, 65, 143))
        expected_norms = {
            77: 339622.7115252295,
            35: 10937828.421665356,
            55: 1.8265085210677226e-09,
            65: 5208481.3827695325,
            143: 4858166.184415171,
        }
        for quotient, expected in expected_norms.items():
            self.assertAlmostEqual(
                receipt["component_norms"][quotient], expected,
                places=5)
        self.assertAlmostEqual(
            receipt["component_self_energy_total"],
            170481491158026.06, places=1)
        self.assertAlmostEqual(
            receipt["total_cross_term"], -21830839163.179787,
            places=3)
        self.assertAlmostEqual(
            receipt["cross_term_to_self_energy_ratio"],
            -.00012805401345852797, places=15)
        self.assertAlmostEqual(
            receipt["aggregate_centered_energy"],
            170459660318862.78, places=1)
        self.assertAlmostEqual(
            receipt["aggregate_centered_l2"],
            13056020.07959787, places=5)
        self.assertLess(
            receipt["energy_reconstruction_relative_error"], 1e-12)
        self.assertAlmostEqual(
            receipt["minimum_offdiagonal_normalized_real_gram"],
            -.0010025610827496898, places=15)
        self.assertAlmostEqual(
            receipt["maximum_offdiagonal_normalized_real_gram"],
            .015594243759942, places=15)
        self.assertFalse(receipt[
            "substantial_negative_pairwise_cancellation_observed"])
        self.assertTrue(receipt["net_negative_cross_term_observed"])
        self.assertFalse(receipt["signed_prime_correlation_estimate_proved"])
        self.assertFalse(receipt["formal_signed_error_identification_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_exact_projected_pairwise_gram_confirms_tiny_cancellation(self):
        receipt = exact_projected_pairwise_gram_receipt()
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["quotients"], (77, 35, 55, 65, 143))
        self.assertAlmostEqual(
            receipt["component_norms"][77], 2710319.2141819294,
            places=5)
        self.assertAlmostEqual(
            receipt["component_self_energy_total"],
            177711977814605.75, places=1)
        self.assertAlmostEqual(
            receipt["total_cross_term"], -49001591515.2,
            places=1)
        self.assertAlmostEqual(
            receipt["cross_term_to_self_energy_ratio"],
            -.00027573600900621266, places=15)
        self.assertAlmostEqual(
            receipt["aggregate_centered_energy"],
            177662976223090.56, places=1)
        self.assertAlmostEqual(
            receipt["minimum_offdiagonal_normalized_real_gram"],
            -.000820360879454023, places=15)
        self.assertAlmostEqual(
            receipt["maximum_offdiagonal_normalized_real_gram"],
            .0004938794511773014, places=15)
        self.assertFalse(receipt[
            "substantial_negative_pairwise_cancellation_observed"])
        self.assertTrue(receipt["net_negative_cross_term_observed"])
        self.assertTrue(receipt["exact_projected_pairwise_gram_confirmed"])
        self.assertFalse(receipt["original_outer_assembly_fully_verified"])
        self.assertFalse(receipt["signed_prime_correlation_estimate_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_combined_coefficient_admissible_mains_are_positive(self):
        receipt = combined_coefficient_admissible_main_receipt()
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["even_target_residue_count"], 5005)
        self.assertEqual(receipt["unit_group_order"], 2880)
        self.assertEqual(receipt["minimum_admissible_unit_count"], 1485)
        self.assertEqual(receipt["maximum_admissible_unit_count"], 2880)
        self.assertEqual(receipt["minimum_local_main_residue"], 4124)
        self.assertAlmostEqual(
            receipt["minimum_local_main_value"].real,
            39463390.92458851, places=5)
        self.assertEqual(receipt["maximum_local_main_residue"], 7140)
        self.assertAlmostEqual(
            receipt["maximum_local_main_value"].real,
            133823614.44192465, places=5)
        self.assertEqual(receipt["negative_local_main_residue_count"], 0)
        self.assertEqual(receipt["near_zero_local_main_residue_count"], 0)
        self.assertLess(
            receipt["maximum_local_main_imaginary_part"], 1e-5)
        self.assertAlmostEqual(
            receipt["mean_local_main_real"],
            72921965.97002855, places=5)
        self.assertAlmostEqual(
            receipt["minimum_to_mean_local_main_ratio"],
            .5411728880267469, places=14)
        self.assertEqual(
            receipt["local_main_quantiles"]["0%"]["residue"], 4124)
        self.assertEqual(
            receipt["local_main_quantiles"]["100%"]["residue"], 7140)
        self.assertEqual(len(receipt["smallest_local_main_rows"]), 12)
        self.assertEqual(len(receipt["largest_local_main_rows"]), 12)
        self.assertTrue(receipt["all_local_mains_positive"])
        self.assertTrue(receipt[
            "fixed_positive_local_main_for_all_even_classes"])
        self.assertTrue(receipt["local_main_profile_measured"])
        self.assertFalse(receipt["pointwise_error_estimate_proved"])
        self.assertFalse(receipt["signed_prime_correlation_estimate_proved"])
        self.assertFalse(receipt["formal_signed_error_identification_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_q77_original_strict_central_action_matches_assembled(self):
        receipt = q77_original_strict_central_action_receipt()
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["common_modulus"], 130)
        self.assertEqual(receipt["quotient"], 77)
        self.assertEqual(receipt["lag"], 130)
        self.assertEqual(receipt["unit_group_order"], 48)
        self.assertEqual(receipt["period_to_common_quotient_factor"], 77)
        self.assertEqual(receipt["unit_fiber_size_over_U130"], 60)
        self.assertEqual(
            receipt["ordered_pair_convention"],
            "ordered; no factor 1/2 is inserted")
        self.assertFalse(receipt["nonunit_prime_pairs"])
        self.assertLess(
            receipt["maximum_coefficient_vector_relative_error"], 1e-12)
        self.assertLess(
            receipt["maximum_assembled_action_relative_error"], 1e-12)
        self.assertLess(
            receipt["maximum_original_receipt_action_relative_error"], 1e-12)
        self.assertLess(
            receipt[
                "maximum_principal_plus_shadow_action_relative_error"],
            1e-12)
        self.assertTrue(receipt[
            "q77_original_equals_assembled_coefficient_vector"])
        self.assertTrue(receipt[
            "q77_original_action_equals_assembled_coefficient_action"])
        self.assertFalse(receipt["endpoint_or_noncentral_terms_analyzed"])
        self.assertFalse(receipt["full_outer_assembly_identification_proved"])
        self.assertFalse(receipt["formal_signed_error_identification_proved"])
        self.assertFalse(receipt[
            "pointwise_signed_prime_correlation_estimate_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_holdout_original_projected_actions_match_assembled(self):
        receipt = holdout_original_projected_action_audit_receipt()
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["audited_quotients"], (35, 55, 65, 143))
        self.assertEqual(receipt["targets"], (1000, 1002))
        self.assertFalse(receipt["nonunit_prime_pairs"])
        for quotient in receipt["audited_quotients"]:
            row = receipt["quotient_rows"][quotient]
            self.assertLess(row["coefficient_vector_relative_error"], 1e-9)
            self.assertLess(row["maximum_action_relative_error"], 1e-9)
        self.assertLess(receipt["maximum_action_relative_error"], 1e-9)
        self.assertTrue(receipt[
            "holdout_original_projected_actions_equal_assembled_components"])
        self.assertTrue(receipt["q77_linked_row_audit_separate"])
        self.assertFalse(receipt["pointwise_error_estimate_proved"])
        self.assertFalse(receipt["signed_prime_correlation_estimate_proved"])
        self.assertFalse(receipt["formal_signed_error_identification_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_combined_coefficient_prime_correlation_diagnostic(self):
        receipt = combined_coefficient_prime_correlation_diagnostic_receipt(
            target_minimum=10000, target_maximum=10100)
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["target_range"], (10000, 10100))
        self.assertEqual(receipt["tested_target_count"], 51)
        self.assertEqual(receipt["covered_even_residue_count"], 51)
        self.assertEqual(receipt["unit_group_order"], 2880)
        self.assertFalse(receipt["nonunit_or_inadmissible_prime_pairs"])
        self.assertTrue(receipt["finite_prime_correlation_diagnostic_measured"])
        self.assertFalse(receipt["pointwise_error_estimate_proved"])
        self.assertFalse(receipt["signed_prime_correlation_estimate_proved"])
        self.assertFalse(receipt["formal_signed_error_identification_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_combined_coefficient_negative_residue_lift_diagnostic(self):
        receipt = combined_coefficient_negative_residue_lift_receipt(
            base_target_minimum=10000, base_target_maximum=10100,
            additional_period_lifts=(0, 1))
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["base_target_range"], (10000, 10100))
        self.assertEqual(receipt["base_tested_target_count"], 51)
        self.assertEqual(receipt["base_covered_even_residue_count"], 51)
        self.assertEqual(receipt["additional_period_lifts"], (0, 1))
        self.assertEqual(
            receipt["tested_negative_residue_count"],
            receipt["base_negative_target_count"])
        self.assertTrue(receipt[
            "negative_residue_lift_diagnostic_measured"])
        self.assertFalse(receipt["pointwise_error_estimate_proved"])
        self.assertFalse(receipt["signed_prime_correlation_estimate_proved"])
        self.assertFalse(receipt["formal_signed_error_identification_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_combined_coefficient_period_cycle_envelope_diagnostic(self):
        receipt = combined_coefficient_period_cycle_envelope_receipt(
            cycle_count=1, targets_per_cycle=21)
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["cycle_count"], 1)
        self.assertEqual(receipt["targets_per_cycle"], 21)
        self.assertEqual(receipt["full_cycle_targets"], 5005)
        self.assertFalse(receipt["full_cycles_scanned"])
        self.assertEqual(
            receipt["cycle_rows"][0]["tested_target_count"], 21)
        self.assertEqual(
            receipt["cycle_rows"][0]["covered_even_residue_count"], 21)
        self.assertTrue(receipt["period_cycle_envelope_measured"])
        self.assertFalse(receipt["pointwise_error_estimate_proved"])
        self.assertFalse(receipt["signed_prime_correlation_estimate_proved"])
        self.assertFalse(receipt["formal_signed_error_identification_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_combined_coefficient_uniform_residue_margin(self):
        receipt = combined_coefficient_uniform_residue_margin_receipt(
            target_minimum=10000, target_maximum=10040)
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["even_target_residue_count"], 5005)
        self.assertEqual(receipt["target_range"], (10000, 10040))
        self.assertEqual(receipt["tested_target_count"], 21)
        self.assertGreater(
            receipt["minimum_sufficient_uniform_relative_error_margin"], 0)
        self.assertTrue(receipt["uniform_residue_margin_computed"])
        self.assertFalse(receipt["pointwise_error_estimate_proved"])
        self.assertFalse(receipt["signed_prime_correlation_estimate_proved"])
        self.assertFalse(receipt["formal_signed_error_identification_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_combined_coefficient_support_descent(self):
        receipt = combined_coefficient_support_descent_receipt()
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["unit_group_order"], 2880)
        self.assertEqual(receipt["factor_primes"], (5, 7, 11, 13))
        self.assertLess(
            receipt["component_reconstruction_relative_error"], 1e-12)
        self.assertLess(
            receipt["maximum_support_descent_relative_error"], 1e-12)
        self.assertEqual(
            receipt["nonzero_natural_moduli"],
            (10, 14, 22, 26, 70, 130, 154, 286))
        self.assertTrue(receipt[
            "all_nonzero_supports_descend_to_lower_moduli"])
        self.assertTrue(receipt[
            "full_modulus_uniformity_not_required_by_coefficient_structure"])
        self.assertTrue(receipt["support_descent_measured"])
        self.assertFalse(receipt["pointwise_error_estimate_proved"])
        self.assertFalse(receipt["signed_prime_correlation_estimate_proved"])
        self.assertFalse(receipt["formal_signed_error_identification_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_combined_coefficient_support_contribution_diagnostic(self):
        receipt = combined_coefficient_support_contribution_receipt(
            targets=(10424,))
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["targets"], (10424,))
        self.assertIn("principal", receipt["component_labels"])
        self.assertIn((11, 13), receipt["component_labels"])
        self.assertLess(
            receipt["maximum_support_reconstruction_relative_error"], 1e-12)
        row = receipt["rows"][10424]
        self.assertEqual(row["ordered_central_prime_pair_count"], 68)
        self.assertAlmostEqual(
            row["direct_weighted_prime_correlation"].real,
            -139240044.1764004, places=4)
        self.assertEqual(row["largest_negative_support"], (11, 13))
        self.assertTrue(receipt["support_contribution_diagnostic_measured"])
        self.assertFalse(receipt["pointwise_error_estimate_proved"])
        self.assertFalse(receipt["signed_prime_correlation_estimate_proved"])
        self.assertFalse(receipt["formal_signed_error_identification_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_combined_coefficient_centered_error_envelope(self):
        receipt = combined_coefficient_centered_error_envelope_receipt(
            cycle_count=1, targets_per_cycle=21)
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertAlmostEqual(
            receipt["principal_mean"].real, 44002.512499999146,
            places=7)
        self.assertEqual(receipt["cycle_count"], 1)
        self.assertEqual(receipt["targets_per_cycle"], 21)
        self.assertEqual(receipt["full_cycle_targets"], 5005)
        self.assertEqual(
            receipt["cycle_rows"][0]["tested_target_count"], 21)
        self.assertTrue(receipt["centered_error_envelope_measured"])
        self.assertFalse(receipt["pointwise_error_estimate_proved"])
        self.assertFalse(receipt["signed_prime_correlation_estimate_proved"])
        self.assertFalse(receipt["formal_signed_error_identification_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_combined_coefficient_support_cycle_envelope(self):
        receipt = combined_coefficient_support_cycle_envelope_receipt(
            cycle_count=1, targets_per_cycle=21)
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertAlmostEqual(
            receipt["principal_mean"].real, 44002.512499999146,
            places=7)
        self.assertIn((11, 13), receipt["component_supports"])
        self.assertEqual(receipt["cycle_count"], 1)
        self.assertEqual(receipt["targets_per_cycle"], 21)
        self.assertEqual(receipt["full_cycle_targets"], 5005)
        self.assertEqual(
            receipt["cycle_rows"][0]["tested_target_count"], 21)
        self.assertTrue(receipt["support_cycle_envelope_measured"])
        self.assertFalse(receipt["pointwise_error_estimate_proved"])
        self.assertFalse(receipt["signed_prime_correlation_estimate_proved"])
        self.assertFalse(receipt["formal_signed_error_identification_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_combined_coefficient_lower_modulus_deviation(self):
        receipt = combined_coefficient_lower_modulus_deviation_receipt(
            targets=(10424,))
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["targets"], (10424,))
        self.assertEqual(
            receipt["supports"], ((11, 13), (5, 7), (7, 11)))
        self.assertTrue(receipt["lower_modulus_deviation_measured"])
        row = receipt["rows"][10424]
        self.assertEqual(row["ordered_central_prime_pair_count"], 68)
        q286 = row["support_rows"][(11, 13)]
        self.assertEqual(q286["natural_modulus"], 286)
        self.assertAlmostEqual(
            q286["actual_to_principal_ratio"],
            -.9583193935945982, places=14)
        self.assertAlmostEqual(
            q286["local_prediction_to_principal_ratio"],
            .01222267157852989, places=14)
        self.assertAlmostEqual(
            q286["deviation_to_principal_ratio"],
            -.970542065173128, places=14)
        self.assertTrue(receipt["any_support_local_prediction_has_bad_sign"])
        self.assertFalse(receipt[
            "dominant_support_local_prediction_has_bad_sign"])
        self.assertTrue(receipt[
            "q286_local_prediction_positive_on_all_targets"])
        self.assertTrue(receipt[
            "dominant_support_deviation_is_q286_on_all_targets"])
        self.assertFalse(receipt["pointwise_error_estimate_proved"])
        self.assertFalse(receipt["signed_prime_correlation_estimate_proved"])
        self.assertFalse(receipt["formal_signed_error_identification_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_q286_residue_discrepancy_profile(self):
        receipt = q286_residue_discrepancy_profile_receipt(
            targets=(10424,), top_count=5)
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["support"], (11, 13))
        self.assertEqual(receipt["natural_modulus"], 286)
        self.assertEqual(receipt["targets"], (10424,))
        self.assertEqual(receipt["top_count"], 5)
        self.assertTrue(
            receipt["q286_residue_discrepancy_profile_measured"])
        self.assertLess(
            receipt["maximum_deviation_reconstruction_error"], 1e-12)
        self.assertTrue(
            receipt["all_weight_coefficient_correlations_negative"])
        self.assertTrue(
            receipt["all_negative_coefficient_weights_overrepresented"])
        self.assertTrue(
            receipt["all_top_negative_lists_show_two_sided_imbalance"])
        row = receipt["rows"][10424]
        self.assertEqual(row["ordered_central_prime_pair_count"], 68)
        self.assertEqual(row["admissible_residue_count"], 99)
        self.assertAlmostEqual(
            row["deviation_to_principal_ratio"],
            -.970542065173128, places=14)
        self.assertLess(row["weight_coefficient_real_correlation"], 0.0)
        self.assertGreater(row["cauchy_bound_to_principal_ratio"], 1.0)
        self.assertLess(row["actual_abs_fraction_of_cauchy_bound"], 1.0)
        self.assertGreater(
            row["l2_deviation_to_total_weight"],
            row["unit_principal_l2_sufficiency_threshold"])
        self.assertFalse(row["l2_sufficiency_for_unit_principal_satisfied"])
        self.assertGreater(
            row["negative_coefficient_weight_to_uniform_ratio"], 1.0)
        self.assertLess(
            row["positive_coefficient_weight_to_uniform_ratio"], 1.0)
        self.assertEqual(
            len(row["top_negative_deviation_rows"]), 5)
        self.assertGreater(
            row["top_negative_underweighted_positive_count"], 0)
        self.assertGreater(
            row["top_negative_overweighted_negative_count"], 0)
        self.assertGreater(
            row["top_negative_deviation_rows"][0]["coefficient_real"], 0.0)
        self.assertLess(
            row["top_negative_deviation_rows"][0][
                "weight_to_uniform_ratio"], 1.0)
        self.assertLess(
            row["top_negative_deviation_rows"][0][
                "deviation_to_principal_ratio"], 0.0)
        self.assertFalse(receipt["pointwise_error_estimate_proved"])
        self.assertFalse(receipt["signed_prime_correlation_estimate_proved"])
        self.assertFalse(receipt["formal_signed_error_identification_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_q286_character_imbalance(self):
        receipt = q286_character_imbalance_receipt(
            targets=(10424,), top_count=5)
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["support"], (11, 13))
        self.assertEqual(receipt["natural_modulus"], 286)
        self.assertEqual(receipt["odd_primes"], (11, 13))
        self.assertEqual(receipt["unit_group_order"], 120)
        self.assertEqual(receipt["character_count"], 120)
        self.assertEqual(receipt["active_character_count"], 59)
        self.assertEqual(receipt["active_both_prime_support_count"], 59)
        self.assertTrue(
            receipt["active_labels_all_have_both_prime_support"])
        self.assertLess(receipt["coefficient_reconstruction_error"], 1e-12)
        self.assertLess(
            receipt["maximum_deviation_reconstruction_error"], 1e-12)
        row = receipt["rows"][10424]
        self.assertEqual(row["admissible_residue_count"], 99)
        self.assertAlmostEqual(
            row["deviation_to_principal_ratio"],
            -.970542065173128, places=14)
        self.assertEqual(len(row["top_negative_character_rows"]), 5)
        self.assertLess(
            row["top_negative_character_rows"][0][
                "contribution_to_principal_ratio"], 0.0)
        self.assertTrue(receipt["q286_character_imbalance_measured"])
        self.assertFalse(receipt["pointwise_error_estimate_proved"])
        self.assertFalse(receipt["signed_prime_correlation_estimate_proved"])
        self.assertFalse(receipt["formal_signed_error_identification_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_q286_character_matrix_structure(self):
        receipt = q286_character_matrix_structure_receipt(leading_count=4)
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["support"], (11, 13))
        self.assertEqual(receipt["natural_modulus"], 286)
        self.assertEqual(receipt["matrix_shape"], (9, 11))
        self.assertEqual(receipt["active_character_count"], 59)
        self.assertEqual(receipt["active_entry_count"], 59)
        self.assertEqual(receipt["numerical_rank"], 9)
        self.assertEqual(receipt["relative_numerical_rank"], 9)
        self.assertAlmostEqual(
            receipt["top_two_singular_energy_fraction"],
            .9760410444893589, places=14)
        self.assertAlmostEqual(
            receipt["top_four_singular_energy_fraction"],
            .9970750809967631, places=14)
        self.assertTrue(
            receipt["low_rank_compression_diagnostic_passes"])
        self.assertFalse(receipt["exact_low_rank_proved"])
        self.assertFalse(receipt["signed_prime_correlation_estimate_proved"])
        self.assertFalse(receipt["formal_signed_error_identification_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_dominant_support_character_matrix_structure(self):
        receipt = dominant_support_character_matrix_structure_receipt(
            leading_count=4)
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(
            receipt["supports"], ((11, 13), (7, 11), (5, 7)))
        self.assertTrue(
            receipt[
                "dominant_support_character_matrix_structure_measured"])
        self.assertTrue(
            receipt["all_supports_have_both_prime_character_support"])
        self.assertIn((11, 13), receipt["support_rows"])
        self.assertIn((7, 11), receipt["support_rows"])
        self.assertIn((5, 7), receipt["support_rows"])
        self.assertTrue(receipt["all_supports_have_low_rank_compression"])
        self.assertAlmostEqual(
            receipt["support_rows"][(11, 13)][
                "top_two_singular_energy_fraction"],
            .9760410444893589, places=14)
        self.assertAlmostEqual(
            receipt["support_rows"][(7, 11)][
                "top_two_singular_energy_fraction"],
            .906627345943789, places=14)
        self.assertAlmostEqual(
            receipt["support_rows"][(5, 7)][
                "top_two_singular_energy_fraction"],
            .9915109122214548, places=14)
        self.assertFalse(receipt["exact_low_rank_proved"])
        self.assertFalse(receipt["signed_prime_correlation_estimate_proved"])
        self.assertFalse(receipt["formal_signed_error_identification_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_dominant_support_singular_tail_scan(self):
        receipt = dominant_support_singular_tail_scan_receipt(
            targets_per_cycle=9)
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["start"], 10000)
        self.assertEqual(receipt["targets_per_cycle"], 9)
        self.assertEqual(
            receipt["support_modes"],
            (((11, 13), 6), ((7, 11), 5), ((5, 7), 3)))
        self.assertIn((11, 13), receipt["support_rows"])
        self.assertIn((7, 11), receipt["support_rows"])
        self.assertIn((5, 7), receipt["support_rows"])
        self.assertTrue(
            receipt["combined_dominant_singular_tail_scan_measured"])
        self.assertLess(receipt["maximum_tail_reconstruction_error"], 1e-12)
        self.assertFalse(receipt["signed_prime_correlation_estimate_proved"])
        self.assertFalse(receipt["formal_signed_error_identification_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_q286_singular_mode_approximation(self):
        receipt = q286_singular_mode_approximation_receipt(
            targets=(10424,), modes=(1, 2, 4, 9))
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["support"], (11, 13))
        self.assertEqual(receipt["natural_modulus"], 286)
        self.assertEqual(receipt["matrix_shape"], (9, 11))
        self.assertEqual(receipt["tested_modes"], (1, 2, 4, 9))
        self.assertLess(
            receipt["maximum_full_singular_reconstruction_error"], 1e-12)
        row = receipt["rows"][10424]
        self.assertAlmostEqual(
            row["deviation_to_principal_ratio"],
            -.970542065173128, places=14)
        self.assertAlmostEqual(
            row["mode_rows"][2]["approximation_to_deviation_ratio"],
            .9015985110298353, places=14)
        self.assertAlmostEqual(
            row["mode_rows"][4]["approximation_to_deviation_ratio"],
            1.0068394435381816, places=14)
        self.assertLess(
            row["mode_rows"][4][
                "absolute_residual_to_abs_deviation_ratio"], .01)
        self.assertTrue(
            receipt["top_two_modes_explain_sampled_signed_deviation"])
        self.assertTrue(
            receipt["top_four_modes_leave_small_sampled_signed_residual"])
        self.assertFalse(receipt["top_four_tail_paid_by_cauchy"])
        self.assertTrue(receipt["singular_mode_approximation_measured"])
        self.assertFalse(receipt["signed_prime_correlation_estimate_proved"])
        self.assertFalse(receipt["formal_signed_error_identification_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_q286_leading_singular_mode_contribution(self):
        receipt = q286_leading_singular_mode_contribution_receipt(
            targets=(10424, 14138, 14680, 88346), mode_count=6)
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["support"], (11, 13))
        self.assertEqual(receipt["natural_modulus"], 286)
        self.assertEqual(receipt["targets"], (10424, 14138, 14680, 88346))
        self.assertEqual(receipt["mode_count"], 6)
        self.assertEqual(len(receipt["singular_values"]), 6)
        self.assertLess(receipt["maximum_mode_reconstruction_error"], 1e-12)
        row = receipt["rows"][10424]
        self.assertEqual(len(row["mode_rows"]), 6)
        self.assertAlmostEqual(
            row["q286_deviation_to_principal_ratio"],
            -.970542065173128, places=14)
        self.assertAlmostEqual(
            row["modeled_sum_to_principal_ratio"],
            -.9618075775131865, places=14)
        self.assertEqual(receipt["common_negative_mode_indices"], (1, 2, 3))
        self.assertTrue(receipt["all_targets_have_multiple_negative_modes"])
        self.assertFalse(receipt["single_mode_obstruction_found"])
        self.assertTrue(
            receipt["leading_singular_mode_contribution_measured"])
        self.assertFalse(receipt["signed_prime_correlation_estimate_proved"])
        self.assertFalse(receipt["formal_signed_error_identification_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_q286_leading_mode_cycle_profile(self):
        receipt = q286_leading_mode_cycle_profile_receipt(
            targets_per_cycle=9, mode_count=6)
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["support"], (11, 13))
        self.assertEqual(receipt["natural_modulus"], 286)
        self.assertEqual(receipt["start"], 10000)
        self.assertEqual(receipt["targets_per_cycle"], 9)
        self.assertEqual(receipt["tested_target_count"], 9)
        self.assertEqual(receipt["mode_count"], 6)
        self.assertIn(1, receipt["mode_stats"])
        self.assertEqual(len(receipt["mode_stats"]), 6)
        self.assertTrue(receipt["leading_mode_cycle_profile_measured"])
        self.assertFalse(receipt["signed_prime_correlation_estimate_proved"])
        self.assertFalse(receipt["formal_signed_error_identification_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_q286_separable_mode_coefficient(self):
        receipt = q286_separable_mode_coefficient_receipt(
            mode_count=6, top_count=4)
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["support"], (11, 13))
        self.assertEqual(receipt["natural_modulus"], 286)
        self.assertEqual(receipt["mode_count"], 6)
        self.assertEqual(len(receipt["mode_rows"]), 6)
        self.assertLess(
            receipt["maximum_factorization_reconstruction_error"], 1e-12)
        self.assertTrue(receipt["all_modes_have_mixed_residue_signs"])
        self.assertAlmostEqual(
            receipt["mode_rows"][0]["singular_value"],
            158279.0938376038, places=7)
        self.assertFalse(receipt["signed_prime_correlation_estimate_proved"])
        self.assertFalse(receipt["formal_signed_error_identification_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_q286_leading_mode_character_shape(self):
        receipt = q286_leading_mode_character_shape_receipt(
            mode_count=3, top_count=3)
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["support"], (11, 13))
        self.assertEqual(receipt["natural_modulus"], 286)
        self.assertEqual(receipt["mode_count"], 3)
        self.assertEqual(len(receipt["mode_rows"]), 3)
        self.assertGreater(
            receipt["minimum_left_effective_character_count"], 3.0)
        self.assertGreater(
            receipt["minimum_right_effective_character_count"], 3.0)
        self.assertLess(
            receipt["maximum_side_character_energy_fraction"], 0.5)
        self.assertTrue(receipt["no_single_character_mode_found"])
        self.assertTrue(receipt["leading_mode_character_shape_measured"])
        self.assertFalse(receipt["single_character_estimate_suffices"])
        self.assertFalse(receipt["signed_prime_correlation_estimate_proved"])
        self.assertFalse(receipt["formal_signed_error_identification_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_q286_separable_mode_local_bias(self):
        receipt = q286_separable_mode_local_bias_receipt(
            targets_per_cycle=9, mode_count=6)
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["support"], (11, 13))
        self.assertEqual(receipt["natural_modulus"], 286)
        self.assertEqual(receipt["start"], 10000)
        self.assertEqual(receipt["targets_per_cycle"], 9)
        self.assertEqual(receipt["tested_target_count"], 9)
        self.assertEqual(receipt["mode_count"], 6)
        self.assertEqual(len(receipt["mode_stats"]), 6)
        self.assertGreater(
            receipt["maximum_mode_approximation_residual_fraction"], 0.0)
        self.assertIn("local_bias_means_near_zero_on_sample", receipt)
        self.assertTrue(receipt["all_modes_have_prime_deviation_variation"])
        self.assertTrue(receipt["separable_mode_local_bias_measured"])
        self.assertFalse(receipt["signed_prime_correlation_estimate_proved"])
        self.assertFalse(receipt["formal_signed_error_identification_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_q286_leading_mode_lift_decay(self):
        receipt = q286_leading_mode_lift_decay_receipt(
            base_targets=(10424,), lifts=(0, 1), mode_count=6)
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["support"], (11, 13))
        self.assertEqual(receipt["natural_modulus"], 286)
        self.assertEqual(receipt["base_targets"], (10424,))
        self.assertEqual(receipt["lifts"], (0, 1))
        self.assertEqual(receipt["mode_count"], 6)
        self.assertIn(10424, receipt["rows"])
        self.assertIn(0, receipt["rows"][10424]["lift_rows"])
        self.assertIn(1, receipt["rows"][10424]["lift_rows"])
        self.assertTrue(receipt["leading_mode_lift_decay_measured"])
        self.assertFalse(receipt["eventual_decay_proved"])
        self.assertFalse(receipt["signed_prime_correlation_estimate_proved"])
        self.assertFalse(receipt["formal_signed_error_identification_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_q286_significant_lift_envelope(self):
        receipt = q286_significant_lift_envelope_receipt(
            start=10400, targets_per_cycle=21, lifts=(0, 1),
            max_base_targets=3)
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["support"], (11, 13))
        self.assertEqual(receipt["natural_modulus"], 286)
        self.assertEqual(receipt["start"], 10400)
        self.assertEqual(receipt["targets_per_cycle"], 21)
        self.assertEqual(receipt["lifts"], (0, 1))
        self.assertLessEqual(
            receipt["selected_base_target_count"],
            receipt["available_base_target_count"])
        self.assertTrue(receipt["significant_lift_envelope_measured"])
        self.assertFalse(receipt["eventual_decay_proved"])
        self.assertFalse(receipt["signed_prime_correlation_estimate_proved"])
        self.assertFalse(receipt["formal_signed_error_identification_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_q286_leading_mode_period_envelope(self):
        receipt = q286_leading_mode_period_envelope_receipt(
            cycle_count=1, targets_per_cycle=9)
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["support"], (11, 13))
        self.assertEqual(receipt["natural_modulus"], 286)
        self.assertEqual(receipt["cycle_count"], 1)
        self.assertEqual(receipt["targets_per_cycle"], 9)
        self.assertEqual(receipt["tested_target_count"], 9)
        self.assertIn(0, receipt["cycle_rows"])
        self.assertTrue(receipt["leading_mode_period_envelope_measured"])
        self.assertFalse(receipt["eventual_decay_proved"])
        self.assertFalse(receipt["signed_prime_correlation_estimate_proved"])
        self.assertFalse(receipt["formal_signed_error_identification_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_reduced_full_lower_envelope(self):
        receipt = reduced_full_lower_envelope_receipt(targets_per_cycle=9)
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["start"], 10000)
        self.assertEqual(receipt["targets_per_cycle"], 9)
        self.assertEqual(receipt["q286_mode_count"], 6)
        self.assertEqual(receipt["tested_target_count"], 9)
        self.assertFalse(receipt["residue_weights_included"])
        self.assertIn((11, 13), receipt["support_order"])
        row = receipt["rows"][10000]
        self.assertEqual(len(row["q286_mode_rows"]), 6)
        mode_sum = sum(
            mode_row["contribution_to_principal_ratio"]
            for mode_row in row["q286_mode_rows"])
        self.assertAlmostEqual(
            mode_sum + row["q286_mode_residual_to_principal_ratio"],
            row["q286_deviation_to_principal_ratio"],
            places=12)
        self.assertTrue(receipt["reduced_full_lower_envelope_measured"])
        self.assertLess(receipt["maximum_reconstruction_error"], 1e-12)
        self.assertFalse(receipt["signed_prime_correlation_estimate_proved"])
        self.assertFalse(receipt["formal_signed_error_identification_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_reduced_full_lower_envelope_cycle_scan(self):
        receipt = reduced_full_lower_envelope_cycle_scan_receipt(
            cycle_count=1, targets_per_cycle=9)
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["start"], 10000)
        self.assertEqual(receipt["cycle_count"], 1)
        self.assertEqual(receipt["targets_per_cycle"], 9)
        self.assertEqual(receipt["q286_mode_count"], 6)
        self.assertEqual(receipt["tested_target_count"], 9)
        self.assertIn(0, receipt["cycle_rows"])
        self.assertTrue(
            receipt["all_full_negatives_captured_by_reduced_model"])
        self.assertTrue(receipt["all_reduced_and_full_signs_agree"])
        self.assertTrue(
            receipt["reduced_full_lower_envelope_cycle_scan_measured"])
        self.assertFalse(receipt["eventual_lower_envelope_proved"])
        self.assertFalse(receipt["signed_prime_correlation_estimate_proved"])
        self.assertFalse(receipt["formal_signed_error_identification_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_q286_first_two_mode_lower_tail(self):
        receipt = q286_first_two_mode_lower_tail_receipt(
            selected_targets=(10000, 10002, 10004))
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["support"], (11, 13))
        self.assertEqual(receipt["natural_modulus"], 286)
        self.assertEqual(receipt["start"], 10000)
        self.assertEqual(receipt["cycle_count"], 1)
        self.assertEqual(receipt["targets_per_cycle"], 3)
        self.assertEqual(receipt["tested_target_count"], 3)
        self.assertFalse(receipt["residue_weights_included"])
        self.assertEqual(receipt["selected_targets"], (10000, 10002, 10004))
        self.assertIn(10000, receipt["rows"])
        row = receipt["rows"][10000]
        self.assertIn("first_two_modes_to_principal_ratio", row)
        self.assertIn("full_without_first_two_to_principal_ratio", row)
        self.assertIn("first_three_modes_to_principal_ratio", row)
        self.assertIn("full_without_first_three_to_principal_ratio", row)
        self.assertTrue(receipt["first_two_mode_lower_tail_measured"])
        self.assertFalse(
            receipt["first_two_modes_alone_prove_lower_envelope"])
        self.assertFalse(receipt["eventual_lower_envelope_proved"])
        self.assertFalse(receipt["signed_prime_correlation_estimate_proved"])
        self.assertFalse(receipt["formal_signed_error_identification_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_q286_first_three_ap_discrepancy_proxy(self):
        receipt = q286_first_three_ap_discrepancy_proxy_receipt(
            selected_targets=(10424, 14138), top_count=3)
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["support"], (11, 13))
        self.assertEqual(receipt["natural_modulus"], 286)
        self.assertEqual(receipt["tested_target_count"], 2)
        self.assertEqual(receipt["selected_targets"], (10424, 14138))
        self.assertIn(10424, receipt["rows"])
        row = receipt["rows"][10424]
        self.assertIn("maximum_relative_residue_deviation", row)
        self.assertIn("required_uniform_relative_error_for_actual_first_three",
                      row)
        self.assertIn("negative_first_three_mode_count", receipt)
        self.assertIn(
            "largest_required_uniform_relative_error_on_negative_first_three",
            receipt)
        self.assertEqual(len(row["largest_negative_residue_rows"]), 3)
        self.assertEqual(len(row["largest_positive_residue_rows"]), 3)
        self.assertEqual(len(row["largest_abs_residue_rows"]), 3)
        self.assertIn("signed_to_absolute_real_contribution_ratio", row)
        self.assertLess(receipt["maximum_mode_reconstruction_error"], 1e-12)
        self.assertTrue(
            receipt["first_three_ap_discrepancy_proxy_measured"])
        self.assertFalse(receipt["ordinary_ap_discrepancy_estimate_proved"])
        self.assertFalse(receipt["signed_prime_correlation_estimate_proved"])
        self.assertFalse(receipt["formal_signed_error_identification_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_q286_first_three_full_negative_driver(self):
        receipt = q286_first_three_full_negative_driver_receipt(
            targets_per_cycle=9, top_count=3)
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["support"], (11, 13))
        self.assertEqual(receipt["natural_modulus"], 286)
        self.assertEqual(receipt["start"], 10000)
        self.assertEqual(receipt["targets_per_cycle"], 9)
        self.assertEqual(receipt["driver_residues"], (133, 153))
        self.assertIn("full_negative_target_count", receipt)
        self.assertIn("driver_residue_top_negative_counts", receipt)
        self.assertIn("driver_residue_occupancy_counts", receipt)
        if receipt["full_negative_target_count"]:
            target = receipt["full_negative_targets"][0]
            self.assertIn("driver_residue_occupancy_rows",
                          receipt["target_rows"][target])
        self.assertTrue(receipt["full_negative_driver_measured"])
        self.assertFalse(receipt["driver_residues_explain_all_negatives"])
        self.assertFalse(receipt["signed_prime_correlation_estimate_proved"])
        self.assertFalse(receipt["formal_signed_error_identification_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_q286_driver_residue_lift_occupancy(self):
        receipt = q286_driver_residue_lift_occupancy_receipt(
            base_targets=(10424, 14138), lifts=(0, 1))
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["support"], (11, 13))
        self.assertEqual(receipt["natural_modulus"], 286)
        self.assertEqual(receipt["base_targets"], (10424, 14138))
        self.assertEqual(receipt["lifts"], (0, 1))
        self.assertEqual(receipt["driver_residues"], (133, 153))
        self.assertEqual(receipt["tested_target_count"], 4)
        self.assertIn(0, receipt["lift_rows"])
        self.assertIn(10424, receipt["target_rows"])
        self.assertIn(10424, receipt["first_full_positive_lift_by_base"])
        self.assertIn("maximum_first_full_positive_lift", receipt)
        self.assertEqual(receipt["maximum_first_full_positive_lift"], 1)
        self.assertEqual(
            receipt["base_targets_without_positive_full_action_lift_count"],
            0)
        self.assertTrue(receipt["driver_residue_lift_occupancy_measured"])
        self.assertFalse(receipt["driver_residue_hitting_theorem_proved"])
        self.assertFalse(receipt["signed_prime_correlation_estimate_proved"])
        self.assertFalse(receipt["formal_signed_error_identification_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_q286_high_positive_residue_cover(self):
        from lcm_sawtooth_goldbach_transfer import (
            q286_high_positive_residue_cover_receipt)
        receipt = q286_high_positive_residue_cover_receipt(
            selected_targets=(10042,), top_count=12)
        self.assertEqual(receipt["uncovered_target_count"], 0)
        self.assertEqual(
            receipt["greedy_cover_rows"][0]["residue_mod_286"],
            133)
        self.assertTrue(receipt["high_positive_residue_cover_measured"])
        self.assertFalse(receipt["signed_prime_correlation_estimate_proved"])

    def test_q286_high_positive_cover_margin(self):
        from lcm_sawtooth_goldbach_transfer import (
            q286_high_positive_cover_margin_receipt)
        receipt = q286_high_positive_cover_margin_receipt(
            selected_targets=(10042,), top_count=12)
        self.assertEqual(receipt["missing_target_count"], 0)
        self.assertGreater(
            receipt["maximum_required_weight_to_flip_full_action"],
            0)
        self.assertTrue(receipt["high_positive_cover_margin_measured"])
        self.assertFalse(
            receipt["cover_residue_occupancy_lower_bound_proved"])

    def test_q286_cover_pair_compensation_portfolio(self):
        from lcm_sawtooth_goldbach_transfer import (
            q286_cover_pair_compensation_portfolio_receipt)
        receipt = q286_cover_pair_compensation_portfolio_receipt()
        self.assertEqual(receipt["uncovered_target_count"], 0)
        self.assertEqual(
            receipt[
                "greedy_positive_portfolio_rows"][0]["residue_mod_286"],
            263)
        self.assertTrue(receipt["all_first_three_modes_negative"])
        self.assertFalse(receipt["compensation_theorem_proved"])

    def test_q286_positive_both_empty_compensation_cover(self):
        from lcm_sawtooth_goldbach_transfer import (
            q286_positive_both_empty_compensation_cover_receipt)
        receipt = q286_positive_both_empty_compensation_cover_receipt(
            selected_targets=(10012, 10016), top_count=12)
        self.assertEqual(receipt["tested_target_count"], 2)
        self.assertEqual(receipt["uncovered_target_count"], 0)
        self.assertEqual(
            receipt[
                "greedy_positive_portfolio_rows"][0]["residue_mod_286"],
            263)
        first_presence = receipt["top_positive_presence_rows"][0]
        self.assertEqual(
            first_presence["negative_coefficient_deficit_count"], 2)
        self.assertEqual(
            first_presence["positive_coefficient_surplus_count"], 0)
        self.assertTrue(
            receipt["positive_both_empty_compensation_cover_measured"])
        self.assertFalse(receipt["single_compensator_proved"])

    def test_q286_residue_portfolio_local_admissibility(self):
        from lcm_sawtooth_goldbach_transfer import (
            q286_residue_portfolio_local_admissibility_receipt)
        receipt = q286_residue_portfolio_local_admissibility_receipt()
        cover = receipt["portfolio_rows"]["cover_pair"]
        self.assertEqual(
            cover["all_inadmissible_classes_mod_143"], (23, 120))
        portfolio = receipt["portfolio_rows"]["broad_positive_portfolio"]
        self.assertEqual(portfolio["at_least_one_admissible_class_count"], 143)
        self.assertEqual(portfolio["all_inadmissible_class_count"], 0)
        self.assertFalse(receipt["prime_pair_occupancy_proved"])

    def test_q286_positive_both_empty_compensation_min_cover(self):
        from lcm_sawtooth_goldbach_transfer import (
            q286_positive_both_empty_compensation_min_cover_receipt)
        receipt = q286_positive_both_empty_compensation_min_cover_receipt(
            selected_targets=(10012, 10016),
            top_count=12,
            max_cover_size=2)
        self.assertEqual(receipt["tested_target_count"], 2)
        self.assertEqual(receipt["minimum_observed_cover_size"], 1)
        self.assertTrue(receipt["observed_set_cover_measured"])
        self.assertFalse(receipt["compensation_theorem_proved"])

    def test_q286_positive_both_empty_remainder_compensation(self):
        from lcm_sawtooth_goldbach_transfer import (
            q286_positive_both_empty_remainder_compensation_receipt)
        receipt = q286_positive_both_empty_remainder_compensation_receipt(
            selected_targets=(10012, 10016))
        self.assertEqual(receipt["tested_target_count"], 2)
        self.assertEqual(receipt["first_three_negative_count"], 2)
        self.assertEqual(
            receipt["full_without_first_three_positive_count"], 2)
        self.assertTrue(receipt["remainder_compensation_measured"])
        self.assertFalse(receipt["remainder_compensation_theorem_proved"])

    def test_q286_first_three_to_complement_ratio(self):
        from lcm_sawtooth_goldbach_transfer import (
            q286_first_three_to_complement_ratio_receipt)
        receipt = q286_first_three_to_complement_ratio_receipt(
            selected_targets=(14138,))
        self.assertEqual(receipt["tested_target_count"], 1)
        self.assertEqual(receipt["worst_tail_to_complement_target"], 14138)
        self.assertGreater(
            receipt["maximum_tail_to_complement_ratio"], 40)
        self.assertTrue(
            receipt["first_three_to_complement_ratio_measured"])
        self.assertFalse(receipt["relative_tail_bound_proved"])

    def test_q286_tail_complement_lift_profile(self):
        from lcm_sawtooth_goldbach_transfer import (
            q286_tail_complement_lift_profile_receipt)
        receipt = q286_tail_complement_lift_profile_receipt(
            bases=(14138,), lifts=(0, 1))
        self.assertEqual(receipt["tested_target_count"], 2)
        self.assertEqual(receipt["ratio_greater_than_one_count"], 1)
        self.assertEqual(
            receipt["base_rows"][14138][
                "ratio_greater_than_one_lifts"],
            (0,))
        self.assertTrue(receipt["tail_complement_lift_profile_measured"])
        self.assertFalse(receipt["persistent_bad_residue_class_proved"])

    def test_q286_boundary_layer_clearance(self):
        from lcm_sawtooth_goldbach_transfer import (
            q286_boundary_layer_clearance_receipt)
        receipt = q286_boundary_layer_clearance_receipt(
            bases=(14138,), lifts=(0, 1))
        self.assertEqual(receipt["tested_target_count"], 2)
        self.assertEqual(receipt["cleared_by_lift_one_count"], 1)
        self.assertEqual(receipt["lift_one_complement_positive_count"], 1)
        self.assertTrue(
            receipt["base_rows"][14138]["ratio_clears_by_lift_one"])
        self.assertFalse(
            receipt["driver_occupancy_explains_all_clearance"])

    def test_q286_complement_cycle_envelope(self):
        from lcm_sawtooth_goldbach_transfer import (
            q286_complement_cycle_envelope_receipt)
        receipt = q286_complement_cycle_envelope_receipt(
            cycle_count=1, targets_per_cycle=3)
        self.assertEqual(receipt["tested_target_count"], 3)
        self.assertEqual(len(receipt["cycle_rows"]), 1)
        self.assertTrue(receipt["complement_cycle_envelope_measured"])
        self.assertFalse(receipt["eventual_complement_lower_bound_proved"])

    def test_q286_boundary_component_split(self):
        from lcm_sawtooth_goldbach_transfer import (
            q286_boundary_component_split_receipt)
        receipt = q286_boundary_component_split_receipt()
        self.assertEqual(receipt["targets"], (14138, 24148))
        self.assertEqual(
            receipt["minimum_full_without_first_three_target"], 14138)
        self.assertGreater(
            receipt["target_rows"][24148][
                "full_without_first_three_to_principal_ratio"],
            receipt["target_rows"][14138][
                "full_without_first_three_to_principal_ratio"])
        self.assertTrue(receipt["boundary_component_split_measured"])
        self.assertFalse(receipt["component_lower_bound_proved"])

    def test_q286_boundary_complement_support_split(self):
        receipt = q286_boundary_complement_support_split_receipt()
        self.assertEqual(receipt["targets"], (14138, 24148))
        self.assertEqual(receipt["minimum_complement_target"], 14138)
        self.assertEqual(receipt["maximum_complement_target"], 24148)
        self.assertLess(
            receipt["maximum_support_reconstruction_error"], 1e-12)
        boundary = receipt["target_rows"][14138]
        lifted = receipt["target_rows"][24148]
        self.assertAlmostEqual(
            boundary["full_without_first_three_to_principal_ratio"],
            .018073313793834367, places=14)
        self.assertEqual(
            lifted["dominant_positive_centered_support"], (5, 7))
        self.assertGreater(
            lifted["support_ratios_to_principal"][(5, 7)], .35)
        self.assertLess(
            lifted[
                "q286_deviation_after_first_three_to_principal_ratio"],
            0)
        self.assertGreater(
            lifted["full_without_first_three_to_principal_ratio"], 1.3)
        self.assertTrue(receipt[
            "boundary_complement_support_split_measured"])
        self.assertFalse(receipt["component_lower_bound_proved"])

    def test_q286_first_three_removed_support_envelope(self):
        receipt = q286_first_three_removed_support_envelope_receipt(
            selected_targets=(14138, 24148, 30164))
        self.assertEqual(receipt["tested_target_count"], 3)
        self.assertEqual(receipt["minimum_complement_target"], 14138)
        self.assertLess(
            receipt["maximum_support_reconstruction_error"], 1e-12)
        self.assertEqual(receipt["nonpositive_complement_count"], 0)
        self.assertGreater(
            receipt["rows"][24148]["q70_to_principal_ratio"], 0)
        self.assertTrue(receipt[
            "first_three_removed_support_envelope_measured"])
        self.assertFalse(receipt["eventual_complement_lower_bound_proved"])

    def test_q286_subcone_lower_support_package(self):
        receipt = q286_subcone_lower_support_package_receipt(
            targets=(1222142,), first_two_threshold=.2,
            tail_threshold=.3)
        self.assertEqual(receipt["tested_target_count"], 1)
        self.assertEqual(receipt["subcone_targets"], (1222142,))
        self.assertEqual(receipt["rescued_subcone_targets"], (1222142,))
        self.assertEqual(
            receipt["without_q70_rescued_subcone_targets"], (1222142,))
        self.assertEqual(
            receipt["lower_package_positive_subcone_targets"], (1222142,))
        row = receipt["rows"][1222142]
        self.assertLess(row["first_two_modes_to_principal_ratio"], -.2)
        self.assertLess(row["first_three_modes_to_principal_ratio"], -.3)
        self.assertGreater(
            row["visible_lower_support_package_to_principal_ratio"], 0)
        self.assertGreater(
            row["lower_support_package_rescue_margin_to_principal_ratio"], 0)
        self.assertGreater(
            row["without_q70_full_margin_to_principal_ratio"], 0)
        self.assertAlmostEqual(
            row["lower_support_package_rescue_margin_to_principal_ratio"],
            row["full_action_to_principal_ratio"], places=12)
        self.assertAlmostEqual(
            row["without_q70_package_rescue_margin_to_principal_ratio"],
            row["without_q70_full_margin_to_principal_ratio"], places=12)
        self.assertGreater(row["full_action_to_principal_ratio"], 0)
        self.assertTrue(receipt["subcone_lower_support_package_measured"])
        self.assertFalse(receipt[
            "eventual_lower_support_package_positivity_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_q286_lower_support_package_support_only_obstruction(self):
        receipt = q286_lower_support_package_support_only_obstruction_receipt()
        self.assertEqual(
            receipt["witness_subcone_failure_targets"], (10664, 14138))
        self.assertEqual(
            receipt["comparison_success_targets"],
            (1222142, 1323632, 1379072))
        self.assertTrue(receipt["all_witnesses_are_subcone_failures"])
        self.assertTrue(receipt["all_comparisons_are_subcone_successes"])
        self.assertTrue(receipt[
            "support_nonnegativity_total_mass_only_proof_refuted"])
        self.assertTrue(receipt[
            "lower_support_package_support_only_obstruction_measured"])
        self.assertFalse(receipt["support_only_rescue_theorem_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_q286_lower_support_package_local_discrepancy(self):
        receipt = q286_lower_support_package_local_discrepancy_receipt(
            targets=(1222142,))
        self.assertEqual(receipt["tested_target_count"], 1)
        self.assertEqual(receipt["subcone_targets"], (1222142,))
        self.assertEqual(receipt["raw_l2_sufficient_targets"], ())
        self.assertEqual(receipt["raw_l2_insufficient_targets"], (1222142,))
        row = receipt["rows"][1222142]
        self.assertGreater(row["local_mean_margin_to_required_floor"], 0)
        self.assertGreater(
            row["centered_lower_support_action_to_principal_ratio"], 0)
        self.assertGreater(
            row["actual_l2_relative_discrepancy"],
            row["sufficient_l2_relative_discrepancy_for_rescue"])
        self.assertFalse(row["actual_l2_bound_suffices_for_rescue"])
        self.assertTrue(receipt[
            "lower_support_package_local_discrepancy_measured"])
        self.assertFalse(receipt["raw_l2_discrepancy_theorem_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_q286_lower_support_package_component_local_discrepancy(self):
        _q286_lower_support_component_data.cache_clear()
        receipt = (
            q286_lower_support_package_component_local_discrepancy_receipt(
                targets=(1222142,)))
        self.assertEqual(receipt["tested_target_count"], 1)
        self.assertLess(
            receipt["maximum_component_reconstruction_error"], 1e-12)
        row = receipt["rows"][1222142]
        self.assertTrue(row["subcone_member"])
        self.assertTrue(row["rescued_by_full_complement"])
        self.assertEqual(row["dominant_abs_centered_support"], (7, 11))
        self.assertEqual(row["dominant_positive_centered_support"], (7, 11))
        self.assertIn((5, 7), row["negative_centered_supports"])
        self.assertGreater(
            row["local_mean_lower_support_to_principal_ratio"],
            row["required_lower_support_package_to_rescue"])
        self.assertAlmostEqual(
            row["actual_lower_support_package_to_principal_ratio"],
            row["local_mean_lower_support_to_principal_ratio"]
            + row["centered_lower_support_action_to_principal_ratio"],
            places=12)
        self.assertTrue(receipt[
            "lower_support_package_component_local_discrepancy_measured"])
        self.assertFalse(receipt[
            "component_signed_residue_weight_theorem_proved"])
        self.assertFalse(receipt["goldbach_proved"])
        misses_after_first = _q286_lower_support_component_data.cache_info().misses
        receipt_again = (
            q286_lower_support_package_component_local_discrepancy_receipt(
                targets=(1222142,)))
        cache_info = _q286_lower_support_component_data.cache_info()
        self.assertEqual(receipt_again["component_supports"],
                         receipt["component_supports"])
        self.assertEqual(cache_info.misses, misses_after_first)
        self.assertGreaterEqual(cache_info.hits, 1)

    def test_q286_lower_support_component_pair_tail_window(self):
        receipt = q286_lower_support_component_pair_tail_window_receipt(
            selected_targets=(1222142,),
            first_two_threshold=.2, tail_threshold=.3)
        self.assertEqual(receipt["tested_target_count"], 1)
        self.assertEqual(receipt["tail_subcone_targets"], (1222142,))
        self.assertEqual(
            receipt["both_pair_components_centered_negative_targets"], ())
        self.assertIsNone(receipt[
            "source_subcone_complement_window_receipt"])
        self.assertIsNotNone(receipt["source_lower_tail_receipt"])
        self.assertTrue(receipt["source_lower_tail_receipt"][
            "residue_weights_included"])
        row = receipt["rows"][1222142]
        self.assertIsNone(row["source_subcone_row"])
        self.assertIsNotNone(row["source_lower_tail_row"])
        self.assertIn(
            "strict_central_residue_weight_rows",
            row["source_lower_tail_row"])
        self.assertTrue(row["rescued_by_full_complement"])
        self.assertGreater(
            row["component_centered_actions_to_principal_ratio"][(7, 11)],
            0)
        self.assertLess(
            abs(row["component_centered_actions_to_principal_ratio"][
                (5, 7)]),
            .01)
        self.assertFalse(row["both_pair_components_centered_negative"])
        self.assertEqual(
            receipt["component_negative_threshold_rows"][.02][
                "both_components_below_negative_threshold_targets"],
            ())
        self.assertTrue(receipt[
            "lower_support_component_pair_tail_window_measured"])
        self.assertFalse(receipt[
            "eventual_component_pair_exclusion_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_q286_lower_support_component_pair_coefficient_geometry(self):
        receipt = (
            q286_lower_support_component_pair_coefficient_geometry_receipt())
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["unit_residue_count"], 2880)
        self.assertEqual(receipt["even_target_residue_count"], 5005)
        self.assertIn(1485, receipt["admissible_counts"])
        self.assertLess(abs(receipt[
            "maximum_absolute_pair_coefficient_cosine_row"][
                "pair_coefficient_cosine"]), .05)
        self.assertLess(receipt[
            "minimum_pair_coefficient_cosine_row"][
                "pair_coefficient_cosine"], 0)
        self.assertGreater(receipt[
            "maximum_pair_coefficient_cosine_row"][
                "pair_coefficient_cosine"], 0)
        sample = receipt["sample_target_rows"][1222142]
        self.assertEqual(sample["target_residue"], 1222142 % 10010)
        self.assertEqual(sample["admissible_count"], 1485)
        self.assertAlmostEqual(
            sample["pair_coefficient_cosine"],
            -0.0010921005009287641)
        self.assertTrue(receipt[
            "component_pair_coefficient_geometry_measured"])
        self.assertFalse(receipt[
            "pure_coefficient_geometry_exclusion_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_q286_lower_support_component_pair_cone_projection(self):
        receipt = q286_lower_support_component_pair_cone_projection_receipt()
        self.assertEqual(receipt["tested_target_count"], 4)
        self.assertEqual(
            receipt["both_pair_components_centered_negative_targets"],
            (14138,))
        boundary = receipt["rows"][14138]
        self.assertTrue(boundary[
            "both_pair_components_centered_negative"])
        self.assertLess(boundary[
            "component_actions_to_principal_ratio"][(5, 7)], 0)
        self.assertLess(boundary[
            "component_actions_to_principal_ratio"][(7, 11)], 0)
        self.assertGreater(
            boundary["weight_l2_relative_discrepancy"], .1)
        late = receipt["rows"][1379072]
        self.assertFalse(late[
            "both_pair_components_centered_negative"])
        self.assertLess(late[
            "component_actions_to_principal_ratio"][(5, 7)], 0)
        self.assertGreater(late[
            "component_actions_to_principal_ratio"][(7, 11)], 0)
        self.assertLess(
            late["weight_l2_relative_discrepancy"], .02)
        self.assertGreaterEqual(
            receipt["maximum_span_projection_fraction_row"][
                "span_projection_fraction_of_discrepancy_l2"],
            receipt["minimum_span_projection_fraction_row"][
                "span_projection_fraction_of_discrepancy_l2"])
        self.assertTrue(receipt[
            "component_pair_cone_projection_measured"])
        self.assertFalse(receipt[
            "component_pair_cone_avoidance_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_q286_lower_support_component_pair_support_geometry_obstruction(
            self):
        receipt = (
            q286_lower_support_component_pair_support_geometry_obstruction_receipt())
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["even_target_residue_count"], 5005)
        self.assertEqual(
            receipt["obstructed_even_target_residue_count"], 5005)
        self.assertTrue(receipt["all_even_target_residues_obstructed"])
        least_negative = receipt["least_negative_max_action_row"]
        self.assertLess(
            least_negative["maximum_component_action_to_principal_ratio"],
            0)
        self.assertGreaterEqual(
            receipt["minimum_weight_row"]["minimum_weight"], 0)
        sample = receipt["sample_target_rows"][14138]
        self.assertTrue(sample[
            "both_pair_components_centered_negative"])
        self.assertAlmostEqual(sample["total_weight"], 1.0)
        self.assertLess(
            sample["component_actions_to_principal_ratio"][(5, 7)], 0)
        self.assertLess(
            sample["component_actions_to_principal_ratio"][(7, 11)], 0)
        self.assertTrue(receipt[
            "support_geometry_obstruction_measured"])
        self.assertFalse(receipt[
            "support_geometry_exclusion_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_q286_lower_support_component_pair_reflection_support_obstruction(
            self):
        receipt = (
            q286_lower_support_component_pair_reflection_support_geometry_obstruction_receipt())
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["even_target_residue_count"], 5005)
        self.assertEqual(
            receipt["obstructed_even_target_residue_count"], 5005)
        self.assertTrue(receipt["all_even_target_residues_obstructed"])
        self.assertLessEqual(
            receipt["maximum_reflection_weight_error"], 1e-15)
        least_negative = receipt["least_negative_max_action_row"]
        self.assertEqual(least_negative["target_residue"], 9864)
        self.assertLess(
            least_negative["maximum_component_action_to_principal_ratio"],
            0)
        self.assertGreaterEqual(
            receipt["minimum_weight_row"]["minimum_weight"], 0)
        sample = receipt["sample_target_rows"][14138]
        self.assertTrue(sample[
            "both_pair_components_centered_negative"])
        self.assertAlmostEqual(sample["total_weight"], 1.0)
        self.assertLessEqual(sample["reflection_weight_error"], 1e-15)
        self.assertLess(
            sample["component_actions_to_principal_ratio"][(5, 7)], 0)
        self.assertLess(
            sample["component_actions_to_principal_ratio"][(7, 11)], 0)
        self.assertTrue(receipt[
            "reflection_support_geometry_obstruction_measured"])
        self.assertFalse(receipt[
            "reflection_support_geometry_exclusion_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_q286_lower_support_component_pair_character_mixture(self):
        receipt = q286_lower_support_component_pair_character_mixture_receipt()
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["tested_target_count"], 4)
        self.assertEqual(
            receipt["component_character_counts"][(5, 7)], 8)
        self.assertEqual(
            receipt["component_character_counts"][(7, 11)], 23)
        self.assertEqual(receipt["active_union_character_count"], 31)
        self.assertEqual(tuple(
            row["label"] for row in receipt[
                "component_character_rows"][(5, 7)]), (
                    (1, 1, 0, 0), (1, 3, 0, 0), (1, 5, 0, 0),
                    (2, 2, 0, 0), (2, 4, 0, 0), (3, 1, 0, 0),
                    (3, 3, 0, 0), (3, 5, 0, 0)))
        self.assertEqual(tuple(
            row["label"] for row in receipt[
                "component_character_rows"][(7, 11)]), (
                    (0, 1, 1, 0), (0, 1, 3, 0), (0, 1, 5, 0),
                    (0, 1, 7, 0), (0, 1, 9, 0), (0, 2, 2, 0),
                    (0, 2, 4, 0), (0, 2, 6, 0), (0, 2, 8, 0),
                    (0, 3, 1, 0), (0, 3, 3, 0), (0, 3, 5, 0),
                    (0, 3, 7, 0), (0, 3, 9, 0), (0, 4, 2, 0),
                    (0, 4, 4, 0), (0, 4, 6, 0), (0, 4, 8, 0),
                    (0, 5, 1, 0), (0, 5, 3, 0), (0, 5, 5, 0),
                    (0, 5, 7, 0), (0, 5, 9, 0)))
        self.assertLess(
            receipt["maximum_component_character_reconstruction_error"],
            1e-12)
        self.assertLess(receipt["maximum_action_reconstruction_error"], 1e-9)
        boundary = receipt["rows"][14138]
        self.assertTrue(boundary[
            "both_pair_components_centered_negative"])
        self.assertLess(boundary[
            "component_actions_to_principal_ratio"][(5, 7)], 0)
        self.assertLess(boundary[
            "component_actions_to_principal_ratio"][(7, 11)], 0)
        late = receipt["rows"][1379072]
        self.assertFalse(late[
            "both_pair_components_centered_negative"])
        self.assertLess(late[
            "component_actions_to_principal_ratio"][(5, 7)], 0)
        self.assertGreater(late[
            "component_actions_to_principal_ratio"][(7, 11)], 0)
        self.assertTrue(receipt[
            "component_pair_character_mixture_measured"])
        self.assertFalse(receipt[
            "pointwise_character_sum_estimate_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_q286_lower_support_component_pair_real_channel(self):
        receipt = q286_lower_support_component_pair_real_channel_receipt()
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(
            receipt["component_complex_character_counts"][(5, 7)], 8)
        self.assertEqual(
            receipt["component_complex_character_counts"][(7, 11)], 23)
        self.assertEqual(
            receipt["component_real_channel_counts"][(5, 7)], 4)
        self.assertEqual(
            receipt["component_real_channel_counts"][(7, 11)], 12)
        self.assertEqual(
            receipt["component_self_conjugate_channel_counts"][(5, 7)], 0)
        self.assertEqual(
            receipt["component_self_conjugate_channel_counts"][(7, 11)], 1)
        self.assertEqual(
            receipt["active_union_complex_character_count"], 31)
        self.assertEqual(receipt["active_union_real_channel_count"], 16)
        self.assertEqual(
            receipt["active_union_self_conjugate_channel_count"], 1)
        self.assertAlmostEqual(
            receipt["pair_sum_real_channel_l1_to_principal_mean"],
            15.262957606760951)
        self.assertLess(
            receipt["maximum_conjugate_coefficient_error"], 1e-12)
        first_pair = receipt[
            "component_conjugacy_orbit_rows"][(5, 7)][0]
        self.assertEqual(
            first_pair["labels"], ((1, 1, 0, 0), (3, 5, 0, 0)))
        self.assertEqual(first_pair["representative_label"], (1, 1, 0, 0))
        self.assertEqual(first_pair["real_formula_multiplier"], 2.0)
        self.assertEqual(first_pair["real_formula"], "2*Re(c*S_chi)")
        self.assertGreater(first_pair["representative_coefficient_abs"], 0)
        self_conjugate = receipt[
            "component_conjugacy_orbit_rows"][(7, 11)][-1]
        self.assertEqual(
            self_conjugate["labels"], ((0, 3, 5, 0),))
        self.assertEqual(
            self_conjugate["representative_label"], (0, 3, 5, 0))
        self.assertEqual(
            self_conjugate["real_formula_multiplier"], 1.0)
        self.assertEqual(self_conjugate["real_formula"], "Re(c*S_chi)")
        self.assertEqual(
            len(receipt["union_conjugacy_orbit_rows"]), 16)
        self.assertTrue(receipt[
            "complex_to_real_channel_reduction_measured"])
        self.assertFalse(receipt[
            "pointwise_real_channel_estimate_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_q286_lower_support_component_pair_real_channel_action(self):
        receipt = q286_lower_support_component_pair_real_channel_action_receipt()
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["tested_target_count"], 4)
        self.assertEqual(receipt["active_union_real_channel_count"], 16)
        self.assertAlmostEqual(
            receipt["pair_sum_real_channel_l1_to_principal_mean"],
            15.262957606760951)
        self.assertLess(
            receipt["maximum_real_channel_reconstruction_error"], 1e-12)
        boundary = receipt["rows"][14138]
        self.assertTrue(boundary[
            "both_pair_components_centered_negative"])
        self.assertAlmostEqual(
            boundary["real_channel_pair_sum_action_to_principal_ratio"],
            boundary["direct_pair_sum_action_to_principal_ratio"])
        self.assertLess(
            boundary["direct_pair_sum_action_to_principal_ratio"], -1)
        self.assertEqual(len(boundary["real_channel_rows"]), 16)
        self.assertLess(
            boundary["most_negative_real_channel_row"][
                "contribution_to_principal_ratio"], 0)
        self.assertAlmostEqual(
            receipt["rows"][1222142][
                "real_channel_pair_sum_action_to_principal_ratio"],
            0.01374295170801024)
        self.assertAlmostEqual(
            receipt["rows"][1323632][
                "real_channel_pair_sum_action_to_principal_ratio"],
            0.08749508122821215)
        late = receipt["rows"][1379072]
        self.assertFalse(late[
            "both_pair_components_centered_negative"])
        self.assertAlmostEqual(
            late["real_channel_pair_sum_action_to_principal_ratio"],
            0.046724251505157584)
        self.assertEqual(
            late["most_positive_real_channel_row"]["real_formula"],
            "2*Re(c*S_chi)")
        self.assertTrue(receipt[
            "real_channel_action_decomposition_measured"])
        self.assertFalse(receipt[
            "pointwise_real_channel_estimate_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_q286_lower_support_component_pair_real_channel_rescue_margin(
            self):
        receipt = (
            q286_lower_support_component_pair_real_channel_rescue_margin_receipt())
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["tested_target_count"], 4)
        self.assertEqual(
            receipt["failing_centered_real_channel_pair_floor_targets"],
            (14138,))
        self.assertEqual(
            receipt["rescued_by_centered_real_channel_pair_floor_targets"],
            (1222142, 1323632, 1379072))
        self.assertAlmostEqual(
            receipt["uniform_rescued_centered_pair_floor"],
            -0.8982746156725305)
        self.assertAlmostEqual(
            receipt["uniform_rescued_centered_pair_floor_margin"],
            0.9120175673805407)
        self.assertEqual(
            receipt["minimum_rescued_actual_centered_pair_sum_row"][
                "target"], 1222142)
        boundary = receipt["rows"][14138]
        self.assertAlmostEqual(
            boundary["required_centered_pair_sum_to_rescue"],
            -0.2756019941861918)
        self.assertAlmostEqual(
            boundary["centered_real_channel_pair_margin_to_rescue"],
            -0.8769412734408442)
        self.assertFalse(
            boundary["rescued_by_centered_real_channel_pair_floor"])
        for target, expected_floor, expected_margin in (
                (1222142, -0.9319733145059023, 0.9457162662139125),
                (1323632, -0.9367241850081613, 1.0242192662363734),
                (1379072, -0.8982746156725305, 0.944998867177687)):
            row = receipt["rows"][target]
            self.assertAlmostEqual(
                row["required_centered_pair_sum_to_rescue"],
                expected_floor)
            self.assertAlmostEqual(
                row["centered_real_channel_pair_margin_to_rescue"],
                expected_margin)
            self.assertTrue(
                row["rescued_by_centered_real_channel_pair_floor"])
            self.assertTrue(
                row["centered_pair_margin_matches_package_margin"])
        self.assertEqual(
            receipt["minimum_centered_real_channel_pair_margin_row"][
                "target"], 14138)
        self.assertTrue(receipt["real_channel_rescue_margin_measured"])
        self.assertFalse(receipt[
            "pointwise_real_channel_floor_estimate_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_q286_lower_support_component_pair_real_channel_bound_budget(
            self):
        receipt = (
            q286_lower_support_component_pair_real_channel_bound_budget_receipt())
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["tested_target_count"], 4)
        self.assertEqual(receipt["active_union_real_channel_count"], 16)
        self.assertAlmostEqual(
            receipt["real_channel_l1_to_principal_mean"],
            15.262957606760951)
        self.assertGreater(
            receipt["real_channel_l2_to_principal_mean"], 0)
        self.assertAlmostEqual(
            receipt["rescued_uniform_floor_budget"]["floor"],
            -0.8982746156725305)
        self.assertAlmostEqual(
            receipt["rescued_uniform_floor_budget"][
                "sufficient_normalized_linf_bound"],
            0.05885324711081062)
        self.assertAlmostEqual(
            receipt["rescued_uniform_floor_budget"][
                "sufficient_normalized_l2_bound"],
            0.2155408076755675)
        self.assertLess(
            receipt["all_selected_floor_budget"][
                "sufficient_normalized_linf_bound"],
            receipt["rescued_uniform_floor_budget"][
                "sufficient_normalized_linf_bound"])
        self.assertGreater(
            receipt["rows"][14138]["maximum_normalized_real_channel_sum"],
            receipt["rows"][1222142]["maximum_normalized_real_channel_sum"])
        self.assertGreater(
            receipt["rows"][14138]["triangle_bound_to_principal_ratio"],
            1)
        self.assertTrue(receipt["real_channel_bound_budget_measured"])
        self.assertFalse(receipt[
            "pointwise_real_channel_norm_estimate_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_q286_lower_support_component_pair_conditional_norm_closure(
            self):
        receipt = (
            q286_lower_support_component_pair_conditional_norm_closure_receipt())
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["tested_target_count"], 4)
        self.assertAlmostEqual(
            receipt["assumption_floor_ceiling_to_principal_ratio"],
            -0.8982746156725305)
        self.assertAlmostEqual(
            receipt["assumption_normalized_linf_bound"],
            0.05885324711081062)
        self.assertAlmostEqual(
            receipt["guaranteed_centered_pair_floor_to_principal_ratio"],
            -0.8982746156725305)
        self.assertEqual(
            receipt["conditional_hypotheses_selected_targets"],
            (1222142, 1323632, 1379072))
        self.assertEqual(
            receipt["conditional_rescue_verified_targets"],
            (1222142, 1323632, 1379072))
        self.assertEqual(receipt["failing_condition_targets"], (14138,))
        boundary = receipt["rows"][14138]
        self.assertFalse(boundary["floor_stability_condition_met"])
        self.assertFalse(boundary["normalized_linf_condition_met"])
        self.assertFalse(boundary["conditional_hypotheses_met"])
        late = receipt["rows"][1222142]
        self.assertTrue(late["floor_stability_condition_met"])
        self.assertTrue(late["normalized_linf_condition_met"])
        self.assertTrue(late["conditional_rescue_forced"])
        self.assertTrue(late[
            "actually_rescued_by_centered_real_channel_pair_floor"])
        self.assertTrue(receipt["conditional_norm_closure_measured"])
        self.assertFalse(receipt["floor_stability_theorem_proved"])
        self.assertFalse(receipt[
            "pointwise_real_channel_norm_estimate_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_q286_lower_support_component_pair_floor_stability_decomposition(
            self):
        receipt = (
            q286_lower_support_component_pair_floor_stability_decomposition_receipt())
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["tested_target_count"], 4)
        self.assertAlmostEqual(
            receipt["uniform_rescued_centered_pair_floor"],
            -0.8982746156725305)
        self.assertAlmostEqual(
            receipt["rescued_required_lower_support_package_ceiling"],
            -0.6751407665271594)
        self.assertAlmostEqual(
            receipt["rescued_floor_offset_floor"],
            0.2231338491453711)
        self.assertEqual(
            receipt["floor_stable_targets"],
            (1222142, 1323632, 1379072))
        self.assertEqual(
            receipt["sufficient_term_condition_targets"],
            (1222142, 1323632, 1379072))
        boundary = receipt["rows"][14138]
        self.assertFalse(boundary[
            "rescued_required_lower_support_condition_met"])
        self.assertFalse(boundary["rescued_offset_floor_condition_met"])
        self.assertGreater(
            boundary["required_lower_support_package_to_rescue"], -0.2)
        self.assertAlmostEqual(
            boundary["floor_offset_to_principal_ratio"],
            0.1377282064675911)
        late = receipt["rows"][1379072]
        self.assertTrue(late[
            "rescued_required_lower_support_condition_met"])
        self.assertTrue(late["rescued_offset_floor_condition_met"])
        self.assertAlmostEqual(
            late["floor_stability_gap_to_uniform_ceiling"], 0.0)
        self.assertTrue(receipt[
            "floor_stability_decomposition_measured"])
        self.assertFalse(receipt["floor_stability_theorem_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_q286_lower_support_component_pair_floor_identity(self):
        receipt = q286_lower_support_component_pair_floor_identity_receipt()
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["tested_target_count"], 4)
        self.assertAlmostEqual(
            receipt["uniform_rescued_centered_pair_floor"],
            -0.8982746156725305)
        self.assertAlmostEqual(
            receipt["combined_floor_driver_floor"],
            -0.1017253843274695)
        self.assertLess(
            receipt["maximum_required_floor_reconstruction_error"], 1e-12)
        self.assertEqual(
            receipt["floor_stable_targets"],
            (1222142, 1323632, 1379072))
        boundary = receipt["rows"][14138]
        self.assertAlmostEqual(
            boundary["first_three_plus_q286_tail_to_principal_ratio"],
            -0.8621262122813993)
        self.assertAlmostEqual(
            boundary["floor_offset_to_principal_ratio"],
            0.1377282064675911)
        self.assertLess(
            boundary["combined_floor_driver_to_principal_ratio"],
            receipt["combined_floor_driver_floor"])
        self.assertFalse(boundary["floor_stability_condition_met"])
        late = receipt["rows"][1379072]
        self.assertAlmostEqual(
            late["combined_floor_driver_to_principal_ratio"],
            receipt["combined_floor_driver_floor"])
        self.assertAlmostEqual(
            late["required_centered_pair_sum_to_rescue"],
            late["reconstructed_required_centered_pair_sum_to_rescue"])
        self.assertTrue(late["floor_stability_condition_met"])
        self.assertTrue(receipt["floor_identity_measured"])
        self.assertFalse(receipt["combined_floor_driver_theorem_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_q286_lower_support_component_pair_combined_driver_channel_closure(
            self):
        receipt = (
            q286_lower_support_component_pair_combined_driver_channel_closure_receipt())
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["tested_target_count"], 4)
        self.assertAlmostEqual(
            receipt["combined_floor_driver_floor"],
            -0.1017253843274695)
        self.assertAlmostEqual(
            receipt["normalized_real_channel_linf_bound"],
            0.05885324711081062)
        self.assertAlmostEqual(
            receipt["real_channel_l1_to_principal_mean"],
            15.262957606760951)
        self.assertEqual(
            receipt["conditional_closure_targets"],
            (1222142, 1323632, 1379072))
        boundary = receipt["rows"][14138]
        self.assertFalse(boundary["combined_driver_condition_met"])
        self.assertFalse(boundary["real_channel_linf_condition_met"])
        self.assertFalse(boundary["conditional_rescue_forced"])
        late = receipt["rows"][1222142]
        self.assertTrue(late["combined_driver_condition_met"])
        self.assertTrue(late["real_channel_linf_condition_met"])
        self.assertTrue(late["conditional_rescue_forced"])
        self.assertTrue(late[
            "actually_rescued_by_centered_real_channel_pair_floor"])
        self.assertTrue(receipt[
            "combined_driver_channel_closure_measured"])
        self.assertFalse(receipt["combined_floor_driver_theorem_proved"])
        self.assertFalse(receipt[
            "pointwise_real_channel_norm_estimate_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_q286_lower_support_component_pair_action_identity(self):
        receipt = q286_lower_support_component_pair_action_identity_receipt()
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["tested_target_count"], 4)
        self.assertLess(
            receipt["maximum_full_action_reconstruction_error"], 1e-12)
        self.assertEqual(
            receipt["identity_positive_targets"],
            (1222142, 1323632, 1379072))
        self.assertEqual(
            receipt["actual_positive_targets"],
            (1222142, 1323632, 1379072))
        self.assertEqual(
            receipt["conditional_closure_positive_targets"],
            (1222142, 1323632, 1379072))
        boundary = receipt["rows"][14138]
        self.assertAlmostEqual(
            boundary["reconstructed_full_action_to_principal_ratio"],
            -0.8769412734408442)
        self.assertAlmostEqual(
            boundary["full_action_to_principal_ratio"],
            -0.8769412734408442)
        self.assertFalse(boundary["positive_by_reconstructed_identity"])
        late = receipt["rows"][1222142]
        self.assertAlmostEqual(
            late["reconstructed_full_action_to_principal_ratio"],
            0.9457162662139125)
        self.assertTrue(late["conditional_closure_forces_positive"])
        self.assertTrue(receipt["component_pair_action_identity_measured"])
        self.assertFalse(receipt["combined_floor_driver_theorem_proved"])
        self.assertFalse(receipt[
            "pointwise_real_channel_norm_estimate_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_q286_lower_support_component_pair_closure_margin_profile(self):
        receipt = (
            q286_lower_support_component_pair_closure_margin_profile_receipt())
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["tested_target_count"], 4)
        self.assertAlmostEqual(
            receipt["combined_floor_driver_floor"],
            -0.1017253843274695)
        self.assertAlmostEqual(
            receipt["centered_pair_sum_floor"],
            -0.8982746156725305)
        self.assertAlmostEqual(
            receipt["normalized_real_channel_linf_bound"],
            0.05885324711081062)
        self.assertAlmostEqual(
            receipt["real_channel_l1_to_principal_mean"],
            15.262957606760978)
        self.assertEqual(
            receipt["worst_driver_margin_row"]["target"], 14138)
        self.assertEqual(
            receipt["worst_channel_margin_row"]["target"], 14138)
        self.assertEqual(
            receipt["worst_conditional_closure_margin_row"]["target"],
            14138)
        self.assertEqual(
            receipt["minimum_positive_full_action_row"]["target"], 1379072)
        boundary = receipt["rows"][14138]
        self.assertAlmostEqual(
            boundary["driver_margin_to_floor"], -0.6226726214863387)
        self.assertAlmostEqual(
            boundary["channel_margin_to_linf_bound"],
            -0.20705269440121776)
        self.assertAlmostEqual(
            boundary["conditional_closure_margin_to_endpoint"],
            -3.782909118497761)
        self.assertFalse(
            boundary["strict_conditional_closure_slack_positive"])
        self.assertTrue(boundary["fails_driver_floor"])
        self.assertTrue(boundary["fails_channel_bound"])
        self.assertFalse(boundary["positive_by_identity"])
        late = receipt["rows"][1379072]
        self.assertAlmostEqual(
            late["minimum_assumption_margin"], 0.0)
        self.assertAlmostEqual(
            late["conditional_closure_margin_to_endpoint"],
            0.48379401372791037)
        self.assertTrue(
            late["strict_conditional_closure_slack_positive"])
        self.assertFalse(late["fails_driver_floor"])
        self.assertFalse(late["fails_channel_bound"])
        self.assertTrue(late["positive_by_identity"])
        self.assertTrue(receipt["closure_margin_profile_measured"])
        self.assertFalse(receipt["combined_floor_driver_theorem_proved"])
        self.assertFalse(receipt[
            "pointwise_real_channel_norm_estimate_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_q286_lower_support_component_pair_channel_pressure_profile(self):
        receipt = (
            q286_lower_support_component_pair_channel_pressure_profile_receipt())
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["tested_target_count"], 4)
        self.assertEqual(receipt["top_count"], 3)
        self.assertAlmostEqual(
            receipt["normalized_real_channel_linf_bound"],
            0.05885324711081062)
        self.assertEqual(
            receipt["worst_channel_pressure_row"]["target"], 14138)
        self.assertEqual(
            receipt["worst_positive_channel_pressure_row"]["target"],
            1379072)
        boundary = receipt["rows"][14138]
        self.assertAlmostEqual(
            boundary["maximum_channel_normalized_abs_sum"],
            0.2659059415120284)
        self.assertAlmostEqual(
            boundary["maximum_channel_margin_to_linf_bound"],
            -0.20705269440121776)
        self.assertLess(
            boundary["maximum_channel_margin_to_linf_bound"], 0.0)
        positive = receipt["rows"][1379072]
        self.assertEqual(
            positive["maximum_channel_representative_label"],
            (0, 3, 3, 0))
        self.assertGreaterEqual(
            positive["maximum_channel_margin_to_linf_bound"], 0.0)
        self.assertEqual(len(positive["top_channel_pressure_rows"]), 3)
        self.assertTrue(receipt["channel_pressure_profile_measured"])
        self.assertFalse(receipt[
            "pointwise_real_channel_norm_estimate_proved"])
        self.assertFalse(receipt["signed_prime_correlation_estimate_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_q286_lower_support_component_pair_channel_conductor_profile(self):
        receipt = (
            q286_lower_support_component_pair_channel_conductor_profile_receipt())
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["active_union_real_channel_count"], 16)
        self.assertEqual(receipt["active_channel_conductors"], (35, 77))
        self.assertEqual(receipt["active_channel_conductor_counts"], {
            35: 4, 77: 12})
        self.assertFalse(receipt["uses_factor_13"])
        self.assertTrue(receipt["all_active_channels_on_adjacent_conductors"])
        self.assertEqual(
            receipt["worst_channel_pressure_row"]["target"], 14138)
        self.assertEqual(
            receipt["worst_channel_pressure_row"][
                "maximum_channel_conductor"], 35)
        self.assertEqual(
            receipt["worst_positive_channel_pressure_row"]["target"],
            1379072)
        self.assertEqual(
            receipt["worst_positive_channel_pressure_row"][
                "maximum_channel_conductor"], 77)
        self.assertTrue(receipt["channel_conductor_profile_measured"])
        self.assertFalse(receipt[
            "pointwise_fixed_conductor_twisted_goldbach_estimate_proved"])
        self.assertFalse(receipt["signed_prime_correlation_estimate_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_q286_lower_support_component_pair_fixed_conductor_reduction(
            self):
        receipt = (
            q286_lower_support_component_pair_fixed_conductor_reduction_receipt())
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["active_channel_conductors"], (35, 77))
        self.assertEqual(receipt["active_union_real_channel_count"], 16)
        self.assertLess(
            receipt["maximum_character_sum_reduction_error"], 1e-8)
        self.assertLess(
            receipt["maximum_residue_character_consistency_error"], 1e-12)
        boundary_rows = {
            row["representative_label"]: row
            for row in receipt["rows"][14138]["channel_rows"]}
        boundary = boundary_rows[(1, 1, 0, 0)]
        self.assertEqual(boundary["conductor"], 35)
        self.assertAlmostEqual(
            boundary["normalized_abs_sum"], 0.2659059415120284)
        positive_rows = {
            row["representative_label"]: row
            for row in receipt["rows"][1379072]["channel_rows"]}
        positive = positive_rows[(0, 3, 3, 0)]
        self.assertEqual(positive["conductor"], 77)
        self.assertAlmostEqual(
            positive["normalized_abs_sum"], 0.027155981994015317)
        self.assertTrue(receipt["fixed_conductor_reduction_measured"])
        self.assertFalse(receipt[
            "pointwise_fixed_conductor_twisted_goldbach_estimate_proved"])
        self.assertFalse(receipt["signed_prime_correlation_estimate_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_q286_lower_support_component_pair_fixed_conductor_residue_pressure(
            self):
        receipt = (
            q286_lower_support_component_pair_fixed_conductor_residue_pressure_receipt())
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["active_channel_conductors"], (35, 77))
        self.assertAlmostEqual(
            receipt["normalized_real_channel_linf_bound"],
            0.05885324711081062)
        self.assertEqual(receipt["top_count"], 5)
        self.assertEqual(
            receipt["worst_residue_linf_row"]["target"], 14138)
        self.assertEqual(
            receipt["worst_residue_linf_row"]["conductor"], 35)
        self.assertAlmostEqual(
            receipt["worst_residue_linf_row"][
                "residue_linf_to_total_weight"],
            0.05327502632021343)
        self.assertEqual(
            receipt["worst_residue_l1_row"]["target"], 14138)
        self.assertEqual(
            receipt["worst_residue_l1_row"]["conductor"], 77)
        self.assertAlmostEqual(
            receipt["worst_residue_l1_row"][
                "residue_l1_to_total_weight"],
            0.4624962038193246)
        boundary = receipt["rows"][14138]["conductor_rows"][35]
        self.assertEqual(boundary["conductor_residue_count"], 24)
        self.assertLess(
            boundary["linf_margin_to_sufficient_residue_bound"], 0.0)
        positive = receipt["rows"][1379072]["conductor_rows"][77]
        self.assertEqual(positive["conductor_residue_count"], 60)
        self.assertAlmostEqual(
            positive["residue_linf_to_total_weight"],
            0.003645150940944693)
        self.assertAlmostEqual(
            positive["plain_linf_triangle_bound_to_channel_sum"],
            0.2187090564566816)
        self.assertGreater(
            positive["plain_linf_triangle_bound_to_channel_sum"],
            receipt["normalized_real_channel_linf_bound"])
        self.assertTrue(receipt[
            "fixed_conductor_residue_pressure_measured"])
        self.assertFalse(receipt[
            "plain_residue_linf_proves_channel_bound"])
        self.assertFalse(receipt[
            "pointwise_fixed_conductor_twisted_goldbach_estimate_proved"])
        self.assertFalse(receipt["signed_prime_correlation_estimate_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_q286_lower_support_component_pair_fixed_conductor_character_cancellation(
            self):
        receipt = (
            q286_lower_support_component_pair_fixed_conductor_character_cancellation_receipt())
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["active_channel_conductors"], (35, 77))
        self.assertEqual(receipt["active_union_real_channel_count"], 16)
        self.assertAlmostEqual(
            receipt["normalized_real_channel_linf_bound"],
            0.05885324711081062)
        worst_positive = receipt["worst_positive_actual_channel_row"]
        self.assertEqual(worst_positive["target"], 1379072)
        self.assertEqual(
            worst_positive["representative_label"], (0, 3, 3, 0))
        self.assertEqual(worst_positive["conductor"], 77)
        self.assertAlmostEqual(
            worst_positive["actual_normalized_abs_sum"],
            0.02715598199401531)
        self.assertAlmostEqual(
            worst_positive["actual_to_linf_triangle_ratio"],
            0.12416487197179206)
        self.assertAlmostEqual(
            worst_positive["actual_to_l1_triangle_ratio"],
            0.3153405593261632)
        self.assertLess(
            worst_positive["actual_to_linf_triangle_ratio"],
            worst_positive[
                "needed_linf_triangle_ratio_to_clear_bound"])
        least_cancelled = receipt[
            "least_cancelled_linf_triangle_channel_row"]
        self.assertEqual(least_cancelled["target"], 14138)
        self.assertEqual(
            least_cancelled["representative_label"], (1, 1, 0, 0))
        self.assertAlmostEqual(
            least_cancelled["actual_to_linf_triangle_ratio"],
            0.20796637739931306)
        self.assertTrue(worst_positive["actual_clears_channel_bound"])
        self.assertFalse(
            worst_positive["plain_linf_triangle_clears_channel_bound"])
        self.assertTrue(receipt[
            "fixed_conductor_character_cancellation_measured"])
        self.assertFalse(receipt["character_cancellation_theorem_proved"])
        self.assertFalse(receipt[
            "pointwise_fixed_conductor_twisted_goldbach_estimate_proved"])
        self.assertFalse(receipt["signed_prime_correlation_estimate_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_q286_lower_support_component_pair_fixed_conductor_reflection_orbit(
            self):
        receipt = (
            q286_lower_support_component_pair_fixed_conductor_reflection_orbit_receipt())
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["active_channel_conductors"], (35, 77))
        self.assertAlmostEqual(
            receipt["normalized_real_channel_linf_bound"],
            0.05885324711081062)
        self.assertEqual(
            receipt["passing_positive_targets_by_reflection_orbit_bound"],
            (1222142, 1323632))
        self.assertEqual(
            receipt["failing_positive_targets_by_reflection_orbit_bound"],
            (1379072,))
        worst = receipt["worst_reflection_orbit_l1_row"]
        self.assertEqual(worst["target"], 14138)
        self.assertEqual(worst["representative_label"], (0, 1, 3, 0))
        self.assertAlmostEqual(
            worst["reflection_orbit_l1_to_total_weight"],
            0.3296060502917276)
        positive = receipt["worst_positive_reflection_orbit_l1_row"]
        self.assertEqual(positive["target"], 1379072)
        self.assertEqual(positive["representative_label"], (0, 2, 6, 0))
        self.assertAlmostEqual(
            positive["reflection_orbit_l1_to_total_weight"],
            0.06039386426228221)
        self.assertLess(
            positive["reflection_orbit_margin_to_channel_bound"], 0.0)
        self.assertFalse(receipt[
            "reflection_orbit_bound_proves_all_positive_channel_bounds"])
        self.assertTrue(receipt[
            "fixed_conductor_reflection_orbit_profile_measured"])
        self.assertFalse(receipt[
            "pointwise_fixed_conductor_twisted_goldbach_estimate_proved"])
        self.assertFalse(receipt["signed_prime_correlation_estimate_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_q286_lower_support_component_pair_fixed_conductor_residual_orbit_cancellation(
            self):
        receipt = (
            q286_lower_support_component_pair_fixed_conductor_residual_orbit_cancellation_receipt())
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["active_channel_conductors"], (35, 77))
        self.assertAlmostEqual(
            receipt["normalized_real_channel_linf_bound"],
            0.05885324711081062)
        self.assertEqual(receipt["positive_reflection_failure_count"], 2)
        failures = receipt["positive_reflection_failure_rows"]
        self.assertEqual(
            tuple(row["representative_label"] for row in failures),
            ((0, 1, 5, 0), (0, 2, 6, 0)))
        self.assertTrue(all(
            row["target"] == 1379072 for row in failures))
        self.assertTrue(all(row[
            "reflection_failure_rescued_by_signed_orbit_cancellation"]
            for row in failures))
        worst_failure = receipt["worst_positive_reflection_failure_ratio_row"]
        self.assertEqual(
            worst_failure["representative_label"], (0, 2, 6, 0))
        self.assertAlmostEqual(
            worst_failure["actual_to_reflection_orbit_l1_ratio"],
            0.289119636096235)
        self.assertAlmostEqual(
            worst_failure["needed_actual_to_orbit_l1_ratio_to_clear_bound"],
            0.9744905021347716)
        self.assertTrue(receipt[
            "all_positive_reflection_failures_rescued_by_signed_orbit_cancellation"])
        self.assertTrue(receipt[
            "fixed_conductor_residual_orbit_cancellation_measured"])
        self.assertFalse(receipt[
            "residual_orbit_cancellation_theorem_proved"])
        self.assertFalse(receipt[
            "pointwise_fixed_conductor_twisted_goldbach_estimate_proved"])
        self.assertFalse(receipt["signed_prime_correlation_estimate_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_q286_lower_support_component_pair_fixed_conductor_orbit_polygon(
            self):
        receipt = (
            q286_lower_support_component_pair_fixed_conductor_orbit_polygon_receipt())
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["active_channel_conductors"], (35, 77))
        self.assertEqual(receipt["polygon_row_count"], 2)
        self.assertEqual(
            tuple(row["representative_label"]
                  for row in receipt["polygon_rows"]),
            ((0, 1, 5, 0), (0, 2, 6, 0)))
        self.assertTrue(all(row["target"] == 1379072
                            for row in receipt["polygon_rows"]))
        self.assertTrue(all(row["conductor"] == 77
                            for row in receipt["polygon_rows"]))
        for row in receipt["polygon_rows"]:
            self.assertLess(row["resultant_reconstruction_error"], 1e-12)
            self.assertGreater(row["resultant_margin_to_channel_bound"], 0.0)
            self.assertLess(row["perimeter_margin_to_channel_bound"], 0.0)
        worst = receipt["worst_closure_ratio_row"]
        self.assertEqual(worst["representative_label"], (0, 2, 6, 0))
        self.assertAlmostEqual(
            worst["closure_ratio"], 0.289119636096235)
        self.assertAlmostEqual(
            worst["polygon_perimeter"], 0.0603938642622822)
        self.assertTrue(receipt["fixed_conductor_orbit_polygon_measured"])
        self.assertFalse(receipt["orbit_polygon_theorem_proved"])
        self.assertFalse(receipt[
            "pointwise_fixed_conductor_twisted_goldbach_estimate_proved"])
        self.assertFalse(receipt["signed_prime_correlation_estimate_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_q286_lower_support_component_pair_fixed_conductor_orbit_phase_profile(
            self):
        receipt = (
            q286_lower_support_component_pair_fixed_conductor_orbit_phase_profile_receipt())
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["active_channel_conductors"], (35, 77))
        self.assertEqual(receipt["phase_bin_count"], 12)
        self.assertEqual(
            tuple(row["representative_label"] for row in receipt["rows"]),
            ((0, 1, 5, 0), (0, 2, 6, 0)))
        for row in receipt["rows"]:
            self.assertEqual(row["target"], 1379072)
            self.assertEqual(row["conductor"], 77)
            self.assertLess(row["phase_bin_l1_reconstruction_error"], 1e-12)
            self.assertGreater(row["nonzero_phase_bin_count"], 2)
            self.assertLess(
                row["largest_phase_bin_fraction_of_perimeter"], 0.5)
        self.assertTrue(receipt[
            "fixed_conductor_orbit_phase_profile_measured"])
        self.assertFalse(receipt["phase_bin_balance_theorem_proved"])
        self.assertFalse(receipt["orbit_polygon_theorem_proved"])
        self.assertFalse(receipt[
            "pointwise_fixed_conductor_twisted_goldbach_estimate_proved"])
        self.assertFalse(receipt["signed_prime_correlation_estimate_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_q286_lower_support_component_pair_fixed_conductor_phase_bin_compression(
            self):
        receipt = (
            q286_lower_support_component_pair_fixed_conductor_phase_bin_compression_receipt())
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["active_channel_conductors"], (35, 77))
        self.assertEqual(receipt["phase_bin_count"], 12)
        self.assertEqual(
            tuple(row["representative_label"] for row in receipt["rows"]),
            ((0, 1, 5, 0), (0, 2, 6, 0)))
        self.assertEqual(
            receipt["passing_polygon_labels_by_phase_bin_signed_bound"],
            ((0, 1, 5, 0),))
        self.assertEqual(
            receipt["failing_polygon_labels_by_phase_bin_signed_bound"],
            ((0, 2, 6, 0),))
        self.assertFalse(
            receipt["all_residual_polygons_clear_by_phase_bin_signed_bound"])
        by_label = {
            row["representative_label"]: row for row in receipt["rows"]}
        self.assertAlmostEqual(
            by_label[(0, 1, 5, 0)]["phase_bin_signed_l1"],
            0.058765359273537675)
        self.assertGreater(
            by_label[(0, 1, 5, 0)][
                "signed_bin_l1_margin_to_channel_bound"],
            0.0)
        self.assertAlmostEqual(
            by_label[(0, 2, 6, 0)]["phase_bin_signed_l1"],
            0.06015000330167732)
        self.assertLess(
            by_label[(0, 2, 6, 0)][
                "signed_bin_l1_margin_to_channel_bound"],
            0.0)
        worst = receipt["worst_signed_bin_l1_margin_row"]
        self.assertEqual(worst["representative_label"], (0, 2, 6, 0))
        self.assertAlmostEqual(
            worst["signed_bin_l1_margin_to_channel_bound"],
            -0.001296756190866699)
        self.assertTrue(receipt[
            "fixed_conductor_phase_bin_compression_measured"])
        self.assertFalse(receipt["phase_bin_compression_theorem_proved"])
        self.assertFalse(receipt["phase_bin_balance_theorem_proved"])
        self.assertFalse(receipt["orbit_polygon_theorem_proved"])
        self.assertFalse(receipt[
            "pointwise_fixed_conductor_twisted_goldbach_estimate_proved"])
        self.assertFalse(receipt["signed_prime_correlation_estimate_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_q286_lower_support_component_pair_fixed_conductor_phase_antipodal_compression(
            self):
        receipt = (
            q286_lower_support_component_pair_fixed_conductor_phase_antipodal_compression_receipt())
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["active_channel_conductors"], (35, 77))
        self.assertEqual(receipt["phase_bin_count"], 12)
        self.assertEqual(receipt["antipodal_pair_count"], 6)
        self.assertEqual(
            tuple(row["representative_label"] for row in receipt["rows"]),
            ((0, 1, 5, 0), (0, 2, 6, 0)))
        self.assertEqual(
            receipt["passing_polygon_labels_by_antipodal_phase_bound"],
            ((0, 1, 5, 0), (0, 2, 6, 0)))
        self.assertEqual(
            receipt["failing_polygon_labels_by_antipodal_phase_bound"],
            ())
        self.assertTrue(
            receipt["all_residual_polygons_clear_by_antipodal_phase_bound"])
        by_label = {
            row["representative_label"]: row for row in receipt["rows"]}
        self.assertAlmostEqual(
            by_label[(0, 1, 5, 0)]["antipodal_phase_pair_l1"],
            0.009229827584054894)
        self.assertAlmostEqual(
            by_label[(0, 1, 5, 0)][
                "antipodal_phase_pair_margin_to_channel_bound"],
            0.049623419526755724)
        self.assertAlmostEqual(
            by_label[(0, 2, 6, 0)]["antipodal_phase_pair_l1"],
            0.03657040255445905)
        self.assertAlmostEqual(
            by_label[(0, 2, 6, 0)][
                "antipodal_phase_pair_margin_to_channel_bound"],
            0.022282844556351572)
        worst = receipt["worst_antipodal_phase_pair_margin_row"]
        self.assertEqual(worst["representative_label"], (0, 2, 6, 0))
        self.assertTrue(receipt[
            "fixed_conductor_phase_antipodal_compression_measured"])
        self.assertFalse(receipt[
            "phase_antipodal_compression_theorem_proved"])
        self.assertFalse(receipt["phase_bin_compression_theorem_proved"])
        self.assertFalse(receipt["phase_bin_balance_theorem_proved"])
        self.assertFalse(receipt["orbit_polygon_theorem_proved"])
        self.assertFalse(receipt[
            "pointwise_fixed_conductor_twisted_goldbach_estimate_proved"])
        self.assertFalse(receipt["signed_prime_correlation_estimate_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_q286_lower_support_component_pair_fixed_conductor_phase_antipodal_pair_balance(
            self):
        receipt = (
            q286_lower_support_component_pair_fixed_conductor_phase_antipodal_pair_balance_receipt())
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["active_channel_conductors"], (35, 77))
        self.assertEqual(receipt["phase_bin_count"], 12)
        self.assertEqual(receipt["high_ratio_threshold"], 0.75)
        self.assertEqual(
            tuple(row["representative_label"] for row in receipt["rows"]),
            ((0, 1, 5, 0), (0, 2, 6, 0)))
        self.assertFalse(receipt["all_antipodal_pairs_uniformly_cancel"])
        by_label = {
            row["representative_label"]: row for row in receipt["rows"]}
        self.assertAlmostEqual(
            by_label[(0, 1, 5, 0)][
                "weighted_antipodal_cancellation_ratio"],
            0.15706238672161288)
        self.assertEqual(
            by_label[(0, 1, 5, 0)]["high_ratio_pair_count"], 1)
        self.assertAlmostEqual(
            by_label[(0, 1, 5, 0)]["largest_antipodal_pair_abs"],
            0.0031320675991354753)
        self.assertAlmostEqual(
            by_label[(0, 2, 6, 0)][
                "weighted_antipodal_cancellation_ratio"],
            0.6079867090121881)
        self.assertEqual(
            by_label[(0, 2, 6, 0)]["high_ratio_pair_count"], 2)
        self.assertAlmostEqual(
            by_label[(0, 2, 6, 0)]["largest_antipodal_pair_abs"],
            0.015424610859844602)
        self.assertAlmostEqual(
            by_label[(0, 2, 6, 0)]["largest_pair_cancellation_ratio"],
            0.9711661073614952)
        worst = receipt["worst_weighted_antipodal_cancellation_ratio_row"]
        self.assertEqual(worst["representative_label"], (0, 2, 6, 0))
        self.assertTrue(receipt[
            "fixed_conductor_phase_antipodal_pair_balance_measured"])
        self.assertFalse(receipt[
            "phase_antipodal_pair_balance_theorem_proved"])
        self.assertFalse(receipt[
            "phase_antipodal_compression_theorem_proved"])
        self.assertFalse(receipt["phase_bin_compression_theorem_proved"])
        self.assertFalse(receipt["phase_bin_balance_theorem_proved"])
        self.assertFalse(receipt["orbit_polygon_theorem_proved"])
        self.assertFalse(receipt[
            "pointwise_fixed_conductor_twisted_goldbach_estimate_proved"])
        self.assertFalse(receipt["signed_prime_correlation_estimate_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_q286_lower_support_component_pair_fixed_conductor_phase_antipodal_threshold_envelope(
            self):
        receipt = (
            q286_lower_support_component_pair_fixed_conductor_phase_antipodal_threshold_envelope_receipt())
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["active_channel_conductors"], (35, 77))
        self.assertEqual(receipt["phase_bin_count"], 12)
        self.assertEqual(receipt["high_ratio_threshold"], 0.75)
        self.assertEqual(
            tuple(row["representative_label"] for row in receipt["rows"]),
            ((0, 1, 5, 0), (0, 2, 6, 0)))
        self.assertEqual(
            receipt["passing_polygon_labels_by_thresholded_envelope"],
            ((0, 1, 5, 0), (0, 2, 6, 0)))
        self.assertEqual(
            receipt["failing_polygon_labels_by_thresholded_envelope"],
            ())
        self.assertTrue(
            receipt["all_residual_polygons_clear_by_thresholded_envelope"])
        by_label = {
            row["representative_label"]: row for row in receipt["rows"]}
        self.assertAlmostEqual(
            by_label[(0, 1, 5, 0)][
                "thresholded_antipodal_l1_envelope"],
            0.044857036354937124)
        self.assertAlmostEqual(
            by_label[(0, 1, 5, 0)][
                "thresholded_envelope_margin_to_channel_bound"],
            0.013996210755873498)
        self.assertEqual(
            by_label[(0, 1, 5, 0)]["high_ratio_pair_count"], 1)
        self.assertAlmostEqual(
            by_label[(0, 2, 6, 0)][
                "thresholded_antipodal_l1_envelope"],
            0.049789406359944485)
        self.assertAlmostEqual(
            by_label[(0, 2, 6, 0)][
                "thresholded_envelope_margin_to_channel_bound"],
            0.009063840750866137)
        self.assertEqual(
            by_label[(0, 2, 6, 0)]["high_ratio_pair_count"], 2)
        worst = receipt["worst_thresholded_envelope_margin_row"]
        self.assertEqual(worst["representative_label"], (0, 2, 6, 0))
        self.assertTrue(receipt[
            "fixed_conductor_phase_antipodal_threshold_envelope_measured"])
        self.assertFalse(receipt[
            "phase_antipodal_threshold_envelope_theorem_proved"])
        self.assertFalse(receipt[
            "phase_antipodal_pair_balance_theorem_proved"])
        self.assertFalse(receipt[
            "phase_antipodal_compression_theorem_proved"])
        self.assertFalse(receipt["phase_bin_compression_theorem_proved"])
        self.assertFalse(receipt["phase_bin_balance_theorem_proved"])
        self.assertFalse(receipt["orbit_polygon_theorem_proved"])
        self.assertFalse(receipt[
            "pointwise_fixed_conductor_twisted_goldbach_estimate_proved"])
        self.assertFalse(receipt["signed_prime_correlation_estimate_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_q286_lower_support_component_pair_fixed_conductor_phase_antipodal_thin_exception(
            self):
        receipt = (
            q286_lower_support_component_pair_fixed_conductor_phase_antipodal_thin_exception_receipt())
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["active_channel_conductors"], (35, 77))
        self.assertEqual(receipt["phase_bin_count"], 12)
        self.assertEqual(receipt["high_ratio_threshold"], 0.75)
        self.assertEqual(receipt["thin_side_ratio_threshold"], 0.05)
        self.assertTrue(
            receipt["all_high_ratio_exceptions_have_thin_opposite_side"])
        by_label = {
            row["representative_label"]: row for row in receipt["rows"]}
        self.assertEqual(
            by_label[(0, 1, 5, 0)]["high_ratio_pair_count"], 1)
        self.assertAlmostEqual(
            by_label[(0, 1, 5, 0)][
                "maximum_small_to_large_side_ratio"],
            0.0)
        self.assertAlmostEqual(
            by_label[(0, 1, 5, 0)][
                "high_ratio_exception_abs_sum"],
            0.0031320675991354753)
        self.assertEqual(
            by_label[(0, 2, 6, 0)]["high_ratio_pair_count"], 2)
        self.assertAlmostEqual(
            by_label[(0, 2, 6, 0)][
                "maximum_small_to_large_side_ratio"],
            0.046829417626061014)
        self.assertAlmostEqual(
            by_label[(0, 2, 6, 0)][
                "high_ratio_exception_abs_sum"],
            0.024020095646099474)
        worst = receipt["worst_thin_side_ratio_row"]
        self.assertEqual(worst["representative_label"], (0, 2, 6, 0))
        self.assertTrue(receipt[
            "fixed_conductor_phase_antipodal_thin_exception_measured"])
        self.assertFalse(receipt[
            "phase_antipodal_thin_exception_theorem_proved"])
        self.assertFalse(receipt[
            "phase_antipodal_threshold_envelope_theorem_proved"])
        self.assertFalse(receipt[
            "phase_antipodal_pair_balance_theorem_proved"])
        self.assertFalse(receipt[
            "phase_antipodal_compression_theorem_proved"])
        self.assertFalse(receipt["phase_bin_compression_theorem_proved"])
        self.assertFalse(receipt["phase_bin_balance_theorem_proved"])
        self.assertFalse(receipt["orbit_polygon_theorem_proved"])
        self.assertFalse(receipt[
            "pointwise_fixed_conductor_twisted_goldbach_estimate_proved"])
        self.assertFalse(receipt["signed_prime_correlation_estimate_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_q286_lower_support_component_pair_fixed_conductor_phase_antipodal_exception_budget(
            self):
        receipt = (
            q286_lower_support_component_pair_fixed_conductor_phase_antipodal_exception_budget_receipt())
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["active_channel_conductors"], (35, 77))
        self.assertEqual(receipt["phase_bin_count"], 12)
        self.assertEqual(receipt["high_ratio_threshold"], 0.75)
        self.assertEqual(receipt["thin_side_ratio_threshold"], 0.05)
        self.assertEqual(
            receipt["passing_polygon_labels_by_exception_budget"],
            ((0, 1, 5, 0), (0, 2, 6, 0)))
        self.assertEqual(
            receipt["failing_polygon_labels_by_exception_budget"],
            ())
        self.assertTrue(
            receipt["all_residual_polygons_clear_by_exception_budget"])
        by_label = {
            row["representative_label"]: row for row in receipt["rows"]}
        self.assertAlmostEqual(
            by_label[(0, 1, 5, 0)][
                "allowed_high_ratio_exception_abs_sum_after_low_mass"],
            0.01712827835500897)
        self.assertAlmostEqual(
            by_label[(0, 1, 5, 0)][
                "high_ratio_exception_budget_margin"],
            0.013996210755873494)
        self.assertAlmostEqual(
            by_label[(0, 1, 5, 0)][
                "high_ratio_exception_fraction_of_budget"],
            0.18285945231731582)
        self.assertAlmostEqual(
            by_label[(0, 2, 6, 0)][
                "allowed_high_ratio_exception_abs_sum_after_low_mass"],
            0.033083936396965614)
        self.assertAlmostEqual(
            by_label[(0, 2, 6, 0)][
                "high_ratio_exception_budget_margin"],
            0.00906384075086614)
        self.assertAlmostEqual(
            by_label[(0, 2, 6, 0)][
                "high_ratio_exception_fraction_of_budget"],
            0.7260349964976521)
        worst = receipt["worst_exception_budget_margin_row"]
        self.assertEqual(worst["representative_label"], (0, 2, 6, 0))
        self.assertTrue(receipt[
            "fixed_conductor_phase_antipodal_exception_budget_measured"])
        self.assertFalse(receipt[
            "phase_antipodal_exception_budget_theorem_proved"])
        self.assertFalse(receipt[
            "phase_antipodal_thin_exception_theorem_proved"])
        self.assertFalse(receipt[
            "phase_antipodal_threshold_envelope_theorem_proved"])
        self.assertFalse(receipt[
            "phase_antipodal_pair_balance_theorem_proved"])
        self.assertFalse(receipt[
            "phase_antipodal_compression_theorem_proved"])
        self.assertFalse(receipt["phase_bin_compression_theorem_proved"])
        self.assertFalse(receipt["phase_bin_balance_theorem_proved"])
        self.assertFalse(receipt["orbit_polygon_theorem_proved"])
        self.assertFalse(receipt[
            "pointwise_fixed_conductor_twisted_goldbach_estimate_proved"])
        self.assertFalse(receipt["signed_prime_correlation_estimate_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_q286_lower_support_component_pair_fixed_conductor_phase_antipodal_nonthin_ratio(
            self):
        receipt = (
            q286_lower_support_component_pair_fixed_conductor_phase_antipodal_nonthin_ratio_receipt())
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["active_channel_conductors"], (35, 77))
        self.assertEqual(receipt["phase_bin_count"], 12)
        self.assertEqual(receipt["ratio_bound"], 0.75)
        self.assertEqual(receipt["thin_side_ratio_threshold"], 0.05)
        self.assertTrue(receipt["all_nonthin_pairs_clear_ratio_bound"])
        by_label = {
            row["representative_label"]: row for row in receipt["rows"]}
        self.assertEqual(by_label[(0, 1, 5, 0)]["nonthin_pair_count"], 5)
        self.assertEqual(by_label[(0, 1, 5, 0)]["thin_pair_count"], 1)
        self.assertAlmostEqual(
            by_label[(0, 1, 5, 0)]["nonthin_pair_mass_sum"],
            0.05563329167440221)
        self.assertAlmostEqual(
            by_label[(0, 1, 5, 0)]["nonthin_pair_abs_sum"],
            0.006097759984919418)
        self.assertAlmostEqual(
            by_label[(0, 1, 5, 0)][
                "maximum_nonthin_pair_cancellation_ratio"],
            0.2161610623897297)
        self.assertEqual(by_label[(0, 2, 6, 0)]["nonthin_pair_count"], 3)
        self.assertEqual(by_label[(0, 2, 6, 0)]["thin_pair_count"], 3)
        self.assertAlmostEqual(
            by_label[(0, 2, 6, 0)]["nonthin_pair_mass_sum"],
            0.03435908095179335)
        self.assertAlmostEqual(
            by_label[(0, 2, 6, 0)]["nonthin_pair_abs_sum"],
            0.012550306908359576)
        self.assertAlmostEqual(
            by_label[(0, 2, 6, 0)][
                "maximum_nonthin_pair_cancellation_ratio"],
            0.6626326478324716)
        self.assertAlmostEqual(
            by_label[(0, 2, 6, 0)]["nonthin_ratio_margin_to_bound"],
            0.08736735216752844)
        worst = receipt["worst_nonthin_ratio_margin_row"]
        self.assertEqual(worst["representative_label"], (0, 2, 6, 0))
        self.assertTrue(receipt[
            "fixed_conductor_phase_antipodal_nonthin_ratio_measured"])
        self.assertFalse(receipt[
            "phase_antipodal_nonthin_ratio_theorem_proved"])
        self.assertFalse(receipt[
            "phase_antipodal_exception_budget_theorem_proved"])
        self.assertFalse(receipt[
            "phase_antipodal_thin_exception_theorem_proved"])
        self.assertFalse(receipt[
            "phase_antipodal_threshold_envelope_theorem_proved"])
        self.assertFalse(receipt[
            "phase_antipodal_pair_balance_theorem_proved"])
        self.assertFalse(receipt[
            "phase_antipodal_compression_theorem_proved"])
        self.assertFalse(receipt["phase_bin_compression_theorem_proved"])
        self.assertFalse(receipt["phase_bin_balance_theorem_proved"])
        self.assertFalse(receipt["orbit_polygon_theorem_proved"])
        self.assertFalse(receipt[
            "pointwise_fixed_conductor_twisted_goldbach_estimate_proved"])
        self.assertFalse(receipt["signed_prime_correlation_estimate_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_q286_lower_support_component_pair_fixed_conductor_phase_antipodal_sector_geometry(
            self):
        receipt = (
            q286_lower_support_component_pair_fixed_conductor_phase_antipodal_sector_geometry_receipt())
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["active_channel_conductors"], (35, 77))
        self.assertEqual(receipt["phase_bin_count"], 12)
        self.assertEqual(receipt["ratio_bound"], 0.75)
        self.assertEqual(receipt["thin_side_ratio_threshold"], 0.05)
        self.assertAlmostEqual(
            receipt["sector_width_radians"], math.pi / 6.0)
        self.assertAlmostEqual(
            receipt["minimum_opposite_sector_angle_radians"],
            5.0 * math.pi / 6.0)
        self.assertAlmostEqual(receipt["sector_cosine_bound"],
                               -0.8660254037844387)
        self.assertTrue(
            receipt["all_nonthin_pairs_clear_by_sector_geometry"])
        by_label = {
            row["representative_label"]: row for row in receipt["rows"]}
        self.assertAlmostEqual(
            by_label[(0, 1, 5, 0)][
                "maximum_sector_geometry_envelope_ratio"],
            0.3325400441705825)
        self.assertAlmostEqual(
            by_label[(0, 1, 5, 0)][
                "sector_geometry_margin_to_ratio_bound"],
            0.4174599558294175)
        self.assertAlmostEqual(
            by_label[(0, 2, 6, 0)][
                "maximum_sector_geometry_envelope_ratio"],
            0.6862033816719031)
        self.assertAlmostEqual(
            by_label[(0, 2, 6, 0)][
                "sector_geometry_margin_to_ratio_bound"],
            0.06379661832809691)
        worst = receipt["worst_sector_geometry_margin_row"]
        self.assertEqual(worst["representative_label"], (0, 2, 6, 0))
        self.assertTrue(receipt[
            "fixed_conductor_phase_antipodal_sector_geometry_measured"])
        self.assertFalse(receipt[
            "phase_antipodal_sector_geometry_theorem_proved"])
        self.assertFalse(receipt[
            "phase_antipodal_nonthin_ratio_theorem_proved"])
        self.assertFalse(receipt[
            "phase_antipodal_exception_budget_theorem_proved"])
        self.assertFalse(receipt[
            "phase_antipodal_thin_exception_theorem_proved"])
        self.assertFalse(receipt[
            "phase_antipodal_threshold_envelope_theorem_proved"])
        self.assertFalse(receipt[
            "phase_antipodal_pair_balance_theorem_proved"])
        self.assertFalse(receipt[
            "phase_antipodal_compression_theorem_proved"])
        self.assertFalse(receipt["phase_bin_compression_theorem_proved"])
        self.assertFalse(receipt["phase_bin_balance_theorem_proved"])
        self.assertFalse(receipt["orbit_polygon_theorem_proved"])
        self.assertFalse(receipt[
            "pointwise_fixed_conductor_twisted_goldbach_estimate_proved"])
        self.assertFalse(receipt["signed_prime_correlation_estimate_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_q286_lower_support_component_pair_fixed_conductor_phase_antipodal_thin_large_side_budget(
            self):
        receipt = (
            q286_lower_support_component_pair_fixed_conductor_phase_antipodal_thin_large_side_budget_receipt())
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["active_channel_conductors"], (35, 77))
        self.assertEqual(receipt["phase_bin_count"], 12)
        self.assertEqual(receipt["ratio_bound"], 0.75)
        self.assertEqual(receipt["thin_side_ratio_threshold"], 0.05)
        self.assertEqual(
            receipt["passing_polygon_labels_by_thin_large_side_budget"],
            ((0, 1, 5, 0), (0, 2, 6, 0)))
        self.assertEqual(
            receipt["failing_polygon_labels_by_thin_large_side_budget"],
            ())
        self.assertTrue(
            receipt["all_residual_polygons_clear_by_thin_large_side_budget"])
        by_label = {
            row["representative_label"]: row for row in receipt["rows"]}
        self.assertAlmostEqual(
            by_label[(0, 1, 5, 0)]["thin_exception_large_side_mass"],
            0.0031320675991354753)
        self.assertAlmostEqual(
            by_label[(0, 1, 5, 0)]["thin_large_side_envelope"],
            0.0032886709790922493)
        self.assertAlmostEqual(
            by_label[(0, 1, 5, 0)][
                "thin_large_side_envelope_margin_to_exception_budget"],
            0.01383960737591672)
        self.assertAlmostEqual(
            by_label[(0, 2, 6, 0)]["thin_exception_large_side_mass"],
            0.02490542589058863)
        self.assertAlmostEqual(
            by_label[(0, 2, 6, 0)]["thin_large_side_envelope"],
            0.026150697185118062)
        self.assertAlmostEqual(
            by_label[(0, 2, 6, 0)][
                "thin_large_side_envelope_margin_to_exception_budget"],
            0.006933239211847552)
        worst = receipt["worst_thin_large_side_budget_margin_row"]
        self.assertEqual(worst["representative_label"], (0, 2, 6, 0))
        self.assertTrue(receipt[
            "fixed_conductor_phase_antipodal_thin_large_side_budget_measured"])
        self.assertFalse(receipt[
            "phase_antipodal_thin_large_side_budget_theorem_proved"])
        self.assertFalse(receipt[
            "phase_antipodal_sector_geometry_theorem_proved"])
        self.assertFalse(receipt[
            "phase_antipodal_nonthin_ratio_theorem_proved"])
        self.assertFalse(receipt[
            "phase_antipodal_exception_budget_theorem_proved"])
        self.assertFalse(receipt[
            "phase_antipodal_thin_exception_theorem_proved"])
        self.assertFalse(receipt[
            "phase_antipodal_threshold_envelope_theorem_proved"])
        self.assertFalse(receipt[
            "phase_antipodal_pair_balance_theorem_proved"])
        self.assertFalse(receipt[
            "phase_antipodal_compression_theorem_proved"])
        self.assertFalse(receipt["phase_bin_compression_theorem_proved"])
        self.assertFalse(receipt["phase_bin_balance_theorem_proved"])
        self.assertFalse(receipt["orbit_polygon_theorem_proved"])
        self.assertFalse(receipt[
            "pointwise_fixed_conductor_twisted_goldbach_estimate_proved"])
        self.assertFalse(receipt["signed_prime_correlation_estimate_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_q286_lower_support_component_pair_fixed_conductor_phase_antipodal_thin_large_side_support(
            self):
        receipt = (
            q286_lower_support_component_pair_fixed_conductor_phase_antipodal_thin_large_side_support_receipt())
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["active_channel_conductors"], (35, 77))
        self.assertEqual(receipt["phase_bin_count"], 12)
        self.assertEqual(receipt["ratio_bound"], 0.75)
        self.assertEqual(receipt["thin_side_ratio_threshold"], 0.05)
        self.assertEqual(receipt["total_high_ratio_exception_pair_count"], 3)
        self.assertEqual(receipt["large_side_bin_indices"], (4, 5, 7))
        self.assertEqual(receipt["large_side_orientations"],
                         ("opposite", "primary"))
        self.assertTrue(receipt["all_large_side_bins_distinct"])
        self.assertFalse(receipt["all_large_sides_single_orientation"])
        self.assertTrue(receipt[
            "single_orientation_large_side_theorem_falsified"])
        self.assertEqual(receipt["large_side_bin_mass"], (
            (4, 0.016182424368813935),
            (5, 0.008723001521774694),
            (7, 0.0031320675991354753),
        ))

        by_label = {
            row["representative_label"]: row for row in receipt["rows"]}
        self.assertEqual(
            by_label[(0, 1, 5, 0)]["large_side_bin_indices"], (7,))
        self.assertEqual(
            by_label[(0, 1, 5, 0)]["large_side_orientations"],
            ("opposite",))
        self.assertTrue(
            by_label[(0, 1, 5, 0)]["all_large_sides_single_orientation"])
        self.assertEqual(
            by_label[(0, 2, 6, 0)]["large_side_bin_indices"], (4, 5))
        self.assertEqual(
            by_label[(0, 2, 6, 0)]["large_side_orientations"],
            ("primary", "primary"))
        self.assertTrue(
            by_label[(0, 2, 6, 0)]["all_large_sides_single_orientation"])
        self.assertAlmostEqual(
            by_label[(0, 2, 6, 0)][
                "thin_large_side_envelope_margin_to_exception_budget"],
            0.006933239211847552)
        self.assertTrue(receipt[
            "fixed_conductor_phase_antipodal_thin_large_side_support_measured"])
        self.assertFalse(receipt[
            "phase_antipodal_thin_large_side_support_theorem_proved"])
        self.assertFalse(receipt[
            "phase_antipodal_thin_large_side_budget_theorem_proved"])
        self.assertFalse(receipt[
            "pointwise_fixed_conductor_twisted_goldbach_estimate_proved"])
        self.assertFalse(receipt["signed_prime_correlation_estimate_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_q286_lower_support_component_pair_fixed_conductor_phase_antipodal_thin_large_side_edge_support(
            self):
        receipt = (
            q286_lower_support_component_pair_fixed_conductor_phase_antipodal_thin_large_side_edge_support_receipt())
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["active_channel_conductors"], (35, 77))
        self.assertEqual(receipt["phase_bin_count"], 12)
        self.assertEqual(receipt["ratio_bound"], 0.75)
        self.assertEqual(receipt["thin_side_ratio_threshold"], 0.05)
        self.assertEqual(receipt["total_high_ratio_exception_pair_count"], 3)
        self.assertEqual(receipt["maximum_large_side_edge_count"], 5)
        self.assertAlmostEqual(
            receipt["maximum_largest_edge_fraction"],
            0.837564290793937)
        self.assertAlmostEqual(
            receipt["minimum_large_side_abs_to_edge_mass_ratio"],
            0.9959771123914983)
        self.assertTrue(receipt["single_edge_large_side_theorem_falsified"])

        by_label = {
            row["representative_label"]: row for row in receipt["rows"]}
        self.assertEqual(
            by_label[(0, 1, 5, 0)]["maximum_large_side_edge_count"], 3)
        self.assertAlmostEqual(
            by_label[(0, 1, 5, 0)]["maximum_largest_edge_fraction"],
            0.837564290793937)
        self.assertEqual(
            by_label[(0, 2, 6, 0)]["maximum_large_side_edge_count"], 5)
        self.assertAlmostEqual(
            by_label[(0, 2, 6, 0)]["maximum_largest_edge_fraction"],
            0.7605019497301692)

        hard_rows = {
            (row["bin_index"], row["opposite_bin_index"]): row
            for row in by_label[(0, 2, 6, 0)]["exception_rows"]}
        self.assertEqual(hard_rows[(4, 10)]["large_side_edge_count"], 5)
        self.assertAlmostEqual(
            hard_rows[(4, 10)]["largest_large_side_edge_fraction"],
            0.4406627296301651)
        self.assertEqual(
            hard_rows[(4, 10)]["top_large_side_edge_rows"][0]["orbit"],
            (26, 53))
        self.assertEqual(hard_rows[(5, 11)]["large_side_edge_count"], 2)
        self.assertAlmostEqual(
            hard_rows[(5, 11)]["large_side_abs_to_edge_mass_ratio"],
            0.9959771123914983)
        self.assertEqual(
            hard_rows[(5, 11)]["top_large_side_edge_rows"][0]["orbit"],
            (6, 73))

        easy_row = by_label[(0, 1, 5, 0)]["exception_rows"][0]
        self.assertEqual(easy_row["large_side_edge_count"], 3)
        self.assertEqual(
            easy_row["top_large_side_edge_rows"][0]["orbit"], (3, 76))
        self.assertTrue(receipt[
            "fixed_conductor_phase_antipodal_thin_large_side_edge_support_measured"])
        self.assertFalse(receipt[
            "phase_antipodal_thin_large_side_edge_support_theorem_proved"])
        self.assertFalse(receipt[
            "phase_antipodal_thin_large_side_support_theorem_proved"])
        self.assertFalse(receipt[
            "phase_antipodal_thin_large_side_budget_theorem_proved"])
        self.assertFalse(receipt[
            "pointwise_fixed_conductor_twisted_goldbach_estimate_proved"])
        self.assertFalse(receipt["signed_prime_correlation_estimate_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_q286_lower_support_component_pair_fixed_inequality_stress(
            self):
        _q286_first_two_mode_lower_tail_selected_cached.cache_clear()
        receipt = (
            q286_lower_support_component_pair_fixed_inequality_stress_receipt(
                targets=(1379072,),
                component_pairs=(((5, 7), (7, 11)), ((5,), (7,)))))
        cache_info = (
            _q286_first_two_mode_lower_tail_selected_cached.cache_info())
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["targets"], (1379072,))
        self.assertEqual(receipt["tested_target_count"], 1)
        self.assertEqual(receipt["component_pair_selection"],
                         "caller_supplied")
        self.assertEqual(receipt["tested_component_pair_count"], 2)
        self.assertEqual(receipt["phase_bin_count"], 12)
        self.assertEqual(receipt["ratio_bound"], 0.75)
        self.assertEqual(receipt["thin_side_ratio_threshold"], 0.05)
        self.assertIn(
            "(1 + thin_side_ratio_threshold) * thin_large_side_mass",
            receipt["quantified_inequality"])
        self.assertEqual(receipt["evaluated_component_pair_count"], 1)
        self.assertEqual(receipt["passing_component_pair_count"], 1)
        self.assertEqual(receipt["failing_component_pair_count"], 0)
        self.assertEqual(receipt["not_applicable_component_pair_count"], 1)
        self.assertEqual(receipt["error_component_pair_count"], 0)
        self.assertEqual(receipt["total_residual_polygon_row_count"], 2)
        self.assertEqual(receipt["total_failure_row_count"], 0)
        self.assertTrue(receipt["all_evaluated_rows_pass_fixed_inequality"])
        self.assertFalse(receipt["all_requested_component_pairs_evaluated"])
        self.assertEqual(receipt["counterexample_rows"], ())
        row = next(row for row in receipt["rows"] if row["evaluated"])
        self.assertEqual(row["component_pair"], ((5, 7), (7, 11)))
        self.assertEqual(row["status"], "passed")
        self.assertEqual(row["polygon_row_count"], 2)
        self.assertEqual(row["active_channel_conductors"], (35, 77))
        self.assertEqual(row["worst_representative_label"], (0, 2, 6, 0))
        self.assertAlmostEqual(row["worst_margin"], 0.006933239211847554)
        not_applicable_row = next(
            row for row in receipt["rows"] if not row["evaluated"])
        self.assertEqual(not_applicable_row["component_pair"], ((5,), (7,)))
        self.assertEqual(
            not_applicable_row["status"],
            "not_applicable_no_residual_polygons")
        self.assertTrue(receipt["fixed_inequality_stress_measured"])
        self.assertEqual(cache_info.misses, 1)
        self.assertGreaterEqual(cache_info.hits, 1)
        self.assertFalse(receipt["fixed_inequality_uniform_theorem_proved"])
        self.assertFalse(receipt[
            "phase_antipodal_thin_large_side_budget_theorem_proved"])
        self.assertFalse(receipt[
            "pointwise_fixed_conductor_twisted_goldbach_estimate_proved"])
        self.assertFalse(receipt["signed_prime_correlation_estimate_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_q286_lower_support_component_pair_fixed_inequality_target_census(
            self):
        _q286_first_two_mode_lower_tail_selected_cached.cache_clear()
        receipt = (
            q286_lower_support_component_pair_fixed_inequality_target_census_receipt(
                selected_targets=(1379072,)))
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["target_source"],
                         "caller_supplied_selected_targets")
        self.assertFalse(receipt["target_census_is_neutral_window_sample"])
        self.assertEqual(receipt["selected_targets"], (1379072,))
        self.assertEqual(receipt["scanned_target_count"], 1)
        self.assertEqual(receipt["tail_target_count"], 1)
        self.assertEqual(receipt["stress_tested_targets"], (1379072,))
        self.assertTrue(receipt["all_tail_targets_stressed"])
        self.assertEqual(receipt["component_pair"], ((5, 7), (7, 11)))
        self.assertEqual(receipt["phase_bin_count"], 12)
        self.assertEqual(receipt["ratio_bound"], 0.75)
        self.assertEqual(receipt["thin_side_ratio_threshold"], 0.05)
        self.assertEqual(receipt["evaluated_target_count"], 1)
        self.assertEqual(receipt["passing_target_count"], 1)
        self.assertEqual(receipt["failing_target_count"], 0)
        self.assertEqual(receipt["not_applicable_target_count"], 0)
        self.assertEqual(receipt["error_target_count"], 0)
        self.assertEqual(receipt["total_residual_polygon_row_count"], 2)
        self.assertEqual(receipt["total_failure_row_count"], 0)
        self.assertTrue(receipt["no_target_counterexamples_found"])
        self.assertTrue(receipt[
            "all_evaluated_target_rows_pass_fixed_inequality"])
        row = receipt["target_rows"][1379072]
        self.assertEqual(row["status"], "passed")
        self.assertEqual(row["polygon_row_count"], 2)
        self.assertEqual(row["worst_representative_label"], (0, 2, 6, 0))
        self.assertAlmostEqual(row["worst_margin"], 0.006933239211847554)
        self.assertTrue(receipt["fixed_inequality_target_census_measured"])
        self.assertFalse(receipt["fixed_inequality_uniform_theorem_proved"])
        self.assertFalse(receipt[
            "phase_antipodal_thin_large_side_budget_theorem_proved"])
        self.assertFalse(receipt[
            "pointwise_fixed_conductor_twisted_goldbach_estimate_proved"])
        self.assertFalse(receipt["signed_prime_correlation_estimate_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_q286_lower_support_component_pair_tail_selector_grid(self):
        receipt = q286_lower_support_component_pair_tail_selector_grid_receipt(
            starts=(1379072,), targets_per_window=5)
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["starts"], (1379072,))
        self.assertEqual(receipt["targets_per_window"], 5)
        self.assertEqual(receipt["window_count"], 1)
        self.assertEqual(receipt["scanned_target_count"], 5)
        self.assertEqual(receipt["tail_target_count"], 1)
        self.assertEqual(receipt["tail_targets"], (1379072,))
        self.assertEqual(receipt["window_rows"][0]["tail_targets"],
                         (1379072,))
        self.assertTrue(receipt["target_rows"][1379072][
            "selected_by_tail_predicate"])
        self.assertFalse(receipt["fixed_inequality_stress_run"])
        self.assertTrue(receipt["tail_selector_grid_measured"])
        self.assertFalse(receipt["fixed_inequality_uniform_theorem_proved"])
        self.assertFalse(receipt[
            "pointwise_fixed_conductor_twisted_goldbach_estimate_proved"])
        self.assertFalse(receipt["signed_prime_correlation_estimate_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_q286_active_lane_strict_closure_margin_census(self):
        receipt = q286_active_lane_strict_closure_margin_census_receipt(
            starts=(1222142, 1323632, 1379072), targets_per_window=5)
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["starts"], (1222142, 1323632, 1379072))
        self.assertEqual(receipt["scanned_target_count"], 15)
        self.assertEqual(receipt["tail_target_count"], 3)
        self.assertEqual(
            receipt["tail_targets"], (1222142, 1323632, 1379072))
        self.assertEqual(receipt["calibration_targets"], (
            14138, 1222142, 1323632, 1379072))
        self.assertAlmostEqual(
            receipt["calibrated_combined_floor_driver_floor"],
            -0.1017253843274695)
        self.assertAlmostEqual(
            receipt["calibrated_normalized_real_channel_linf_bound"],
            0.05885324711081062)
        self.assertAlmostEqual(
            receipt["calibrated_real_channel_l1_to_principal_mean"],
            15.262957606760978)
        self.assertEqual(
            receipt["positive_strict_margin_targets"],
            (1222142, 1323632, 1379072))
        self.assertEqual(receipt["nonpositive_strict_margin_targets"], ())
        self.assertTrue(receipt[
            "all_tail_targets_have_positive_strict_margin"])
        early_row = receipt["target_rows"][1222142]
        self.assertAlmostEqual(
            early_row["strict_closure_margin_to_calibrated_endpoint"],
            0.5506633762515991)
        self.assertAlmostEqual(
            early_row["channel_margin_contribution_to_strict_closure"],
            0.5169646774182272)
        self.assertEqual(
            early_row["dominant_strict_margin_source"], "channel")
        middle_row = receipt["target_rows"][1323632]
        self.assertAlmostEqual(
            middle_row["strict_closure_margin_to_calibrated_endpoint"],
            0.546820393849208)
        self.assertEqual(
            middle_row["dominant_strict_margin_source"], "channel")
        row = receipt["target_rows"][1379072]
        self.assertAlmostEqual(
            row["strict_closure_margin_to_calibrated_endpoint"],
            0.48379401372791037)
        self.assertEqual(row["dominant_strict_margin_source"], "channel")
        self.assertTrue(row["strict_closure_margin_positive"])
        self.assertTrue(row["positive_by_reconstructed_identity"])
        self.assertTrue(receipt["strict_closure_margin_census_measured"])
        self.assertFalse(receipt[
            "strict_closure_margin_theorem_proved"])
        self.assertFalse(receipt["combined_floor_driver_theorem_proved"])
        self.assertFalse(receipt[
            "pointwise_real_channel_norm_estimate_proved"])
        self.assertFalse(receipt["signed_prime_correlation_estimate_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_q286_first_three_removed_support_gram(self):
        receipt = q286_first_three_removed_support_gram_receipt(
            selected_targets=(14138, 24148, 30164))
        self.assertEqual(receipt["tested_target_count"], 3)
        self.assertEqual(receipt["component_labels"], (
            "q286_after_first_three", "q70", "q154",
            "small_supports", "non_q286", "complement"))
        self.assertIn(
            ("q70", "q154"), receipt["centered_correlation_matrix"])
        self.assertIn(
            ("non_q286", "complement"),
            receipt["centered_correlation_matrix"])
        self.assertTrue(receipt[
            "first_three_removed_support_gram_measured"])
        self.assertFalse(receipt["eventual_vector_envelope_proved"])

    def test_q286_first_three_removed_vector_stress(self):
        receipt = q286_first_three_removed_vector_stress_receipt(
            selected_targets=(14138, 24148, 30164))
        self.assertEqual(receipt["tested_target_count"], 3)
        self.assertEqual(receipt["component_labels"], (
            "q286_after_first_three", "q70", "q154", "small_supports"))
        self.assertEqual(receipt["minimum_complement_target"], 14138)
        self.assertIn("normalized_cross_term_total",
                      receipt["variance_decomposition"])
        self.assertIn("sum_direction_cosine",
                      receipt["minimum_complement_row"])
        self.assertTrue(receipt[
            "first_three_removed_vector_stress_measured"])
        self.assertFalse(receipt["norm_only_lower_bound_proved"])

    def test_q286_first_three_removed_low_tail_multi_period(self):
        receipt = q286_first_three_removed_low_tail_multi_period_receipt(
            base_start=14138, cycle_count=1, targets_per_cycle=1,
            low_threshold=.05, lifts=(0, 1))
        self.assertEqual(receipt["selected_base_targets"], (14138,))
        self.assertEqual(receipt["selected_base_count"], 1)
        self.assertEqual(receipt["selected_base_counts_by_cycle"], {0: 1})
        self.assertEqual(receipt["below_threshold_counts_by_lift"], {
            0: 1, 1: 0})
        self.assertEqual(receipt["maximum_first_clear_lift"], 1)
        self.assertTrue(receipt[
            "all_selected_bases_clear_threshold_on_tested_lifts"])
        self.assertTrue(receipt[
            "first_three_removed_low_tail_multi_period_measured"])
        self.assertFalse(receipt["eventual_lift_clearance_proved"])

    def test_q286_first_three_removed_complement_threshold_horizon(self):
        receipt = (
            q286_first_three_removed_complement_threshold_horizon_receipt(
                cycle_count=1, targets_per_cycle=3, thresholds=(.3,)))
        self.assertEqual(receipt["cycle_count"], 1)
        self.assertEqual(receipt["targets_per_cycle"], 3)
        self.assertEqual(receipt["thresholds"], (.3,))
        self.assertIn(.3, receipt["threshold_rows"])
        self.assertEqual(
            receipt["threshold_rows"][.3]["cycle_count_below_threshold"],
            0)
        self.assertTrue(receipt[
            "first_three_removed_complement_threshold_horizon_measured"])
        self.assertFalse(receipt["eventual_threshold_horizon_proved"])

    def test_q286_first_three_tail_threshold_horizon(self):
        receipt = q286_first_three_tail_threshold_horizon_receipt(
            cycle_count=1, targets_per_cycle=3,
            negative_tail_thresholds=(.3,))
        self.assertEqual(receipt["cycle_count"], 1)
        self.assertEqual(receipt["targets_per_cycle"], 3)
        self.assertEqual(receipt["negative_tail_thresholds"], (.3,))
        self.assertIn(.3, receipt["threshold_rows"])
        self.assertTrue(receipt[
            "first_three_tail_threshold_horizon_measured"])
        self.assertFalse(receipt[
            "uniform_first_three_tail_bound_proved"])

    def test_q286_first_three_tail_mode_only_horizon(self):
        receipt = q286_first_three_tail_mode_only_horizon_receipt(
            cycle_count=1, targets_per_cycle=5,
            negative_tail_thresholds=(.3,))
        baseline = q286_first_three_tail_threshold_horizon_receipt(
            cycle_count=1, targets_per_cycle=5,
            negative_tail_thresholds=(.3,))
        self.assertEqual(receipt["cycle_count"], 1)
        self.assertEqual(receipt["targets_per_cycle"], 5)
        self.assertEqual(receipt["negative_tail_thresholds"], (.3,))
        self.assertEqual(
            receipt["cycle_rows"][0]["threshold_counts"][.3],
            baseline["cycle_rows"][0]["threshold_counts"][.3])
        self.assertEqual(
            receipt["global_minimum_first_three_target"],
            baseline["global_minimum_first_three_target"])
        self.assertAlmostEqual(
            receipt["global_minimum_first_three_to_principal_ratio"],
            baseline["global_minimum_first_three_to_principal_ratio"])
        self.assertTrue(receipt[
            "first_three_tail_mode_only_horizon_measured"])
        self.assertFalse(receipt["complement_rescue_measured"])
        self.assertFalse(receipt["full_action_negativity_measured"])

    def test_q286_first_three_tail_mode_only_fast_horizon(self):
        receipt = q286_first_three_tail_mode_only_fast_horizon_receipt(
            cycle_count=1, targets_per_cycle=5,
            negative_tail_thresholds=(.3,))
        baseline = q286_first_three_tail_mode_only_horizon_receipt(
            cycle_count=1, targets_per_cycle=5,
            negative_tail_thresholds=(.3,))
        self.assertEqual(receipt["cycle_count"], 1)
        self.assertEqual(receipt["targets_per_cycle"], 5)
        self.assertEqual(receipt["negative_tail_thresholds"], (.3,))
        self.assertEqual(
            receipt["cycle_rows"][0]["threshold_counts"][.3],
            baseline["cycle_rows"][0]["threshold_counts"][.3])
        self.assertEqual(
            receipt["global_minimum_first_three_target"],
            baseline["global_minimum_first_three_target"])
        self.assertAlmostEqual(
            receipt["global_minimum_first_three_to_principal_ratio"],
            baseline["global_minimum_first_three_to_principal_ratio"],
            places=12)
        for target, row in receipt["rows"].items():
            self.assertAlmostEqual(
                row["first_three_modes_to_principal_ratio"],
                baseline["rows"][target][
                    "first_three_modes_to_principal_ratio"],
                places=12)
        self.assertTrue(receipt[
            "first_three_tail_mode_only_fast_horizon_measured"])
        self.assertFalse(receipt["complement_rescue_measured"])
        self.assertFalse(receipt["full_action_negativity_measured"])

    def test_q286_first_three_tail_mode_only_fast_late_tail_hit(self):
        receipt = q286_first_three_tail_mode_only_fast_horizon_receipt(
            start=1222142, cycle_count=1, targets_per_cycle=1,
            negative_tail_thresholds=(.3,))
        baseline = q286_first_three_tail_mode_only_horizon_receipt(
            start=1222142, cycle_count=1, targets_per_cycle=1,
            negative_tail_thresholds=(.3,))
        self.assertEqual(
            receipt["global_minimum_first_three_target"], 1222142)
        self.assertEqual(
            receipt["cycle_rows"][0]["threshold_counts"][.3], 1)
        self.assertEqual(
            receipt["cycle_rows"][0]["threshold_counts"][.3],
            baseline["cycle_rows"][0]["threshold_counts"][.3])
        self.assertAlmostEqual(
            receipt["global_minimum_first_three_to_principal_ratio"],
            baseline["global_minimum_first_three_to_principal_ratio"],
            places=12)
        self.assertLess(
            receipt["global_minimum_first_three_to_principal_ratio"], -.3)
        self.assertTrue(receipt[
            "first_three_tail_mode_only_fast_horizon_measured"])

    def test_q286_active_selector_necessary_condition_scout(self):
        receipt = q286_active_selector_necessary_condition_scout_receipt()
        self.assertEqual(receipt["starts"], (
            1120120, 1240240, 1500500, 2001000))
        self.assertEqual(receipt["cycle_count_per_start"], 12)
        self.assertEqual(receipt["targets_per_cycle"], 25)
        self.assertEqual(receipt["tested_target_count"], 1200)
        self.assertEqual(receipt["first_three_tail_target_count"], 0)
        self.assertEqual(receipt["first_three_tail_targets"], ())
        self.assertTrue(receipt[
            "active_selector_rows_excluded_by_first_three_condition"])
        self.assertEqual(
            receipt["global_minimum_first_three_row"][
                "minimum_first_three_target"],
            1240258)
        self.assertAlmostEqual(
            receipt["global_minimum_first_three_row"][
                "minimum_first_three_to_principal_ratio"],
            -0.23248485272080724)
        self.assertEqual(
            [row["first_three_tail_count_below_threshold"]
             for row in receipt["block_rows"]],
            [0, 0, 0, 0])
        self.assertTrue(receipt[
            "active_selector_necessary_condition_scout_measured"])
        self.assertFalse(receipt["first_two_selector_condition_measured"])
        self.assertFalse(receipt["strict_closure_stress_run"])
        self.assertFalse(receipt["fixed_inequality_stress_run"])
        self.assertFalse(receipt["active_selector_rarity_theorem_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_q286_first_three_weighted_discrepancy_norm(self):
        receipt = q286_first_three_weighted_discrepancy_norm_receipt(
            start=3309688, cycle_count=1, targets_per_cycle=1,
            theorem_threshold=.2, include_rows=True)
        self.assertEqual(receipt["tested_target_count"], 1)
        self.assertEqual(receipt["theorem_threshold"], .2)
        self.assertEqual(receipt["tail_target_count"], 0)
        self.assertEqual(receipt["negative_target_count"], 0)
        self.assertEqual(receipt["linf_certified_clear_count"], 0)
        self.assertEqual(receipt["l2_certified_clear_count"], 0)
        self.assertEqual(receipt["top_negative_alignment_rows"], ())
        self.assertIn(3309688, receipt["rows"])
        row = receipt["rows"][3309688]
        self.assertEqual(row["target_mod_286"], 96)
        self.assertGreater(
            row["first_three_to_principal_ratio"], 0)
        self.assertGreater(row["l2_alignment_cosine"], 0)
        self.assertGreater(row["linf_to_sufficient_ratio"], 5.0)
        self.assertGreater(row["l2_to_sufficient_ratio"], 2.0)
        self.assertEqual(
            receipt["l2_ratio_exceedance_counts"][1.0], 1)
        self.assertEqual(
            receipt["l2_ratio_exceedance_counts"][2.0], 1)
        self.assertEqual(
            receipt["l2_ratio_exceedance_counts"][3.0], 0)
        self.assertEqual(
            receipt["negative_l2_utilization_counts"][.125], 0)
        self.assertGreater(
            row["linf_bound_to_principal"],
            receipt["theorem_threshold"])
        self.assertEqual(
            receipt["maximum_linf_to_sufficient_ratio_row"]["target"],
            3309688)
        self.assertTrue(receipt[
            "first_three_weighted_discrepancy_norm_measured"])
        self.assertFalse(receipt[
            "eventual_weighted_discrepancy_estimate_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_q286_first_three_reflection_support_obstruction(self):
        receipt = q286_first_three_reflection_support_obstruction_receipt(
            tail_threshold=.3, slack_factor=1.25)
        self.assertEqual(receipt["arithmetic_modulus"], 286)
        self.assertEqual(receipt["even_target_residue_count"], 143)
        self.assertEqual(
            receipt["obstructed_even_target_residue_count"], 143)
        self.assertEqual(
            receipt["positive_witness_even_target_residue_count"], 143)
        self.assertTrue(receipt[
            "all_even_target_residues_have_extremal_obstruction"])
        self.assertTrue(receipt[
            "all_even_target_residues_have_positive_reflection_witness"])
        self.assertTrue(receipt[
            "support_reflection_rarity_theorem_refuted"])
        self.assertEqual(
            receipt["worst_extremal_row"]["target_residue"], 0)
        self.assertLess(
            receipt["worst_extremal_row"][
                "minimum_extremal_first_three_to_principal_ratio"],
            -6.7)
        self.assertEqual(
            receipt["least_negative_extremal_row"]["target_residue"], 10)
        self.assertLess(
            receipt["least_negative_extremal_row"][
                "minimum_extremal_first_three_to_principal_ratio"],
            -2.5)
        self.assertLess(
            receipt["least_negative_positive_witness_row"][
                "constructed_first_three_to_principal_ratio"],
            -.3)
        self.assertLess(
            receipt["maximum_reflection_weight_error"], 1e-12)
        self.assertLess(
            receipt["maximum_constructed_reconstruction_error"], 1e-12)
        self.assertTrue(receipt[
            "first_three_reflection_support_obstruction_measured"])
        self.assertFalse(receipt["eventual_first_three_tail_bound_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_q286_first_three_reflection_orbit_cap(self):
        receipt = q286_first_three_reflection_orbit_cap_receipt(
            start=10000, cycle_count=1, targets_per_cycle=501,
            tail_threshold=.3)
        self.assertEqual(receipt["arithmetic_modulus"], 286)
        self.assertEqual(receipt["tested_target_count"], 501)
        self.assertEqual(
            receipt["minimum_sufficient_max_orbit_mass_row"][
                "target_residue"],
            0)
        self.assertAlmostEqual(
            receipt["minimum_sufficient_max_orbit_mass_row"][
                "sufficient_max_orbit_mass"],
            0.016823304298596065)
        self.assertGreater(
            receipt["maximum_sufficient_max_orbit_mass_row"][
                "sufficient_max_orbit_mass"],
            0.026)
        self.assertEqual(receipt["cap_certified_target_count"], 0)
        self.assertEqual(
            receipt["cap_violation_target_count"],
            receipt["tested_targets_with_prime_pairs"])
        self.assertGreater(
            receipt["maximum_orbit_mass_row"][
                "maximum_reflection_orbit_mass_fraction"],
            .07)
        self.assertGreater(
            receipt["worst_cap_ratio_row"][
                "max_orbit_to_sufficient_ratio"],
            3.0)
        self.assertTrue(receipt[
            "first_three_reflection_orbit_cap_measured"])
        self.assertFalse(receipt[
            "reflection_orbit_cap_rarity_theorem_proved"])
        self.assertTrue(receipt["signed_orbit_cancellation_required"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_q286_first_three_reflection_orbit_signed_cancellation(self):
        receipt = (
            q286_first_three_reflection_orbit_signed_cancellation_receipt(
                start=10000, cycle_count=1, targets_per_cycle=501,
                tail_threshold=.3))
        self.assertEqual(receipt["arithmetic_modulus"], 286)
        self.assertEqual(receipt["tested_target_count"], 501)
        self.assertGreater(receipt["tested_targets_with_prime_pairs"], 450)
        self.assertGreater(receipt["negative_pressure_target_count"], 0)
        self.assertGreater(
            receipt["rescued_negative_pressure_target_count"], 0)
        self.assertGreater(
            receipt["rescued_negative_pressure_fraction"], .5)
        self.assertLess(
            receipt["maximum_orbit_reconstruction_error"], 1e-12)
        self.assertLess(
            receipt["maximum_reflection_pair_weight_fraction_error"], 1e-12)
        self.assertLess(
            receipt["maximum_negative_pressure_row"][
                "negative_orbit_contribution_to_principal_ratio"],
            -.3)
        self.assertGreater(
            receipt["maximum_positive_compensation_row"][
                "positive_orbit_contribution_to_principal_ratio"],
            .3)
        self.assertLess(
            receipt["minimum_compensation_surplus_row"][
                "positive_compensation_surplus_to_threshold"],
            0)
        self.assertTrue(receipt[
            "first_three_reflection_orbit_signed_cancellation_measured"])
        self.assertTrue(receipt["signed_orbit_cancellation_required"])
        self.assertFalse(receipt["eventual_first_three_tail_bound_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_q286_first_three_reflection_orbit_ratio_certificate(self):
        receipt = q286_first_three_reflection_orbit_ratio_certificate_receipt(
            start=1120120, cycle_count=1, targets_per_cycle=501,
            tail_threshold=.3, pressure_ceiling=1.25,
            compensation_ratio_floor=.76)
        self.assertEqual(receipt["arithmetic_modulus"], 286)
        self.assertEqual(receipt["tested_target_count"], 501)
        self.assertAlmostEqual(receipt["algebraic_certificate_bound"], -.3)
        self.assertTrue(receipt["algebraic_certificate_valid"])
        self.assertEqual(receipt["tail_target_count"], 0)
        self.assertEqual(
            receipt["certified_target_count"],
            receipt["tested_targets_with_prime_pairs"])
        self.assertEqual(receipt["certified_tail_target_count"], 0)
        self.assertEqual(receipt["uncertified_clear_target_count"], 0)
        self.assertEqual(receipt["uncertified_tail_target_count"], 0)
        self.assertGreater(
            receipt["minimum_ratio_row"][
                "positive_to_negative_pressure_ratio"],
            .76)
        self.assertLess(
            receipt["maximum_pressure_row"][
                "negative_pressure_to_principal_ratio"],
            1.25)
        self.assertTrue(receipt[
            "first_three_reflection_orbit_ratio_certificate_measured"])
        self.assertTrue(receipt[
            "ratio_certificate_algebraic_sufficient_condition"])
        self.assertTrue(receipt["ratio_certificate_all_targets_certified"])
        self.assertFalse(receipt[
            "ratio_certificate_has_certified_tail_counterexample"])
        self.assertFalse(receipt["eventual_pressure_ratio_bounds_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_q286_first_three_reflection_orbit_ratio_cycle_horizon(self):
        receipt = (
            q286_first_three_reflection_orbit_ratio_cycle_horizon_receipt(
                start=1120120, cycle_count=2, targets_per_cycle=101,
                tail_threshold=.3, pressure_ceiling=1.25,
                compensation_ratio_floor=.76))
        self.assertEqual(receipt["arithmetic_modulus"], 286)
        self.assertEqual(receipt["tested_target_count"], 202)
        self.assertEqual(len(receipt["cycle_rows"]), 2)
        self.assertAlmostEqual(receipt["algebraic_certificate_bound"], -.3)
        self.assertTrue(receipt["algebraic_certificate_valid"])
        self.assertEqual(receipt["tail_target_count"], 0)
        self.assertEqual(
            receipt["certified_target_count"],
            receipt["tested_targets_with_prime_pairs"])
        self.assertEqual(receipt["certified_tail_target_count"], 0)
        self.assertEqual(receipt["uncertified_tail_target_count"], 0)
        self.assertEqual(receipt["all_certified_cycles"], (0, 1))
        self.assertEqual(receipt["no_tail_cycles"], (0, 1))
        self.assertEqual(
            receipt["no_pressure_or_ratio_failure_cycles"], (0, 1))
        self.assertEqual(receipt["first_all_certified_cycle"], 0)
        self.assertEqual(receipt["first_no_tail_cycle"], 0)
        self.assertIsNone(receipt["last_uncertified_tail_cycle"])
        self.assertTrue(receipt[
            "first_three_reflection_orbit_ratio_cycle_horizon_measured"])
        self.assertFalse(receipt[
            "ratio_certificate_has_certified_tail_counterexample"])
        self.assertFalse(receipt["eventual_pressure_ratio_bounds_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_q286_first_three_reflection_orbit_dual_rectangle(self):
        receipt = q286_first_three_reflection_orbit_dual_rectangle_receipt(
            start=1157462, cycle_count=1, targets_per_cycle=1,
            tail_threshold=.3,
            rectangles=((1.25, .76), (1.0, .70)))
        self.assertEqual(receipt["arithmetic_modulus"], 286)
        self.assertEqual(receipt["tested_target_count"], 1)
        self.assertEqual(receipt["tail_target_count"], 0)
        self.assertEqual(receipt["union_certified_target_count"], 0)
        self.assertEqual(receipt["union_uncertified_clear_target_count"], 1)
        self.assertEqual(receipt["union_uncertified_tail_target_count"], 0)
        self.assertGreater(
            receipt["minimum_exact_curve_margin_row"][
                "exact_curve_margin"],
            0)
        for row in receipt["rectangle_rows"]:
            self.assertEqual(row["failure_count"], 1)
            self.assertEqual(row["tail_failure_count"], 0)
            self.assertEqual(row["clear_failure_count"], 1)
        intersection = next(
            iter(receipt["intersection_fail_sets"].values()))
        self.assertEqual(intersection["count"], 1)
        self.assertEqual(intersection["tail_count"], 0)
        self.assertEqual(intersection["clear_count"], 1)
        self.assertTrue(receipt[
            "first_three_reflection_orbit_dual_rectangle_measured"])
        self.assertTrue(receipt["all_tail_targets_union_uncertified"])
        self.assertFalse(receipt[
            "union_certificate_has_tail_counterexample"])
        self.assertFalse(receipt["eventual_dual_rectangle_bounds_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_q286_first_three_reflection_orbit_staircase_certificate(self):
        receipt = q286_first_three_reflection_orbit_dual_rectangle_receipt(
            start=1157462, cycle_count=1, targets_per_cycle=1,
            tail_threshold=.3,
            rectangles=((1.0, .70), (21.0 / 20.0, 5.0 / 7.0),
                        (1.25, .76)))
        self.assertEqual(receipt["tested_target_count"], 1)
        self.assertEqual(receipt["tail_target_count"], 0)
        self.assertEqual(receipt["union_certified_target_count"], 1)
        self.assertEqual(receipt["union_uncertified_target_count"], 0)
        row = receipt["minimum_exact_curve_margin_row"]
        self.assertGreater(row["exact_curve_margin"], 0)
        self.assertEqual(row["rectangle_certified"], (False, True, False))
        self.assertTrue(receipt[
            "first_three_reflection_orbit_dual_rectangle_measured"])
        self.assertFalse(receipt[
            "union_certificate_has_tail_counterexample"])
        self.assertFalse(receipt["eventual_dual_rectangle_bounds_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_q286_first_three_reflection_orbit_refined_staircase(self):
        rectangles = ((1.0, .70), (101.0 / 100.0, 71.0 / 101.0),
                      (21.0 / 20.0, 5.0 / 7.0), (1.25, .76))
        tail_receipt = q286_first_three_reflection_orbit_dual_rectangle_receipt(
            start=1222142, cycle_count=1, targets_per_cycle=1,
            tail_threshold=.3, rectangles=rectangles, include_rows=True)
        clear_receipt = q286_first_three_reflection_orbit_dual_rectangle_receipt(
            start=1242118, cycle_count=1, targets_per_cycle=1,
            tail_threshold=.3, rectangles=rectangles, include_rows=True)
        tail_row = tail_receipt["target_rows"][1222142]
        clear_row = clear_receipt["target_rows"][1242118]
        self.assertTrue(tail_row["tail_target"])
        self.assertFalse(tail_row["union_certified"])
        self.assertEqual(
            tail_row["rectangle_certified"],
            (False, False, False, False))
        self.assertFalse(clear_row["tail_target"])
        self.assertTrue(clear_row["union_certified"])
        self.assertEqual(
            clear_row["rectangle_certified"],
            (False, True, False, False))
        self.assertFalse(clear_receipt[
            "union_certificate_has_tail_counterexample"])
        self.assertTrue(clear_receipt[
            "first_three_reflection_orbit_dual_rectangle_measured"])
        self.assertFalse(clear_receipt[
            "eventual_dual_rectangle_bounds_proved"])
        self.assertFalse(clear_receipt["goldbach_proved"])

    def test_q286_first_three_positive_orbit_landing_profile(self):
        receipt = q286_first_three_positive_orbit_landing_profile_receipt(
            start=1222142, cycle_count=2, targets_per_cycle=5005,
            reference_target=1222142)
        self.assertEqual(receipt["tested_target_count"], 10010)
        self.assertEqual(receipt["near_boundary_target_count"], 3)
        self.assertEqual(receipt["near_boundary_tail_target_count"], 1)
        self.assertEqual(receipt["near_boundary_clear_target_count"], 2)
        self.assertEqual(receipt["reference_target"], 1222142)
        self.assertIn(
            1242118, receipt[
                "balanced_pressure_and_compensation_targets"])
        self.assertIn(
            1240888, receipt[
                "positive_compensation_overcomes_worse_pressure_targets"])
        rows = {row["target"]: row for row in receipt["pair_rows"]}
        self.assertGreater(
            rows[1242118]["pressure_reduction_component"], 0)
        self.assertGreater(
            rows[1242118][
                "positive_compensation_increase_component"], 0)
        self.assertLess(
            rows[1240888]["pressure_reduction_component"], 0)
        self.assertGreater(
            rows[1240888][
                "positive_compensation_increase_component"],
            -rows[1240888]["pressure_reduction_component"])
        self.assertLess(rows[1240888]["reconstruction_error"], 1e-9)
        self.assertTrue(receipt["positive_orbit_landing_profile_measured"])
        self.assertFalse(receipt[
            "landing_classification_recurrence_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_q286_first_three_positive_mass_threshold_falsifier(self):
        high_tail = (
            q286_first_three_positive_mass_threshold_falsifier_receipt(
                start=10348, cycle_count=1, targets_per_cycle=1,
                positive_mass_floor=.49))
        self.assertEqual(high_tail["near_boundary_target_count"], 1)
        self.assertEqual(
            high_tail["high_positive_mass_tail_counterexample_count"], 1)
        self.assertFalse(high_tail[
            "positive_mass_floor_certifies_clear_on_this_window"])
        low_clear = (
            q286_first_three_positive_mass_threshold_falsifier_receipt(
                start=10116, cycle_count=1, targets_per_cycle=1,
                positive_mass_floor=.49))
        self.assertEqual(low_clear["near_boundary_target_count"], 1)
        self.assertEqual(
            low_clear["low_positive_mass_clear_exception_count"], 1)
        self.assertFalse(low_clear[
            "positive_mass_floor_catches_all_clear_rows_on_this_window"])
        holdout = (
            q286_first_three_positive_mass_threshold_falsifier_receipt(
                start=1222142, cycle_count=2, targets_per_cycle=5005,
                positive_mass_floor=.49))
        self.assertEqual(holdout["near_boundary_target_count"], 3)
        self.assertEqual(
            holdout["high_positive_mass_tail_counterexample_count"], 0)
        self.assertEqual(
            holdout["low_positive_mass_clear_exception_count"], 0)
        self.assertTrue(holdout[
            "positive_mass_floor_certifies_clear_on_this_window"])
        self.assertFalse(holdout["positive_mass_threshold_theorem_proved"])
        self.assertFalse(holdout["goldbach_proved"])

    def test_q286_first_three_character_mixture_norm(self):
        receipt = q286_first_three_character_mixture_norm_receipt(
            targets=(1222142,), theorem_threshold=.2)
        self.assertEqual(receipt["tested_target_count"], 1)
        self.assertEqual(receipt["character_product_count"], 99)
        self.assertEqual(receipt["negative_targets"], (1222142,))
        self.assertIn(1222142, receipt["rows"])
        row = receipt["rows"][1222142]
        self.assertLess(row["first_three_to_principal_ratio"], -.3)
        self.assertGreater(
            row["triangle_character_bound_to_principal"],
            abs(row["first_three_to_principal_ratio"]))
        self.assertGreater(
            row["vector_l2_character_bound_to_principal"],
            abs(row["first_three_to_principal_ratio"]))
        self.assertGreater(row["triangle_to_sufficient_ratio"], 1.0)
        self.assertGreater(row["vector_l2_to_sufficient_ratio"], 1.0)
        self.assertLess(row["first_three_reconstruction_error"], 1e-9)
        self.assertGreater(
            receipt["character_coefficient_l1_to_principal_mean"],
            receipt["character_coefficient_l2_to_principal_mean"])
        self.assertTrue(receipt[
            "first_three_character_mixture_norm_measured"])
        self.assertFalse(receipt[
            "pointwise_character_sum_estimate_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_q286_first_three_character_mode_coordinate(self):
        receipt = q286_first_three_character_mode_coordinate_receipt(
            targets=(1222142,))
        self.assertEqual(receipt["tested_target_count"], 1)
        self.assertEqual(receipt["negative_targets"], (1222142,))
        row = receipt["rows"][1222142]
        self.assertLess(row["first_three_to_principal_ratio"], -.3)
        self.assertEqual(len(row["mode_rows"]), 3)
        self.assertLess(row["mode_reconstruction_error"], 1e-9)
        self.assertGreater(
            row["mode_contribution_absolute_sum_to_principal"],
            abs(row["first_three_to_principal_ratio"]))
        self.assertLess(
            row["signed_to_absolute_mode_contribution_ratio"], 0)
        self.assertGreaterEqual(row["dominant_mode_absolute_fraction"], 1 / 3)
        self.assertTrue(receipt[
            "first_three_character_mode_coordinate_measured"])
        self.assertFalse(receipt[
            "pointwise_character_sum_estimate_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_q286_first_two_mode_sign_window(self):
        receipt = q286_first_two_mode_sign_window_receipt(
            start=1222142, cycle_count=1, targets_per_cycle=1,
            tail_threshold=.3, include_rows=True)
        self.assertEqual(receipt["tested_target_count"], 1)
        self.assertEqual(receipt["first_three_negative_count"], 1)
        self.assertEqual(receipt["first_three_tail_count"], 1)
        self.assertEqual(receipt["first_three_tail_targets"], (1222142,))
        self.assertEqual(receipt["first_two_both_negative_count"], 1)
        self.assertEqual(
            receipt["mode_1_2_sign_pair_counts"]["--"], 1)
        row = receipt["rows"][1222142]
        self.assertEqual(row["mode_1_2_sign_pair"], "--")
        self.assertLess(row["mode_1_to_principal_ratio"], 0)
        self.assertLess(row["mode_2_to_principal_ratio"], 0)
        self.assertLess(row["first_three_to_principal_ratio"], -.3)
        self.assertLess(row["mode_reconstruction_error"], 1e-9)
        self.assertTrue(receipt["first_two_mode_sign_window_measured"])
        self.assertFalse(receipt["eventual_mode_sign_pattern_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_q286_first_two_mode_subcone_magnitude_window(self):
        receipt = q286_first_two_mode_subcone_magnitude_window_receipt(
            start=1222142, cycle_count=1, targets_per_cycle=1,
            first_two_negative_thresholds=(.2,), tail_threshold=.3)
        self.assertEqual(receipt["tested_target_count"], 1)
        self.assertEqual(receipt["first_three_tail_count"], 1)
        self.assertEqual(receipt["both_negative_tail_count"], 1)
        self.assertEqual(receipt["both_negative_tail_fraction"], 1.0)
        self.assertIn(.2, receipt["threshold_rows"])
        self.assertEqual(receipt["threshold_rows"][.2]["targets"], (1222142,))
        self.assertEqual(
            receipt["threshold_rows"][.2]["tail_targets"], (1222142,))
        self.assertTrue(receipt["threshold_rows"][.2][
            "threshold_targets_cover_all_tails"])
        self.assertEqual(
            receipt["most_negative_first_two_row"]["target"], 1222142)
        self.assertTrue(receipt[
            "first_two_mode_subcone_magnitude_window_measured"])
        self.assertFalse(receipt["eventual_mode_subcone_bound_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_q286_first_two_mode_subcone_complement_window(self):
        receipt = q286_first_two_mode_subcone_complement_window_receipt(
            start=1222142, cycle_count=1, targets_per_cycle=1,
            first_two_negative_thresholds=(.2,), tail_threshold=.3)
        self.assertEqual(receipt["tested_target_count"], 1)
        self.assertEqual(receipt["selected_subcone_targets"], (1222142,))
        self.assertEqual(receipt["negative_full_action_count"], 0)
        self.assertTrue(receipt["all_selected_subcone_targets_rescued"])
        self.assertIn(.2, receipt["threshold_rows"])
        threshold_row = receipt["threshold_rows"][.2]
        self.assertEqual(threshold_row["target_count"], 1)
        self.assertEqual(threshold_row["tail_target_count"], 1)
        self.assertEqual(threshold_row["rescued_tail_target_count"], 1)
        self.assertEqual(
            threshold_row["negative_tail_and_negative_full_count"], 0)
        self.assertEqual(threshold_row["tail_rescue_fraction"], 1.0)
        row = receipt["rows"][1222142]
        self.assertLess(row["first_two_modes_to_principal_ratio"], -.2)
        self.assertLess(row["first_three_to_principal_ratio"], -.3)
        self.assertGreater(row["complement_to_principal_ratio"], 0)
        self.assertGreater(row["full_action_to_principal_ratio"], 0)
        self.assertTrue(receipt[
            "first_two_mode_subcone_complement_window_measured"])
        self.assertFalse(receipt["eventual_complement_bound_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_q286_selected_first_three_alignment(self):
        receipt = q286_selected_first_three_alignment_receipt(
            targets=(1222142, 3305200), theorem_threshold=.2,
            alignment_ceiling=.375)
        self.assertEqual(receipt["tested_target_count"], 2)
        self.assertEqual(receipt["tail_targets"], (1222142,))
        self.assertEqual(receipt["negative_target_count"], 2)
        self.assertEqual(receipt["alignment_ceiling_violation_count"], 0)
        self.assertEqual(
            receipt["maximum_negative_alignment_row"]["target"],
            3305200)
        self.assertLess(
            receipt["maximum_negative_alignment_row"][
                "l2_negative_bound_utilization"],
            receipt["alignment_ceiling"])
        self.assertTrue(receipt[
            "selected_first_three_alignment_measured"])
        self.assertFalse(receipt["eventual_alignment_ceiling_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_q286_first_three_tail_alignment_window(self):
        receipt = q286_first_three_tail_alignment_window_receipt(
            start=1222142, cycle_count=1, targets_per_cycle=1,
            tail_threshold=.3, theorem_threshold=.2,
            alignment_ceiling=.375)
        self.assertEqual(receipt["tested_target_count"], 1)
        self.assertEqual(receipt["tail_targets"], (1222142,))
        self.assertEqual(receipt["tail_cycles"], (0,))
        self.assertEqual(receipt["alignment_ceiling_violation_count"], 0)
        self.assertEqual(
            receipt["maximum_negative_alignment_row"]["target"],
            1222142)
        self.assertLess(
            receipt["maximum_negative_alignment_row"][
                "l2_negative_bound_utilization"],
            receipt["alignment_ceiling"])
        self.assertTrue(receipt[
            "first_three_tail_alignment_window_measured"])
        self.assertFalse(receipt["eventual_alignment_ceiling_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_q286_selected_alignment_complement_certificate(self):
        receipt = q286_selected_alignment_complement_certificate_receipt(
            targets=(14138, 3305200), alignment_ceiling=.4)
        self.assertEqual(receipt["tested_target_count"], 2)
        self.assertIn(14138, receipt["failed_certificate_targets"])
        self.assertIn(3305200, receipt["certified_targets"])
        self.assertIn(14138, receipt["actual_negative_targets"])
        self.assertGreater(receipt["target_rows"][3305200][
            "certificate_margin_to_principal"], 0)
        self.assertLess(receipt["target_rows"][14138][
            "certificate_margin_to_principal"], 0)
        self.assertTrue(receipt[
            "alignment_complement_certificate_measured"])
        self.assertFalse(receipt["eventual_complement_bound_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_q286_first_three_tail_alignment_complement_window(self):
        receipt = q286_first_three_tail_alignment_complement_window_receipt(
            start=1222142, cycle_count=1, targets_per_cycle=1,
            tail_threshold=.3, theorem_threshold=.2,
            alignment_ceiling=.4)
        self.assertEqual(receipt["tested_target_count"], 1)
        self.assertEqual(receipt["tail_targets"], (1222142,))
        self.assertEqual(receipt["tail_cycles"], (0,))
        self.assertEqual(receipt["certified_targets"], (1222142,))
        self.assertEqual(receipt["failed_certificate_target_count"], 0)
        self.assertEqual(receipt["actual_negative_targets"], ())
        self.assertGreater(receipt["worst_certificate_margin_row"][
            "certificate_margin_to_principal"], 0)
        self.assertTrue(receipt[
            "first_three_tail_alignment_complement_window_measured"])
        self.assertFalse(receipt["eventual_alignment_ceiling_proved"])
        self.assertFalse(receipt["eventual_complement_bound_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_q286_first_three_tail_hit_residue_profile(self):
        receipt = q286_first_three_tail_hit_residue_profile_receipt(
            start=1222142, cycle_count=1, targets_per_cycle=1,
            negative_tail_thresholds=(.3,))
        self.assertEqual(receipt["tested_target_count"], 1)
        self.assertIn(.3, receipt["threshold_profiles"])
        profile = receipt["threshold_profiles"][.3]
        self.assertEqual(profile["tail_target_count"], 1)
        self.assertEqual(profile["tail_targets"], (1222142,))
        self.assertEqual(profile["residue_counts_mod_286"], {64: 1})
        self.assertEqual(profile["residue_counts_mod_10010"], {922: 1})
        self.assertEqual(profile["target_offset_counts"], {0: 1})
        self.assertTrue(profile["single_residue_mod_286_explains_all_hits"])
        self.assertTrue(profile["single_period_residue_explains_all_hits"])
        self.assertEqual(profile["hit_rows"][0]["target_mod_286"], 64)
        self.assertEqual(profile["hit_rows"][0]["target_mod_10010"], 922)
        self.assertLess(profile["hit_rows"][0][
            "first_three_modes_to_principal_ratio"], -.3)
        self.assertTrue(receipt[
            "first_three_tail_hit_residue_profile_measured"])
        self.assertFalse(receipt["eventual_first_three_tail_bound_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_q286_first_three_tail_threshold_ladder(self):
        receipt = q286_first_three_tail_threshold_ladder_receipt(
            start=1222142, cycle_count=1, targets_per_cycle=1,
            negative_tail_thresholds=(.2, .3, .4), block_size=1)
        self.assertEqual(receipt["tested_target_count"], 1)
        self.assertEqual(receipt["negative_tail_thresholds"], (.2, .3, .4))
        self.assertEqual(
            receipt["threshold_rows"][.2]["tail_target_count"], 1)
        self.assertEqual(
            receipt["threshold_rows"][.3]["tail_target_count"], 1)
        self.assertEqual(
            receipt["threshold_rows"][.4]["tail_target_count"], 0)
        self.assertEqual(receipt["cleared_thresholds"], (.4,))
        self.assertEqual(receipt["strongest_cleared_threshold"], .4)
        self.assertEqual(receipt["block_rows"][0][
            "threshold_counts"], {.2: 1, .3: 1, .4: 0})
        self.assertFalse(receipt["source_fast_horizon_receipt"][
            "target_rows_included"])
        self.assertEqual(receipt["source_fast_horizon_receipt"]["rows"], {})
        self.assertEqual(receipt["global_minimum_first_three_target"], 1222142)
        self.assertLess(
            receipt["global_minimum_first_three_to_principal_ratio"], -.3)
        self.assertTrue(receipt[
            "first_three_tail_threshold_ladder_measured"])
        self.assertFalse(receipt["eventual_first_three_tail_bound_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_q286_first_three_complement_cooccurrence(self):
        receipt = q286_first_three_complement_cooccurrence_receipt(
            cycle_count=1, targets_per_cycle=3,
            negative_tail_thresholds=(.3,))
        self.assertEqual(receipt["cycle_count"], 1)
        self.assertEqual(receipt["targets_per_cycle"], 3)
        self.assertEqual(receipt["negative_tail_thresholds"], (.3,))
        self.assertIn(.3, receipt["threshold_rows"])
        threshold_row = receipt["threshold_rows"][.3]
        self.assertEqual(
            threshold_row["tail_target_count"],
            len(threshold_row["tail_targets"]))
        self.assertEqual(
            threshold_row["rescued_tail_target_count"],
            len(threshold_row["rescued_tail_targets"]))
        self.assertEqual(receipt[
            "minimum_recombined_margin_target"],
            receipt["minimum_full_action_target"])
        self.assertTrue(receipt[
            "first_three_complement_cooccurrence_measured"])
        self.assertFalse(receipt[
            "pointwise_cooccurrence_estimate_proved"])

    def test_q286_nonrescued_first_three_tail_classification(self):
        receipt = q286_nonrescued_first_three_tail_classification_receipt(
            start=14138, cycle_count=1, targets_per_cycle=1, threshold=.3,
            lift_offsets=(0, 1))
        self.assertEqual(receipt["threshold"], .3)
        self.assertEqual(receipt["cycle_count"], 1)
        self.assertEqual(receipt["tested_target_count"], 1)
        self.assertEqual(receipt["tail_target_count"], 1)
        self.assertEqual(receipt["nonrescued_target_count"], 1)
        self.assertEqual(receipt["nonrescued_targets"], (14138,))
        self.assertEqual(receipt["cycle_counts"], {0: 1})
        self.assertEqual(receipt["severity_counts"]["below_.75"], 1)
        self.assertEqual(receipt["lift_negative_counts_by_offset"], {
            0: 1, 1: 0})
        self.assertEqual(receipt["maximum_first_positive_lift"], 1)
        self.assertTrue(receipt[
            "all_nonrescued_clear_by_first_positive_lift"])
        self.assertEqual(receipt["lift_rows"][14138][
            "negative_full_lifts"], (0,))
        self.assertEqual(receipt["lift_rows"][14138][
            "tail_below_threshold_lifts"], (0,))
        self.assertTrue(receipt[
            "nonrescued_first_three_tail_classification_measured"])
        self.assertFalse(receipt[
            "nonrescued_classification_theorem_proved"])

    def test_q286_first_three_filter_order_audit(self):
        receipt = q286_first_three_filter_order_audit_receipt(
            start=14138, cycle_count=1, targets_per_cycle=1,
            tail_threshold=.3, complement_floor=.3)
        self.assertEqual(receipt["tested_target_count"], 1)
        self.assertEqual(receipt["predicate_counts"][
            "first_three_tail"], 1)
        self.assertEqual(receipt["predicate_counts"][
            "full_nonpositive"], 1)
        self.assertEqual(receipt["predicate_counts"][
            "nonrescued_first_three_tail"], 1)
        self.assertEqual(receipt["predicate_counts"][
            "rescued_first_three_tail"], 0)
        self.assertEqual(receipt["predicate_counts"][
            "complement_floor"], 0)
        first_three_order = next(
            row for row in receipt["ordered_filter_rows"]
            if row["order"] == "first_three_then_full_nonpositive")
        full_order = next(
            row for row in receipt["ordered_filter_rows"]
            if row["order"] == "full_nonpositive_then_first_three")
        self.assertEqual(first_three_order["final_survivor_targets"], (14138,))
        self.assertEqual(full_order["final_survivor_targets"], (14138,))
        self.assertEqual(
            first_three_order["final_survivor_targets"],
            full_order["final_survivor_targets"])
        self.assertTrue(receipt["filter_order_audit_measured"])
        self.assertFalse(receipt["filter_order_theorem_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_q286_nonrescued_first_three_tail_cycle_horizon(self):
        receipt = q286_nonrescued_first_three_tail_cycle_horizon_receipt(
            start=80070, cycle_count=2, targets_per_cycle=5005,
            threshold=.3)
        self.assertEqual(receipt["threshold"], .3)
        self.assertEqual(receipt["cycle_count"], 2)
        self.assertEqual(receipt["tested_target_count"], 10010)
        self.assertEqual(receipt["cycle_rows"][0]["global_cycle"], 7)
        self.assertEqual(receipt["cycle_rows"][1]["global_cycle"], 8)
        self.assertEqual(receipt["cycle_rows"][0][
            "nonrescued_tail_target_count"], 2)
        self.assertEqual(receipt["cycle_rows"][1][
            "nonrescued_tail_target_count"], 0)
        self.assertEqual(
            receipt["cycle_rows"][0]["tail_target_count"],
            len(receipt["cycle_rows"][0]["tail_targets"]))
        self.assertEqual(
            receipt["cycle_rows"][1]["rescued_tail_target_count"],
            len(receipt["cycle_rows"][1]["rescued_tail_targets"]))
        self.assertEqual(
            receipt["cycles_with_nonrescued_tail_targets"], (0,))
        self.assertEqual(receipt[
            "last_cycle_with_nonrescued_tail_target"], 0)
        self.assertEqual(receipt[
            "first_cycle_after_last_nonrescued_tail_target"], 1)
        self.assertEqual(receipt["suffix_clear_start_cycle"], 1)
        self.assertEqual(receipt["suffix_clear_global_cycle"], 8)
        self.assertFalse(receipt["all_cycles_clear_nonrescued_tail"])
        self.assertTrue(receipt[
            "nonrescued_first_three_tail_cycle_horizon_measured"])
        self.assertFalse(receipt[
            "eventual_nonrescued_tail_clearance_proved"])

    def test_q286_first_three_tail_rescue_profile(self):
        receipt = q286_first_three_tail_rescue_profile_receipt(
            start=440430, cycle_count=1, targets_per_cycle=5005,
            threshold=.3)
        self.assertEqual(receipt["threshold"], .3)
        self.assertEqual(receipt["cycle_rows"][0]["global_cycle"], 43)
        self.assertEqual(receipt["tail_targets"], (448346,))
        self.assertEqual(receipt["rescued_tail_targets"], (448346,))
        self.assertEqual(receipt["nonrescued_tail_targets"], ())
        self.assertTrue(receipt["all_tail_targets_rescued"])
        self.assertEqual(receipt["deepest_deficit_target"], 448346)
        self.assertEqual(receipt["minimum_rescue_margin_target"], 448346)
        row = receipt["tail_rows"][448346]
        self.assertAlmostEqual(
            row["first_three_to_principal_ratio"],
            -0.3106946886916736)
        self.assertAlmostEqual(
            row["complement_to_principal_ratio"],
            0.9781909468423949)
        self.assertAlmostEqual(
            row["rescue_margin_to_principal_ratio"],
            0.6674962581507213)
        self.assertTrue(receipt[
            "first_three_tail_rescue_profile_measured"])
        self.assertFalse(receipt[
            "eventual_complement_rescue_theorem_proved"])

    def test_q286_first_three_tail_rescue_floor_candidate(self):
        receipt = q286_first_three_tail_rescue_floor_candidate_receipt(
            start=380370, cycle_count=1, targets_per_cycle=5005,
            threshold=.3, complement_floor=.63, rescue_margin_floor=.3,
            deficit_ceiling=.47)
        self.assertEqual(receipt["cycle_rows"][0]["global_cycle"], 37)
        self.assertEqual(receipt["tail_target_count"], 12)
        self.assertEqual(receipt["nonrescued_tail_target_count"], 0)
        self.assertTrue(receipt["candidate_floor_passed"])
        self.assertEqual(receipt["complement_floor_violations"], ())
        self.assertEqual(receipt["rescue_margin_floor_violations"], ())
        self.assertEqual(receipt["deficit_ceiling_violations"], ())
        self.assertGreaterEqual(
            receipt["cycle_rows"][0][
                "minimum_complement_to_principal_ratio"], .63)
        self.assertGreaterEqual(
            receipt["cycle_rows"][0][
                "minimum_rescue_margin_to_principal_ratio"], .3)
        self.assertLessEqual(
            receipt["cycle_rows"][0][
                "maximum_deficit_to_principal_ratio"], .47)
        self.assertTrue(receipt[
            "first_three_tail_rescue_floor_candidate_measured"])
        self.assertFalse(receipt[
            "eventual_rescue_floor_theorem_proved"])

    def test_q286_first_three_removed_low_tail_lift(self):
        receipt = q286_first_three_removed_low_tail_lift_receipt(
            base_targets=(14138,), lifts=(0, 1))
        self.assertEqual(receipt["base_targets"], (14138,))
        self.assertEqual(receipt["lifts"], (0, 1))
        self.assertEqual(receipt["tested_target_count"], 2)
        self.assertEqual(
            receipt["base_rows"][14138]["minimum_complement_lift"], 0)
        self.assertGreater(
            receipt["base_rows"][14138]["lift_rows"][1][
                "complement_to_principal_ratio"],
            receipt["base_rows"][14138]["lift_rows"][0][
                "complement_to_principal_ratio"])
        self.assertTrue(receipt[
            "first_three_removed_low_tail_lift_measured"])
        self.assertFalse(receipt["eventual_lift_clearance_proved"])

    def test_q286_first_three_removed_low_tail_auto_lift(self):
        receipt = q286_first_three_removed_low_tail_auto_lift_receipt(
            base_start=14138, base_targets_per_cycle=1,
            low_threshold=.05, lifts=(0, 1))
        self.assertEqual(receipt["selected_base_targets"], (14138,))
        self.assertEqual(receipt["selected_base_count"], 1)
        self.assertEqual(receipt["maximum_first_clear_lift"], 1)
        self.assertTrue(receipt[
            "all_selected_bases_clear_threshold_on_tested_lifts"])
        self.assertTrue(receipt[
            "first_three_removed_low_tail_auto_lift_measured"])
        self.assertFalse(receipt["eventual_lift_clearance_proved"])

    def test_q286_singular_mode_lower_tail_stress(self):
        receipt = q286_singular_mode_lower_tail_stress_receipt(
            targets=(10424, 10664, 14732))
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["support"], (11, 13))
        self.assertEqual(receipt["natural_modulus"], 286)
        self.assertEqual(receipt["targets"], (10424, 10664, 14732))
        self.assertEqual(
            receipt["negative_q286_deviation_targets"], (10424, 10664))
        self.assertEqual(
            receipt["nonnegative_q286_deviation_targets"], (14732,))
        self.assertAlmostEqual(
            receipt["maximum_negative_top_four_signed_residual_fraction"],
            .055453596612858175, places=14)
        self.assertEqual(
            receipt["worst_negative_top_four_residual_target"], 10664)
        self.assertEqual(
            receipt["worst_all_top_four_residual_target"], 14732)
        self.assertTrue(
            receipt["top_four_modes_control_sampled_negative_lower_tail"])
        self.assertFalse(receipt["top_four_modes_control_all_sampled_targets"])
        self.assertFalse(receipt["top_four_tail_paid_by_cauchy_on_sample"])
        self.assertTrue(
            receipt["singular_mode_lower_tail_stress_measured"])
        self.assertFalse(receipt["signed_prime_correlation_estimate_proved"])
        self.assertFalse(receipt["formal_signed_error_identification_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_q286_singular_mode_cycle_scan(self):
        receipt = q286_singular_mode_cycle_scan_receipt(
            cycle_count=1, targets_per_cycle=9)
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["support"], (11, 13))
        self.assertEqual(receipt["natural_modulus"], 286)
        self.assertEqual(receipt["start"], 10000)
        self.assertEqual(receipt["cycle_count"], 1)
        self.assertEqual(receipt["targets_per_cycle"], 9)
        self.assertEqual(receipt["significant_negative_ratio"], -.4)
        self.assertEqual(receipt["tested_modes"], (2, 4, 6, 9))
        self.assertEqual(receipt["tested_target_count"], 9)
        self.assertTrue(receipt["singular_mode_cycle_scan_measured"])
        self.assertIn(0, receipt["cycle_rows"])
        self.assertEqual(
            receipt["cycle_rows"][0]["tested_target_count"], 9)
        self.assertFalse(receipt["signed_prime_correlation_estimate_proved"])
        self.assertFalse(receipt["formal_signed_error_identification_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_symbolic_principal_plus_centered_channel(self):
        receipt = symbolic_principal_plus_centered_channel_receipt()
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["common_modulus"], 130)
        self.assertEqual(receipt["unit_group_order"], 48)
        self.assertEqual(
            receipt["principal_constant_rational_witness"], (-3143, 16))
        self.assertLess(
            receipt["principal_constant_rational_error"], 1e-10)
        self.assertEqual(
            receipt["principal_constant_rational_tolerance"], 1e-10)
        self.assertLess(
            receipt[
                "quotient77_source_equals_constant_plus_fiber_shadow_error"],
            1e-12)
        self.assertEqual(receipt["central_unit_threshold"], 40)
        self.assertTrue(receipt["principal_constant_channel_identified"])
        self.assertTrue(receipt["centered_channel_identified"])
        self.assertTrue(receipt[
            "strict_central_quotient77_channel_identified_for_N_ge_40"])
        self.assertFalse(receipt["endpoint_or_noncentral_terms_analyzed"])
        self.assertFalse(receipt["full_outer_assembly_identification_proved"])
        self.assertFalse(receipt["formal_signed_error_identification_proved"])
        self.assertFalse(receipt["goldbach_proved"])

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
