import unittest

from lcm_sawtooth_signed_conductor_ablation import (
    classify_conductor_ablation,
    classify_pair_interactions,
    project_active_full_pair_rayleigh_split_receipt,
    project_cluster_matrix_stabilization_receipt,
    project_cluster_pair_interaction_receipt,
    project_frozen_whitening_interaction_receipt,
    project_pair_matrix_interaction_receipt,
    project_primewise_pair_rayleigh_receipt,
    project_signed_conductor_ablation_receipt,
)


class LcmSawtoothSignedConductorAblationTests(unittest.TestCase):
    def test_classifier_requires_both_magnitude_and_upper_location(self):
        lower_largest = (
            {"excluded_conductor": 2, "parameter_shift": -.006},
            {"excluded_conductor": 11, "parameter_shift": .004},
        )
        result = classify_conductor_ablation(lower_largest, (11,))
        self.assertTrue(result["magnitude_falsifier_passes"])
        self.assertFalse(result["upper_half_location_falsifier_passes"])
        self.assertFalse(result["sparse_upper_conductor_hypothesis_passes"])

        upper_largest = (
            {"excluded_conductor": 2, "parameter_shift": -.004},
            {"excluded_conductor": 11, "parameter_shift": .006},
        )
        result = classify_conductor_ablation(upper_largest, (11,))
        self.assertTrue(result["sparse_upper_conductor_hypothesis_passes"])

    def test_classifier_guards_empty_rows_and_threshold(self):
        with self.assertRaises(ValueError):
            classify_conductor_ablation((), ())
        with self.assertRaises(ValueError):
            classify_conductor_ablation(
                ({"excluded_conductor": 2, "parameter_shift": 0},),
                (), 0)

    def test_pair_classifier_requires_both_thresholds(self):
        rows = (
            {"conductors": (2, 3), "interaction_shift": .0003,
             "relative_interaction": .2},
            {"conductors": (2, 5), "interaction_shift": .0002,
             "relative_interaction": .3},
            {"conductors": (3, 5), "interaction_shift": .0003,
             "relative_interaction": .3},
        )
        receipt = classify_pair_interactions(rows)
        self.assertEqual(receipt["qualifying_interaction_pairs"], ((3, 5),))
        self.assertTrue(
            receipt["nonlinear_pair_interaction_hypothesis_passes"])
        with self.assertRaises(ValueError):
            classify_pair_interactions(())
        with self.assertRaises(ValueError):
            classify_pair_interactions(rows, relative_threshold=0)

    def test_m127_rejects_single_sparse_upper_conductor_control(self):
        receipt = project_signed_conductor_ablation_receipt(127)
        ranked = sorted(
            receipt["rows"],
            key=lambda row: abs(row["parameter_shift"]),
            reverse=True)
        self.assertAlmostEqual(
            receipt["baseline_best_parameter"], .2795716513419446)
        self.assertEqual(
            tuple(row["excluded_conductor"] for row in ranked[:4]),
            (55, 78, 143, 77))
        self.assertEqual(receipt["largest_influence_conductor"], 55)
        self.assertAlmostEqual(
            receipt["largest_absolute_parameter_shift"],
            .0009974649895388987)
        self.assertFalse(receipt["magnitude_falsifier_passes"])
        self.assertTrue(receipt["upper_half_location_falsifier_passes"])
        self.assertFalse(
            receipt["sparse_upper_conductor_hypothesis_passes"])
        self.assertFalse(receipt["signed_prime_correlation_proved"])

    def test_m127_upper_cluster_has_nonlinear_pair_interactions(self):
        receipt = project_cluster_pair_interaction_receipt(
            127, (55, 77, 78, 143))
        self.assertEqual(
            receipt["qualifying_interaction_pairs"],
            ((55, 143), (77, 78), (77, 143), (78, 143)))
        self.assertEqual(receipt["largest_interaction_pair"], (77, 143))
        self.assertAlmostEqual(
            receipt["largest_absolute_interaction_shift"],
            .001702794772824423)
        self.assertAlmostEqual(
            receipt[
                "largest_interaction_relative_to_single_magnitudes"],
            .9803545148975872)
        self.assertTrue(
            receipt["nonlinear_pair_interaction_hypothesis_passes"])
        self.assertFalse(receipt["signed_prime_correlation_proved"])

    def test_m127_strongest_interaction_survives_frozen_whitening(self):
        receipt = project_frozen_whitening_interaction_receipt(
            127, (77, 143))
        self.assertAlmostEqual(
            receipt["frozen_whitening_interaction_shift"],
            .0016634474513739228)
        self.assertAlmostEqual(
            receipt["interaction_retained_fraction"],
            .9768925051459755)
        self.assertTrue(receipt["interaction_sign_preserved"])
        self.assertTrue(receipt[
            "frozen_whitening_retention_hypothesis_passes"])
        self.assertFalse(receipt["signed_prime_correlation_proved"])

    def test_frozen_whitening_receipt_guards_pair_and_threshold(self):
        with self.assertRaises(ValueError):
            project_frozen_whitening_interaction_receipt(127, (77,))
        with self.assertRaises(ValueError):
            project_frozen_whitening_interaction_receipt(
                127, (77, 143), retention_threshold=0)

    def test_m127_cross_matrix_stabilizes_the_fragile_direction(self):
        receipt = project_pair_matrix_interaction_receipt(127, (77, 143))
        self.assertAlmostEqual(
            receipt["matrix_cross_output_fraction"], .7683214684040077)
        self.assertAlmostEqual(
            receipt["additive_surrogate_traceless_smallest_eigenvalue"],
            -.7445050404108796)
        self.assertAlmostEqual(
            receipt["exact_joint_traceless_smallest_eigenvalue"],
            .052517093474779286)
        self.assertAlmostEqual(
            receipt["cross_rayleigh_on_additive_weakest_direction"],
            1.0940198731962434)
        self.assertLess(abs(receipt["decomposition_residual"]), 1e-15)
        self.assertTrue(receipt[
            "matrix_cross_output_dominance_hypothesis_passes"])
        self.assertTrue(receipt[
            "cross_restores_traceless_positive_definiteness"])
        self.assertFalse(receipt["signed_prime_correlation_proved"])

    def test_pair_matrix_receipt_guards_pair_and_threshold(self):
        with self.assertRaises(ValueError):
            project_pair_matrix_interaction_receipt(127, (77,))
        with self.assertRaises(ValueError):
            project_pair_matrix_interaction_receipt(
                127, (77, 143), dominance_threshold=1.1)

    def test_m127_cluster_stabilizes_all_four_fragile_modes(self):
        pairs = ((55, 143), (77, 78), (77, 143), (78, 143))
        receipt = project_cluster_matrix_stabilization_receipt(127, pairs)
        self.assertEqual(
            receipt["positive_fragile_direction_rayleigh_pairs"], pairs)
        self.assertEqual(
            receipt["positive_definiteness_restoration_pairs"], pairs)
        self.assertEqual(
            receipt["positive_definiteness_restoration_fraction"], 1)
        measured = {
            row["conductors"]: (
                row["additive_surrogate_traceless_smallest_eigenvalue"],
                row["exact_joint_traceless_smallest_eigenvalue"],
                row["cross_rayleigh_on_additive_weakest_direction"])
            for row in receipt["rows"]
        }
        expected = {
            (55, 143): (-.1033168874069742, .09500378572432736,
                        .2342041070706142),
            (77, 78): (-.23568244027752927, .2232498794788733,
                       1.1876021360675244),
            (77, 143): (-.7445050404108796, .052517093474779286,
                        1.0940198731962434),
            (78, 143): (-.08833756349499475, .09898488816478801,
                        .21533787174406685),
        }
        for pair in pairs:
            for actual, target in zip(measured[pair], expected[pair]):
                self.assertAlmostEqual(actual, target)
        self.assertTrue(receipt[
            "cluster_fragile_mode_stabilization_hypothesis_passes"])
        self.assertFalse(receipt["uniform_pair_matrix_stabilization_proved"])
        self.assertFalse(receipt["signed_prime_correlation_proved"])

    def test_cluster_matrix_receipt_guards_pairs_and_fraction(self):
        with self.assertRaises(ValueError):
            project_cluster_matrix_stabilization_receipt(127, ())
        with self.assertRaises(ValueError):
            project_cluster_matrix_stabilization_receipt(
                127, ((55, 143),), 0)

    def test_m127_strongest_pair_has_no_broad_primewise_sign(self):
        receipt = project_primewise_pair_rayleigh_receipt(127, (77, 143))
        self.assertEqual(receipt["prime_count"], 24)
        self.assertEqual(receipt["nonnegative_prime_count"], 13)
        self.assertAlmostEqual(receipt["nonnegative_prime_fraction"], 13 / 24)
        self.assertAlmostEqual(
            receipt["positive_rayleigh_mass"], 1.6041394773378064)
        self.assertAlmostEqual(
            receipt["negative_rayleigh_mass"], .5101198145771794)
        self.assertEqual(receipt["largest_positive_contributor"], 167)
        self.assertAlmostEqual(
            receipt["largest_positive_mass_share"], .34150542466322575)
        self.assertLess(abs(receipt["primewise_aggregate_residual"]), 3e-7)
        self.assertFalse(receipt["nonnegative_fraction_falsifier_passes"])
        self.assertFalse(receipt[
            "positive_mass_concentration_falsifier_passes"])
        self.assertFalse(receipt["broad_primewise_sign_hypothesis_passes"])
        active = receipt["active_window_component"]
        self.assertEqual(active["nonnegative_count"], 13)
        self.assertEqual(active["largest_positive_contributor"], 167)
        self.assertAlmostEqual(
            active["largest_positive_mass_share"], .3668353024206913)
        full_subtraction = receipt["minus_half_full_component"]
        self.assertEqual(full_subtraction["nonnegative_count"], 20)
        self.assertEqual(
            full_subtraction["largest_positive_contributor"], 191)
        self.assertAlmostEqual(
            full_subtraction["largest_positive_mass_share"],
            .20158411406592963)
        self.assertFalse(receipt[
            "active_component_broad_sign_hypothesis_passes"])
        self.assertTrue(receipt[
            "full_subtraction_broad_sign_candidate_passes"])
        self.assertFalse(receipt["signed_prime_correlation_proved"])

    def test_primewise_receipt_guards_pair_and_thresholds(self):
        with self.assertRaises(ValueError):
            project_primewise_pair_rayleigh_receipt(127, (77,))
        with self.assertRaises(ValueError):
            project_primewise_pair_rayleigh_receipt(
                127, (77, 143), nonnegative_fraction_threshold=0)
        with self.assertRaises(ValueError):
            project_primewise_pair_rayleigh_receipt(
                127, (77, 143), maximum_positive_mass_share=1.1)

    def test_m127_active_window_leads_the_fragile_reinforcement(self):
        receipt = project_active_full_pair_rayleigh_split_receipt(
            127, (77, 143))
        self.assertAlmostEqual(
            receipt["active_window_boolean_cross_rayleigh"],
            .9755092481272897)
        self.assertAlmostEqual(
            receipt["full_residue_boolean_cross_rayleigh"],
            -.23702123573859438)
        self.assertAlmostEqual(
            receipt["net_boolean_cross_rayleigh"], 1.094019865996587)
        self.assertAlmostEqual(
            receipt["active_window_fraction_of_net_reinforcement"],
            .89167416282579)
        self.assertTrue(receipt[
            "full_subtraction_reinforces_fragile_direction"])
        self.assertTrue(receipt[
            "active_window_leading_hypothesis_passes"])
        self.assertFalse(receipt["signed_prime_correlation_proved"])

    def test_active_full_split_guards_pair_and_threshold(self):
        with self.assertRaises(ValueError):
            project_active_full_pair_rayleigh_split_receipt(127, (77,))
        with self.assertRaises(ValueError):
            project_active_full_pair_rayleigh_split_receipt(
                127, (77, 143), active_fraction_threshold=0)


if __name__ == "__main__":
    unittest.main()
