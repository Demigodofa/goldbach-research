"""New exact transform and full-box boundary checks, not prime experiments."""
from fractions import Fraction as F
from itertools import combinations, product
from math import gcd
import unittest

from hyperbola_prime_kernel import (
    kl3_fourier_exact, kl2_fourier_prediction, box_budget,
)


def vertices(inequalities):
    """Vertices of a bounded 3D rational polytope; rows mean a.x<=rhs."""
    found = set()
    for chosen in combinations(inequalities, 3):
        matrix = [list(map(F, coefficients))+[F(rhs)] for coefficients, rhs in chosen]
        for col in range(3):
            pivot = next((r for r in range(col, 3) if matrix[r][col]), None)
            if pivot is None:
                break
            matrix[col], matrix[pivot] = matrix[pivot], matrix[col]
            divisor = matrix[col][col]
            matrix[col] = [v/divisor for v in matrix[col]]
            for row in range(3):
                if row != col:
                    factor = matrix[row][col]
                    matrix[row] = [a-factor*b for a, b in zip(matrix[row], matrix[col])]
        else:
            point = tuple(row[3] for row in matrix)
            if all(sum(a*v for a, v in zip(coefficients, point)) <= rhs
                   for coefficients, rhs in inequalities):
                found.add(point)
    return found


class HyperbolaPrimeKernelTests(unittest.TestCase):
    def test_exact_linear_fourier_identity_and_zero_convention(self):
        for p in (2, 3, 5, 7, 11, 17):
            for multiplier, frequency, zero_extension in product(
                    (1, p-1), (0, 1, 2, p, -1), (False, True)):
                self.assertEqual(
                    kl3_fourier_exact(p, multiplier, frequency, zero_extension=zero_extension),
                    kl2_fourier_prediction(p, multiplier, frequency,
                                           zero_extension=zero_extension))
            self.assertEqual(kl3_fourier_exact(p, 1, 0), (0,)*(p-1))
            self.assertEqual(kl3_fourier_exact(p, 1, 0, zero_extension=True),
                             (-1,)+(0,)*(p-2))

    def test_progression_translation_and_dilation_including_T_above_p(self):
        for p, period in ((5, 2), (5, 7), (7, 10)):
            self.assertEqual(gcd(p, period), 1)
            for residue, frequency in product((0, 1, period-1), (0, 1, -2)):
                direct = [0]*p
                for j, u, v in product(range(p), range(1, p), range(1, p)):
                    phase = (u+v+2*(residue+period*j)*pow(u*v, -1, p)-frequency*j) % p
                    direct[phase] += 1
                inv_period = pow(period, -1, p)
                unshifted = list(kl2_fourier_prediction(p, 2, frequency*inv_period))+[0]
                shift = frequency*residue*inv_period % p
                shifted = [unshifted[(i-shift) % p] for i in range(p)]
                self.assertEqual(tuple(v-direct[-1] for v in direct[:-1]),
                                 tuple(v-shifted[-1] for v in shifted[:-1]))

    def test_new_cases_include_former_length_endpoint_and_small_divisor(self):
        cap = F(1, 4096)
        for b in (F(49, 100), F(1, 2)):
            budget = box_budget(b, (1-b)/2, F(1, 2))
            self.assertEqual(budget.branch, "bilinear")
            self.assertEqual(budget.off_axis_exponent, F(127, 128))
        linear = box_budget(F(1, 2), F(1, 32), F(1, 2), cap, cap, cap)
        self.assertEqual(linear.branch, "linear")
        self.assertEqual(linear.off_axis_exponent, F(25, 32)+7*cap)
        self.assertEqual(box_budget(F(13, 25), F(6, 25), F(1, 2)).branch, "schwartz")
        self.assertEqual(box_budget(F(13, 25), F(6, 25), F(3, 10)).branch, "pointwise")
        self.assertEqual(box_budget(F(1, 5), 0, 0).branch, "empty")

    def test_exact_box_vertices_and_source_hypothesis_margins(self):
        # These are exact boundary fixtures at all eight decoration corners.
        # The analytic inequalities in the proof own continuous uniformity.
        cap = F(1, 4096)
        checked = 0
        for s, j, h in product((F(0), cap), repeat=3):
            base = [((-1, 0, 0), -F(1, 5)), ((1, 0, 0), F(13, 25)),
                    ((0, -1, 0), 0), ((1, 2, 0), 1),
                    ((0, 0, -1), 0), ((0, 0, 1), F(1, 2)),
                    ((-1, -1, -1), h-1)]
            pieces = {
                "pointwise": [((0, 0, 1), F(49, 100))],
                "linear": [((0, 0, -1), -F(49, 100)),
                           ((0, 1, 0), F(1, 16)), ((1, 0, -1), s+j)],
                "bilinear": [((0, 0, -1), -F(49, 100)),
                             ((0, -1, 0), -F(1, 16)), ((1, 0, -1), s+j)],
                "schwartz": [((0, 0, -1), -F(49, 100)), ((-1, 0, 1), -s-j)],
            }
            for piece, extra in pieces.items():
                points = vertices(base+extra)
                self.assertTrue(points, piece)
                for b, x, y in points:
                    checked += 1
                    budget = box_budget(b, x, y, s, j, h)
                    self.assertGreaterEqual(y, F(6, 25)-cap)
                    self.assertLess(budget.frequency, y)
                    self.assertLess(s+j, y)
                    self.assertLess(budget.exception_exponent, F(77, 100))
                    self.assertLessEqual(budget.total_exponent, budget.uniform_ceiling)
                    self.assertLessEqual(budget.uniform_ceiling, F(4073, 4096))
                    if piece == "bilinear":
                        v, w = budget.dual_divisor, budget.grouped_frequency
                        self.assertGreaterEqual(v, F(9, 100))
                        self.assertGreaterEqual(w, F(17, 400))
                        self.assertLess(max(v, w), y)
                        self.assertTrue(y/4 < budget.source_product < 5*y/4)
                        bulk = F(3, 16)*budget.source_product-F(11, 64)*y
                        self.assertGreaterEqual(bulk, (25*y-12)/64)
                        self.assertLessEqual(2*y-(25*y-12)/64, F(127, 128))
                    if piece == "linear":
                        self.assertTrue(0 < y-x <= y)
                        self.assertLessEqual(x+F(3, 2)*y, F(13, 16))
        self.assertGreater(checked, 100)

    def test_exact_domains_and_unit_requirement(self):
        for args in ((4, 1, 1), (5, 5, 1), (5, 1, 0.0), (True, 1, 0)):
            with self.assertRaises(ValueError):
                kl3_fourier_exact(*args)
        for args in ((0.2, 0, 0), (F(1, 5), F(1, 2), F(1, 2)),
                     (F(3, 5), 0, 0), (F(1, 5), 0, F(3, 5)),
                     (F(1, 5), 0, 0, F(1, 4000))):
            with self.assertRaises(ValueError):
                box_budget(*args)


if __name__ == "__main__":
    unittest.main()
