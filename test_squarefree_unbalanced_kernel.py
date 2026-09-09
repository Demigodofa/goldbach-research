"""New exact guards for divisor shifts, normality, partitions and full costs."""
from fractions import Fraction as F
from itertools import product
from math import gcd
import unittest

from major_arc_kernel import _factorization
from reciprocal_energy_kernel import _divisors
from two_prime_kl3_kernel import toy_crt_values
from squarefree_unbalanced_kernel import (
    affine_normality, shift_correlation_exact, shift_correlation_crt,
    divisor_shift_identity, factorization_route, natural_bilinear_direct,
    natural_bilinear_partition, unbalanced_squarefree_budget, squarefull_split_budget,
)


def fixture(p, seed=1):
    return ((0, 0),)+tuple((1+(i*seed+1) % 3, (i*i+seed) % 5-2)
                            for i in range(1, p))


class SquarefreeUnbalancedKernelTests(unittest.TestCase):
    def test_prime_affine_maps_have_explicit_rank_three_normality(self):
        for p in (3, 5, 7, 11, 13):
            for u, v, shift in product(range(1, p), repeat=3):
                if (u-v) % p and (u+v) % p:
                    balances = affine_normality(p, u, v, shift)
                    self.assertTrue(all(abs(value) == 1 for value in balances))
                    self.assertTrue(any(value % 3 for value in balances))
            # The two genuinely diagonal families cannot be called generic.
            self.assertFalse(any(value % 3 for value in affine_normality(p, 1, 1, 1)))
            self.assertFalse(any(value % 3 for value in affine_normality(p, 1, 2, 0)))

    def test_four_factor_crt_with_nonunit_shifts_and_frequency_twists(self):
        for primes in ((3, 5), (3, 7), (2, 3, 5)):
            local = {p: fixture(p, i+1) for i, p in enumerate(primes)}
            values = toy_crt_values(local)
            for u, v, shift, twist in ((1, 2, 1, 2), (1, 1, 3, 0),
                                       (2, 4, 5, -1), (1, -1, 0, 1)):
                self.assertEqual(shift_correlation_exact(values, u, v, shift, twist),
                                 shift_correlation_crt(local, u, v, shift, twist))

    def test_divisor_shift_averaging_overlap_energy_and_cauchy(self):
        for r, s, length, shifts in ((3, 5, 17, 2), (5, 7, 43, 4), (2, 15, 19, 4)):
            first, second = fixture(r), fixture(s, 2)
            result = divisor_shift_identity(first, second, length, shifts)
            self.assertEqual(result['averaged'], tuple(shifts*x for x in result['original']))
            self.assertEqual(result['energy'], result['expanded'])
            self.assertGreater(result['energy'], 0)
            self.assertLessEqual(result['cauchy_left'], result['cauchy_right'])

    def test_weighted_signed_congruence_graph_bound_for_all_divisors(self):
        for s, length in ((15, 19), (30, 31), (105, 43)):
            weights = {m: (m*m+1) % 5 for m in range(1, length+1) if gcd(m, s) == 1}
            norm = sum(w*w for w in weights.values())
            for d in _divisors(s):
                edges = [(a, b) for a, b in product(weights, repeat=2) if (a*a-b*b) % d == 0]
                row_max = max(sum(a == m for a, _ in edges) for m in weights)
                row_bound = 2**len(_factorization(d))*(length//d+1)
                self.assertLessEqual(row_max, row_bound)
                quadratic = sum(weights[a]*weights[b] for a, b in edges)
                self.assertLessEqual(quadratic, row_max*norm)
            # d=0 in the difference is included, not put into tau(0).
            self.assertEqual(gcd(s, 7*7-7*7), s)

    def test_integer_factorization_classification_including_small_cofactor_cores(self):
        values = [q for q in range(2, 1200) if all(e == 1 for _, e in _factorization(q))]
        values += [101*103, 2*65537*65539, 2*4294967311]
        core_sizes = set()
        for q in values:
            kind, first, second = factorization_route(q)
            if kind == 'divisor':
                self.assertEqual(first*second, q)
                self.assertGreaterEqual(first**32, q)
                self.assertLessEqual(first**5, q*q)
            else:
                self.assertLess(first**32, q)
                self.assertIn(len(second), (1, 2))
                restored = first
                for p in second:
                    self.assertGreater(p**5, q*q)
                    restored *= p
                self.assertEqual(restored, q)
                if first > 1:
                    core_sizes.add(len(second))
        self.assertEqual(core_sizes, {1, 2})
        for q in (1, 12, 25):
            with self.assertRaises(ValueError):
                factorization_route(q)

    def test_natural_extension_partition_including_shared_nonunit_factors(self):
        alpha, beta = (1, -1, 0, 2, -2, 1), (2, 0, -1, 1, -2, 1, 3)
        for q, c in product((6, 15, 30, 35), (0, 1, 6, 15, -10)):
            self.assertEqual(natural_bilinear_direct(q, c, alpha, beta),
                             natural_bilinear_partition(q, c, alpha, beta))

    def test_exact_factor_core_natural_and_period_budget_margins(self):
        for x, rho in product((F(1, 2), F(65, 128)), (F(1, 32), F(2, 5))):
            savings = ((x-rho)/4, (2*x-1+rho)/8, 3*x/4-(1-rho)/4)
            self.assertGreaterEqual(min(savings), F(1, 256))
        self.assertLess(F(99, 256), F(2, 5))
        self.assertLess(F(65, 128), F(31, 32)*F(5, 8))
        self.assertGreater(F(1, 64)-F(21, 64)*F(1, 32), F(1, 256))
        self.assertLess(F(1, 2)+F(1, 256), (1-F(1, 256))*(F(1, 2)+F(1, 128)))
        cap = F(1, 4096)
        result = unbalanced_squarefree_budget(cap, cap, cap)
        self.assertEqual(result['off_axis'], 1-F(511, 1048576))
        self.assertEqual(result['padded_x'], F(1025, 2047))
        self.assertLess(result['padded_x'], result['small_d_ceiling'])
        self.assertLess(result['off_axis'], result['claimed'])
        self.assertLess(result['axes'], result['claimed'])
        for j, h, g in product((0, cap), repeat=3):
            if g <= j:
                self.assertLess(unbalanced_squarefree_budget(j, h, g)['off_axis'], result['claimed'])
        for bad in (True, 0.0001, F(1, 1024)):
            with self.assertRaises(ValueError):
                unbalanced_squarefree_budget(bad)

    def test_density_costed_squarefull_split_still_fails_at_full_caps(self):
        result = squarefull_split_budget()
        self.assertEqual(result['cutoff'], F(199, 233472))
        self.assertLess(result['cutoff'], F(1, 1024))
        self.assertEqual(result['best'], F(467315, 466944))
        self.assertGreater(result['best'], 1)
        self.assertEqual(result['head_saving_threshold'], F(73, 225280))
        self.assertEqual(result['tail_saving_threshold'], F(5, 2048))
        self.assertLess(result['head_saving_threshold'], result['tail_saving_threshold'])
        self.assertLess(result['support_at_upper_cutoff'], result['support_ceiling'])


if __name__ == '__main__':
    unittest.main()
