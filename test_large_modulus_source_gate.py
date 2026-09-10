import unittest
from fractions import Fraction as F

from large_modulus_source_gate import (actual_top_core_gate,
                                       balanced_triple_support_obstruction,
                                       numerical_margin,
                                       product_modulus_exponent,
                                       source_hypothesis_gate)


class LargeModulusSourceGateTests(unittest.TestCase):
    def test_top_core_is_numerically_just_below_three_fifths(self):
        self.assertEqual(product_modulus_exponent(F(41, 100)), F(599, 1000))
        self.assertEqual(numerical_margin(), F(1, 1000))

    def test_exponent_match_does_not_license_theorem(self):
        result = actual_top_core_gate()
        self.assertFalse(result["licensed"])
        self.assertFalse(result["fixed_bounded_residue"])
        self.assertFalse(result["triply_well_factorable"])
        self.assertTrue(result["balanced_triple_support_obstruction"])
        self.assertTrue(balanced_triple_support_obstruction())

    def test_every_source_hypothesis_is_required(self):
        self.assertTrue(source_hypothesis_gate(
            fixed_bounded_residue=True, triply_well_factorable=True,
            endpoint_coupling_transferred=True, shift_family_transferred=True))
        names = ("fixed_bounded_residue", "triply_well_factorable",
                 "endpoint_coupling_transferred", "shift_family_transferred")
        for missing in names:
            values = {name: True for name in names}
            values[missing] = False
            self.assertFalse(source_hypothesis_gate(**values))


if __name__ == "__main__":
    unittest.main()
