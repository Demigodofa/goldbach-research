import unittest
from fractions import Fraction as F

from dual_burgess_gate import (H, burgess_dual_exponent,
                               direct_burgess_gate, excess_numerator,
                               formal_r1_exponent, top_factorization_identity)


class DualBurgessGateTests(unittest.TestCase):
    def test_formal_r1_only_recovers_direct_bound_but_is_not_licensed(self):
        self.assertEqual(formal_r1_exponent(), H)
        with self.assertRaises(ValueError):
            burgess_dual_exponent(1)

    def test_every_nontrivial_burgess_parameter_is_worse(self):
        for r in range(2, 65):
            self.assertGreater(burgess_dual_exponent(r), H)
            self.assertGreater(excess_numerator(r), 0)

    def test_exact_excess_factorization(self):
        for r in range(1, 65):
            self.assertEqual(excess_numerator(r), top_factorization_identity(r))

    def test_receipt_does_not_claim_saving(self):
        result = direct_burgess_gate()
        self.assertTrue(result["formal_r1_matches_direct"])
        self.assertTrue(result["every_licensed_r_worse"])
        self.assertFalse(result["saving_proved"])

    def test_r2_value_keeps_all_transform_factors(self):
        self.assertEqual(burgess_dual_exponent(2), F(2597, 16000))
        self.assertGreater(F(2597, 16000), F(1, 10))

    def test_even_free_reduction_to_prime_component_is_worse(self):
        self.assertEqual(burgess_dual_exponent(2, F(59, 100)), F(257, 1600))
        self.assertGreater(F(257, 1600), F(1, 10))


if __name__ == "__main__":
    unittest.main()
