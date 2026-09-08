"""Independent character enumeration checks the arithmetic classification."""
from fractions import Fraction
from math import gcd, lcm
import unittest

from character_suppression import count_suppression_targets, suppression_classes
from exceptional_character_model import character_values


def direct_moments(chi, target):
    d = len(chi)
    units = [a for a in range(d) if chi[a] and chi[(target-a) % d]]
    return (len(units), sum(chi[a] for a in units),
            sum(chi[a]*chi[(target-a) % d] for a in units))


class CharacterSuppressionTests(unittest.TestCase):
    def test_complete_period_classification_against_character_enumeration(self):
        checked = 0
        for d in (*range(25, 161), 280, 385, 840):
            for sign in (1, -1):
                try:
                    chi = character_values(d, two_sign=sign)
                except ValueError:
                    continue
                q, period, residues = suppression_classes(d, two_sign=sign)
                self.assertGreater(q, 1)
                self.assertEqual(gcd(q, 6), 1)
                self.assertIn(d//q, (1, 3, 4, 8, 12, 24))
                self.assertEqual(period, lcm(2, d))
                self.assertLessEqual(period//q, 24)
                direct = []
                for target in range(0, period, 2):
                    a, b, c = direct_moments(chi, target)
                    if b == 0 and c == -a:
                        direct.append(target)
                    checked += 1
                self.assertEqual(residues, tuple(direct))
                self.assertTrue(all(r % q == 0 and r % 2 == 0 for r in residues))
        self.assertGreater(checked, 5000)

    def test_margin_and_exact_suppression_at_corners_and_near_endpoint(self):
        rho = Fraction(49, 100)
        for d, sign in ((29, 1), (31, 1), (33, 1), (35, 1),
                        (40, 1), (40, -1), (120, 1), (120, -1)):
            chi = character_values(d, two_sign=sign)
            _, period, residues = suppression_classes(d, two_sign=sign)
            for target in range(0, period, 2):
                a, b, c = direct_moments(chi, target)
                for u, v in ((0, 0), (0, 1), (1, 0), (1, 1),
                             (Fraction(999999, 1000000), 1),
                             (Fraction(2, 3), Fraction(4, 5))):
                    minus = a-(u+v)*b+u*v*c
                    plus = a+(u+v)*b+u*v*c
                    if target in residues:
                        self.assertEqual(minus, a*(1-u*v))
                        self.assertEqual(minus, plus)
                    else:
                        self.assertGreaterEqual(3*minus, 2*a)
                        self.assertGreaterEqual(minus-rho*plus, Fraction(11, 90)*a)
        self.assertEqual(suppression_classes(29)[2], ())
        self.assertEqual(suppression_classes(31)[2], (0,))
        self.assertEqual(suppression_classes(33)[2], (22, 44))
        self.assertEqual(suppression_classes(40)[2], (20,))
        self.assertEqual(suppression_classes(40, two_sign=-1)[2], (0,))
        self.assertEqual(suppression_classes(120)[2], (0, 20, 100))

    def test_exact_band_counts_against_direct_moments_including_edges(self):
        for d, sign in ((29, 1), (31, 1), (33, 1), (40, 1), (120, -1)):
            chi = character_values(d, two_sign=sign)
            for first, last in ((2, 2), (20, 20), (14, 240), (38, 1320),
                                (2*d, 2*d), (2*d-2, 2*d+2)):
                direct = 0
                for target in range(first, last+1, 2):
                    a, b, c = direct_moments(chi, target)
                    direct += b == 0 and c == -a
                self.assertEqual(count_suppression_targets(d, first, last,
                                                           two_sign=sign), direct)

    def test_input_meaning_and_primitive_conductor_boundary(self):
        for d in (True, 24, 25, 27, 30, 32, 36, 40.0, 45, 54):
            with self.assertRaises(ValueError):
                suppression_classes(d)
        for d, sign in ((31, -1), (40, True), (40, 0)):
            with self.assertRaises(ValueError):
                suppression_classes(d, two_sign=sign)
        for first, last in ((True, 4), (2, 4.0), (0, 2), (3, 6), (6, 4)):
            with self.assertRaises(ValueError):
                count_suppression_targets(31, first, last)
        self.assertIn("not prime flags", suppression_classes.__doc__)


if __name__ == "__main__":
    unittest.main()
