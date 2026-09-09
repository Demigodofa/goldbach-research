"""Exact guards for grouped periods, rectangular amplification and box cover."""
from fractions import Fraction as F
from itertools import combinations, product
import unittest

from full_model_box_kernel import (
    CAP, box_route, full_box_budget, balanced_region_budget,
    grouped_region_budget, grouped_period_sums, grouped_mass_squared,
)


def intersection(equations):
    rows = [list(map(F, row)) for row in equations]
    for column in range(3):
        pivot = next((i for i in range(column, 3) if rows[i][column]), None)
        if pivot is None:
            return None
        rows[column], rows[pivot] = rows[pivot], rows[column]
        scale = rows[column][column]
        rows[column] = [v/scale for v in rows[column]]
        for i in range(3):
            if i != column:
                factor = rows[i][column]
                rows[i] = [a-factor*b for a, b in zip(rows[i], rows[column])]
    return tuple(row[3] for row in rows)


class FullModelBoxTests(unittest.TestCase):
    def test_shared_period_grouping_with_nonunit_kappa_and_reduced_modulus(self):
        eta = tuple((i*i+1) % 7-2 for i in range(1, 18))
        kappa = tuple((2*i+1) % 5-2 for i in range(1, 14))
        lam = tuple((i*i+2) % 5-1 for i in range(1, 20))
        nonzero = nonunit_nonzero = False
        for q, d, hd, ld, period, r in ((20, 1, 1, 1, 6, 4),
                (60, 3, 3, 1, 6, 4), (140, 5, 5, 5, 6, 4), (180, 4, 2, 4, 6, 9)):
            for a, b, kclass in product((0, 1, 3), (0, 1, 2), range(period)):
                direct, after, support = grouped_period_sums(
                    q, d, hd, ld, period, r, a, b, kclass, eta, kappa, lam)
                self.assertEqual(direct, after, (q, d, hd, ld, a, b, kclass))
                nonzero = nonzero or bool(direct and support)
                nonunit_nonzero = nonunit_nonzero or bool(direct and kclass == 0)
        self.assertTrue(nonzero)
        self.assertTrue(nonunit_nonzero)

    def test_grouped_norm_mass_is_bounded_but_need_not_save_a_divisor(self):
        attained_one = False
        for p, e, vm in product((2, 3, 5), range(1, 6), range(7)):
            for mass, ceiling, volume, volume_ceiling in grouped_mass_squared(p, e, vm):
                self.assertLessEqual(mass, ceiling)
                self.assertLessEqual(volume, volume_ceiling)
                attained_one = attained_one or (mass == 1 and volume < 1)
        self.assertTrue(attained_one)

    def test_rectangular_amplification_balances_the_correct_moments(self):
        for m, n, r in ((F(2, 5), F(3, 5), F(1)),
                        (F(9, 20), F(11, 20), F(31, 32)),
                        (F(1, 2), F(1, 2), F(1))):
            a, b = (n-m)/2+r/8, (m+n)/2-r/8
            length = a+m
            self.assertEqual(a+b, n)
            diagonal = 2*b+2*length+r
            bad = 3*b+2*length+r/2
            generic = 4*b+F(3, 2)*r
            self.assertEqual(diagonal, 2*(m+n)+r)
            self.assertEqual(generic, diagonal)
            self.assertLessEqual(bad, diagonal)
            second_moment = -(a+b)+F(3, 4)*(a+n)+m/2+diagonal/4
            self.assertEqual(second_moment/2, F(11, 64)*r+F(5, 16)*(m+n))

    def test_residual_rectangle_support_and_all_costs_at_every_corner(self):
        for x, y, j, h in product((F(31, 128), F(17, 64)),
                (F(49, 100), F(1, 2)), (0, CAP), (0, CAP)):
            result = grouped_region_budget(x, y, j, h)
            for key, value in result.items():
                if key.endswith('_margin'):
                    self.assertGreater(value, 0, (key, x, y, j, h))
                else:
                    self.assertLess(value, 1-CAP, (key, x, y, j, h))
                    if key.startswith('core_error'):
                        self.assertLess(value, F(19, 20))
        capped = grouped_region_budget(F(1, 4), F(1, 2), CAP, CAP)
        self.assertEqual(capped['vd_second'], 1-F(19, 8)*CAP)
        self.assertEqual(capped['core'], 1-F(81, 16)*CAP)
        self.assertEqual(capped['large_divisor'], 1-2*CAP)

    def test_balanced_region_swaps_the_grouping_and_pays_the_cutoff(self):
        for d, y, j, h in product((F(9, 32), F(15, 32)),
                (F(49, 100), F(1, 2)), (0, CAP), (0, CAP)):
            result = balanced_region_budget(d, y, j, h)
            self.assertLessEqual(max(result.values()), 1-3*CAP)
        result = balanced_region_budget(F(15, 32), F(1, 2), CAP, CAP)
        self.assertEqual(result['head'], 1-3*CAP)
        self.assertEqual(result['tail'], 1-3*CAP)

    def test_each_route_has_a_nonempty_exact_example(self):
        examples = {'empty': (F(1, 5), F(0), F(0)),
            'pointwise': (F(1, 2), F(1, 4), F(2, 5)),
            'linear': (F(13, 25), F(6, 25), F(1, 2)),
            'energy': (F(1, 4), F(1, 4), F(1, 2)),
            'balanced': (F(1, 3), F(1, 3), F(1, 2)),
            'grouped-period': (F(12, 25), F(51, 200), F(1, 2))}
        for expected, coordinates in examples.items():
            result = full_box_budget(*coordinates, CAP, CAP)
            self.assertEqual(result['route'], expected)
            self.assertLess(result['power'], result['claimed'])

    def test_exact_domain_cut_vertices_and_residual_inclusion(self):
        # Boundary/cut intersections are exact rational guard points for the
        # elementary domain partition proved in section I, not a prime scan.
        for j, h in product((0, CAP), repeat=2):
            planes = [(1, 0, 0, v) for v in (F(1, 5), F(31, 128), F(9, 32), F(15, 32), F(13, 25))]
            planes += [(0, 1, 0, v) for v in (F(0), F(31, 128), F(17, 64), F(9, 32), F(15, 32))]
            planes += [(0, 0, 1, v) for v in (F(0), F(49, 100), F(1, 2))]
            planes += [(1, 2, 0, 1), (1, 1, 1, 1-h), (0, 2, 1, 1-h), (1, -1, 0, 0)]
            points = set()
            for rows in combinations(planes, 3):
                value = intersection(rows)
                if value is None:
                    continue
                b, x, y = value
                if F(1, 5) <= b <= F(13, 25) and 0 <= x <= (1-b)/2 and 0 <= y <= F(1, 2):
                    points.add(value)
            self.assertGreater(len(points), 40)
            for b, x, y in points:
                result = full_box_budget(b, x, y, j, h)
                self.assertLess(result['power'], result['claimed'], (b, x, y, result))
                if result['route'] == 'grouped-period':
                    self.assertGreater(b, F(15, 32))
                    self.assertGreater(x, F(31, 128))
                    self.assertLess(x, F(17, 64))
                    self.assertGreater(y, F(49, 100))

    def test_rejects_out_of_domain_and_inexact_exponents(self):
        for coordinates in ((True, 0, 0), (0.3, F(1, 4), F(1, 2)),
                            (F(1, 2), F(1, 3), F(1, 2)),
                            (F(1, 3), F(1, 3), F(3, 4))):
            with self.assertRaises(ValueError):
                box_route(*coordinates)
        with self.assertRaises(ValueError):
            grouped_region_budget(F(1, 4), F(1, 2), F(1, 1024))


if __name__ == '__main__':
    unittest.main()
