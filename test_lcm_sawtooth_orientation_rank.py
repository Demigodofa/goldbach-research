import unittest

from lcm_sawtooth_orientation_rank import (
    endpoint_orientation_symmetry_receipt,
    fully_resonant_orientation_rank_receipt,
)


class OrientationRankTests(unittest.TestCase):
    def test_guards(self):
        with self.assertRaises(ValueError):
            fully_resonant_orientation_rank_receipt(lag=0)
        with self.assertRaises(ValueError):
            fully_resonant_orientation_rank_receipt(
                maximum_third_singular_value_ratio=-1)
        with self.assertRaises(ValueError):
            fully_resonant_orientation_rank_receipt(tolerance=-1)
        with self.assertRaises(ValueError):
            fully_resonant_orientation_rank_receipt(
                maximum_orientation_profile_residual=-1)
        with self.assertRaises(ValueError):
            endpoint_orientation_symmetry_receipt(families=((9, 3),))

    def test_endpoint_orientation_source_modes_are_identical(self):
        receipt = endpoint_orientation_symmetry_receipt()
        self.assertEqual(receipt["source_function_orientation_multiplicity"], 2)
        self.assertLess(
            receipt["maximum_coefficient_relative_error"], 1e-10)
        self.assertTrue(receipt[
            "all_orientation_symmetry_identities_pass"])
        for row in receipt["rows"].values():
            self.assertTrue(row["residue_supports_match"])
            self.assertTrue(row["frequency_supports_match"])

    def test_failing_two_prime_quotients(self):
        expected_ratios = {
            110: (91, 6.458795524370455e-16),
            70: (143, 2.514844824284387e-16),
        }
        for lag, (quotient, expected_ratio) in expected_ratios.items():
            receipt = fully_resonant_orientation_rank_receipt(lag=lag)
            self.assertEqual(receipt["quotient_period"], quotient)
            self.assertLess(
                receipt[
                    "maximum_reconstruction_natural_scale_relative_error"],
                1e-12)
            self.assertTrue(receipt[
                "orientation_sector_reconstruction_passes"])
            self.assertAlmostEqual(
                receipt["third_singular_value_ratio"],
                expected_ratio, places=20)
            self.assertTrue(receipt["orientation_rank_two_gate_passes"])
            self.assertLess(
                receipt["maximum_orientation_pair_reference_residual"],
                1e-12)
            self.assertTrue(receipt[
                "orientation_profiles_identical_gate_passes"])
            for scalar in receipt[
                    "orientation_pair_reference_scalars"].values():
                self.assertAlmostEqual(scalar[0], 1.0, places=12)
                self.assertAlmostEqual(scalar[1], 0.0, places=12)


if __name__ == "__main__":
    unittest.main()
