import unittest

from divisor_active_full_gram import finite_active_full_comparison
from divisor_schur_falsifier import (
    schur_falsifier,
    single_modulus_schur_falsifier,
)


class DivisorSchurFalsifierTests(unittest.TestCase):
    def test_reconstructs_active_full_generalized_eigenvalue(self):
        expected = finite_active_full_comparison(32000, modulus_limit=3)
        receipt = schur_falsifier(32000, modulus_limit=3)
        self.assertAlmostEqual(
            receipt["actual_generalized_eigenvalue"],
            expected["uniform_largest_generalized_eigenvalue"], places=10)

    def test_receipt_distinguishes_failed_and_hybrid_bounds(self):
        receipt = schur_falsifier(32000, modulus_limit=3)
        self.assertGreater(receipt["active_schur_row_sum_max"], 0)
        self.assertGreater(
            receipt["schur_over_exact_full_bound"],
            receipt["actual_generalized_eigenvalue"])
        self.assertEqual(
            receipt["diagonal_schur_gershgorin_proof_survives"],
            receipt["full_gershgorin_lower"] > 0)

    def test_single_modulus_receipt(self):
        receipt = single_modulus_schur_falsifier(1009, 5, 9, 3, 8)
        self.assertEqual(len(receipt["divisors"]), 5)
        self.assertGreater(
            receipt["schur_over_exact_full_bound"],
            receipt["actual_generalized_eigenvalue"])


if __name__ == "__main__":
    unittest.main()
