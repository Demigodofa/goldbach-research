"""Exact new algebra and budget guards; no prime-coverage scan."""
from fractions import Fraction as F
from itertools import product
from math import gcd
import unittest

from all_moduli_balanced_kernel import complete_exact, squarefull_parts
from all_moduli_unbalanced_kernel import (
    cube_roots_square, square_kl3_prediction, square_correlation_raw,
    square_stationary_raw, recursion_prediction, local_mass_terms,
    repeated_factor_route, all_integer_unbalanced_budget,
)
from composite_linear_kernel import _reduce
from major_arc_kernel import _factorization
from reciprocal_energy_kernel import _divisors


class AllModuliUnbalancedTests(unittest.TestCase):
    def test_prime_square_root_formula_against_original_double_sum(self):
        for p in (5, 7):
            q = p*p
            for z in range(q):
                expected = tuple(F(v, q) for v in complete_exact(q, 1, 1, z))
                self.assertEqual(square_kl3_prediction(p, z), expected)
        for p in (2, 3, 9):
            with self.assertRaises(ValueError):
                cube_roots_square(p)

    def test_four_factor_tangent_sum_including_twists_and_exceptions(self):
        for p, u, v in ((5, 1, 2), (7, 1, 6), (13, 1, 5), (7, 1, 2),
                        (5, 1, 1), (7, 1, 8), (5, 5, 1)):
            for shift, twist in ((1, 0), (2, 1), (1, p), (0, 0), (p, 2)):
                direct = square_correlation_raw(p, u, v, shift, twist)
                stationary = square_stationary_raw(p, u, v, shift, twist)
                self.assertEqual(_reduce(direct, p*p), _reduce(stationary, p*p),
                                 (p, u, v, shift, twist))

    def test_elimination_polynomial_has_exactly_the_stationary_bases(self):
        nonempty = False
        for p in (5, 7, 13):
            q = p*p
            roots = cube_roots_square(p)
            for v in range(2, p):
                for lam, mu in product(roots[v], repeat=2):
                    aa, bb = (1-lam) % p, (1-mu) % p
                    for b, c in product((1, 2), (0, 1, 2)):
                        actual = {(x, y) for x, y in product(range(1, p), repeat=2)
                                  if (y**3-x**3-b) % p == 0
                                  and (aa*x*x-bb*y*y+c*x*x*y*y) % p == 0}
                        def poly(x):
                            return ((bb-c*x*x)**3*(x**3+b)**2-aa**3*x**6) % p
                        self.assertNotEqual(poly(0), 0)
                        xs = {x for x in range(p) if poly(x) == 0}
                        predicted = {(x, (x**3+b)*(bb-c*x*x)*pow(aa*x*x, -1, p) % p)
                                     for x in xs}
                        self.assertEqual(actual, predicted)
                        self.assertLessEqual(len(actual), 12)
                        nonempty = nonempty or bool(actual)
        self.assertTrue(nonempty)

    def test_both_exceptional_families_exceed_the_generic_constant(self):
        p = 113
        for u, v, shift, expected in ((1, 1, 1, p*(p-2)), (1, 2, 0, p*(p-1))):
            counts = square_correlation_raw(p, u, v, shift, 0)
            self.assertEqual(counts[0], expected)
            self.assertFalse(any(counts[1:]))
            self.assertGreater(expected, 108*p)

    def test_prime_power_recursion_all_zero_patterns_and_small_primes(self):
        for p, e in ((2, 2), (2, 3), (3, 2), (3, 3), (5, 2), (5, 3)):
            q = p**e
            for h, l, t in ((1, 2, 3), (0, 1, p), (p, p, 1),
                            (p, p, p), (0, 0, p), (0, 0, 0),
                            (p*p, p*p, p*p)):
                expected = tuple(F(v, q) for v in complete_exact(q, h, l, t))
                self.assertEqual(recursion_prediction(p, e, h, l, t), expected,
                                 (p, e, h, l, t))

    def test_every_local_degeneracy_term_pays_volume_and_squared_norm_mass(self):
        for p, e in product((2, 3, 5, 7), range(1, 7)):
            for d, coefficient, hd, ld, td, allowance in local_mass_terms(p, e):
                for vm in range(e+2):
                    kd = td//gcd(td, p**vm)
                    volume = F(coefficient, hd*ld*kd)
                    norm_squared = F(coefficient**2, hd*hd*ld*kd)
                    self.assertLessEqual(volume, allowance/d)
                    self.assertLessEqual(norm_squared, allowance**2/d)

    def test_repeated_factor_classification_and_widened_transition_window(self):
        found_repeated = False
        for q in range(2, 2500):
            u, _, _, _ = squarefull_parts(q)
            if u**5 > q*q:
                continue
            kind, r, remaining = repeated_factor_route(q)
            found_repeated = found_repeated or u > 1
            if kind == 'divisor':
                self.assertEqual(r*remaining, q)
                self.assertEqual(gcd(r, remaining), 1)
                self.assertTrue(all(e == 1 for _, e in _factorization(remaining)))
                self.assertGreaterEqual(r**32, q)
                self.assertLessEqual(r**160, q**69)
            else:
                self.assertLess(r**32, q)
                self.assertIn(len(remaining), (1, 2))
                restored = r
                for p in remaining:
                    self.assertGreater(p**5, q*q)
                    restored *= p
                self.assertEqual(restored, q)
        self.assertTrue(found_repeated)
        # A full part .03 and simple primes .371,.599 defeat the old .4
        # window, but the new allowed divisor exponent .401 handles them.
        rho = F(3, 100)+F(371, 1000)
        self.assertGreater(rho, F(2, 5))
        self.assertLess(rho, F(69, 160))
        for q in (1, True, 25):
            with self.assertRaises(ValueError):
                repeated_factor_route(q)

    def test_period_lift_keeps_original_frequency_divisibility(self):
        witnessed_shared = False
        for q, period in product((12, 18, 25, 36), (2, 3, 4, 5)):
            for a, h in product(range(period), range(-2*q, 2*q+1)):
                if (h+q*a) % period:
                    continue
                shifted = (h+q*a)//period
                for d in _divisors(q):
                    if shifted % d == 0:
                        self.assertEqual(h % d, 0)
                        witnessed_shared = witnessed_shared or gcd(d, period) > 1
        self.assertTrue(witnessed_shared)

    def test_all_integer_exponents_and_support_margins(self):
        for x, rho in product((F(1, 2), F(65, 128)), (F(1, 32), F(69, 160))):
            savings = ((x-rho)/4, (2*x-1+rho)/8, 3*x/4-(1-rho)/4)
            self.assertGreaterEqual(min(savings), F(1, 256))
            self.assertLess(rho, x)
            self.assertLess(x, 1-rho)
        cap = F(1, 4096)
        for j, h in product((0, cap), repeat=2):
            result = all_integer_unbalanced_budget(j, h)
            for key in ('good', 'bad', 'axes'):
                self.assertLess(result[key], result['claimed'])
            self.assertLess(result['support'], result['support_ceiling'])
            self.assertLess(result['fullpart'], result['fullpart_ceiling'])
        self.assertEqual(all_integer_unbalanced_budget(cap, cap)['good'], 1-F(3, 4096))
        self.assertEqual(1-F(39, 200), F(161, 200))
        for bad in (True, 0.0001, F(1, 1024)):
            with self.assertRaises(ValueError):
                all_integer_unbalanced_budget(bad)


if __name__ == '__main__':
    unittest.main()
