"""Rational factor-share controls; no numerical prime-density assertion."""
from fractions import Fraction as F
from itertools import combinations
import unittest

from cubic_character_minorant import negative_cubic_coefficients, negative_semiprime_sign
from log_weight_barrier import (balanced_kernel_enclosure, safe_subtraction_coefficients,
                                semiprime_kernel)


def evaluate(coefficients, x):
    result = F(0)
    for coefficient in reversed(coefficients):
        result = result*x+coefficient
    return result


def integrate(coefficients, lower, upper):
    return sum((coefficient*(upper**(degree+1)-lower**(degree+1))/(degree+1)
                for degree, coefficient in enumerate(coefficients)), F(0))


class LogWeightBarrierTests(unittest.TestCase):
    def test_complete_polynomial_identity_reflection_and_enclosure(self):
        cases = [(0, *([0]*(degree-1)), 1) for degree in range(1, 13)]
        cases += [(0, 10, 0, -9), (0, -3, 7, -3), (0, 21, 0, -30, 0, 10),
                  (0, F(3, 2), -1, F(1, 2))]
        for coefficients in cases:
            kernel = semiprime_kernel(coefficients)
            self.assertEqual(evaluate(kernel, F(1, 2)), 1)
            self.assertEqual(evaluate(kernel, F(0)), 2)
            self.assertEqual(evaluate(kernel, F(1)), 0)
            for b in (F(0), F(1, 7), F(1, 3), F(1, 2)):
                self.assertEqual(integrate(kernel, b, 1-b), 1-2*b)
            for numerator in range(38):
                a = F(numerator, 37)
                value = evaluate(kernel, a)
                self.assertEqual(value, 1+evaluate(coefficients, 1-a)-evaluate(coefficients, a))
                self.assertEqual(value+evaluate(kernel, 1-a), 2)
                lower, upper = balanced_kernel_enclosure(coefficients, a)
                self.assertLessEqual(lower, value)
                self.assertLessEqual(value, upper)
                if value <= 0 and a != F(1, 2):
                    norm = sum(j*abs(c) for j, c in enumerate(coefficients))
                    self.assertGreaterEqual(norm, 1/abs(1-2*a))

    def test_cubic_kernel_matches_previously_checked_exact_numerator(self):
        coefficients = safe_subtraction_coefficients((0, 9))
        self.assertEqual(coefficients, (0, 10, 0, -9))
        self.assertEqual(semiprime_kernel(coefficients), (2, 7, -27, 18))
        self.assertEqual(integrate(semiprime_kernel(coefficients), F(0), F(2, 3)), F(10, 9))
        self.assertEqual(integrate(semiprime_kernel(coefficients), F(2, 3), F(1)), F(-1, 9))
        _, cubic_numerator = negative_cubic_coefficients(11*19, 31)
        for numerator in range(1, 30):
            a = F(numerator, 30)
            formal_logs = {11: 1-a, 19: a}
            direct = sum(coefficient*formal_logs[p]*formal_logs[q]*formal_logs[r]
                         for (p, q, r), coefficient in cubic_numerator)
            self.assertEqual(direct, evaluate(semiprime_kernel(coefficients), a))
        # A genuine finite factor/sign guard; the rational grid above is formal.
        self.assertEqual(negative_semiprime_sign(43*5, 31), (43, 5, 1))

    def test_every_safe_penalty_increases_the_smaller_positive_factor_weight(self):
        penalties = [(), (F(5, 3),), (0, 9), (1, 2, 3, 4, 5),
                     (*([0]*62), F(7, 4))]
        for values in penalties:
            coefficients = safe_subtraction_coefficients(values)
            kernel = semiprime_kernel(coefficients)
            self.assertEqual(sum(coefficients), 1)
            for numerator in range(1, 25):
                a = F(numerator, 48)
                value, original = evaluate(kernel, a), 2*(1-a)
                self.assertGreaterEqual(value, original)
                if len(values) <= 1 or not any(values[1:]) or a == F(1, 2):
                    self.assertEqual(value, original)
                else:
                    self.assertGreater(value, original)
        # Rejecting negative penalties matters: the opposite sign can reduce
        # this side, but leaves the safe nonnegative-subtraction family.
        self.assertLess(evaluate(semiprime_kernel((0, -8, 0, 9)), F(1, 4)), F(3, 2))

    def test_higher_mixed_finite_differences_are_nonnegative(self):
        for degree in range(1, 9):
            for count in range(1, 9):
                steps = tuple(F(i+1, 7) for i in range(count))
                for base in (F(0), F(2, 3)):
                    total = F(0)
                    for size in range(count+1):
                        for removed in combinations(range(count), size):
                            argument = base+sum(steps)-sum(steps[i] for i in removed)
                            total += (-1)**size*argument**degree
                    self.assertGreaterEqual(total, 0)
                    if count > degree:
                        self.assertEqual(total, 0)

    def test_exact_domains_and_balanced_half_value(self):
        invalid = ([0, 1], (1,), (1, 0), (0, 2), (False, 1), (0, 1.0),
                   (0, *([0]*64), 1))
        for coefficients in invalid:
            for function, args in ((semiprime_kernel, (coefficients,)),
                                   (balanced_kernel_enclosure, (coefficients, F(1, 2)))):
                with self.assertRaises(ValueError):
                    function(*args)
        for share in (True, 0.5, -1, 2):
            with self.assertRaises(ValueError):
                balanced_kernel_enclosure((0, 1), share)
        self.assertEqual(balanced_kernel_enclosure((0, 10, 0, -9), F(1, 2)), (1, 1))
        self.assertEqual(balanced_kernel_enclosure((0, 10, 0, -9), F(75, 148)),
                         (F(1, 2), F(3, 2)))
        for penalties in ([1], (True,), (1.0,), (-1,), (0,)*64):
            with self.assertRaises(ValueError):
                safe_subtraction_coefficients(penalties)


if __name__ == '__main__':
    unittest.main()
