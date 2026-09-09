"""New exact correlation/degeneracy checks; no infinite bound is inferred."""
from fractions import Fraction as F
from itertools import product
from math import gcd
import unittest

from major_arc_kernel import _factorization
from separate_factor_prime_kernel import complete_transform
from squarefree_correlation_kernel import (
    kl3_exact, kl3_crt_prediction, nonunit_multiplier_prediction,
    correlation_exact, correlation_crt_prediction, partition_budget,
    balanced_kernel_budget,
)


class SquarefreeCorrelationKernelTests(unittest.TestCase):
    def test_crt_normalization_at_units_and_nonunits(self):
        for q in (1, 6, 10, 15, 21, 30):
            for parameter in (0, 1, 2, q, -3):
                self.assertEqual(kl3_exact(q, parameter), kl3_crt_prediction(q, parameter))
            self.assertEqual(kl3_exact(q, 0)[0], F(1, q))
            self.assertTrue(all(v == 0 for v in kl3_exact(q, 0)[1:]))

    def test_nonunit_multiplier_reduction_including_constant_modulus(self):
        for q in (6, 15, 30, 35):
            for multiplier, argument in product((0, 1, 2, 3, q, -5), (0, 1, 2, -3)):
                self.assertEqual(kl3_exact(q, multiplier*argument),
                                 nonunit_multiplier_prediction(q, multiplier, argument))

    def test_correlation_crt_and_conjugated_zero_twist(self):
        for q in (6, 10, 15, 21):
            for second, twist in product((1, q-1), (0, 1, -2)):
                self.assertEqual(correlation_exact(q, 1, second, twist),
                                 correlation_crt_prediction(q, 1, second, twist))
        for p in (3, 5, 7):
            for second in (1, p-1):
                expected = F(p if second == 1 else 0)-1-F(1, p)
                correlation = correlation_exact(p, 1, second, 0)
                self.assertEqual(correlation[0], expected)
                self.assertTrue(all(v == 0 for v in correlation[1:]))

    def test_exact_nonunit_zero_pattern_expansion(self):
        for p in (2, 3, 5, 7):
            for h, l, parameter in product((0, 1), repeat=3):
                predicted = [p*v for v in kl3_exact(p, parameter*h*l)]
                ih, il, it = int(h == 0), int(l == 0), int(parameter == 0)
                predicted[0] += -p*(ih*il+ih*it+il*it)+(p*p+p)*ih*il*it
                self.assertEqual(tuple(predicted), complete_transform(p, parameter, h, l))

    def test_all_degenerate_partition_costs_and_target_divisors(self):
        # Five choices at each prime: main, hl, ht, lt, or all three.
        for choices in product(range(5), repeat=4):
            parts = [1]*4
            for prime, choice in zip((2, 3, 5, 7), choices):
                if choice:
                    parts[choice-1] *= prime
            for target in (0, 1, 6, 35, 210):
                budget = partition_budget(*parts, target)
                self.assertEqual(budget.normalized_mass*budget.h_divisor
                                 *budget.l_divisor*budget.k_divisor, parts[3])
                self.assertLessEqual(budget.first_fourth_power, 1)
                self.assertLessEqual(budget.short_square, 1)
                self.assertLessEqual(budget.long_fourth_power, 1)
        # The short factor can be D^-1/2; do not claim D^-3/4 for every term.
        boundary = partition_budget(1, 1, 7, 1, 7)
        self.assertEqual(boundary.short_square, F(1, 7))

    def test_bounded_exceptional_pairs_determine_two_residue_classes(self):
        for q, length, radius in product((6, 10, 15, 30), (1, 4, 8), (0, 2, 4)):
            primes = [p for p, _ in _factorization(q)]
            exceptional = {p: {(1, 0), (p-1, 1)} for p in primes}
            count = 0
            for a, b, h in product(range(1, length+1), range(1, length+1),
                                    range(-radius, radius+1)):
                if gcd(a*b, q) != 1:
                    continue
                if all((a*pow(b, -1, p) % p, h*pow(b, -1, p) % p)
                       in exceptional[p] for p in primes):
                    count += 1
            upper = 2**len(primes)*length*(length//q+1)*(2*radius//q+1)
            self.assertLessEqual(count, upper)

    def test_improved_balanced_budget_and_scope_guards(self):
        cap = F(1, 4096)
        self.assertEqual(balanced_kernel_budget(), F(23, 24))
        self.assertEqual(balanced_kernel_budget(cap, cap), F(11803, 12288))
        self.assertLess(balanced_kernel_budget(cap, cap), 1)
        for q in (0, 4, 9, 12, True):
            with self.assertRaises(ValueError):
                kl3_exact(q, 1)
        with self.assertRaises(ValueError):
            correlation_exact(15, 3, 1, 0)
        with self.assertRaises(ValueError):
            partition_budget(2, 2, 1, 1, 1)
        with self.assertRaises(ValueError):
            partition_budget(4, 1, 1, 1, 1)
        for args in ((0.0,), (F(1, 4000),), (0, True)):
            with self.assertRaises(ValueError):
                balanced_kernel_budget(*args)


if __name__ == "__main__":
    unittest.main()
