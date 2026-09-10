import unittest
from fractions import Fraction as F

from short_divisor_complement_gate import (largest_prime_boundary_terms,
                                           top_core_exponent_gate,
                                           verify_complement)


class ShortDivisorComplementTests(unittest.TestCase):
    def test_exact_complement_and_largest_prime_partition(self):
        for cutoff in range(2, 13):
            for n in range(2, 100):
                self.assertTrue(verify_complement(n, cutoff)["exact"])

    def test_negative_witness_survives_partition(self):
        result = verify_complement(15, 7)
        self.assertEqual(result["short"], -1)
        self.assertEqual(result["partition"], -1)
        self.assertEqual(largest_prime_boundary_terms(15, 7), ((5, 3, -1),))

    def test_positive_prime_cofactor_also_survives(self):
        result = verify_complement(11, 7)
        self.assertEqual(result["short"], result["partition"])
        self.assertEqual(result["short"], 1)

    def test_boundary_starts_above_point_599_and_old_dispersion_loses(self):
        gate = top_core_exponent_gate()
        self.assertEqual(gate["boundary_modulus_exponent_infimum"], F(599, 1000))
        self.assertEqual(gate["full_boundary_modulus_supremum"], 1)
        self.assertEqual(gate["previous_dispersion_power_loss"], F(49, 1000))
        self.assertFalse(gate["sign_resolved"])


if __name__ == "__main__":
    unittest.main()
