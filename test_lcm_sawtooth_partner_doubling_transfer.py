import unittest

from lcm_sawtooth_partner_doubling_transfer import (
    doubled_partner_geometric_receipt,
    partner_doubling_transfer_receipt,
)


class PartnerDoublingTransferTests(unittest.TestCase):
    def test_half_interval_identity_and_primitive_lift(self):
        receipt = doubled_partner_geometric_receipt(17, 5)
        self.assertEqual(receipt["primitive_residue_count"], 4)
        self.assertTrue(receipt["primitive_odd_lift_is_bijection_proved"])
        self.assertLess(
            receipt["half_interval_factorization_maximum_relative_error"],
            1e-12)
        self.assertTrue(receipt[
            "exact_half_interval_geometric_identity_test_passes"])
        self.assertLess(
            receipt["diagonal_transfer_maximum_relative_error"], 1e-12)
        self.assertTrue(receipt[
            "exact_residue_diagonal_transfer_test_passes"])

    def test_project_fixture_applies_predeclared_scalar_gate(self):
        receipt = partner_doubling_transfer_receipt()
        self.assertEqual(receipt["odd_partners"], (35, 65))
        self.assertEqual(len(receipt["prime_moduli"]), 24)
        self.assertEqual(receipt["tolerance"], 1e-12)
        self.assertTrue(receipt[
            "exact_primitive_lift_half_interval_identity_proved"])
        self.assertTrue(receipt[
            "exact_residue_dependent_diagonal_transfer_proved"])
        self.assertLess(
            receipt["maximum_base_half_factorization_relative_error"],
            1e-12)
        self.assertLess(
            receipt["maximum_residue_diagonal_transfer_relative_error"],
            1e-12)
        self.assertLess(
            receipt["maximum_half_interval_factorization_relative_error"],
            1e-12)
        self.assertAlmostEqual(
            receipt[
                "minimum_nontrivial_full_geometric_transfer_relative_residual"],
            .6972166887783966, places=10)
        self.assertEqual(receipt["trivial_zero_geometric_channel_count"], 2)
        self.assertAlmostEqual(
            receipt[
                "maximum_nontrivial_full_geometric_transfer_relative_residual"],
            .9981053173424562, places=10)
        exact_zero_channels = {
            (row["prime_modulus"], row["odd_partner"])
            for row in receipt["geometric_transfer_rows"]
            if row["both_geometric_vectors_are_exactly_zero"]}
        self.assertEqual(exact_zero_channels, {(131, 65), (211, 35)})
        polynomial = {
            row["odd_partner"]: row
            for row in receipt["polynomial_transfer_rows"]}
        self.assertAlmostEqual(
            polynomial[35]["best_polynomial_transfer_relative_residual"],
            .2755577081330059, places=10)
        self.assertAlmostEqual(
            polynomial[65]["best_polynomial_transfer_relative_residual"],
            .29666696754607497, places=10)
        self.assertFalse(receipt[
            "single_scalar_geometric_transfer_all_channels_passes"])
        self.assertFalse(receipt[
            "single_scalar_polynomial_transfer_all_partners_passes"])
        self.assertFalse(receipt[
            "single_scalar_partner_doubling_transfer_hypothesis_passes"])
        self.assertFalse(receipt["signed_prime_correlation_proved"])

    def test_guards(self):
        with self.assertRaises(ValueError):
            doubled_partner_geometric_receipt(15, 5)
        with self.assertRaises(ValueError):
            doubled_partner_geometric_receipt(17, 6)
        with self.assertRaises(ValueError):
            partner_doubling_transfer_receipt(127, (35, 70))


if __name__ == "__main__":
    unittest.main()
