import unittest

from lcm_sawtooth_linked_prime_character import (
    linked_prime_character_receipt,
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


if __name__ == "__main__":
    unittest.main()
