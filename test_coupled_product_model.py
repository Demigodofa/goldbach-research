"""Tiny exhaustive groups and direct modular products check the model."""
from fractions import Fraction
import unittest

from coupled_product_model import skew_product_profile


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


if __name__ == "__main__":
    unittest.main()
