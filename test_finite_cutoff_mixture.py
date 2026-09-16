"""Exact finite algebra for the multiscale obstruction, not asymptotic tests."""

import unittest
from fractions import Fraction as F
from math import lcm

from complementary_divisor_correlation import (
    central_interval, complementary_expansion, divisor_value,
)
from cutoff_normalized_remainder import (
    common_divisor_density_blocks, cutoff_log_vectors,
    cutoff_mixture_norm_parts, selberg_coordinates,
)
from major_arc_kernel import _factorization, _mobius_phi
from unexceptional_vaughan_gate import mangoldt_log_vector


class FiniteCutoffMixtureTests(unittest.TestCase):
    def test_rectangular_common_divisor_grouping(self):
        left = {1: 2, 2: -3, 3: F(-1, 2), 6: 1}
        right = {1: 3, 2: -2, 5: -1, 10: 2, 15: F(2, 3)}
        for n in (30, 50, 210):
            actual = common_divisor_density_blocks(n, left, right)
            self.assertEqual(sum(actual.values(), F(0)),
                             complementary_expansion(n, left, right).density)
            self.assertEqual(actual, common_divisor_density_blocks(n, right, left))
        self.assertEqual(common_divisor_density_blocks(30, left, {}), {})
        with self.assertRaises(ValueError):
            common_divisor_density_blocks(30, left, {4: 1})

    def test_selberg_bilinear_diagonalization_including_nonsquarefree(self):
        left = {1: 2, 2: -1, 4: F(3, 2), 6: -2}
        right = {1: -1, 3: 2, 9: F(-1, 3)}
        wl, wr = selberg_coordinates(left), selberg_coordinates(right)
        diagonal = sum((_mobius_phi(q)[1] * value * wr.get(q, 0)
                        for q, value in wl.items()), F(0))
        density = sum((F(ca * cb, lcm(a, b)) for a, ca in left.items()
                       for b, cb in right.items()), F(0))
        self.assertEqual(diagonal, density)
        period = lcm(*left, *right)
        average = sum((divisor_value(n, left) * divisor_value(n, right)
                       for n in range(1, period + 1)), F(0)) / period
        self.assertEqual(average, density)

    def test_selberg_tail_is_a_positive_norm_not_a_signed_tail(self):
        coordinates = selberg_coordinates({1: 2, 2: -3, 3: 1, 6: 2})
        small = sum((_mobius_phi(q)[1] * v * v
                     for q, v in coordinates.items() if q <= 2), F(0))
        tail = sum((_mobius_phi(q)[1] * v * v
                    for q, v in coordinates.items() if q > 2), F(0))
        self.assertGreater(tail, 0)
        self.assertEqual(small + tail, sum((_mobius_phi(q)[1] * v * v
                                          for q, v in coordinates.items()), F(0)))

    def test_quadratic_norm_equals_completed_squares(self):
        exponents = (F(1, 8), F(1, 4), F(2, 5))
        for weights in ((0, 0, 1), (1, 0, 0), (2, -3, 2),
                        (F(1, 2), 0, F(1, 2)), (0, 0, 0), (1, 2, -1)):
            floor, penalties = cutoff_mixture_norm_parts(exponents, weights)
            direct = (1 - 2 * sum(c * t for c, t in zip(weights, exponents))
                      + sum(weights[i] * weights[j] * min(exponents[i], exponents[j])
                            for i in range(3) for j in range(3)))
            self.assertEqual(direct, floor + sum(penalties))
            self.assertGreaterEqual(direct, 1 - exponents[-1])

    def test_minimum_requires_largest_cutoff_alone(self):
        exponents = (F(1, 8), F(1, 4), F(2, 5))
        floor, penalties = cutoff_mixture_norm_parts(exponents, (0, 0, 1))
        self.assertEqual(floor, F(3, 5))
        self.assertEqual(penalties, (0, 0, 0))
        for weights in ((1, 0, 0), (0, 1, 0), (-1, 0, 2), (0, 0, 2)):
            self.assertGreater(sum(cutoff_mixture_norm_parts(exponents, weights)[1]), 0)
        self.assertEqual(cutoff_mixture_norm_parts((F(1, 3),), (1,)),
                         (F(2, 3), (F(0),)))

    def test_suffix_summation_by_parts_correction(self):
        # Regression for a helper's incorrect telescoping to theta_k*c_k.
        t = (F(1, 4), F(2, 5))
        c = (1, 0)
        suffix = (1, 0)
        gaps = (t[0], t[1] - t[0])
        first_moment = sum(gap * s for gap, s in zip(gaps, suffix))
        self.assertEqual(first_moment, sum(a * b for a, b in zip(t, c)))
        self.assertNotEqual(first_moment, t[-1] * c[-1])
        self.assertEqual(cutoff_mixture_norm_parts(t, c),
                         (F(3, 5), (F(0), F(3, 20))))

    def test_cross_residual_identity_and_nonunit_signal_shift(self):
        # Rational log-prime substitution checks the identities, not log estimates.
        def value(vector):
            return sum(p * power for p, power in vector)

        n, cutoffs = 50, (3, 7, 11)
        interval = central_interval(n)
        lam = {x: value(mangoldt_log_vector(x)) for x in interval}
        prime = {x: x if _factorization(x) == ((x, 1),) else 0 for x in interval}
        shorts = [{x: value(cutoff_log_vectors(x, r)[0]) for x in interval}
                  for r in cutoffs]

        def corr(left, right):
            return sum(left[x] * right[n - x] for x in interval)

        h = F(17, 3)  # Arbitrary independent baseline; no asymptotic substitution.
        delta = corr(prime, prime) - h
        powers = corr(lam, lam) - corr(prime, prime)
        self.assertGreater(powers, 0)
        e = [corr(a, lam) - h for a in shorts]
        f = [[corr(a, b) - h for b in shorts] for a in shorts]
        for i, ai in enumerate(shorts):
            for j, aj in enumerate(shorts):
                di = {x: lam[x] - ai[x] for x in interval}
                dj = {x: lam[x] - aj[x] for x in interval}
                self.assertEqual(corr(di, dj), delta + powers - e[i] - e[j] + f[i][j])
        for weights in ((2, -3, 2), (0, 0, 0), (1, 1, 0)):
            s = sum(weights)
            residual = {x: lam[x] - sum(c * a[x] for c, a in zip(weights, shorts))
                        for x in interval}
            error = (-2 * sum(c * error for c, error in zip(weights, e))
                     + sum(weights[i] * weights[j] * f[i][j]
                           for i in range(3) for j in range(3)))
            self.assertEqual(corr(residual, residual),
                             delta + (s - 1) ** 2 * h + powers + error)

    def test_input_validation(self):
        for exponents, weights in (((), ()), ((F(1, 4),), ()),
                                   ((F(1, 2),), (1,)), ((0,), (1,)),
                                   ((F(1, 3), F(1, 4)), (1, 0)),
                                   ((F(1, 4), F(1, 4)), (1, 0)),
                                   ((0.25,), (1,)), ((F(1, 4),), (True,))):
            with self.assertRaises(ValueError):
                cutoff_mixture_norm_parts(exponents, weights)
        with self.assertRaises(ValueError):
            selberg_coordinates({0: 1})
        with self.assertRaises(ValueError):
            selberg_coordinates({2: 0.5})
        self.assertEqual(selberg_coordinates({}), {})


if __name__ == "__main__":
    unittest.main()
