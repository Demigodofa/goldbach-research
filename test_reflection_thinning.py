"""Finite algebra only; the simultaneous concentration theorem is analytical."""

import unittest
from fractions import Fraction as F
from itertools import product
from math import isqrt

from complementary_divisor_correlation import central_interval, frozen_mobius_log_vector
from cutoff_normalized_remainder import cutoff_log_vectors
from reflection_thinning import collision_pairs, prefix_perturbation_form, reflection_thin
from unexceptional_vaughan_gate import mangoldt_log_vector


def log_value(vector):
    return sum(p * exponent for p, exponent in vector)


class ReflectionThinningTests(unittest.TestCase):
    def setUp(self):
        self.n = 50
        # Additive rational log-prime substitution retains prime-power support.
        self.weights = {n: F(log_value(mangoldt_log_vector(n)))
                        for n in range(1, self.n + 1)}
        self.weights = {n: v for n, v in self.weights.items() if v}
        self.signs = tuple(product((-1, 1), repeat=len(collision_pairs(self.n, self.weights))))

    def test_collisions_include_prime_power_partner_but_not_midpoint(self):
        self.assertEqual(collision_pairs(50, self.weights), ((19, 31), (23, 27)))
        self.assertGreater(self.weights[25], 0)

    def test_every_orientation_removes_pairs_preserves_noncolliding_support(self):
        changed = {19, 31, 23, 27, 25}
        for signs in self.signs:
            model = reflection_thin(self.n, self.weights, signs)
            self.assertNotIn(25, model)
            for n in range(1, self.n + 1):
                self.assertGreaterEqual(model.get(n, 0), 0)
                self.assertLessEqual(model.get(n, 0), 2 * self.weights.get(n, 0))
                if n not in changed:
                    self.assertEqual(model.get(n, 0), self.weights.get(n, 0))
            self.assertEqual(sum(model.get(n, 0) * model.get(self.n - n, 0)
                                 for n in central_interval(self.n)), 0)

    def test_expectation_retains_each_weight_except_midpoint(self):
        models = [reflection_thin(self.n, self.weights, s) for s in self.signs]
        for n in range(1, self.n + 1):
            average = sum((model.get(n, F(0)) for model in models), F(0)) / len(models)
            self.assertEqual(average, 0 if n == 25 else self.weights.get(n, 0))

    def test_all_selected_prefix_perturbations_match_sign_linear_form(self):
        for q in range(1, isqrt(self.n) + 1):
            for residue in range(q):
                for prefix in (0, 17, 25, 33, 50):
                    v, bias = prefix_perturbation_form(self.n, self.weights, q, residue, prefix)
                    for signs in self.signs:
                        model = reflection_thin(self.n, self.weights, signs)
                        observed = sum((model.get(n, 0) - self.weights.get(n, 0)
                                        for n in range(1, prefix + 1) if n % q == residue), F(0))
                        self.assertEqual(observed, sum(a * b for a, b in zip(signs, v)) + bias)

    def test_pair_variance_proxy_retains_negative_covariance(self):
        for q, residue, prefix in ((1, 0, 50), (3, 1, 50), (7, 2, 25)):
            v, _ = prefix_perturbation_form(self.n, self.weights, q, residue, prefix)
            samples = [sum(a * b for a, b in zip(signs, v)) for signs in self.signs]
            self.assertEqual(sum(samples), 0)
            self.assertEqual(sum(x * x for x in samples) / len(samples), sum(x * x for x in v))
            endpoint_bound = sum(value ** 2 for n, value in self.weights.items()
                                 if n <= prefix and n % q == residue)
            self.assertLessEqual(sum(x * x for x in v), endpoint_bound)
        v, _ = prefix_perturbation_form(50, self.weights, 3, 1, 50)
        self.assertEqual(v[0], self.weights[19] - self.weights[31])

    def test_moment_change_supported_only_on_collision_endpoints(self):
        interval = central_interval(self.n)
        collision_count = sum(self.weights.get(n, 0) > 0 and self.weights.get(50 - n, 0) > 0
                              for n in interval)
        maximum = max(self.weights.values())
        for signs in self.signs:
            model = reflection_thin(self.n, self.weights, signs)
            for k in (2, 3, 4):
                difference = abs(sum(model.get(n, 0) ** k - self.weights.get(n, 0) ** k
                                     for n in interval))
                self.assertLessEqual(difference, (2 ** k + 1) * (collision_count + 1) * maximum ** k)

    def test_reflected_residual_saturates_exact_baseline_identity(self):
        interval, h = central_interval(self.n), F(17, 3)
        short = {n: log_value(cutoff_log_vectors(n, 7)[0]) for n in interval}
        def corr(left, right):
            return sum(left.get(n, 0) * right.get(50 - n, 0) for n in interval)
        for signs in self.signs:
            model = reflection_thin(self.n, self.weights, signs)
            residual = {n: model.get(n, 0) - short[n] for n in interval}
            mixed_error, main_error = corr(short, model) - h, corr(short, short) - h
            self.assertEqual(corr(residual, residual), -h - 2 * mixed_error + main_error)

    def test_model_is_not_the_actual_full_mobius_identity(self):
        model = reflection_thin(self.n, self.weights, (1, 1))
        actual = log_value(frozen_mobius_log_vector(31, 7))
        self.assertEqual(actual, self.weights[31])
        self.assertEqual(model.get(31, 0), 0)
        self.assertNotEqual(actual, model.get(31, 0))

    def test_disjoint_windows_glue_without_restoring_pairs(self):
        targets = (50, 250)
        original = {n: F(log_value(mangoldt_log_vector(n))) for n in range(1, 251)}
        glued = dict(original)
        intervals = [set(central_interval(n)) for n in targets]
        self.assertFalse(intervals[0] & intervals[1])
        for target, interval in zip(targets, intervals):
            weights = {n: value for n, value in original.items() if n <= target}
            signs = (1,) * len(collision_pairs(target, weights))
            local = reflection_thin(target, weights, signs)
            for n in interval:
                glued[n] = local.get(n, 0)
        for target, interval in zip(targets, intervals):
            self.assertEqual(sum(glued[n] * glued[target - n] for n in interval), 0)
        for n in range(1, 251):
            self.assertLessEqual(glued[n], 2 * original[n])
            if n not in intervals[0] | intervals[1]:
                self.assertEqual(glued[n], original[n])

    def test_no_collisions_and_validation(self):
        self.assertEqual(reflection_thin(50, {17: 2, 25: 1}, ()), {17: F(2)})
        for weights, signs in (({1: -1}, ()), ({51: 1}, ()), ({1: 0.5}, ()),
                               (self.weights, (1,)), (self.weights, (True, 1))):
            with self.assertRaises(ValueError):
                reflection_thin(50, weights, signs)
        for q, r, x in ((0, 0, 20), (3, 0.0, 20), (3, 0, 51)):
            with self.assertRaises(ValueError):
                prefix_perturbation_form(50, self.weights, q, r, x)


if __name__ == "__main__":
    unittest.main()
