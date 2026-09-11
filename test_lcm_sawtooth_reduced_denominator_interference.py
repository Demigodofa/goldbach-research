import unittest

from lcm_sawtooth_reduced_denominator_interference import (
    _require_no_mixed_high_q_packet,
    _cross_by_denominator,
    _offdiagonal_lags_by_denominator,
    _packet_hermitian_symmetry_error,
    classify_near_lag_mass,
    classify_crt_rank_one_near_lag_separation,
    classify_primewise_denominator_signs,
    classify_shared_prime_denominator_mass,
    project_reduced_denominator_interference_receipt,
    conductor_high_q_retention_obstruction,
    lag_inversion_symmetry_receipt,
    shared_prime_high_q_support_obstruction,
)


class ReducedDenominatorInterferenceTests(unittest.TestCase):
    def test_packet_hermitian_error_detects_missing_reverse_cell(self):
        packet = {
            (5, 0): 2.0,
            (5, 1): 1 + 3j,
            (5, 4): 1 - 3j,
        }
        self.assertEqual(_packet_hermitian_symmetry_error(packet), 0.0)
        del packet[(5, 4)]
        self.assertGreater(_packet_hermitian_symmetry_error(packet), 0.0)

    def test_even_lag_half_sum_keeps_self_inverse_term(self):
        receipt = lag_inversion_symmetry_receipt(
            (0.0, 2.0, -1.0, .5, -1.0, 2.0))
        self.assertEqual(receipt["self_inverse_half_period_term"], .5)
        self.assertEqual(receipt["inversion_maximum_error"], 0.0)
        self.assertEqual(receipt["half_lag_reconstruction_error"], 0.0)
        self.assertTrue(receipt["finite_even_lag_symmetry_test_passes"])

    def test_crt_rank_one_classifier_reindexes_exactly(self):
        matrix = [[0.0, 0.0], [2.0, -4.0], [3.0, -6.0],
                  [4.0, -8.0], [5.0, -10.0]]
        contributions = [matrix[lag % 5][lag % 2] for lag in range(10)]
        receipt = classify_crt_rank_one_near_lag_separation(
            {10: contributions}, 5, 1, minimum_passing_channel_count=1)
        row = receipt["crt_rank_one_near_lag_channel_rows"][0]
        self.assertLess(row["crt_reconstruction_maximum_error"], 1e-15)
        self.assertAlmostEqual(
            row["rank_one_frobenius_energy_fraction"], 1.0, places=12)
        self.assertTrue(receipt[
            "crt_rank_one_near_lag_separation_hypothesis_passes"])

    def test_full_conductors_are_forced_by_actual_cutoff(self):
        receipt = conductor_high_q_retention_obstruction(
            127, 28, 3, 13, (77, 143))
        self.assertEqual(receipt["linked_conductor_core"], 1001)
        bounds = {
            (row["conductor"], factor["prime_factor"]):
            factor["nondivisible_reduced_denominator_upper_bound"]
            for row in receipt["conductor_retention_rows"]
            for factor in row["factor_rows"]}
        self.assertEqual(bounds, {
            (77, 7): 1430, (77, 11): 910,
            (143, 11): 910, (143, 13): 770})
        self.assertTrue(receipt[
            "every_interfering_denominator_has_linked_core_proved"])

    def test_fft_lag_decomposition_reconstructs_offdiagonal_cross(self):
        left = {
            (5, 0): 1 + 2j,
            (5, 2): -3 + 1j,
            (5, 4): 2 - 4j,
        }
        right = {
            (5, 1): 2 - 1j,
            (5, 2): 4 + 3j,
            (5, 3): -2 + 2j,
        }
        direct = _cross_by_denominator(left, right, 4)[5][2]
        lags = _offdiagonal_lags_by_denominator(left, right, 4, 4)[5]
        self.assertAlmostEqual(float(lags.sum()), direct, places=10)

    def test_near_lag_classifier_uses_cyclic_main_lobe(self):
        contributions = [0.0] * 12
        contributions[1] = 3.0
        contributions[5] = -1.0
        receipt = classify_near_lag_mass(
            {12: contributions}, 4, minimum_passing_channel_count=1)
        row = receipt["near_lag_channel_rows"][0]
        self.assertEqual(row["near_lag_maximum_cyclic_distance"], 3)
        self.assertEqual(row["near_lag_absolute_mass_fraction"], .75)
        self.assertTrue(receipt["near_lag_absolute_mass_hypothesis_passes"])

    def test_primewise_classifier_applies_both_channel_thresholds(self):
        rows = tuple(
            {"modulus": modulus, "reduced_denominator": denominator,
             "off_diagonal_window_interference": value}
            for denominator, values in (
                (10, (3.0, 2.0, 1.0, -1.0)),
                (15, (1.0, -1.0, -2.0, -3.0)))
            for modulus, value in enumerate(values, start=101))
        receipt = classify_primewise_denominator_signs(
            rows, (10, 15), maximum_positive_mass_share=.5,
            minimum_passing_channel_count=1)
        self.assertEqual(receipt["passing_denominators"], (10,))
        self.assertTrue(receipt[
            "denominatorwise_prime_sign_hypothesis_passes"])

    def test_mass_classifier_uses_absolute_contributions(self):
        rows = (
            {"reduced_denominator": 22,
             "off_diagonal_window_interference": 3.0},
            {"reduced_denominator": 35,
             "off_diagonal_window_interference": -1.0},
        )
        receipt = classify_shared_prime_denominator_mass(rows, 11, .75)
        self.assertEqual(receipt["absolute_off_diagonal_mass"], 4.0)
        self.assertEqual(receipt["shared_prime_absolute_mass_fraction"], .75)
        self.assertTrue(receipt[
            "shared_prime_denominator_mass_hypothesis_passes"])

    def test_actual_support_forces_shared_prime_on_high_q_packets(self):
        receipt = shared_prime_high_q_support_obstruction(
            127, 28, 3, 13, (77, 143), 11)
        self.assertEqual(receipt["maximum_nonshared_q_upper_bound"], 910)
        self.assertEqual(receipt["high_q_threshold"], 3556)
        self.assertTrue(receipt[
            "every_high_q_single_packet_denominator_has_shared_prime_proved"])

    def test_project_fixture_localizes_all_nonzero_mass(self):
        receipt = project_reduced_denominator_interference_receipt(127)
        self.assertEqual(receipt["prime_count"], 24)
        self.assertEqual(receipt["mixed_packet_high_q_pair_count"], 0)
        self.assertEqual(
            receipt["nonshared_single_packet_high_q_pair_count"], 0)
        self.assertEqual(
            receipt["nonconductor_single_packet_high_q_pair_count"], 0)
        self.assertEqual(receipt["linked_conductor_core"], 1001)
        self.assertTrue(receipt[
            "every_interfering_denominator_has_linked_core_proved"])
        self.assertEqual(
            receipt["nonzero_off_diagonal_denominators"],
            (5005, 6006, 10010))
        self.assertEqual(receipt["positive_nonzero_denominator_count"], 3)
        self.assertEqual(receipt["passing_channel_count"], 0)
        self.assertEqual(receipt["passing_denominators"], ())
        self.assertFalse(receipt[
            "denominatorwise_prime_sign_hypothesis_passes"])
        self.assertEqual(receipt["near_lag_passing_channel_count"], 0)
        self.assertEqual(receipt["near_lag_passing_denominators"], ())
        self.assertFalse(receipt["near_lag_absolute_mass_hypothesis_passes"])
        self.assertEqual(
            receipt["crt_rank_one_near_lag_passing_channel_count"], 0)
        self.assertEqual(
            receipt["crt_rank_one_near_lag_passing_denominators"], ())
        self.assertFalse(receipt[
            "linked_core_crt_near_lag_separation_hypothesis_passes"])
        self.assertLess(max(
            abs(error) for _, error in receipt["lag_reconstruction_errors"]),
            3e-12)
        primewise = {
            row["reduced_denominator"]: row
            for row in receipt["primewise_denominator_rows"]}
        lag_rows = {
            row["reduced_denominator"]: row
            for row in receipt["near_lag_channel_rows"]}
        crt_rows = {
            row["reduced_denominator"]: row
            for row in receipt["crt_rank_one_near_lag_channel_rows"]}
        self.assertEqual(
            {denominator: row["crt_cofactor"]
             for denominator, row in crt_rows.items()},
            {5005: 5, 6006: 6, 10010: 10})
        self.assertAlmostEqual(
            crt_rows[5005]["rank_one_frobenius_energy_fraction"],
            .5252071997172114, places=10)
        self.assertAlmostEqual(
            crt_rows[6006]["rank_one_frobenius_energy_fraction"],
            .6738134851177743, places=10)
        self.assertAlmostEqual(
            crt_rows[10010]["rank_one_frobenius_energy_fraction"],
            .3612744181634573, places=10)
        self.assertEqual(max(
            row["crt_reconstruction_maximum_error"]
            for row in crt_rows.values()), 0.0)
        self.assertLessEqual(
            receipt["packet_hermitian_maximum_error"], 1e-12)
        self.assertLessEqual(
            receipt["prime_lag_inversion_maximum_error"], 1e-12)
        self.assertLessEqual(
            receipt["aggregate_lag_inversion_maximum_error"], 1e-12)
        self.assertLessEqual(
            receipt["aggregate_half_sum_reconstruction_maximum_error"],
            1e-12)
        self.assertTrue(receipt[
            "finite_hermitian_even_lag_symmetry_test_passes"])
        self.assertTrue(receipt[
            "ordered_pair_reversal_hermitian_packet_identity_proved"])
        self.assertTrue(receipt[
            "hermitian_packets_imply_even_lag_interference_proved"])
        self.assertFalse(receipt[
            "even_lag_identity_assigns_favorable_sign_proved"])
        self.assertAlmostEqual(
            lag_rows[5005]["near_lag_absolute_mass_fraction"],
            .5084107132570644, places=10)
        self.assertAlmostEqual(
            lag_rows[6006]["near_lag_absolute_mass_fraction"],
            .5041716929298857, places=10)
        self.assertAlmostEqual(
            lag_rows[10010]["near_lag_absolute_mass_fraction"],
            .517849903995512, places=10)
        self.assertTrue(all(
            row["near_lag_signed_sum"] > 0 for row in lag_rows.values()))
        self.assertTrue(all(
            row["far_lag_signed_sum"] < 0 for row in lag_rows.values()))
        self.assertEqual(
            (primewise[5005]["positive_prime_count"],
             primewise[5005]["nonzero_prime_count"]), (6, 9))
        self.assertEqual(
            (primewise[6006]["positive_prime_count"],
             primewise[6006]["nonzero_prime_count"]), (11, 14))
        self.assertEqual(
            (primewise[10010]["positive_prime_count"],
             primewise[10010]["nonzero_prime_count"]), (9, 22))
        self.assertAlmostEqual(
            primewise[5005]["largest_positive_mass_share"],
            .5138201694084494, places=10)
        self.assertAlmostEqual(
            primewise[6006]["largest_positive_mass_share"],
            .4276844398695563, places=10)
        self.assertAlmostEqual(
            primewise[10010]["largest_positive_mass_share"],
            .27089628808477967, places=10)
        self.assertAlmostEqual(
            primewise[5005]["signed_sum"], .6392452867667243, places=10)
        self.assertAlmostEqual(
            primewise[6006]["signed_sum"], .5258316742755542, places=10)
        self.assertAlmostEqual(
            primewise[10010]["signed_sum"], .047452775903835676,
            places=10)
        self.assertAlmostEqual(
            receipt["shared_prime_absolute_mass_fraction"], 1.0, places=12)
        self.assertAlmostEqual(
            receipt["active_window_boolean_cross_rayleigh"],
            .9755090695006173, places=8)
        self.assertAlmostEqual(
            receipt["full_residue_boolean_cross_rayleigh"],
            -.2370206674454969, places=8)
        self.assertAlmostEqual(
            receipt["off_diagonal_window_boolean_cross_rayleigh"],
            1.2125297369461143, places=8)
        self.assertLess(
            abs(receipt["active_matrix_reconstruction_residual"]), 2e-6)
        self.assertLess(
            abs(receipt["full_matrix_reconstruction_residual"]), 2e-6)
        self.assertTrue(receipt[
            "shared_prime_denominator_mass_hypothesis_passes"])
        self.assertFalse(receipt["signed_prime_correlation_proved"])

    def test_guards(self):
        with self.assertRaises(ValueError):
            classify_shared_prime_denominator_mass((), 11)
        with self.assertRaises(ValueError):
            classify_shared_prime_denominator_mass(({
                "reduced_denominator": 11,
                "off_diagonal_window_interference": 1.0},), 12)
        with self.assertRaises(ValueError):
            project_reduced_denominator_interference_receipt(
                127, (66, 78))
        with self.assertRaises(ArithmeticError):
            _require_no_mixed_high_q_packet(1)
        with self.assertRaises(ValueError):
            _require_no_mixed_high_q_packet(-1)


if __name__ == "__main__":
    unittest.main()
