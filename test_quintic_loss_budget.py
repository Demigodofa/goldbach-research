"""Independent finite controls for the quintic loss deduction, not prime densities."""
from fractions import Fraction as F
from itertools import product
from math import comb, gcd, lcm, prod
import unittest

from exceptional_character_model import character_values
from quintic_loss_budget import (adaptive_semiprime_indices, formal_quintic_cancellation,
                                 quintic_range_exponents, simplex_polynomial_integral,
                                 switched_residue_density)
from quintic_partner_weight import quintic_formal_weight
from test_character_partner_weight import trial_factors


def iterated_stick_integral(powers):
    # Substitute xi=ti*product_{j<i}(1-tj). The Jacobian contributes
    # (1-ti)^(k-i-2); expand each one-dimensional polynomial and integrate.
    answer = F(1)
    for i, a in enumerate(powers[:-1]):
        b = sum(powers[i+1:])+len(powers)-i-2
        answer *= sum(F((-1)**j*comb(b, j), a+j+1) for j in range(b+1))
    return answer


class QuinticLossBudgetTests(unittest.TestCase):
    def test_adaptive_indices_by_independent_cofactor_enumeration(self):
        level, limit = 1700, 160
        candidates = []
        for m in range(1, limit+1):
            fs = trial_factors(m)
            if len(fs) == 2 and all(a == 1 for a in fs.values()):
                candidates.append((m, max(fs)))
        for cutoff in (3, 7, 13):
            for index in range(1, level+2):
                expected = []
                fs = trial_factors(index)
                if index <= level and all(a == 1 for a in fs.values()):
                    for m, r2 in candidates:
                        if index % m == 0:
                            e = index//m
                            if gcd(m, e) == 1 and all(p <= min(r2, cutoff)
                                                     for p in trial_factors(e)):
                                expected.append((m, e))
                actual = adaptive_semiprime_indices(index, level, limit, cutoff)
                self.assertEqual(actual, tuple(expected))
                self.assertLessEqual(len(actual), comb(len(fs), 2))
        self.assertEqual(adaptive_semiprime_indices(385, 1000, 100, 11),
                         ((55, 7), (77, 5)))  # (35,11) fails the adaptive cutoff.
        self.assertEqual(adaptive_semiprime_indices(5005, 6000, 200, 11),
                         ((65, 77), (91, 55), (143, 35)))  # Still NOT injective.
        self.assertEqual(adaptive_semiprime_indices(5005, 6000, 200, 7), ((143, 35),))
        self.assertEqual(adaptive_semiprime_indices(35, 35, 35, 7), ((35, 1),))

    def test_switched_residues_and_local_density_by_complete_crt(self):
        checked = 0
        for d, m, sign in ((31, 62, 1), (33, 22, 1), (40, 20, 1),
                           (40, 40, -1), (120, 20, 1)):
            chi = character_values(d, two_sign=sign)
            for cofactor in range(2, 24):
                if gcd(cofactor, d*m) != 1 or chi[cofactor % d] != -1:
                    continue
                expected_classes = tuple(q for q in range(d) if chi[q] == 1
                                         and gcd(m-cofactor*q, d) == 1)
                negative_partners = {n for n in range(d) if chi[n] == -1
                                     and gcd(m-n, d) == 1}
                self.assertEqual({cofactor*q % d for q in expected_classes}, negative_partners)
                phi_d = sum(gcd(q, d) == 1 for q in range(d))
                for divisor in range(1, 20):
                    if any(a > 1 for a in trial_factors(divisor).values()):
                        continue
                    classes, density = switched_residue_density(d, m, cofactor, divisor,
                                                                two_sign=sign)
                    self.assertEqual(classes, expected_classes)
                    modulus = lcm(d, divisor)
                    units = [q for q in range(modulus) if gcd(q, modulus) == 1]
                    selected = sum(chi[q % d] == 1 and gcd(m-cofactor*q, d) == 1
                                   and (m-cofactor*q) % divisor == 0 for q in units)
                    direct_density = F(selected, len(units))/F(len(classes), phi_d)
                    self.assertEqual(density, direct_density)
                    checked += 1
        self.assertGreater(checked, 100)

    def test_absolute_range_slack_and_weighted_cofactor_shape(self):
        self.assertEqual(quintic_range_exponents(F(1, 100), F(1, 300)),
                         (F(7, 80), F(12, 25), F(19, 25)))
        for denominator in (100, 200, 1000):
            epsilon = F(1, denominator)
            for delta in (epsilon/3, epsilon/17):
                level, scale, error = quintic_range_exponents(epsilon, delta)
                self.assertGreater(level, F(2, 25))
                self.assertGreaterEqual(scale, F(12, 25))
                self.assertLessEqual(error, F(19, 25))
        # Finite rational controls of the different cofactor log weights.
        for k in (1, 3, 5):
            for qshare in (F(12, 25), F(1, 2), F(3, 4), F(99, 100)):
                for shares in (tuple((1-qshare)/k for _ in range(k)),
                               tuple((1-qshare)*F(j, k*(k+1)//2) for j in range(1, k+1))):
                    for kappa in (F(0), F(1), F(100)):
                        weight = quintic_formal_weight(kappa, shares, (qshare,))
                        self.assertLessEqual(abs(weight), 480*(1+kappa)*prod(shares))
        # Ordered five-factor shares force the two-smallest cofactor <=2/5;
        # AM-GM supplies the displayed five-factor weight bound.
        for values in ((1, 1, 1, 1, 1), (1, 2, 3, 4, 5), (1, 1, 1, 1, 30)):
            shares = tuple(F(x, sum(values)) for x in values)
            self.assertLessEqual(shares[0]+shares[1], F(2, 5))
            self.assertLessEqual(quintic_formal_weight(F(100), shares),
                                 F(24000, 27)*shares[0]*shares[1])

    def test_formal_integrals_by_independent_iterated_polynomial_integration(self):
        for dimension in range(2, 6):
            for powers in product(range(3), repeat=dimension):
                actual = simplex_polynomial_integral({powers: F(1)})
                self.assertEqual(actual, iterated_stick_integral(powers))
        mixed = {(2, 0, 1): F(-7, 3), (0, 3, 0): F(5, 2), (0, 0, 0): F(4)}
        self.assertEqual(simplex_polynomial_integral(mixed),
                         sum(c*iterated_stick_integral(powers) for powers, c in mixed.items()))
        for kappa in (F(0), F(1), F(100), F(7, 3)):
            triple, five = formal_quintic_cancellation(kappa)
            self.assertEqual((triple, five), (-kappa/12, kappa/12))
            self.assertEqual(triple+five, 0)
        # Positive triple mass is NOT zero merely because the signed
        # triple integral is negative; this prevents the wrong inference.
        self.assertGreater(quintic_formal_weight(F(100),
                           (F(9, 10), F(1, 25), F(3, 50))), 0)

    def test_exact_domains_and_no_prime_density_claims(self):
        for args in ((True, F(1, 300)), (F(0), F(0)), (F(1, 99), F(1, 300)),
                     (F(1, 100), F(1, 200)), (F(1, 100), 0.001)):
            with self.assertRaises(ValueError):
                quintic_range_exponents(*args)
        for args in ((True, 100, 20, 5), (0, 100, 20, 5), (1, 100, 101, 5),
                     (1, 100, 20, 101), (1, 100, 20, 1), (1, 100.0, 20, 5)):
            with self.assertRaises(ValueError):
                adaptive_semiprime_indices(*args)
        for args in ((31, 62, True, 1), (31, 62, 31, 1), (31, 62, 1, 1),
                     (31, 62, 3, 4), (31, 62, 3, True), (31, 2, 3, 1)):
            with self.assertRaises(ValueError):
                switched_residue_density(*args)
        for terms in ({}, {(1,): F(1)}, {(True, 0): F(1)}, {(-1, 0): F(1)},
                      {(65, 0): F(1)}, {(1, 0): 1}, {(1, 0): F(1), (0, 0, 0): F(1)}):
            with self.assertRaises(ValueError):
                simplex_polynomial_integral(terms)
        for kappa in (True, 100, 100.0, F(-1)):
            with self.assertRaises(ValueError):
                formal_quintic_cancellation(kappa)
        self.assertIn('not an actual prime count', switched_residue_density.__doc__)


if __name__ == '__main__':
    unittest.main()
