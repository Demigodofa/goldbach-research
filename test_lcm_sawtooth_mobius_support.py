import math
import unittest

from lcm_sawtooth_mobius_support import (
    _divisor_level_inverse_support_formula,
    mobius_divisor_support_receipt,
)


class MobiusDivisorSupportTests(unittest.TestCase):
    def test_guards(self):
        with self.assertRaises(ValueError):
            mobius_divisor_support_receipt(denominators=())
        with self.assertRaises(ValueError):
            mobius_divisor_support_receipt(tolerance=-1)

    def test_exact_support_formula_examples(self):
        self.assertEqual(
            _divisor_level_inverse_support_formula(77, 7, 1), 0.0)
        self.assertEqual(
            _divisor_level_inverse_support_formula(77, 11, 1), 0.0)
        self.assertAlmostEqual(
            _divisor_level_inverse_support_formula(77, 7, 11),
            -1 / math.tan(math.pi / 7),
            places=14)

    def test_proper_levels_vanish_at_primitive_indices(self):
        receipt = mobius_divisor_support_receipt()
        self.assertEqual(receipt["denominators"], (77, 130, 143, 70))
        self.assertTrue(receipt["all_support_reconstructions_pass"])
        for row in receipt["rows"].values():
            self.assertTrue(row["exact_primitive_support_obstruction"])
            self.assertLess(
                row["maximum_support_formula_relative_error"], 1e-12)
            self.assertLess(
                row["maximum_proper_level_absolute_value"], 1e-12)
            self.assertLess(
                row["maximum_terminal_level_relative_error"], 1e-12)
        self.assertFalse(receipt[
            "proper_divisor_mobius_signs_survive_at_primitive_inverse_indices"])
        self.assertFalse(receipt[
            "proposed_inverse_level_sign_mechanism_passes"])
        self.assertFalse(receipt["signed_prime_correlation_proved"])


if __name__ == "__main__":
    unittest.main()
