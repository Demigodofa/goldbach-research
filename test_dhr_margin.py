"""Exact checks of independently derived comparison constants and scope."""
from fractions import Fraction as F
import unittest

from dhr_margin import BETA_LOWER, BETA_UPPER, raw_limsup_upper


class DhrMarginTests(unittest.TestCase):
    def test_certified_parameter_enclosure_and_reviewed_constants(self):
        self.assertEqual(BETA_UPPER-BETA_LOWER, F(1, 10**20))
        self.assertLess(BETA_UPPER, F(43, 10))
        self.assertEqual(raw_limsup_upper(F(6)), -F(347, 14042))
        # Here the logarithm's argument is exactly 3/2 and I>=248/495.
        self.assertEqual(raw_limsup_upper(F(119, 20)), -F(1, 496))

    def test_insufficient_margin_is_not_promoted_to_failure(self):
        self.assertGreater(raw_limsup_upper(F(5)), 0)

    def test_unproved_parameter_bounds_and_formula_range_are_rejected(self):
        for u, b in [(F(6), F(42, 10)), (F(7), F(43, 10)),
                     (F(4), F(43, 10)), (6.0, F(43, 10))]:
            with self.subTest(u=u, b=b), self.assertRaises(ValueError):
                raw_limsup_upper(u, b)


if __name__ == "__main__":
    unittest.main()
