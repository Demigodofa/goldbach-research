"""Finite identities only; no zero, analytic error, or Goldbach claim."""
from fractions import Fraction as F
from math import gcd
import unittest

from exceptional_character_model import character_values, pair_moments
from periodic_character_comparison import periodic_pair_data, periodic_progression_sum


class PeriodicComparisonTests(unittest.TestCase):
    def test_crt_lifts_direct_products_and_suppressed_positive_margin(self):
        cases = ((29, 58, 1), (29, 116, 1), (31, 930, 1), (40, 120, 1),
                 (40, 240, -1), (60, 420, 1), (33, 330, 1))
        for d, q, sign in cases:
            chi = character_values(d, two_sign=sign)
            units = [a for a in range(q) if gcd(a, q) == 1]
            for n in (6, 8, 30, 62, 120):
                a_d, b_d, c_d = pair_moments(d, n, two_sign=sign)
                for u, v in ((0, 0), (1, 0), (0, 1), (1, 1),
                             (F(1, 2), F(3, 4)), (F(999, 1000), F(999, 1000))):
                    k, b, c, margin = periodic_pair_data(d, q, n, u, v, two_sign=sign)
                    self.assertEqual((b, c), (F(b_d, a_d), F(c_d, a_d)))
                    direct = sum((1-u*chi[a % d])*(1-v*chi[(n-a) % d])
                                 for a in units if gcd(n-a, q) == 1)
                    self.assertEqual(k*margin, F(q, len(units)**2)*direct)
                    self.assertGreaterEqual(margin, F(3, 4)*(1-u*v))
                    self.assertGreaterEqual(k, 1)
        _, b, c, margin = periodic_pair_data(31, 62, 62, F(9, 10), F(9, 10))
        self.assertEqual((b, c, margin), (0, -1, F(19, 100)))
        self.assertEqual(periodic_pair_data(31, 62, 62, 1, 1)[3], 0)

    def test_complete_progressions_signed_periods_and_boundary_remainders(self):
        for q in range(1, 9):
            values = [F((-1)**j*(j+1), j % 3+1) for j in range(q)]
            for divisor in (1, 3, 2*q+1):
                if gcd(divisor, q) != 1:
                    continue
                for target, start in ((0, 0), (17, -4), (-9, 3)):
                    for terms in (0, 1, q-1, q, q+3, 10*q+2):
                        result = periodic_progression_sum(values, target, divisor, start, terms)
                        direct = sum(values[(target-divisor*k) % q]
                                     for k in range(start, start+terms))
                        self.assertEqual(result, direct)
                        self.assertLessEqual(abs(result-F(terms, q)*sum(values)),
                                             2*q*max(map(abs, values)))

    def test_missing_prime_factor_creates_exact_local_density_discrepancy(self):
        for q in (2, 6, 30):
            phi_q = sum(gcd(a, q) == 1 for a in range(q))
            values = [F(q, phi_q) if gcd(a, q) == 1 else F(0) for a in range(q)]
            for ell in (7, 11):
                period = q*ell
                n = 8  # Coprime to both selected outside primes.
                phi_full = sum(gcd(a, period) == 1 for a in range(period))
                model = sum(values[a % q] for a in range(period) if a % ell == n % ell)/period
                prime_local = sum(F(period, phi_full) for a in range(period)
                                  if a % ell == n % ell and gcd(a, period) == 1)/period
                self.assertEqual(model, F(1, ell))
                self.assertEqual(prime_local, F(1, ell-1))
                self.assertEqual(prime_local-model, F(1, ell*(ell-1)))

    def test_input_meanings_primitive_ranges_and_coprime_requirement(self):
        for d, q, n, u, v in ((True, 62, 62, 0, 0), (24, 24, 32, 0, 0),
                              (25, 50, 50, 0, 0), (31, 31, 62, 0, 0),
                              (31, 64, 62, 0, 0), (31, 62, 7, 0, 0),
                              (31, 62, 62, True, 0), (31, 62, 62, 0.5, 0),
                              (31, 62, 62, F(3, 2), 0)):
            with self.assertRaises(ValueError):
                periodic_pair_data(d, q, n, u, v)
        with self.assertRaises(ValueError):
            periodic_pair_data(40, 80, 80, 0, 0, two_sign=True)
        for values, divisor, terms in (([], 1, 1), ([True], 1, 1),
                                       ([0, 2], 2, 5), ([0, 2], 1, -1),
                                       ([0, 2], True, 1), ([0, 0.5], 1, 2)):
            with self.assertRaises(ValueError):
                periodic_progression_sum(values, 8, divisor, 0, terms)
        self.assertIn("not supplied zero estimates", periodic_pair_data.__doc__)


if __name__ == "__main__":
    unittest.main()
