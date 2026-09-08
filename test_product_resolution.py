"""Finite-field mixing, exact density distance, and single-modulus controls."""
from fractions import Fraction
from itertools import combinations, product
import unittest

from coupled_product_model import bounded_product_profile
from product_resolution import atomic_cap_distance, field_product_pairs, jacobi_pair_floor
from redistribution import trial_prime


class ProductResolutionTests(unittest.TestCase):
    def test_nonzero_mixing_and_independent_exponent_coordinates(self):
        for ell, generator in ((7, 3), (11, 2), (13, 2)):
            m = ell-1
            supports = list(combinations(range(m), m//2))
            # All half-supports at7; a fixed bounded selection thereafter.
            if ell > 7:
                supports = supports[:6]+supports[-6:]
            profiles = [tuple(2*int(x in support) for x in range(m)) for support in supports]
            residues = [pow(generator, x, ell) for x in range(m)]
            self.assertEqual(set(residues), set(range(1, ell)))
            for i, first in enumerate(profiles):
                for second0 in (profiles[(i+1) % len(profiles)], profiles[-i-1]):
                    second = tuple((v+1)/Fraction(2) for v in second0)
                    g, pairs = field_product_pairs(first, second)
                    first_exp = tuple(first[a-1] for a in residues)
                    second_exp = tuple(second[a-1] for a in residues)
                    g_exp, pair_zero = bounded_product_profile(first_exp, second_exp)
                    self.assertEqual(g_exp, tuple(g[a] for a in residues))
                    self.assertEqual(pair_zero, pairs[0])
                    self.assertEqual(g[0], 0)
                    self.assertEqual(sum(g), m)
                    for value in pairs[1:]:
                        self.assertGreaterEqual(value, jacobi_pair_floor(ell))
                        # Exact radical inequality, not a floating endpoint.
                        residual = m*abs(value-Fraction(ell-2, m))-2
                        if residual > 0:
                            self.assertLessEqual(residual*residual, ell)

    def test_prime_threshold_zero_target_and_rational_enclosure(self):
        _, pairs5 = field_product_pairs((2, 0, 0, 2), (2, 0, 0, 2))
        self.assertEqual(pairs5[1], 0)
        quadratic7 = (2, 2, 0, 2, 0, 0)
        _, pairs7 = field_product_pairs(quadratic7, quadratic7)
        self.assertEqual(pairs7[0], 0)
        self.assertTrue(all(value > 0 for value in pairs7[1:]))
        self.assertGreater(jacobi_pair_floor(7), 0)
        self.assertEqual(jacobi_pair_floor(7, denominator=1), 0)
        for ell in (7, 11, 13, 17, 29, 101):
            bound = jacobi_pair_floor(ell)
            sqrt_upper = ell-4-(ell-1)*bound
            self.assertGreater(sqrt_upper*sqrt_upper, ell)
            self.assertGreaterEqual((sqrt_upper-Fraction(1, 16))**2, 0)
            self.assertLess((sqrt_upper-Fraction(1, 16))**2, ell)
            self.assertGreater(bound, 0)

    def test_atomic_distance_attainment_and_competing_bounded_densities(self):
        for m in (2, 4, 6):
            competitors = [v for v in product((0, 1, 2), repeat=m) if sum(v) == m]
            for k in range(1, m+1):
                atoms = (Fraction(m, k),)*k+(Fraction(0),)*(m-k)
                minimum = atomic_cap_distance(m, k)
                if 2*k < m:
                    minimizer = (Fraction(2),)*k+(Fraction(m-2*k, m-k),)*(m-k)
                else:
                    minimizer = atoms
                self.assertEqual(sum(minimizer), m)
                self.assertTrue(all(0 <= v <= 2 for v in minimizer))
                distance = sum(abs(a-b) for a, b in zip(atoms, minimizer))/m
                self.assertEqual(distance, minimum)
                for candidate in competitors:
                    self.assertGreaterEqual(sum(abs(a-b) for a, b in zip(atoms, candidate))/m,
                                            minimum)

    def test_actual_small_prime_atoms_at_sufficient_no_alias_moduli(self):
        for high, z, ell in ((26, 2, 53), (124, 4, 251), (500, 7, 1009)):
            self.assertTrue(trial_prime(ell))
            self.assertGreater(ell, 2*high)
            bound = high//(z+1)
            primes = [p for p in range(3, bound+1, 2) if trial_prime(p)]
            self.assertEqual(len(primes), len({p % ell for p in primes}))
            density = Fraction(ell-1, len(primes))
            self.assertGreater(density, 2)
            self.assertGreaterEqual(atomic_cap_distance(ell-1, len(primes)),
                                    Fraction(2*z, z+1))
        # Small moduli really can combine different integer target sums.
        self.assertNotEqual(3+7, 3+17)
        self.assertEqual((3+7) % 5, (3+17) % 5)

    def test_input_semantics(self):
        for first, second in (((), ()), ((1,), (1,)), ([1, 1], (1, 1)),
                              ((1, 1), (1, 1, 1, 1)), ((True, 1), (1, 1)),
                              ((1.0, 1), (1, 1)), ((3, -1), (1, 1)),
                              ((0, 0), (1, 1)), ((1,)*8, (1,)*8)):
            with self.assertRaises(ValueError):
                field_product_pairs(first, second)
        for ell in (True, 2, 9, 7.0):
            with self.assertRaises(ValueError):
                jacobi_pair_floor(ell)
        for denominator in (True, 0, 1.0):
            with self.assertRaises(ValueError):
                jacobi_pair_floor(7, denominator=denominator)
        for m, k in ((0, 0), (4, 0), (4, 5), (True, 1), (4, 1.0)):
            with self.assertRaises(ValueError):
                atomic_cap_distance(m, k)
        self.assertIn("DISTINCT", atomic_cap_distance.__doc__)


if __name__ == "__main__":
    unittest.main()
