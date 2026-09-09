"""New exact prime-power, periodic-lift and density-split guards."""
from fractions import Fraction as F
from itertools import product
from math import gcd, isqrt
import unittest

from composite_linear_kernel import _reduce
from major_arc_kernel import _factorization
from all_moduli_balanced_kernel import (
    complete_exact, stationary_prediction, valuation_prediction,
    periodic_exact, periodic_lift_prediction, squarefull_parts, balanced_budget,
)


class AllModuliBalancedKernelTests(unittest.TestCase):
    def test_even_and_odd_stationary_identities_including_bad_primes(self):
        for p, n in ((2, 2), (2, 3), (2, 4), (2, 5), (3, 2), (3, 3),
                     (3, 4), (5, 2), (5, 3), (7, 2), (7, 3)):
            q = p**n
            for h, l, t in ((1, 1, 1), (1, 2, -1), (p, 1, 1), (p, p, p),
                            (p, p*p, 0), (0, 0, 0)):
                with self.subTest(p=p, n=n, triple=(h, l, t)):
                    self.assertEqual(complete_exact(q, h, l, t),
                                     stationary_prediction(p, n, h, l, t))

    def test_valuation_reduction_and_distinct_modulus_one_case(self):
        for p, n in ((2, 3), (3, 3), (5, 2)):
            q = p**n
            for h, l, t in product((0, 1, p, p*p, q, -p), repeat=3):
                self.assertEqual(complete_exact(q, h, l, t),
                                 valuation_prediction(p, n, h, l, t))
            value = valuation_prediction(p, n, q, 0, -q)
            self.assertEqual(value[0], (q-q//p)**2)
            self.assertTrue(all(v == 0 for v in value[1:]))
            self.assertNotEqual(value[0], q*q)
            for h, l, t in ((1, 0, 1), (1, 1, 0), (p, 1, 1)):
                self.assertTrue(all(v == 0 for v in complete_exact(q, h, l, t)))

    def test_cubic_stationary_classes_and_quadratic_gauss_degeneracy(self):
        for p, r in ((2, 1), (2, 3), (3, 1), (3, 3), (5, 2), (7, 2)):
            modulus = p**r
            units = [x for x in range(modulus) if x % p]
            for t in units:
                roots = [z for z in units if (z**3-t) % modulus == 0]
                pairs = [(x, y) for x in units for y in units
                         if (x*x*y-t) % modulus == 0 and (x*y*y-t) % modulus == 0]
                self.assertEqual(pairs, [(z, z) for z in roots])
                self.assertLessEqual(len(roots), 1 if p == 2 else 3)
        # Exact |sum e_p(a^2+ab+b^2+A*a+B*b)|^2, no float threshold.
        for p in (2, 3, 5, 7):
            for linear_x, linear_y in product(range(p), repeat=2):
                phases = [(a*a+a*b+b*b+linear_x*a+linear_y*b) % p
                          for a, b in product(range(p), repeat=2)]
                counts = [0]*p
                for first in phases:
                    for second in phases:
                        counts[(first-second) % p] += 1
                squared = _reduce(counts, p)
                self.assertTrue(all(v == 0 for v in squared[1:]))
                if p not in (2, 3):
                    self.assertEqual(squared[0], p*p)
                elif p == 3:
                    self.assertIn(squared[0], (0, p**3))
                else:
                    self.assertLessEqual(squared[0], 16)

    def test_double_period_lift_and_common_gcd_with_shared_factors(self):
        for q, period in ((4, 2), (8, 4), (9, 3), (12, 4), (18, 6), (15, 2)):
            weight = tuple(tuple(((r+2*s+r*s) % 3)-1 for s in range(period))
                           for r in range(period))
            for h, l, t in ((0, 0, 0), (1, -2, 3), (2, 4, 6), (q, -q, q)):
                self.assertEqual(periodic_exact(q, period, t, h, l, weight),
                                 periodic_lift_prediction(q, period, t, h, l, weight))
                for a, b in product(range(period), repeat=2):
                    if (h+q*a) % period or (l+q*b) % period:
                        continue
                    reduced_gcd = gcd(q, (h+q*a)//period, (l+q*b)//period, t)
                    self.assertEqual(gcd(q, h, l, t) % reduced_gcd, 0)

    def test_full_squarefull_part_and_small_core_decomposition(self):
        self.assertEqual(squarefull_parts(2**5*3), (32, 3, 2, 2))
        for q in range(1, 1601):
            u, v, a, b = squarefull_parts(q)
            self.assertEqual(q, u*v)
            self.assertEqual(gcd(u, v), 1)
            self.assertEqual(u, a*a*b**3)
            self.assertTrue(all(e >= 2 for _, e in _factorization(u)))
            self.assertTrue(all(e == 1 for _, e in _factorization(v*b)))
            for period in (1, 2, 6, 12):
                radical = 1
                for prime, _ in _factorization(period):
                    radical *= prime
                small = u*gcd(v, radical)
                core = q//small
                self.assertEqual(gcd(core, small*period), 1)
                self.assertTrue(all(e == 1 for _, e in _factorization(core)))
                self.assertLessEqual(small, u*period)
        # Independent a^2*b^3 enumeration and exact divisibility-count upper bound.
        limit = 1600
        generated = {a*a*b**3 for b in range(1, 12)
                     if all(e == 1 for _, e in _factorization(b))
                     for a in range(1, isqrt(limit//(b**3))+1)}
        factored = {q for q in range(1, limit+1)
                    if all(e >= 2 for _, e in _factorization(q))}
        self.assertEqual(generated, factored)
        for threshold in (4, 16, 64, 256):
            count = sum(squarefull_parts(q)[0] > threshold for q in range(800, 1601))
            upper = sum(limit//u for u in generated if u > threshold)
            self.assertLessEqual(count, upper)

    def test_exact_capped_budget_and_input_boundary(self):
        budget = balanced_budget(F(1, 4096), F(1, 4096))
        self.assertEqual(budget.small_part, F(12115, 12288))
        self.assertEqual(budget.large_part, F(4085, 4096))
        self.assertEqual(budget.axes, F(2, 3)+F(2, 4096))
        self.assertEqual(budget.total, F(4085, 4096))
        self.assertEqual(budget.saving, F(11, 4096))
        for j, h in ((0, 0), (F(1, 4096), 0), (0, F(1, 4096))):
            self.assertLess(balanced_budget(j, h).total, 1)
        for bad in (0.0, True, -1, F(1, 4095)):
            with self.assertRaises(ValueError):
                balanced_budget(bad)
        with self.assertRaises(ValueError):
            stationary_prediction(4, 2, 1, 1, 1)
        with self.assertRaises(ValueError):
            stationary_prediction(3, 1, 1, 1, 1)


if __name__ == "__main__":
    unittest.main()
