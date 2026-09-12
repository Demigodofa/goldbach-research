import unittest

from lcm_sawtooth_goldbach_transfer import (
    all_even_residue_goldbach_main_receipt,
    all_residue_centered_outer_fiber_shadow_receipt,
    canonical_direct_resonant_goldbach_main_receipt,
    combined_coefficient_character_spectrum_receipt,
    combined_fixed_strict_central_coefficient_receipt,
    count_four_outer_holdout_sector_receipt,
    holdout_full_projected_prime_coefficient_receipt,
    holdout_lag_fiber_shadow_candidate_receipt,
    holdout_q65_dual_prime_target_sum_receipt,
    holdout_q65_active_row_bridge_receipt,
    holdout_q65_naive_spatial_prime_coefficient_receipt,
    holdout_q65_projected_spatial_fiber_bridge_receipt,
    holdout_q55_projected_principal_channel_receipt,
    centered_outer_fiber_shadow_receipt,
    direct_source_fiber_average_receipt,
    even_even_goldbach_transfer_receipt,
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
