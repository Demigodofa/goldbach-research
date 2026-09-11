import unittest

from lcm_sawtooth_linked_prime_character import (
    affine_reflection_residue_scan_receipt,
    affine_reflection_selection_receipt,
    linked_prime_character_receipt,
    linked_prime_parity_selection_receipt,
)


class LinkedPrimeCharacterTests(unittest.TestCase):
    def test_guards(self):
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
        self.assertFalse(receipt[
            "all_even_target_residues_in_canonical_cells_pass_gate"])
        self.assertFalse(receipt[
            "uniform_all_source_energy_theorem_proved"])
        self.assertFalse(receipt["signed_prime_correlation_proved"])
        self.assertFalse(receipt["goldbach_proved"])


if __name__ == "__main__":
    unittest.main()
