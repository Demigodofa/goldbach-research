import math
import unittest

from lcm_sawtooth_endpoint_resonance_score import (
    endpoint_resonance_score_receipt,
)
from lcm_sawtooth_global_residue_energy import (
    global_residue_energy_receipt,
)
from lcm_sawtooth_lifted_endpoint_frame import (
    _generalized_psd_receipt,
    _lifted_frequency_data,
    _symmetric_pair_coordinates,
    lifted_endpoint_residue_gram_receipt,
    project_prime_block_lifted_endpoint_scan,
)

import numpy as np


class LcmSawtoothLiftedEndpointFrameTests(unittest.TestCase):
    def test_singular_denominator_minimum_uses_nullspace_coupling(self):
        denominator = np.diag((1.0, 0.0))
        coupled = np.ones((2, 2))
        uncoupled = np.eye(2)
        self.assertAlmostEqual(
            _generalized_psd_receipt(
                coupled, denominator)["smallest_generalized_eigenvalue"],
            0.0)
        self.assertAlmostEqual(
            _generalized_psd_receipt(
                uncoupled, denominator)["smallest_generalized_eigenvalue"],
            1.0)
        self.assertTrue(np.isinf(
            _generalized_psd_receipt(
                np.zeros((2, 2)), np.zeros((2, 2)))[
                    "smallest_generalized_eigenvalue"]))

    def test_symmetric_coordinates_reconstruct_pair_product(self):
        left = np.array(((2.0, -3.0, 5.0), (7.0, 11.0, -13.0)))
        right = np.array(((-17.0, 19.0, 23.0), (29.0, -31.0, 37.0)))
        parameter = np.array((3.0, -2.0, 4.0))
        lift = np.array((
            parameter[0] ** 2,
            parameter[0] * parameter[1],
            parameter[0] * parameter[2],
            parameter[1] ** 2,
            parameter[1] * parameter[2],
            parameter[2] ** 2,
        ))
        reconstructed = _symmetric_pair_coordinates(left, right) @ lift
        direct = (left @ parameter) * (right @ parameter)
        np.testing.assert_allclose(reconstructed, direct)

    def test_actual_selector_reconstructs_existing_exact_receipts(self):
        controls = (101, 10, 12, 3, 12)
        receipt = lifted_endpoint_residue_gram_receipt(*controls)
        endpoint = endpoint_resonance_score_receipt(
            101, 10, 10, 12, 3, 12)
        global_energy = global_residue_energy_receipt(
            101, 10, 10, 12, 3, 12)
        complete_squared = endpoint["complete_energy"] ** 2
        self.assertAlmostEqual(
            receipt["actual_endpoint_pair_square_envelope"]
            / complete_squared,
            endpoint[
                "high_Q_Q_weighted_squared_coefficient_product_over_complete_squared"],
            places=8)
        self.assertAlmostEqual(
            receipt["actual_full_residue_energy"] / complete_squared,
            global_energy[
                "global_Q_weighted_residue_l2_over_complete_squared"],
            places=8)
        self.assertAlmostEqual(
            receipt["actual_active_window_residue_energy"]
            / complete_squared,
            global_energy[
                "active_window_Q_weighted_l2_over_complete_squared"],
            places=8)
        self.assertAlmostEqual(
            receipt[
                "actual_endpoint_over_active_window_residue_energy"],
            global_energy[
                "endpoint_pair_square_envelope_over_active_window_l2"],
            places=8)
        self.assertFalse(
            receipt["numerator_positive_denominator_null_direction"])
        self.assertTrue(
            receipt["six_coordinate_symmetric_square_identity_proved"])

    def test_nontrivial_parameter_matches_direct_scalar_pair_grouping(self):
        modulus, row_count, ell_freeze, lower, upper = (31, 1, 10, 2, 8)
        receipt = lifted_endpoint_residue_gram_receipt(
            modulus, row_count, ell_freeze, lower, upper)
        self.assertEqual(receipt["active_row_start"], row_count)
        self.assertEqual(receipt["active_row_stop"], 2 * row_count)
        denominators, numerators, geometrics, coordinates = (
            _lifted_frequency_data(modulus, ell_freeze, lower, upper))
        parameter = np.array((2.0, -1.0, 3.0))
        lift = np.array((4.0, -2.0, 6.0, 1.0, -3.0, 9.0))
        coefficients = geometrics * (coordinates @ parameter)
        endpoint = (
            (numerators == 1) | (numerators == denominators - 1))
        direct_numerator = 0.0
        cells = {}
        for left in range(len(coefficients)):
            for right in range(len(coefficients)):
                common = math.lcm(
                    int(denominators[left]), int(denominators[right]))
                difference = (
                    int(numerators[left])
                    * (common // int(denominators[left]))
                    - int(numerators[right])
                    * (common // int(denominators[right])))
                common_factor = math.gcd(abs(difference), common)
                reduced = common // common_factor
                if reduced <= modulus * row_count:
                    continue
                residue = modulus * (difference // common_factor) % reduced
                product = coefficients[left] * coefficients[right].conjugate()
                key = (reduced, residue)
                cells[key] = cells.get(key, 0j) + product
                if endpoint[left] and endpoint[right]:
                    direct_numerator += reduced * abs(product) ** 2
        direct_denominator = sum(
            reduced * abs(value) ** 2
            for (reduced, _), value in cells.items())
        direct_active = 0.0
        for ell in range(row_count, 2 * row_count):
            transforms = {}
            for (reduced, residue), value in cells.items():
                transforms[reduced] = transforms.get(reduced, 0j) + (
                    value * np.exp(2j * np.pi * residue * ell / reduced))
            direct_active += sum(
                reduced * abs(value) ** 2
                for reduced, value in transforms.items()) / row_count
        numerator_gram = np.asarray(receipt["endpoint_pair_square_gram"])
        denominator_gram = np.asarray(receipt["full_residue_energy_gram"])
        active_gram = np.asarray(
            receipt["active_window_residue_energy_gram"])
        self.assertAlmostEqual(
            float(lift @ numerator_gram @ lift), direct_numerator,
            delta=1e-8 * direct_numerator)
        self.assertAlmostEqual(
            float(lift @ denominator_gram @ lift), direct_denominator,
            delta=1e-8 * direct_denominator)
        self.assertAlmostEqual(
            float(lift @ active_gram @ lift), direct_active,
            delta=1e-8 * direct_active)
        active_over_full = direct_active / direct_denominator
        self.assertGreaterEqual(
            active_over_full,
            receipt[
                "active_over_full_smallest_generalized_eigenvalue"]
            * (1 - 1e-10))
        self.assertLessEqual(
            active_over_full,
            receipt[
                "active_over_full_largest_generalized_eigenvalue"]
            * (1 + 1e-10))

    def test_active_row_start_changes_only_active_window_rows(self):
        modulus, row_count, ell_freeze, lower, upper = (31, 2, 10, 2, 8)
        shifted = lifted_endpoint_residue_gram_receipt(
            modulus, row_count, ell_freeze, lower, upper,
            active_row_start=0)
        self.assertEqual(shifted["active_row_start"], 0)
        self.assertEqual(shifted["active_row_stop"], row_count)
        denominators, numerators, geometrics, coordinates = (
            _lifted_frequency_data(modulus, ell_freeze, lower, upper))
        parameter = np.array((2.0, -1.0, 3.0))
        lift = np.array((4.0, -2.0, 6.0, 1.0, -3.0, 9.0))
        coefficients = geometrics * (coordinates @ parameter)
        cells = {}
        for left in range(len(coefficients)):
            for right in range(len(coefficients)):
                common = math.lcm(
                    int(denominators[left]), int(denominators[right]))
                difference = (
                    int(numerators[left])
                    * (common // int(denominators[left]))
                    - int(numerators[right])
                    * (common // int(denominators[right])))
                common_factor = math.gcd(abs(difference), common)
                reduced = common // common_factor
                if reduced <= modulus * row_count:
                    continue
                residue = modulus * (difference // common_factor) % reduced
                product = coefficients[left] * coefficients[right].conjugate()
                key = (reduced, residue)
                cells[key] = cells.get(key, 0j) + product
        direct_active = 0.0
        for ell in range(0, row_count):
            transforms = {}
            for (reduced, residue), value in cells.items():
                transforms[reduced] = transforms.get(reduced, 0j) + (
                    value * np.exp(2j * np.pi * residue * ell / reduced))
            direct_active += sum(
                reduced * abs(value) ** 2
                for reduced, value in transforms.items()) / row_count
        active_gram = np.asarray(
            shifted["active_window_residue_energy_gram"])
        self.assertAlmostEqual(
            float(lift @ active_gram @ lift), direct_active,
            delta=1e-8 * direct_active)
        with self.assertRaises(ValueError):
            lifted_endpoint_residue_gram_receipt(
                modulus, row_count, ell_freeze, lower, upper,
                active_row_start=-1)

    def test_conductor_exclusion_removes_only_requested_frequencies(self):
        baseline = _lifted_frequency_data(31, 10, 2, 8)
        excluded = _lifted_frequency_data(31, 10, 2, 8, (7,))
        self.assertIn(7, baseline[0])
        self.assertNotIn(7, excluded[0])
        self.assertEqual(len(baseline[0]) - len(excluded[0]), 6)
        with self.assertRaises(ValueError):
            _lifted_frequency_data(31, 10, 2, 8, (1,))
        with self.assertRaises(ValueError):
            _lifted_frequency_data(31, 10, 2, 8, (7.0,))

        receipt = lifted_endpoint_residue_gram_receipt(
            31, 1, 10, 2, 8, (value for value in (7,)))
        self.assertEqual(receipt["excluded_conductors"], (7,))
        self.assertEqual(receipt["primitive_frequency_count"], len(excluded[0]))

    def test_complete_small_prime_block_is_finite(self):
        receipt = project_prime_block_lifted_endpoint_scan(127)
        self.assertEqual(receipt["prime_count"], 24)
        self.assertEqual(receipt["denominator_rank"], 6)
        self.assertFalse(
            receipt["numerator_positive_denominator_null_direction"])
        self.assertEqual(receipt["active_window_denominator_rank"], 6)
        self.assertFalse(receipt[
            "active_window_numerator_positive_denominator_null_direction"])
        self.assertGreaterEqual(
            receipt["largest_generalized_eigenvalue"],
            receipt["aggregate_actual_endpoint_over_full_residue_energy"])
        self.assertGreaterEqual(
            receipt["active_window_largest_generalized_eigenvalue"],
            receipt[
                "aggregate_actual_endpoint_over_active_window_residue_energy"])
        self.assertAlmostEqual(
            receipt["active_window_largest_generalized_eigenvalue"],
            0.33121619640978345)
        self.assertAlmostEqual(
            receipt[
                "aggregate_actual_endpoint_over_active_window_residue_energy"],
            0.28715990792912854)
        self.assertAlmostEqual(
            receipt["aggregate_actual_active_window_over_full_residue_energy"],
            0.9507351890844087)
        self.assertGreater(
            receipt[
                "minimum_individual_active_over_full_generalized_eigenvalue"],
            0)
        self.assertGreater(
            receipt[
                "aggregate_active_over_full_smallest_generalized_eigenvalue"],
            0)
        self.assertGreaterEqual(
            receipt[
                "aggregate_active_over_full_largest_generalized_eigenvalue"],
            receipt[
                "aggregate_active_over_full_smallest_generalized_eigenvalue"])
        self.assertAlmostEqual(
            receipt[
                "minimum_individual_active_over_full_generalized_eigenvalue"],
            0.5208139494941257)
        self.assertAlmostEqual(
            receipt[
                "aggregate_active_over_full_smallest_generalized_eigenvalue"],
            0.8768802946823543)
        self.assertAlmostEqual(
            receipt[
                "aggregate_active_over_full_largest_generalized_eigenvalue"],
            1.1462894236938728)
        weighted = receipt["weighted_active_window_receipts"]
        self.assertEqual(set(weighted), {
            "unweighted", "log_squared_over_m",
            "rho_log_squared_over_m", "rho_m_log_squared"})
        self.assertAlmostEqual(
            weighted["unweighted"]["largest_generalized_eigenvalue"],
            receipt["active_window_largest_generalized_eigenvalue"])
        self.assertAlmostEqual(
            weighted["unweighted"][
                "actual_endpoint_over_active_window_residue_energy"],
            receipt[
                "aggregate_actual_endpoint_over_active_window_residue_energy"])
        for mode in weighted.values():
            self.assertEqual(mode["denominator_rank"], 6)
            self.assertFalse(
                mode["numerator_positive_denominator_null_direction"])
            self.assertGreaterEqual(
                mode["largest_generalized_eigenvalue"],
                mode[
                    "actual_endpoint_over_active_window_residue_energy"])
        self.assertAlmostEqual(
            weighted["log_squared_over_m"][
                "largest_generalized_eigenvalue"],
            0.3306259203720875)
        self.assertAlmostEqual(
            weighted["rho_log_squared_over_m"][
                "largest_generalized_eigenvalue"],
            0.3307205508118922)
        self.assertAlmostEqual(
            weighted["rho_m_log_squared"][
                "largest_generalized_eigenvalue"],
            0.3342054806044802)
        self.assertTrue(
            receipt["finite_complete_prime_block_lifted_measurement"])
        self.assertFalse(receipt["uniform_lifted_endpoint_bound_proved"])


if __name__ == "__main__":
    unittest.main()
