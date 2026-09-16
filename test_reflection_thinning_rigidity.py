"""Exact finite identities, not numerical evidence for asymptotic rigidity."""

import unittest
from fractions import Fraction as F
from itertools import product

from complementary_divisor_correlation import central_interval
from reflection_thinning import (collision_pairs, pair_deletion_floor,
                                 quadratic_terms, reflection_thin)


class ReflectionThinningRigidityTests(unittest.TestCase):
    def setUp(self):
        self.target = 50
        self.weights = {17: F(13), 19: F(3), 23: F(7), 25: F(11),
                        27: F(2), 31: F(5), 40: F(17)}
        self.interval = central_interval(self.target)

    def correlation(self, model):
        return sum((model.get(n, 0) * model.get(50 - n, 0)
                    for n in self.interval), F(0))

    def test_exact_quadratic_polarization_keeps_cross_term(self):
        model = {17: F(14), 19: F(2), 23: F(9), 31: F(8)}
        change, distance, cross = quadratic_terms(50, self.weights, model)
        self.assertEqual(change, distance + 2 * cross)
        self.assertNotEqual(change, distance)

    def test_pair_floor_includes_midpoint_once_and_is_attained(self):
        # Delete the smaller-weight endpoint of each pair and the midpoint.
        model = {n: value for n, value in self.weights.items() if n not in (19, 27, 25)}
        self.assertEqual(self.correlation(model), 0)
        floor = pair_deletion_floor(50, self.weights)
        self.assertEqual(floor, F(9 + 4 + 121))
        self.assertEqual(quadratic_terms(50, self.weights, model)[1], floor)

    def test_all_deletion_choices_obey_exact_floor(self):
        pairs = collision_pairs(50, self.weights)
        for choices in product((0, 1), repeat=len(pairs)):
            for extra in (F(0), F(1, 2), F(3)):
                model = dict(self.weights)
                model.pop(25)
                for pair, choice in zip(pairs, choices):
                    model.pop(pair[choice])
                    model[pair[1 - choice]] += extra
                self.assertEqual(self.correlation(model), 0)
                self.assertGreaterEqual(quadratic_terms(50, self.weights, model)[1],
                                        pair_deletion_floor(50, self.weights))

    def test_thinning_distance_is_collision_energy_for_every_orientation(self):
        pairs = collision_pairs(50, self.weights)
        collision_energy = sum((self.weights[n] ** 2 + self.weights[m] ** 2
                                for n, m in pairs), F(0)) + self.weights[25] ** 2
        imbalance = sum(((self.weights[n] - self.weights[m]) ** 2
                         for n, m in pairs), F(0))
        self.assertEqual(collision_energy, self.correlation(self.weights) + imbalance)
        for signs in product((-1, 1), repeat=len(pairs)):
            model = reflection_thin(50, self.weights, signs)
            change, distance, cross = quadratic_terms(50, self.weights, model)
            self.assertEqual(distance, collision_energy)
            self.assertEqual(change - 2 * cross, self.correlation(self.weights) + imbalance)

    def test_comparable_weights_give_ordered_half_mass_floor(self):
        ratios = [min(self.weights[n], self.weights[m]) /
                  max(self.weights[n], self.weights[m])
                  for n, m in collision_pairs(50, self.weights)]
        ratio = min(ratios)
        self.assertGreaterEqual(pair_deletion_floor(50, self.weights),
                                ratio * self.correlation(self.weights) / 2)
        # The factor 1/2 is sharp for the unconstrained finite pair problem.
        self.assertEqual(pair_deletion_floor(50, {19: F(3), 31: F(3)}), F(9))

    def test_discrete_partial_summation_controls_weighted_cross_term(self):
        model = reflection_thin(50, self.weights, (1, -1))
        delta = {n: model.get(n, 0) - self.weights.get(n, 0) for n in self.interval}
        prefix, partial = F(0), {}
        for n in self.interval:
            prefix += delta[n]
            partial[n] = prefix
        weight = {n: F(n, 7) for n in self.interval}
        left = sum((weight[n] * delta[n] for n in self.interval), F(0))
        lo, hi = self.interval.start, self.interval.stop - 1
        right = weight[hi] * partial[hi] - sum(
            ((weight[n + 1] - weight[n]) * partial[n] for n in range(lo, hi)), F(0))
        self.assertEqual(left, right)
        self.assertLessEqual(abs(left), max(map(abs, partial.values())) *
                             (weight[hi] + weight[hi] - weight[lo]))

    def test_noncolliding_and_outside_weights_do_not_change_floor(self):
        self.assertEqual(pair_deletion_floor(50, {17: F(4), 40: F(10)}), 0)
        self.assertEqual(quadratic_terms(50, {40: 1}, {40: 9}), (0, 0, 0))
        self.assertEqual(pair_deletion_floor(50, {25: F(3, 2)}), F(9, 4))

    def test_invalid_rational_measures_rejected(self):
        for weights in ({19: -1}, {51: 1}, {19: 0.5}):
            with self.assertRaises(ValueError):
                pair_deletion_floor(50, weights)
            with self.assertRaises(ValueError):
                quadratic_terms(50, {}, weights)


if __name__ == "__main__":
    unittest.main()
