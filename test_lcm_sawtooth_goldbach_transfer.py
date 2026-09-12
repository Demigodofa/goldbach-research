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
    q286_leading_singular_mode_contribution_receipt,
    q286_residue_discrepancy_profile_receipt,
    q286_separable_mode_coefficient_receipt,
    q286_separable_mode_local_bias_receipt,
    q286_singular_mode_approximation_receipt,
    q286_singular_mode_cycle_scan_receipt,
    q286_singular_mode_lower_tail_stress_receipt,
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
