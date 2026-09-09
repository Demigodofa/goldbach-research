"""New exact fourth-moment and integer-divisor checks for the energy route."""
from fractions import Fraction as F
from itertools import product
from math import gcd
import unittest

from reciprocal_energy_kernel import (
    reciprocal_polynomial, rational_pair_solutions, reciprocal_energy,
    fourth_moment_exact, modulus_energy_prediction, energy_budget,
)


class ReciprocalEnergyKernelTests(unittest.TestCase):
    def test_rational_zero_relations_by_independent_divisor_factorization(self):
        for lower, upper in ((1, 9), (4, 12), (9, 18)):
            for a, b in product(range(lower, upper+1), repeat=2):
                direct = tuple((c, d) for c, d in product(range(lower, upper+1), repeat=2)
                               if F(1, a)+F(1, b) == F(1, c)+F(1, d))
                self.assertEqual(direct, rational_pair_solutions(a, b, lower, upper))
        # A non-diagonal rational relation must remain in the D=0 term.
        self.assertEqual(reciprocal_polynomial(3, 6, 4, 4), 0)
        self.assertIn((4, 4), rational_pair_solutions(3, 6, 1, 9))

    def test_exact_weighted_fourth_moment_with_nonunit_parameter(self):
        for q, parameter in product((4, 8, 9, 12, 15, 18), (0, 1, 6, -9)):
            for weights in ((1,)*7, (1, -1, 0, 1, -1, 1, 0)):
                moment = fourth_moment_exact(q, parameter, 3, 9, weights)
                self.assertEqual(moment[0], q*reciprocal_energy(q, parameter, 3, 9, weights))
                self.assertTrue(all(value == 0 for value in moment[1:]))
                self.assertLessEqual(reciprocal_energy(q, parameter, 3, 9, weights),
                                     reciprocal_energy(q, parameter, 3, 9))

    def test_modulus_average_decomposition_and_nonzero_divisor_triangle(self):
        for c, parameter in product((4, 8, 12), (1, 6, -12)):
            predicted = modulus_energy_prediction(c, parameter, 3, 7)
            direct = sum(reciprocal_energy(q, parameter, 3, 7) for q in range(c, 2*c+1))
            self.assertEqual(predicted.total, direct)
            self.assertLessEqual(predicted.zero_relation, (c+1)*predicted.rational_quadruples)
            self.assertLessEqual(predicted.nonzero_relation, predicted.divisor_triangle)
            self.assertGreater(predicted.nonzero_relation, 0)
        for q in (8, 9, 12, 15):
            for unit in range(1, q):
                if gcd(unit, q) == 1:
                    self.assertEqual(reciprocal_energy(q, unit*6, 3, 9),
                                     reciprocal_energy(q, 6, 3, 9))

    def test_inverse_residue_multiplicity_for_intervals_longer_than_modulus(self):
        for q, lower, upper in product((4, 9, 15), (1, 7), (16, 31)):
            counts = [0]*q
            for value in range(lower, upper+1):
                if gcd(value, q) == 1:
                    counts[pow(value, -1, q)] += 1
            self.assertLessEqual(max(counts), (upper-lower)//q+1)
        # Allowing t_q=q destroys the common nonzero-parameter divisor step.
        for q in (8, 9, 12):
            units = sum(gcd(a, q) == 1 for a in range(3, 10))
            self.assertEqual(reciprocal_energy(q, q, 3, 9), units**4)
        with self.assertRaises(ValueError):
            modulus_energy_prediction(8, 0, 3, 9)

    def test_exact_geometry_budget_coverage_and_retained_failure(self):
        critical = energy_budget(F(1, 4), F(1, 4), F(1, 2))
        self.assertEqual(critical.first_orientation, F(15, 16))
        self.assertEqual(critical.total, F(15, 16))
        capped = energy_budget(F(1, 4), F(1, 4), F(1, 2), F(1, 4096), F(1, 4096))
        self.assertEqual(capped.total, F(3843, 4096))
        endpoint = energy_budget(F(9, 32), F(9, 32), F(1, 2), F(1, 4096), F(1, 4096))
        self.assertEqual(endpoint.total, F(4067, 4096))
        # Piecewise-linear expression is coordinatewise monotone; endpoint
        # proof owns full coverage, these values guard orientations and caps.
        for b, x, y in product((F(1, 5), F(1, 4), F(9, 32)),
                               (0, F(1, 4), F(9, 32)), (F(1, 4), F(1, 2))):
            result = energy_budget(b, x, y, F(1, 4096), F(1, 4096))
            self.assertLessEqual(result.total, F(4067, 4096))
        residual = energy_budget(F(1, 2), F(1, 4), F(1, 2))
        self.assertEqual(residual.total, F(9, 8))
        self.assertLess(residual.saving, 0)
        old_balanced = energy_budget(F(1, 3), F(1, 3), F(1, 2))
        self.assertEqual(old_balanced.total, F(13, 12))
        for bad in (True, 0.25, F(3, 4)):
            with self.assertRaises(ValueError):
                energy_budget(bad, F(1, 4), F(1, 2))


if __name__ == "__main__":
    unittest.main()
