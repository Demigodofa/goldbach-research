"""Complete-period controls, including the exceptional conductor factors."""
from fractions import Fraction
from math import gcd, lcm
import unittest

from exceptional_character_model import character_values, pair_models, pair_moments
from major_arc_kernel import sampled_kernel
from signed_pair_main_term import gcd_exception_cover, pair_coefficients


def complete_kernel_arrays(samples, conductor, two_sign):
    period = lcm(conductor, *(q for q in range(1, len(samples)) if samples[q]))
    chi = character_values(conductor, two_sign=two_sign)
    phi_d = sum(value != 0 for value in chi)
    principal = []
    exceptional = []
    for residue in range(period):
        representative = residue or period
        principal.append(sampled_kernel(representative, 1, samples))
        exceptional.append(chi[residue % conductor]*Fraction(conductor, phi_d)*
                           sampled_kernel(representative, conductor, samples))
    return period, principal, exceptional


class SignedPairMainTermTests(unittest.TestCase):
    def test_coefficients_against_complete_periods_for_all_conductor_types(self):
        # Mixed rational samples need not represent an analytic cutoff.
        samples = tuple(Fraction((k*5) % 9-4, k+1) for k in range(9))
        for conductor, sign in ((3, 1), (4, 1), (5, 1), (8, 1), (8, -1), (12, 1)):
            period, principal, exceptional = complete_kernel_arrays(samples, conductor, sign)
            for target in (0, 2, 8, 2*conductor, -2*conductor):
                u0, mixed, quadratic = pair_coefficients(target, samples, conductor, two_sign=sign)
                direct0 = sum(principal[n]*principal[(target-n) % period] for n in range(period))/period
                direct1 = sum(principal[n]*exceptional[(target-n) % period] for n in range(period))/period
                direct2 = sum(exceptional[n]*exceptional[(target-n) % period] for n in range(period))/period
                self.assertEqual((u0, mixed, quadratic), (direct0, direct1, direct2))
                for u, v in ((0, 1), (1, 1), (Fraction(2, 3), Fraction(4, 5))):
                    direct_minus = sum((principal[n]-u*exceptional[n])*
                                       (principal[(target-n) % period]-v*exceptional[(target-n) % period])
                                       for n in range(period))/period
                    self.assertEqual(direct_minus, u0-(u+v)*mixed+u*v*quadratic)

    def test_active_composite_conductors_with_multiple_cofactor_terms(self):
        for conductor, sign in ((15, 1), (33, 1), (40, 1), (40, -1)):
            # Sparse support keeps a complete period small while activating
            # the conductor and a second coprime cofactor in Lambda_R,D.
            cofactor = 2 if conductor % 2 else 3
            samples = [Fraction(0)]*(conductor*cofactor+1)
            for q in (1, 2, 3, 5, conductor, conductor*cofactor):
                samples[q] = Fraction(q % 7-3, q+1)
            samples[conductor] = Fraction(2, 3)
            samples[conductor*cofactor] = Fraction(-3, 5)
            samples = tuple(samples)
            period, principal, exceptional = complete_kernel_arrays(samples, conductor, sign)
            for target in (2, 8, 10, 2*conductor):
                direct = tuple(sum(first[n]*second[(target-n) % period] for n in range(period))/period
                               for first, second in ((principal, principal),
                                                     (principal, exceptional),
                                                     (exceptional, exceptional)))
                self.assertEqual(pair_coefficients(target, samples, conductor, two_sign=sign), direct)

    def test_cutoff_boundary_absent_character_and_nonsquarefree_conductor(self):
        samples = (0, 1, 1, Fraction(1, 2), 1, 0, 0, 0, 0)
        # At conductor4 the mixed term vanishes because Gamma has no
        # primitive denominator4; the character-character term can survive.
        _, mixed, quadratic = pair_coefficients(8, samples, 4)
        self.assertEqual(mixed, 0)
        self.assertEqual(quadratic, -2)
        # IndexD is the q=1 term of Lambda_R,D. Omitting it removes Xi.
        self.assertNotEqual(pair_coefficients(8, samples, 4)[2], 0)
        self.assertEqual(pair_coefficients(8, samples[:4], 4)[1:], (0, 0))
        self.assertEqual(pair_coefficients(8, samples, 12)[1:], (0, 0))
        self.assertEqual(pair_coefficients(8, samples)[0], pair_coefficients(8, samples, 4)[0])

    def test_suppressed_margin_is_linear_in_one_minus_bias_product(self):
        rho = Fraction(49, 100)
        # Covers B=0, B nonzero of either sign, even conductors, and
        # a suppression arbitrarily close to its zero-bias-distance endpoint.
        for conductor, sign in ((24, -1), (33, 1), (35, 1), (40, 1), (40, -1), (105, 1)):
            for target in range(0, 2*conductor, 2):
                a, _, _ = pair_moments(conductor, target, two_sign=sign)
                for u, v in ((0, 0), (0, 1), (1, 1), (Fraction(999, 1000), 1),
                             (Fraction(3, 5), Fraction(5, 7))):
                    minus, plus = pair_models(conductor, target, u, v, two_sign=sign)
                    floor = a*min(Fraction(2, 3), 1-u*v)
                    self.assertGreaterEqual(minus, floor)
                    self.assertGreaterEqual(minus-rho*plus, Fraction(11, 60)*floor)

    def test_exact_input_meaning(self):
        for target, samples, conductor, sign in ((3, (0, 1), None, 1),
                                                (True, (0, 1), None, 1),
                                                (8, (0,), None, 1),
                                                (8, (0, 0.5), None, 1),
                                                (8, (0, True), None, 1),
                                                (8, (0, 1), 9, 1),
                                                (8, (0, 1), 5, -1),
                                                (8, (0, 1), None, -1),
                                                (8, (0, 1), None, True)):
            with self.assertRaises(ValueError):
                pair_coefficients(target, samples, conductor, two_sign=sign)
        self.assertIn("do not certify", pair_coefficients.__doc__)

    def test_large_conductor_character_correlation_and_exact_divisor_cover(self):
        for conductor, sign in ((8, -1), (24, 1), (33, 1), (40, -1), (105, 1), (120, 1)):
            for target in range(2, 242, 2):
                _, b, c = pair_moments(conductor, target, two_sign=sign)
                self.assertLessEqual(abs(b), 1)
                self.assertLessEqual(abs(c), 2*gcd(conductor, target))
            for scale in (1, Fraction(3, 2), 3, 16):
                divisors, count = gcd_exception_cover(conductor, 14, 240, scale)
                actual = {n for n in range(14, 241, 2) if gcd(conductor, n)*scale > conductor}
                covered = {n for n in range(14, 241, 2) if any(n % d == 0 for d in divisors)}
                self.assertEqual(actual, covered)
                self.assertGreaterEqual(count, len(actual))
        divisors, count = gcd_exception_cover(12, 2, 48, 4)
        self.assertEqual(divisors, (4, 6, 12))
        self.assertGreater(count, len({n for n in range(2, 49, 2) if gcd(12, n)*4 > 12}))
        for arguments in ((0, 2, 8, 1), (12, 3, 8, 1), (12, 8, 2, 1),
                          (12, 2, 8, 0.5), (True, 2, 8, 1), (12, 2, 8, True)):
            with self.assertRaises(ValueError):
                gcd_exception_cover(*arguments)


if __name__ == "__main__":
    unittest.main()
