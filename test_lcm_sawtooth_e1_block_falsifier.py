import unittest

from lcm_sawtooth_e1_block_falsifier import e1_block_counterexample


class LcmSawtoothE1BlockFalsifierTests(unittest.TestCase):
    def test_fixed_counterexample_falsifies_universal_contraction(self):
        receipt = e1_block_counterexample()
        self.assertEqual(receipt["modulus"], 131)
        self.assertEqual(receipt["ell"], 2)
        self.assertEqual(receipt["divisor_range"], (8, 17))
        self.assertEqual(receipt["dominant_block_range"], (16, 32))
        self.assertEqual(receipt["selected_coordinate_count"], 2)
        self.assertGreater(
            receipt["e1_block_square_energy_over_no_common_diagonal"], 32.9)
        self.assertTrue(
            receipt["universal_e1_block_diagonal_bound_falsified"])
        self.assertFalse(receipt["project_scaled_e1_block_bound_proved"])

    def test_counterexample_preserves_exact_reductions(self):
        receipt = e1_block_counterexample()
        self.assertEqual(receipt["maximum_assignment_identity_error"], 0)
        self.assertLess(receipt["maximum_walsh_identity_error"], 2e-16)
        self.assertTrue(receipt["walsh_factorization_retained"])
        self.assertTrue(receipt["dyadic_cauchy_reduction_retained"])


if __name__ == "__main__":
    unittest.main()
