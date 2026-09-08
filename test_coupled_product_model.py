"""Tiny exhaustive groups and direct modular products check the model."""
from fractions import Fraction
from itertools import product as cartesian_product
import unittest

from coupled_product_model import bounded_product_profile, skew_product_profile


def all_half_sets(m):
    h = m//2
    for mask in range(1 << h):
        first = tuple((mask >> x) & 1 for x in range(h))
        yield first+tuple(1-v for v in first)


class CoupledProductModelTests(unittest.TestCase):
    def test_exhaustive_finite_bounds_stability_and_coset_equality(self):
        checked = 0
        for m in range(2, 18, 2):
            h = m//2
            for flags in all_half_sets(m):
                product, pair = skew_product_profile(flags)
                self.assertEqual(sum(product), m)
                self.assertTrue(all(0 <= weight <= 2 for weight in product))
                self.assertTrue(all(product[x]+product[x+h] == 2 for x in range(h)))
                prime_pair = Fraction(sum(4*flags[x]*flags[(x+h) % m]
                                          for x in range(m)), m)
                self.assertEqual(prime_pair, 0)
                if m % 4 == 0:
                    self.assertGreaterEqual(pair, Fraction(1, 2))
                else:
                    bias = Fraction(sum(2*flags[x]*(-1)**x for x in range(m)), m)
                    y = bias*bias
                    distance = Fraction(min(sum(flags[x] != (x % 2 == parity)
                                                for x in range(m)) for parity in (0, 1)), m)
                    self.assertEqual(distance, (1-abs(bias))/2)
                    self.assertGreaterEqual(pair, (1-y)*(1+3*y)/2)
                    self.assertGreaterEqual(pair, distance)
                    self.assertEqual(pair == 0, distance == 0)
                checked += 1
        self.assertEqual(checked, 510)

    def test_independent_product_distribution_in_actual_finite_fields(self):
        for ell, generator in ((3, 2), (5, 2), (7, 3), (11, 2), (13, 2), (17, 3)):
            m = ell-1
            residues = [pow(generator, x, ell) for x in range(m)]
            self.assertEqual(set(residues), set(range(1, ell)))
            self.assertEqual(residues[m//2], ell-1)
            for flags in all_half_sets(m):
                chosen = {residues[x] for x, flag in enumerate(flags) if flag}
                counts = {a: 0 for a in range(1, ell)}
                for a in chosen:
                    for b in chosen:
                        counts[a*b % ell] += 1
                direct_pair = Fraction(16*sum(counts[a]*counts[-a % ell]
                                              for a in range(1, ell)), m**3)
                product, pair = skew_product_profile(flags)
                self.assertEqual(pair, direct_pair)
                self.assertEqual(product, tuple(Fraction(4*counts[a], m) for a in residues))

    def test_sharp_examples_and_negative_signed_model_margin(self):
        weights, pair = skew_product_profile((1, 1, 0, 0))
        self.assertEqual(weights, (1, 2, 1, 0))
        self.assertEqual(pair, Fraction(1, 2))
        rho = Fraction(49, 100)
        self.assertEqual(-rho*pair, -Fraction(49, 200))
        weights, pair = skew_product_profile((1, 1, 1, 0, 0, 0))
        self.assertEqual(weights, (Fraction(2, 3), Fraction(4, 3), 2,
                                   Fraction(4, 3), Fraction(2, 3), 0))
        self.assertEqual(pair, Fraction(16, 27))
        for flags in ((1, 0, 1, 0, 1, 0), (0, 1, 0, 1, 0, 1)):
            _, pair = skew_product_profile(flags)
            self.assertEqual(pair, 0)

    def test_input_semantics_and_reflection_boundary(self):
        for flags in ((), (1,), (1, 0, 0), [1, 0], (True, 0), (1.0, 0),
                      (2, 0), (0, 0), (1, 1), (1, 0, 1, 0)):
            with self.assertRaises(ValueError):
                skew_product_profile(flags)
        self.assertEqual(skew_product_profile((1, 0)), ((2, 0), 0))
        self.assertIn("not prime flags", skew_product_profile.__doc__)

    def test_general_factor_profiles_without_binary_or_skew_assumptions(self):
        for m in (2, 4, 6):
            values = (0, Fraction(1, 2), 1, Fraction(3, 2), 2) if m < 6 else (0, 1, 2)
            profiles = [tuple(p) for p in cartesian_product(values, repeat=m) if sum(p) == m]
            # Different factors, including shifts and non-skew integer densities.
            for i, first in enumerate(profiles):
                for offset in (0, 1, len(profiles)//2):
                    second = profiles[(i+offset) % len(profiles)]
                    weights, pair = bounded_product_profile(first, second)
                    direct = [Fraction(0)]*m
                    for a in range(m):
                        for b in range(m):
                            direct[(a+b) % m] += Fraction(first[a]*second[b], m)
                    self.assertEqual(weights, tuple(direct))
                    self.assertEqual(sum(weights), m)
                    self.assertTrue(all(0 <= v <= 2 for v in weights))
                    if m % 4 == 0:
                        self.assertGreaterEqual(pair, Fraction(1, 2))
                        continue
                    biases = [sum((f[x]*(-1)**x for x in range(m)), Fraction(0))/m
                              for f in (first, second)]
                    x, y = (a*a for a in biases)
                    self.assertGreaterEqual(pair, 1-x*y-(1-x)*(1-y)/2)
                    if pair < Fraction(1, 2):
                        for f, a in zip((first, second), biases):
                            self.assertGreaterEqual(a*a, 1-pair)
                            sign = 1 if a > 0 else -1
                            distance = sum((abs(f[x]-(1+sign*(-1)**x))
                                            for x in range(m)), Fraction(0))/m
                            self.assertEqual(distance, 1-abs(a))
                            self.assertLessEqual(distance, pair)
                            own_pair = sum((f[x]*f[(x+m//2) % m] for x in range(m)),
                                           Fraction(0))/m
                            self.assertLessEqual(own_pair, 2*pair)

    def test_sharp_inverse_and_non_skew_asymmetric_factors(self):
        for b in (Fraction(3, 4), Fraction(9, 10), Fraction(1), -Fraction(9, 10)):
            second = (1+b, 1-b)
            weights, pair = bounded_product_profile((2, 0), second)
            self.assertEqual(weights, second)
            self.assertEqual(pair, 1-b*b)
            distance = min(sum(abs(u-v) for u, v in zip(second, coset))/2
                           for coset in ((2, 0), (0, 2)))
            self.assertEqual((1-distance)**2, 1-pair)  # Sharp square-root bound.
        first = (2, 0, 2, 0, 2, 0)
        second = (2, Fraction(1, 4), Fraction(7, 4), 0, 2, 0)
        self.assertNotEqual(second[1]+second[4], 2)
        _, pair = bounded_product_profile(first, second)
        self.assertEqual(pair, 1-Fraction(11, 12)**2)

    def test_approximate_product_error_and_missing_error_guard(self):
        first, second = (2, 0), (Fraction(19, 10), Fraction(1, 10))
        g, pair = bounded_product_profile(first, second)
        for rate in (0, Fraction(1, 100), Fraction(1, 20), Fraction(1, 2)):
            for w in (tuple((1-rate)*a+rate for a in g), tuple((1-rate)*a for a in g)):
                epsilon = sum((abs(a-b) for a, b in zip(w, g)), Fraction(0))/2
                observed = w[0]*w[1]
                self.assertLessEqual(abs(observed-pair), 4*epsilon)
                budget = observed+4*epsilon
                if budget < Fraction(1, 2):
                    for f in (first, second):
                        bias = (f[0]-f[1])/2
                        self.assertGreaterEqual(bias*bias, 1-budget)
        # Omitting epsilon would wrongly infer a coset from uniform factors.
        g, pair = bounded_product_profile((1, 1, 1, 1), (1, 1, 1, 1))
        w = (0, 0, 0, 0)
        epsilon = sum(abs(a-b) for a, b in zip(w, g))/4
        self.assertEqual(pair, 1)
        self.assertGreaterEqual(4*epsilon, Fraction(1, 2))

    def test_general_profile_input_requirements(self):
        for first, second in (([1, 1], (1, 1)), ((1,), (1,)), ((1, 1), (1, 1, 1, 1)),
                              ((True, 1), (1, 1)), ((1.0, 1), (1, 1)),
                              ((0, 0), (1, 1)), ((4, 0, 0, 0), (1, 1, 1, 1)),
                              ((-1, 3), (1, 1))):
            with self.assertRaises(ValueError):
                bounded_product_profile(first, second)
        # A density spike beyond the cap would defeat the m=4 conclusion.
        unsafe = (4, 0, 0, 0)
        unsafe_product = tuple(Fraction(sum(unsafe[y]*unsafe[(x-y) % 4]
                                            for y in range(4)), 4) for x in range(4))
        self.assertEqual(unsafe_product, unsafe)
        self.assertEqual(sum(unsafe_product[x]*unsafe_product[(x+2) % 4]
                             for x in range(4)), 0)
        self.assertIn("actual primes", bounded_product_profile.__doc__)


if __name__ == "__main__":
    unittest.main()
