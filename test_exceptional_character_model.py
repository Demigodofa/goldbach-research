"""Independent finite controls for the exceptional-character model comparison."""
from fractions import Fraction
from math import gcd, prod
import unittest

from exceptional_character_model import character_values, pair_models, pair_moments


def odd_factors(n):
    return [p for p in range(3, n+1, 2) if n % p == 0
            and all(p % q for q in range(2, p))]


def legendre_by_squares(a, p):
    if a % p == 0:
        return 0
    return 1 if a % p in {x*x % p for x in range(1, p)} else -1


class ExceptionalCharacterTests(unittest.TestCase):
    def test_complete_residue_periods_and_bilinear_corner_certificate(self):
        checked = 0
        for d in range(3, 161):
            for sign in (1, -1):
                try:
                    chi = character_values(d, two_sign=sign)
                except ValueError:
                    continue
                self.assertEqual(sum(chi), 0)
                self.assertEqual(chi[1], 1)
                self.assertTrue(all(bool(chi[a]) == (gcd(a, d) == 1) for a in range(d)))
                # Primitivity concerns the UNIT group, not zero-extended periods.
                for divisor in range(1, d):
                    if d % divisor == 0:
                        fibers = {}
                        for residue in range(d):
                            if chi[residue]:
                                fibers.setdefault(residue % divisor, set()).add(chi[residue])
                        self.assertTrue(any(len(values) == 2 for values in fibers.values()))
                factors = odd_factors(d)
                for n in range(0, 2*d, 2):
                    a, b, c = pair_moments(d, n, two_sign=sign)
                    self.assertGreater(a, 0)
                    if d % 2 == 0 or gcd(n, d) > 1:
                        self.assertEqual(b, 0)
                    if d % 2:
                        self.assertEqual(a, prod(p-1 if n % p == 0 else p-2 for p in factors))
                        self.assertEqual(b, prod(0 if n % p == 0 else -legendre_by_squares(n, p)
                                                 for p in factors))
                        self.assertEqual(c, prod(legendre_by_squares(-1, p) *
                                                 (p-1 if n % p == 0 else -1) for p in factors))
                    for u, v in ((0, 0), (0, 1), (1, 0), (1, 1)):
                        minus, plus = pair_models(d, n, u, v, two_sign=sign)
                        direct_minus = sum((1-u*chi[x]) * (1-v*chi[(n-x) % d])
                                           for x in range(d) if chi[x] and chi[(n-x) % d])
                        direct_plus = sum((1+u*chi[x]) * (1+v*chi[(n-x) % d])
                                          for x in range(d) if chi[x] and chi[(n-x) % d])
                        self.assertEqual((minus, plus), (direct_minus, direct_plus))
                        if d > 21:
                            self.assertGreaterEqual(5*minus, 3*plus)
                    checked += 1
        self.assertGreater(checked, 5000)

    def test_multiplicative_sign_change_and_noncorner_weights(self):
        u, v = Fraction(2, 3), Fraction(4, 5)
        for d, sign in ((5, 1), (33, 1), (40, 1), (40, -1), (84, 1)):
            chi = character_values(d, two_sign=sign)
            units = [a for a in range(d) if gcd(a, d) == 1]
            for n in units:
                convolution = sum((1-u*chi[a])*(1-v*chi[n*pow(a, -1, d) % d])
                                  for a in units) / len(units)
                self.assertEqual(convolution, 1+u*v*chi[n])
            minus, plus = pair_models(d, 128, u, v, two_sign=sign)
            if d > 21:
                self.assertGreaterEqual(minus-Fraction(49, 100)*plus,
                                        Fraction(11, 60)*minus)

    def test_powers_of_two_and_necessary_small_conductor_exclusions(self):
        for d in range(25, 161):
            for sign in (1, -1):
                try:
                    character_values(d, two_sign=sign)
                except ValueError:
                    continue
                for j in range(1, 13):
                    n = 2**j
                    a, _, _ = pair_moments(d, n, two_sign=sign)
                    for u, v in ((0, 0), (0, 1), (1, 0), (1, 1)):
                        minus, plus = pair_models(d, n, u, v, two_sign=sign)
                        self.assertGreaterEqual(3*minus, 2*a)
                        self.assertGreaterEqual(minus-Fraction(49, 100)*plus,
                                                Fraction(11, 90)*a)
        self.assertEqual(pair_models(5, 2, 1, 1), (0, 4))
        # Even conductor gives P=S, but they can both vanish at u=v=1.
        self.assertEqual(pair_models(24, 32, 1, 1, two_sign=-1), (0, 0))

    def test_input_meaning_and_exact_endpoint_checks(self):
        for bad in (True, 1, 2, 6, 9, 16, 18, 27, 45):
            with self.assertRaises(ValueError):
                character_values(bad)
        for d, sign in ((5, -1), (8, True), (8, 0)):
            with self.assertRaises(ValueError):
                character_values(d, two_sign=sign)
        for n in (True, 3, 4.0):
            with self.assertRaises(ValueError):
                pair_moments(33, n)
        for u in (True, 0.5, Fraction(-1, 2), Fraction(3, 2)):
            with self.assertRaises(ValueError):
                pair_models(33, 32, u, 1)


if __name__ == "__main__":
    unittest.main()
