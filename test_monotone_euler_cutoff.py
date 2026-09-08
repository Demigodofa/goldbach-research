"""Finite controls for Euler signs, cutoff requirements, and model margins."""
from fractions import Fraction
from itertools import product
from math import lcm
import unittest

from character_suppression import suppression_classes
from exceptional_character_model import character_values
from monotone_euler_cutoff import cutoff_euler_sum, normalized_comparison
from signed_pair_main_term import pair_coefficients


def direct_moments(chi, target):
    d = len(chi)
    allowed = [x for x in range(d) if chi[x] and chi[(target-x) % d]]
    return (len(allowed), sum(chi[x] for x in allowed),
            sum(chi[x]*chi[(target-x) % d] for x in allowed))


class MonotoneEulerCutoffTests(unittest.TestCase):
    def test_finite_euler_expansion_and_ratio_by_independent_prime_subsets(self):
        # All primes that can enter a nonzero weight (r<=19). The full
        # finite Euler product also includes products beyond that cutoff.
        primes = (2, 3, 5, 7, 11, 13, 17, 19)
        choices = ((0,)*20, (0,)+(1,)*19,
                   (0,)+tuple(Fraction(20-r, 19) for r in range(1, 20)),
                   (0,)+tuple(Fraction(3, 4) if r <= 5 else 0 for r in range(1, 20)))
        for target in (2, 6, 10, 30, 126, 210):
            for d in (1, 3, 4, 15, 31, 40):
                terms = [(1, Fraction(1))]
                for p in primes:
                    if d % p:
                        local = Fraction(p-1 if target % p == 0 else -1, (p-1)**2)
                        terms += [(r*p, coefficient*local) for r, coefficient in terms]
                full = sum(coefficient for _, coefficient in terms)
                absolute = sum(abs(coefficient) for _, coefficient in terms)
                self.assertGreater(full, 0)
                self.assertLess(absolute, Fraction(5, 2)*full)
                for weights in choices:
                    direct = sum(coefficient*weights[r] for r, coefficient in terms
                                 if r < len(weights))
                    actual = cutoff_euler_sum(target, d, weights)
                    self.assertEqual(actual, direct)
                    self.assertGreaterEqual(actual, 0)
                    self.assertLessEqual(actual, Fraction(5, 2)*full)

    def test_cofactor_weight_meaning_against_existing_pair_coefficients(self):
        samples = (0,)+tuple(max(0, min(1, Fraction(100-k, 70))) for k in range(1, 121))
        for d, sign in ((4, 1), (15, 1), (31, 1), (33, 1), (40, 1), (40, -1)):
            chi = character_values(d, two_sign=sign)
            phi_d = sum(bool(value) for value in chi)
            weights = (0,)+tuple(samples[d*r]**2 for r in range(1, (len(samples)-1)//d+1))
            for target in (2, 30, 126):
                _, b, c = direct_moments(chi, target)
                ud = cutoff_euler_sum(target, d, weights)
                _, mixed, quadratic = pair_coefficients(target, samples, d, two_sign=sign)
                self.assertEqual(mixed, Fraction(d*b, phi_d**2)*ud)
                self.assertEqual(quadratic, Fraction(d*c, phi_d**2)*ud)

    def test_model_margins_and_small_A_limitation(self):
        for d, sign in ((29, 1), (31, 1), (33, 1), (35, 1),
                        (40, 1), (40, -1), (77, 1), (120, 1), (120, -1)):
            chi = character_values(d, two_sign=sign)
            _, _, suppressed = suppression_classes(d, two_sign=sign)
            for target in range(0, lcm(2, d), 2):
                a, b, c = direct_moments(chi, target)
                if target in suppressed or (b != 0 and a < 20):
                    continue
                # The expression is multilinear in theta,u,v, so these
                # corners certify the whole box; include an interior control.
                parameters = (*product((0, Fraction(5, 2)), (0, 1), (0, 1)),
                              (Fraction(7, 5), Fraction(2, 3), Fraction(4, 5)))
                for theta, u, v in parameters:
                    floor = Fraction(17, 200) if b == 0 else Fraction(17, 400)
                    self.assertGreaterEqual(normalized_comparison(a, b, c, theta, u, v), floor)
        # An arbitrary theta in the enclosure does NOT yield a margin for
        # every small conductor. This is not a realizability or prime claim.
        a, b, c = direct_moments(character_values(33), 2)
        self.assertEqual((a, b, c), (9, 1, 1))
        self.assertLess(normalized_comparison(a, b, c, Fraction(5, 2), 1, 1), 0)

    def test_monotonicity_is_necessary_and_input_boundaries_are_explicit(self):
        # Keeping only the negative prime3 term gives -1/4 at m=2,D=31.
        # Such weights must be rejected by the monotone lemma's verifier.
        nonmonotone_samples = [0]*94
        nonmonotone_samples[1] = nonmonotone_samples[93] = 1
        _, mixed, _ = pair_coefficients(2, tuple(nonmonotone_samples), 31)
        _, b, _ = direct_moments(character_values(31), 2)
        self.assertEqual(b, -1)
        self.assertEqual(mixed*Fraction(30**2, 31*b), Fraction(-1, 4))
        for weights in ((0, 0, 0, 1), (0, 2), (0, Fraction(-1, 3)),
                        (0, True), (0, 0.5), (0,)):
            with self.assertRaises(ValueError):
                cutoff_euler_sum(2, 31, weights)
        for target, d in ((0, 31), (3, 31), (True, 31), (2, 0), (2, 31.0)):
            with self.assertRaises(ValueError):
                cutoff_euler_sum(target, d, (0, 1))
        for args in ((0, 0, 0, 1, 1, 1), (1, 2, 0, 1, 1, 1),
                     (True, 0, 0, 1, 1, 1), (1, 0, 0, 3, 1, 1),
                     (1, 0, 0, 1, 0.5, 1), (1, 0, 0, 1, 1, -1)):
            with self.assertRaises(ValueError):
                normalized_comparison(*args)
        self.assertIn("do not certify", cutoff_euler_sum.__doc__)


if __name__ == "__main__":
    unittest.main()
