"""Exact lifting controls; no numerical claim about a Siegel zero or primes."""
from fractions import Fraction as F
from math import gcd, lcm
import unittest

from exceptional_character_model import character_values
from relative_type_i import lifted_character_projection


class RelativeTypeITests(unittest.TestCase):
    def test_primitive_inducers_and_exceptional_boundary(self):
        for conductor, sign in ((33, 1), (35, 1), (40, 1), (40, -1), (120, -1)):
            for incoming, incoming_sign in ((1, 1), (3, 1), (4, 1), (5, 1),
                                             (8, 1), (8, -1), (11, 1), (15, 1)):
                period, principal, exceptional = lifted_character_projection(
                    conductor, incoming, two_sign=sign, input_two_sign=incoming_sign)
                self.assertEqual(period, lcm(conductor, incoming))
                self.assertEqual(principal, int(incoming == 1))
                self.assertEqual(exceptional, 0)
            # The exceptional term cannot be dropped when the inducer agrees.
            self.assertEqual(lifted_character_projection(conductor, conductor,
                                                         two_sign=sign, input_two_sign=sign)[1:],
                             (0, 1))
        self.assertEqual(lifted_character_projection(40, 40, two_sign=1,
                                                     input_two_sign=-1)[1:], (0, 0))

    def test_projection_error_has_no_extra_totient_factor(self):
        density, exceptional_mass, error = F(17, 3), F(29, 7), F(2, 13)
        for conductor, incoming in ((33, 1), (33, 5), (40, 3), (40, 40)):
            period, a, b = lifted_character_projection(conductor, incoming)
            chi_d = character_values(conductor)
            chi_r = (1,) if incoming == 1 else character_values(incoming)
            units = [n for n in range(period) if gcd(n, period) == 1]
            # Align every permitted residue error with its lifting coefficient.
            # The resulting total error equals the original error bound exactly.
            actual = sum(F(chi_r[n % incoming], len(units))*
                         (density-chi_d[n % conductor]*exceptional_mass+
                          chi_r[n % incoming]*error) for n in units)
            self.assertEqual(actual-(density*a-exceptional_mass*b), error)
            self.assertGreater(len(units), 1)

    def test_complex_quartic_input_is_orthogonal_after_lifting(self):
        # Exact Gaussian integer pairs for the primitive quartic character mod5.
        quartic = ((0, 0), (1, 0), (0, 1), (0, -1), (-1, 0))
        for conductor in (33, 40):
            period = lcm(5, conductor)
            chi = character_values(conductor)
            units = [a for a in range(period) if gcd(a, period) == 1]
            for exceptional in (False, True):
                result = tuple(sum(quartic[a % 5][component]*
                                   (chi[a % conductor] if exceptional else 1)
                                   for a in units) for component in (0, 1))
                self.assertEqual(result, (0, 0))
            # Their values have modulus exactly1 on the lifted unit group.
            self.assertTrue(all(sum(v*v for v in quartic[a % 5]) == 1 for a in units))

    def test_exact_input_meaning_and_rejected_nonprimitive_characters(self):
        for conductor, incoming, sign, incoming_sign in (
                (True, 1, 1, 1), (25, 1, 1, 1), (33, True, 1, 1),
                (33, 0, 1, 1), (33, 9, 1, 1), (33, 1, 1, -1),
                (33, 1, 1, True), (33, 3, 1, -1), (40, 8, True, 1),
                (33, 1.0, 1, 1)):
            with self.assertRaises(ValueError):
                lifted_character_projection(conductor, incoming, two_sign=sign,
                                              input_two_sign=incoming_sign)
        self.assertIn("not asserted", lifted_character_projection.__doc__)


if __name__ == "__main__":
    unittest.main()
