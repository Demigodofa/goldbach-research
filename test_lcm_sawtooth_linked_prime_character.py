import unittest

from lcm_sawtooth_linked_prime_character import (
    _principal_character_row,
    all_residue_reflection_block_receipt,
    affine_reflection_residue_scan_receipt,
    affine_reflection_selection_receipt,
    linked_prime_character_receipt,
    linked_prime_centering_receipt,
    linked_prime_parity_selection_receipt,
    recombined_centered_character_receipt,
    recombined_centered_prime_phase_scan_receipt,
    residue_orbit_reinforcement_receipt,
    residue_orbit_sign_cube_receipt,
    resonant_progression_diagonal_square_receipt,
    resonant_progression_discrepancy_receipt,
)


class LinkedPrimeCharacterTests(unittest.TestCase):
    def test_guards(self):
        self.assertEqual(
            _principal_character_row(((1, 0), (0, 0), (0, 1))), 1)
        with self.assertRaises(AssertionError):
            _principal_character_row(((1, 0), (0, 1)))
        with self.assertRaises(ValueError):
            linked_prime_character_receipt(targets=(21,))
        with self.assertRaises(ValueError):
            linked_prime_character_receipt(targets=(44,))
        with self.assertRaises(ValueError):
            linked_prime_character_receipt(tolerance=-1)
        with self.assertRaises(ValueError):
            linked_prime_character_receipt(batch_size=0)
        with self.assertRaises(ValueError):
            linked_prime_parity_selection_receipt(tolerance=-1)
        with self.assertRaises(ValueError):
            linked_prime_parity_selection_receipt(batch_size=0)
        with self.assertRaises(ValueError):
            affine_reflection_selection_receipt(
                maximum_symmetric_energy_fraction=-.01)
        with self.assertRaises(ValueError):
            affine_reflection_selection_receipt(
                maximum_symmetric_energy_fraction=1.01)
        with self.assertRaises(ValueError):
            affine_reflection_residue_scan_receipt(
                maximum_symmetric_energy_fraction=-.01)
        with self.assertRaises(ValueError):
            affine_reflection_residue_scan_receipt(tolerance=-1)
        with self.assertRaises(ValueError):
            affine_reflection_residue_scan_receipt(batch_size=0)
        with self.assertRaises(ValueError):
            recombined_centered_character_receipt(leading_count=0)
        with self.assertRaises(ValueError):
            recombined_centered_character_receipt(
                minimum_leading_energy_fraction=1.01)
        with self.assertRaises(ValueError):
            recombined_centered_prime_phase_scan_receipt(
                target_minimum=999)
        with self.assertRaises(ValueError):
            recombined_centered_prime_phase_scan_receipt(
                target_minimum=1002, target_maximum=1000)
        with self.assertRaises(ValueError):
            recombined_centered_prime_phase_scan_receipt(
                maximum_phase_ratio=1.01)
        with self.assertRaises(ValueError):
            recombined_centered_prime_phase_scan_receipt(
                maximum_local_bias_ratio=1.01)
        with self.assertRaises(ValueError):
            resonant_progression_discrepancy_receipt(
                maximum_sqrt_pair_scaled_discrepancy=-1)
        with self.assertRaises(ValueError):
            resonant_progression_discrepancy_receipt(target_residue=87)
        with self.assertRaises(ValueError):
            resonant_progression_discrepancy_receipt(
                target_minimum=1000, target_maximum=1000)
        with self.assertRaises(ValueError):
            resonant_progression_diagonal_square_receipt(
                maximum_pointwise_ratio=-1)
        with self.assertRaises(ValueError):
            resonant_progression_diagonal_square_receipt(
                maximum_paired_pointwise_ratio=-1)
        with self.assertRaises(ValueError):
            resonant_progression_diagonal_square_receipt(target_residue=87)
        with self.assertRaises(ValueError):
            resonant_progression_diagonal_square_receipt(
                target_minimum=1000, target_maximum=1000)
        with self.assertRaises(ValueError):
            all_residue_reflection_block_receipt(target_minimum=999)
        with self.assertRaises(ValueError):
            all_residue_reflection_block_receipt(
                maximum_pointwise_ratio=-1)
        with self.assertRaises(ValueError):
            residue_orbit_reinforcement_receipt(target_residue=71)
        with self.assertRaises(ValueError):
            residue_orbit_reinforcement_receipt(
                maximum_aggregate_orbit_ratio=-1)
        with self.assertRaises(ValueError):
            residue_orbit_reinforcement_receipt(
                target_minimum=1000, target_maximum=1000)
        with self.assertRaises(ValueError):
            residue_orbit_sign_cube_receipt(
                maximum_actual_upper_tail_fraction=-.01)
        with self.assertRaises(ValueError):
            residue_orbit_sign_cube_receipt(
                minimum_stable_dyadic_block_count=-1)

    def test_exact_linked_prime_interface_and_cauchy_obstruction(self):
        receipt = linked_prime_character_receipt()
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["targets"], (1000, 1002))
        self.assertEqual(len(receipt["rows"]), 16)
        self.assertTrue(receipt[
            "all_linked_prime_character_identities_pass"])
        self.assertTrue(receipt[
            "all_character_second_moments_are_positive_residue_moments"])
        self.assertLess(receipt[
            "maximum_reconstruction_natural_scale_relative_error"], 1e-12)
        self.assertLess(receipt[
            "maximum_orthogonality_second_moment_relative_error"], 1e-12)
        self.assertLess(receipt[
            "maximum_cauchy_envelope_relative_identity_error"], 1e-12)
        self.assertAlmostEqual(
            receipt["cauchy_to_direct_triangle_ratio_range"][0],
            1.558534062995353, places=12)
        self.assertAlmostEqual(
            receipt["cauchy_to_direct_triangle_ratio_range"][1],
            2.0184105767602545, places=12)
        self.assertAlmostEqual(
            receipt["actual_to_cauchy_envelope_ratio_range"][0],
            .005839107257712018, places=12)
        self.assertAlmostEqual(
            receipt["actual_to_cauchy_envelope_ratio_range"][1],
            .16558610136723617, places=12)
        pair_counts = {
            target: {
                row["linked_prime_pair_count"]
                for (quotient, divisor, row_target), row
                in receipt["rows"].items()
                if row_target == target}
            for target in receipt["targets"]}
        self.assertEqual(pair_counts, {1000: {18}, 1002: {24}})
        for row in receipt["rows"].values():
            self.assertEqual(row["nonunit_prime_terms"], ())
            self.assertEqual(row["excluded_endpoint_prime_pairs"], ())
            self.assertTrue(row["linked_prime_character_identity_passes"])
            self.assertTrue(row[
                "orthogonality_reduces_to_positive_residue_second_moment"])
            self.assertLessEqual(row["actual_to_cauchy_envelope_ratio"], 1)
        witness = receipt["nonunit_correction_witness"]
        self.assertEqual(witness["target"], 24)
        self.assertEqual(witness["nonunit_prime_terms"], (5, 11))
        self.assertNotEqual(witness["nonunit_correction"], 0j)
        self.assertAlmostEqual(
            witness["nonunit_correction"].real,
            2675.3708724265452, places=9)
        self.assertTrue(witness["linked_prime_character_identity_passes"])
        self.assertFalse(receipt[
            "cauchy_improves_every_direct_triangle_bound"])
        self.assertFalse(receipt[
            "plain_per_target_character_cauchy_supplies_signed_saving"])
        self.assertFalse(receipt[
            "joint_coefficient_prime_phase_estimate_proved"])
        self.assertFalse(receipt["signed_prime_correlation_proved"])
        self.assertFalse(receipt["goldbach_proved"])
    def test_target_divisibility_selects_even_characters(self):
        receipt = linked_prime_parity_selection_receipt()
        self.assertEqual(
            receipt["target_by_quotient"], {77: 1040, 91: 1100})
        self.assertEqual(len(receipt["rows"]), 8)
        self.assertAlmostEqual(
            receipt[
                "maximum_odd_prime_correlation_relative_to_pair_weight"],
            2.2918614104476642e-15, places=20)
        self.assertLess(receipt[
            "maximum_parity_decomposition_natural_scale_relative_error"],
            1e-12)
        for (quotient, _), row in receipt["rows"].items():
            expected = (
                (1040, 20, 24) if quotient == 77 else (1100, 16, 20))
            target, pair_count, parity_count = expected
            self.assertEqual(row["target"], target)
            self.assertEqual(row["linked_prime_pair_count"], pair_count)
            self.assertEqual(row["nonunit_prime_terms"], ())
            self.assertTrue(row["target_divisible_by_common_modulus"])
            self.assertTrue(row["pair_symmetric_interval"])
            self.assertEqual(row["even_character_count"], parity_count)
            self.assertEqual(row["odd_character_count"], parity_count)
            self.assertTrue(row[
                "odd_character_pair_cancellation_applicable"])
            self.assertTrue(row[
                "all_odd_character_prime_correlations_cancel"])
            self.assertTrue(row[
                "even_characters_reconstruct_unit_correlation"])
        self.assertTrue(receipt[
            "all_odd_character_prime_correlations_cancel"])
        self.assertTrue(receipt[
            "all_even_characters_reconstruct_unit_correlations"])
        self.assertTrue(receipt[
            "target_divisibility_parity_selection_proved"])
        self.assertFalse(receipt[
            "uniform_target_parity_selection_proved"])
        self.assertFalse(receipt["signed_prime_correlation_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_affine_reflection_selects_symmetric_source_for_every_target(self):
        receipt = affine_reflection_selection_receipt()
        self.assertEqual(receipt["targets"], (1000, 1002))
        self.assertEqual(len(receipt["rows"]), 16)
        self.assertEqual(receipt["energy_gate_pass_count"], 16)
        self.assertEqual(receipt["energy_gate_cell_count"], 16)
        self.assertAlmostEqual(
            receipt["symmetric_source_energy_fraction_range"][0],
            .27589532711425513, places=12)
        self.assertAlmostEqual(
            receipt["symmetric_source_energy_fraction_range"][1],
            .4278088755045186, places=12)
        admissible_counts = {
            (77, 1000): 44,
            (77, 1002): 33,
            (91, 1000): 36,
            (91, 1002): 27,
        }
        for (quotient, _, target), row in receipt["rows"].items():
            self.assertEqual(
                row["admissible_residue_count"],
                admissible_counts[(quotient, target)])
            self.assertTrue(row["pair_symmetric_interval"])
            self.assertTrue(row[
                "affine_reflection_cancellation_applicable"])
            self.assertTrue(row["affine_reflection_is_involution"])
            self.assertLess(
                row["affine_projector_energy_relative_error"], 1e-12)
            self.assertLess(
                row["affine_projector_orthogonality_relative_error"], 1e-12)
            self.assertTrue(row[
                "affine_symmetric_source_reconstructs_unit_correlation"])
            self.assertTrue(row[
                "affine_antisymmetric_source_cancels"])
            self.assertLessEqual(
                row["symmetric_source_energy_fraction"], .75)
        self.assertTrue(receipt[
            "all_affine_reflection_selection_identities_pass"])
        self.assertTrue(receipt[
            "all_symmetric_source_energy_fractions_pass_gate"])
        self.assertTrue(receipt[
            "target_uniform_affine_reflection_selection_identity_proved"])
        self.assertTrue(receipt[
            "all_canonical_cells_remove_at_least_quarter_energy"])
        self.assertFalse(receipt[
            "uniform_quarter_energy_removal_theorem_proved"])
        self.assertFalse(receipt["signed_prime_correlation_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_uniform_quarter_energy_removal_is_falsified(self):
        receipt = affine_reflection_residue_scan_receipt()
        self.assertEqual(receipt["common_moduli"], (110, 130))
        self.assertEqual(receipt["energy_gate_pass_count"], 328)
        self.assertEqual(receipt["energy_gate_cell_count"], 480)
        summaries = receipt["source_cell_summaries"]
        self.assertEqual(len(summaries), 8)
        for (quotient, _), summary in summaries.items():
            expected = (65, 44) if quotient == 77 else (55, 38)
            self.assertEqual(
                (summary["target_residue_count"],
                 summary["energy_gate_pass_count"]), expected)
        summary_means = tuple(
            summary["mean_symmetric_source_energy_fraction"]
            for summary in summaries.values())
        self.assertAlmostEqual(
            min(summary_means), .49940295588019973, places=12)
        self.assertAlmostEqual(
            max(summary_means), .5002588502303549, places=12)
        weighted_means = tuple(
            summary["energy_weighted_mean_symmetric_fraction"]
            for summary in summaries.values())
        self.assertAlmostEqual(
            min(weighted_means), .500248707154767, places=12)
        self.assertAlmostEqual(
            max(weighted_means), .5007047176902384, places=12)
        for summary in summaries.values():
            self.assertLess(summary[
                "summed_reflection_covariance_relative_error"], 1e-12)
            self.assertLess(summary[
                "summed_admissible_source_energy_relative_error"], 1e-12)
            self.assertLess(summary[
                "closed_form_weighted_mean_relative_error"], 1e-12)
        minimum_key, minimum_row = receipt[
            "minimum_symmetric_energy_cell"]
        maximum_key, maximum_row = receipt[
            "maximum_symmetric_energy_cell"]
        self.assertEqual(minimum_key, (77, 77, 64))
        self.assertAlmostEqual(
            minimum_row["symmetric_source_energy_fraction"],
            .0010931000569213186, places=15)
        self.assertEqual(maximum_key, (77, 1, 0))
        self.assertAlmostEqual(
            maximum_row["symmetric_source_energy_fraction"], 1, places=15)
        self.assertAlmostEqual(
            maximum_row["normalized_affine_reflection_covariance"],
            1, places=15)
        for row in receipt["rows"].values():
            self.assertTrue(row["affine_reflection_is_involution"])
            self.assertLess(
                row["affine_projector_energy_relative_error"], 1e-12)
            self.assertLess(
                row["affine_projector_orthogonality_relative_error"], 1e-12)
        self.assertTrue(receipt[
            "all_affine_projection_identities_pass"])
        self.assertTrue(receipt[
            "all_target_average_convolution_identities_pass"])
        self.assertTrue(receipt[
            "target_average_source_identity_proved_in_canonical_cells"])
        self.assertFalse(receipt[
            "all_even_target_residues_in_canonical_cells_pass_gate"])
        self.assertFalse(receipt[
            "uniform_all_source_energy_theorem_proved"])
        self.assertFalse(receipt["signed_prime_correlation_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_centering_is_the_principal_character_channel(self):
        receipt = linked_prime_centering_receipt()
        self.assertEqual(receipt["targets"], (1000, 1002))
        self.assertEqual(len(receipt["rows"]), 16)
        self.assertLess(receipt[
            "maximum_source_mean_principal_character_relative_error"],
            1e-12)
        self.assertLess(receipt[
            "maximum_principal_constant_component_relative_error"],
            1e-12)
        self.assertLess(receipt[
            "maximum_centered_reconstruction_relative_error"], 1e-12)
        self.assertAlmostEqual(
            receipt["constant_source_amplitude_range"][0],
            463.4505494505553, places=9)
        self.assertAlmostEqual(
            receipt["constant_source_amplitude_range"][1],
            1260.7368131868054, places=9)
        self.assertAlmostEqual(
            receipt[
                "centered_to_original_cauchy_envelope_ratio_range"][0],
            .022407821921949688, places=12)
        self.assertAlmostEqual(
            receipt[
                "centered_to_original_cauchy_envelope_ratio_range"][1],
            .14728612254523085, places=12)
        quotient_77 = receipt["quotient_summaries"][77]
        quotient_91 = receipt["quotient_summaries"][91]
        self.assertAlmostEqual(
            quotient_77["recombined_source_mean"].real,
            -196.4375, places=9)
        self.assertAlmostEqual(
            quotient_77["additive_source_recombination_quotient"],
            .06083544156586752, places=12)
        self.assertFalse(quotient_77[
            "primitive_additive_source_cancels"])
        self.assertLess(
            abs(quotient_91["recombined_source_mean"]), 1e-10)
        self.assertLess(
            quotient_91["additive_source_recombination_quotient"], 1e-12)
        self.assertTrue(quotient_91[
            "primitive_additive_source_cancels"])
        for target_row in quotient_91["target_summaries"].values():
            self.assertLess(
                target_row["recombined_direct_relative_to_natural_scale"],
                1e-12)
        self.assertEqual(
            receipt["cancelling_primitive_source_quotients"], (91,))
        self.assertTrue(receipt[
            "all_constant_source_components_are_principal_channels"])
        self.assertTrue(receipt[
            "all_divisor_recombinations_reconstruct"])
        self.assertFalse(receipt[
            "formal_dickman_main_identification_applicable"])
        self.assertFalse(receipt[
            "centered_target_dispersion_estimate_proved"])
        self.assertFalse(receipt["signed_prime_correlation_proved"])
        self.assertFalse(receipt["goldbach_proved"])
    def test_recombined_centered_source_remains_character_broad(self):
        receipt = recombined_centered_character_receipt()
        self.assertEqual(receipt["quotient"], 77)
        self.assertEqual(receipt["common_modulus"], 130)
        self.assertEqual(receipt["targets"], (1000, 1002))
        self.assertEqual(receipt["divisor_count"], 4)
        self.assertAlmostEqual(
            receipt["recombined_source_mean"].real, -196.4375, places=9)
        self.assertLess(receipt[
            "principal_centered_coefficient_relative_error"], 1e-12)
        self.assertEqual(
            receipt["leading_nonprincipal_character_labels"],
            ((3, 9), (1, 3), (1, 9), (3, 3)))
        self.assertAlmostEqual(
            receipt["leading_nonprincipal_energy_fraction"],
            .43856546708556404, places=12)
        self.assertEqual(
            receipt["characters_for_ninety_percent_energy"], 13)
        self.assertAlmostEqual(
            receipt["effective_nonprincipal_character_rank"],
            12.203257528896303, places=12)
        self.assertLess(receipt["parseval_relative_error"], 1e-12)
        self.assertLess(receipt[
            "reconstruction_natural_scale_relative_error"], 1e-12)
        self.assertLess(receipt[
            "maximum_linked_reconstruction_relative_error"], 1e-12)
        self.assertEqual(set(receipt["linked_prime_rows"]), {1000, 1002})
        self.assertFalse(receipt["four_character_shortcut_gate_passes"])
        self.assertTrue(receipt[
            "recombined_centered_character_expansion_proved"])
        self.assertFalse(receipt[
            "centered_target_dispersion_estimate_proved"])
        self.assertFalse(receipt["signed_prime_correlation_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_finite_target_scan_finds_strong_prime_phase_resonance(self):
        receipt = recombined_centered_prime_phase_scan_receipt()
        self.assertEqual(receipt["quotient"], 77)
        self.assertEqual(receipt["common_modulus"], 130)
        self.assertEqual(receipt["target_range"], (1000, 5000))
        self.assertEqual(receipt["tested_target_count"], 2001)
        self.assertEqual(receipt["nonempty_target_count"], 2001)
        self.assertEqual(receipt["empty_target_count"], 0)
        self.assertEqual(receipt["phase_gate_pass_count"], 1571)
        self.assertEqual(receipt["worst_target"], 1258)
        worst = receipt["worst_target_row"]
        self.assertEqual(worst["target_residue"], 88)
        self.assertEqual(worst["linked_prime_pair_count"], 12)
        self.assertEqual(worst["nonunit_prime_terms"], ())
        self.assertAlmostEqual(
            worst["phase_cancellation_ratio"],
            .9582327297547517, places=12)
        self.assertAlmostEqual(
            worst["direct_centered_correlation"].real,
            -2376517.0151526285, places=6)
        self.assertAlmostEqual(
            worst["direct_triangle_mass"],
            2480104.1974018877, places=6)
        self.assertAlmostEqual(
            worst["local_uniform_main_correlation"].real,
            169051.35380234398, places=6)
        self.assertAlmostEqual(
            worst["prime_residue_discrepancy_correlation"].real,
            -2545568.3689549724, places=6)
        self.assertAlmostEqual(
            worst["local_main_to_triangle_ratio"],
            .06816300459450014, places=12)
        self.assertAlmostEqual(
            worst["discrepancy_to_triangle_ratio"],
            1.0263957343492518, places=12)
        self.assertLess(
            worst["local_uniform_plus_discrepancy_relative_error"], 1e-12)
        self.assertEqual(receipt["worst_local_bias_residue"], 94)
        self.assertAlmostEqual(
            receipt["worst_local_bias_row"]["local_bias_ratio"],
            .1296901334499486, places=12)
        self.assertAlmostEqual(
            receipt["local_bias_rows"][88]["local_bias_ratio"],
            .058630719657540006, places=12)
        self.assertTrue(receipt[
            "all_even_residues_pass_local_bias_gate"])
        self.assertLess(receipt[
            "maximum_local_decomposition_relative_error"], 1e-12)
        self.assertTrue(receipt[
            "all_applicable_local_residue_decompositions_reconstruct"])
        contributions = receipt["worst_target_contributions"]
        self.assertEqual(len(contributions), 12)
        self.assertEqual(contributions[0][:3], (599, 659, 79))
        empty = recombined_centered_prime_phase_scan_receipt(
            target_minimum=26, target_maximum=26)
        self.assertEqual(empty["nonempty_target_count"], 0)
        self.assertEqual(empty["empty_target_count"], 1)
        self.assertEqual(empty["rows"][26]["nonunit_prime_terms"], (13,))
        self.assertIsNone(empty["worst_target"])
        self.assertIsNone(empty["worst_target_row"])
        self.assertEqual(empty["worst_target_contributions"], ())
        self.assertIsNone(empty[
            "all_tested_nonempty_targets_pass_phase_gate"])
        self.assertFalse(empty[
            "finite_range_phase_cancellation_measured"])
        self.assertFalse(empty["rows"][26][
            "local_residue_decomposition_applicable"])
        self.assertIsNone(empty["rows"][26][
            "local_uniform_plus_discrepancy_relative_error"])
        self.assertTrue(receipt["all_prime_terms_are_units"])
        self.assertFalse(receipt[
            "all_tested_nonempty_targets_pass_phase_gate"])
        self.assertTrue(receipt[
            "finite_range_phase_cancellation_measured"])
        self.assertFalse(receipt["uniform_phase_cancellation_proved"])
        self.assertFalse(receipt[
            "prime_residue_discrepancy_estimate_proved"])
        self.assertFalse(receipt[
            "centered_target_dispersion_estimate_proved"])
        self.assertFalse(receipt["signed_prime_correlation_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_resonant_progression_supports_sqrt_pair_scaling(self):
        receipt = resonant_progression_discrepancy_receipt()
        self.assertEqual(receipt["quotient"], 77)
        self.assertEqual(receipt["common_modulus"], 130)
        self.assertEqual(receipt["target_range"], (1000, 100000))
        self.assertEqual(receipt["target_residue"], 88)
        self.assertEqual(receipt["progression_step"], 130)
        self.assertEqual(receipt["tested_target_count"], 761)
        self.assertEqual(receipt["nonempty_target_count"], 761)
        self.assertEqual(receipt["gate_pass_count"], 761)
        self.assertEqual(receipt["worst_target"], 84978)
        worst = receipt["worst_target_row"]
        self.assertEqual(worst["linked_prime_pair_count"], 644)
        self.assertEqual(worst["nonunit_prime_terms"], ())
        self.assertAlmostEqual(
            worst["discrepancy_to_triangle_ratio"],
            .14609459444310946, places=12)
        self.assertAlmostEqual(
            worst["sqrt_pair_scaled_discrepancy"],
            3.70746517966384, places=12)
        self.assertLess(
            worst["local_uniform_plus_discrepancy_relative_error"], 1e-12)
        blocks = receipt["dyadic_block_summaries"]
        self.assertEqual(
            tuple(blocks),
            ((1000, 2000), (2000, 4000), (4000, 8000),
             (8000, 16000), (16000, 32000), (32000, 64000),
             (64000, 100001)))
        self.assertEqual(
            tuple(row["target_count"] for row in blocks.values()),
            (7, 16, 30, 62, 123, 246, 277))
        self.assertAlmostEqual(
            blocks[(1000, 2000)]["maximum_scaled_discrepancy"],
            3.5555391211297445, places=12)
        self.assertAlmostEqual(
            blocks[(64000, 100001)]["maximum_scaled_discrepancy"],
            3.70746517966384, places=12)
        contributions = receipt[
            "worst_residue_discrepancy_contributions"]
        self.assertEqual(len(contributions), 33)
        self.assertEqual(contributions[0][0], 107)
        self.assertLess(receipt[
            "maximum_decomposition_relative_error"], 1e-12)
        self.assertTrue(receipt["all_prime_terms_are_units"])
        self.assertTrue(receipt[
            "all_progression_targets_pass_scaled_discrepancy_gate"])
        self.assertTrue(receipt[
            "finite_progression_discrepancy_measured"])
        self.assertFalse(receipt[
            "square_root_discrepancy_bound_proved"])
        self.assertFalse(receipt["signed_prime_correlation_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_resonant_progression_diagonal_square_function(self):
        receipt = resonant_progression_diagonal_square_receipt()
        self.assertEqual(receipt["quotient"], 77)
        self.assertEqual(receipt["common_modulus"], 130)
        self.assertEqual(receipt["target_range"], (1000, 100000))
        self.assertEqual(receipt["target_residue"], 88)
        self.assertEqual(receipt["progression_step"], 130)
        self.assertEqual(receipt["admissible_residue_count"], 33)
        self.assertLess(receipt["centered_source_sum_relative_error"], 1e-12)
        self.assertEqual(receipt["tested_target_count"], 761)
        self.assertEqual(receipt["nonempty_target_count"], 761)
        self.assertEqual(receipt["gate_pass_count"], 761)
        self.assertEqual(receipt["paired_gate_pass_count"], 761)
        self.assertEqual(receipt["worst_target"], 84978)
        worst = receipt["worst_target_row"]
        self.assertEqual(worst["linked_prime_pair_count"], 644)
        self.assertEqual(worst["nonunit_prime_terms"], ())
        self.assertAlmostEqual(
            worst["pointwise_discrepancy_to_diagonal_ratio"],
            3.2305494244641015, places=12)
        self.assertAlmostEqual(
            worst["centered_discrepancy_correlation"].real,
            -61494865.434606, places=5)
        self.assertEqual(receipt["worst_paired_target"], 84978)
        worst_paired = receipt["worst_paired_target_row"]
        self.assertEqual(worst_paired["reflection_block_count"], 322)
        self.assertAlmostEqual(
            worst_paired["pointwise_discrepancy_to_paired_ratio"],
            2.9815599715307095, places=12)
        self.assertLess(
            worst_paired["ordered_to_paired_discrepancy_relative_error"],
            1e-12)
        self.assertEqual(
            tuple(receipt["dyadic_block_summaries"]),
            ((1000, 2000), (2000, 4000), (4000, 8000),
             (8000, 16000), (16000, 32000), (32000, 64000),
             (64000, 100001)))
        blocks = receipt["dyadic_block_summaries"]
        self.assertAlmostEqual(
            blocks[(1000, 2000)]["summed_squared_to_diagonal_ratio"],
            1.071018021527012, places=12)
        self.assertAlmostEqual(
            blocks[(8000, 16000)]["summed_squared_to_diagonal_ratio"],
            1.1623299689883424, places=12)
        self.assertAlmostEqual(
            blocks[(64000, 100001)]["summed_squared_to_diagonal_ratio"],
            .6845070553648028, places=12)
        self.assertAlmostEqual(
            blocks[(1000, 2000)]["summed_squared_to_paired_ratio"],
            .8681442249014873, places=12)
        self.assertAlmostEqual(
            blocks[(8000, 16000)]["summed_squared_to_paired_ratio"],
            .8721014786656731, places=12)
        self.assertAlmostEqual(
            blocks[(64000, 100001)]["summed_squared_to_paired_ratio"],
            .5602907847712755, places=12)
        self.assertTrue(receipt["all_prime_terms_are_units"])
        self.assertTrue(receipt[
            "all_progression_targets_pass_pointwise_diagonal_gate"])
        self.assertTrue(receipt["finite_diagonal_square_function_measured"])
        self.assertFalse(receipt["pointwise_diagonal_bound_proved"])
        self.assertTrue(receipt[
            "all_ordered_and_paired_discrepancies_reconstruct"])
        self.assertTrue(receipt[
            "all_progression_targets_pass_paired_pointwise_gate"])
        self.assertTrue(receipt[
            "finite_paired_reflection_square_function_measured"])
        self.assertFalse(receipt[
            "pointwise_paired_reflection_bound_proved"])
        self.assertFalse(receipt["averaged_diagonal_bound_proved"])
        self.assertFalse(receipt["signed_prime_correlation_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_all_residue_reflection_block_scan(self):
        receipt = all_residue_reflection_block_receipt()
        self.assertEqual(receipt["quotient"], 77)
        self.assertEqual(receipt["common_modulus"], 130)
        self.assertEqual(receipt["target_range"], (1000, 20000))
        self.assertEqual(len(receipt["residue_summaries"]), 65)
        self.assertEqual(receipt["tested_target_count"], 9501)
        self.assertEqual(receipt["nonempty_target_count"], 9501)
        self.assertEqual(receipt["empty_target_count"], 0)
        self.assertEqual(receipt["gate_pass_count"], 9501)
        self.assertEqual(receipt["worst_target"], 3708)
        worst = receipt["worst_target_row"]
        self.assertEqual(worst["target_residue"], 68)
        self.assertEqual(worst["ordered_linked_prime_pair_count"], 58)
        self.assertEqual(worst["reflection_block_count"], 29)
        self.assertAlmostEqual(
            worst["pointwise_discrepancy_to_paired_ratio"],
            2.996912452633917, places=12)
        blocks = receipt["dyadic_block_summaries"]
        self.assertEqual(
            tuple(blocks),
            ((1000, 2000), (2000, 4000), (4000, 8000),
             (8000, 16000), (16000, 20001)))
        self.assertEqual(
            tuple(row["target_count"] for row in blocks.values()),
            (500, 1000, 2000, 4000, 2001))
        self.assertAlmostEqual(
            blocks[(1000, 2000)]["summed_squared_to_paired_ratio"],
            .9296466125593036, places=12)
        self.assertAlmostEqual(
            blocks[(16000, 20001)]["summed_squared_to_paired_ratio"],
            .7425809321516373, places=12)
        residue_88 = receipt["residue_summaries"][88]
        self.assertEqual(residue_88["maximum_target"], 9578)
        self.assertAlmostEqual(
            residue_88["maximum_pointwise_ratio"],
            2.639006322098773, places=12)
        residue_72 = receipt["residue_summaries"][72]
        self.assertEqual(residue_72["target_count"], 146)
        self.assertEqual(residue_72["maximum_target"], 17622)
        self.assertAlmostEqual(
            residue_72["maximum_pointwise_ratio"],
            2.8015538046555166, places=12)
        self.assertAlmostEqual(
            residue_72["summed_squared_to_paired_ratio"],
            1.8067856583141206, places=12)
        self.assertLess(
            receipt["maximum_centered_source_sum_relative_error"], 1e-12)
        self.assertTrue(receipt["all_prime_terms_are_units"])
        self.assertTrue(receipt["all_even_residue_classes_measured"])
        self.assertTrue(receipt["all_nonempty_targets_pass_pointwise_gate"])
        self.assertTrue(receipt["finite_all_residue_reflection_scan_measured"])
        self.assertFalse(receipt["uniform_residue_pointwise_bound_proved"])
        self.assertFalse(receipt["uniform_residue_averaged_bound_proved"])
        self.assertFalse(receipt["signed_prime_correlation_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_residue_orbit_reinforcement(self):
        receipt = residue_orbit_reinforcement_receipt()
        self.assertEqual(receipt["quotient"], 77)
        self.assertEqual(receipt["common_modulus"], 130)
        self.assertEqual(receipt["target_range"], (1000, 100000))
        self.assertEqual(receipt["target_residue"], 72)
        self.assertEqual(receipt["progression_step"], 130)
        self.assertEqual(len(receipt["admissible_residues"]), 33)
        self.assertEqual(len(receipt["reflection_orbits"]), 17)
        self.assertEqual(
            sum(len(orbit) for orbit in receipt["reflection_orbits"]), 33)
        self.assertLess(receipt["centered_source_sum_relative_error"], 1e-12)
        self.assertLess(receipt["orbit_coefficient_sum_relative_error"], 1e-12)
        self.assertEqual(receipt["tested_target_count"], 761)
        self.assertEqual(receipt["nonempty_target_count"], 761)
        self.assertAlmostEqual(
            receipt["aggregate_orbit_ratio"],
            1.4580525604008545, places=12)
        self.assertAlmostEqual(
            receipt["aggregate_paired_ratio"],
            .7523745606834696, places=12)
        self.assertAlmostEqual(
            receipt["net_cross_orbit_to_orbit_diagonal_ratio"],
            .4580525604008545, places=12)
        self.assertLess(
            receipt["cross_term_reconstruction_relative_error"], 1e-12)
        self.assertFalse(receipt["passes_full_aggregate_orbit_gate"])
        self.assertFalse(receipt[
            "all_dyadic_blocks_pass_aggregate_orbit_gate"])
        self.assertEqual(receipt["worst_target"], 36472)
        worst = receipt["worst_target_row"]
        self.assertEqual(worst["ordered_linked_prime_pair_count"], 176)
        self.assertEqual(worst["reflection_block_count"], 88)
        self.assertAlmostEqual(
            worst["pointwise_discrepancy_to_orbit_ratio"],
            2.9678135069711833, places=12)
        blocks = receipt["dyadic_block_summaries"]
        self.assertEqual(
            tuple(blocks),
            ((1000, 2000), (2000, 4000), (4000, 8000),
             (8000, 16000), (16000, 32000), (32000, 64000),
             (64000, 100001)))
        self.assertEqual(
            tuple(row["target_count"] for row in blocks.values()),
            (7, 16, 30, 62, 123, 246, 277))
        self.assertAlmostEqual(
            blocks[(1000, 2000)]["aggregate_orbit_ratio"],
            2.3059497788961596, places=12)
        self.assertAlmostEqual(
            blocks[(2000, 4000)]["aggregate_orbit_ratio"],
            .6902980747308691, places=12)
        self.assertAlmostEqual(
            blocks[(64000, 100001)]["aggregate_orbit_ratio"],
            1.5486409507787244, places=12)
        self.assertEqual(
            receipt["orbit_pair_cross_terms"][0][:2],
            ((21, 51), (29, 43)))
        self.assertLess(receipt["maximum_reconstruction_relative_error"], 1e-12)
        self.assertLess(
            receipt["maximum_orbit_residue_weight_symmetry_error"], 1e-12)
        self.assertTrue(receipt["all_prime_terms_are_units"])
        self.assertTrue(receipt["all_orbit_discrepancies_reconstruct"])
        self.assertTrue(receipt[
            "all_two_element_orbit_residue_weights_match"])
        self.assertTrue(receipt[
            "finite_residue_orbit_reinforcement_measured"])
        self.assertFalse(receipt["orbit_reinforcement_bound_proved"])
        self.assertFalse(receipt["signed_prime_correlation_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_residue_orbit_sign_cube(self):
        receipt = residue_orbit_sign_cube_receipt()
        self.assertEqual(receipt["quotient"], 77)
        self.assertEqual(receipt["common_modulus"], 130)
        self.assertEqual(receipt["target_range"], (1000, 100000))
        self.assertEqual(receipt["target_residue"], 72)
        self.assertEqual(receipt["progression_step"], 130)
        self.assertEqual(receipt["orbit_count"], 17)
        self.assertEqual(receipt["global_sign_fixed_orbit"], (1, 71))
        self.assertEqual(receipt["pattern_count"], 65536)
        self.assertAlmostEqual(
            receipt["actual_ratio"], 1.4580525604008545, places=12)
        self.assertEqual(receipt["patterns_at_or_above_actual"], 565)
        self.assertAlmostEqual(
            receipt["actual_upper_tail_fraction"],
            565 / 65536, places=15)
        self.assertTrue(receipt["actual_signs_are_in_frozen_upper_tail"])
        self.assertAlmostEqual(
            receipt["minimum_ratio"], .3096717528582582, places=12)
        self.assertAlmostEqual(
            receipt["median_ratio"], .9865146512920753, places=12)
        self.assertAlmostEqual(
            receipt["maximum_ratio"], 1.7394395638936393, places=12)
        self.assertEqual(len(receipt["maximum_sign_pattern"]), 17)
        self.assertEqual(len(receipt["minimum_sign_pattern"]), 17)
        self.assertEqual(
            receipt["maximum_sign_pattern"],
            (1, -1, 1, -1, 1, -1, 1, -1, 1,
             1, 1, -1, -1, 1, -1, -1, -1))
        self.assertLess(
            receipt["actual_ratio_reconstruction_relative_error"], 1e-12)
        self.assertLess(
            receipt["orbit_diagonal_reconstruction_relative_error"], 1e-12)
        self.assertEqual(len(receipt["dyadic_sign_cube_summaries"]), 7)
        dyadic = receipt["dyadic_sign_cube_summaries"]
        self.assertEqual(
            tuple(row["patterns_at_or_above_actual"]
                  for row in dyadic.values()),
            (2816, 48177, 7854, 762, 1344, 19203, 1187))
        self.assertEqual(
            tuple(row["passes_upper_tail_gate"] for row in dyadic.values()),
            (True, False, False, True, True, False, True))
        self.assertTrue(all(
            row["pattern_count"] == 65536 for row in dyadic.values()))
        self.assertTrue(all(
            row["actual_ratio_reconstruction_relative_error"] < 1e-12
            for row in dyadic.values()))
        self.assertEqual(receipt["stable_dyadic_block_count"], 4)
        self.assertFalse(receipt["passes_dyadic_stability_gate"])
        self.assertTrue(receipt["finite_dyadic_sign_cubes_exhausted"])
        self.assertTrue(receipt["finite_sign_cube_exhausted"])
        self.assertFalse(receipt["source_sign_alignment_proved"])
        self.assertFalse(receipt[
            "scale_stable_source_sign_alignment_proved"])
        self.assertFalse(receipt["signed_prime_correlation_proved"])
        self.assertFalse(receipt["goldbach_proved"])


if __name__ == "__main__":
    unittest.main()
