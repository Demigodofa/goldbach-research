"""Rational factor-share controls; no numerical prime-density assertion."""
from fractions import Fraction as F
from itertools import combinations
import unittest

from cubic_character_minorant import negative_cubic_coefficients, negative_semiprime_sign
from log_weight_barrier import (balanced_kernel_enclosure, safe_subtraction_coefficients,
                                semiprime_kernel, negative_triple_kernel,
                                safe_subtraction_tradeoff, type_i_endpoint_coefficient)


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

    def test_endpoint_cost_and_sharp_cubic_quartic_efficiency(self):
        for a in (F(51, 100), F(3, 5), F(3, 4), F(9, 10), F(99, 100)):
            b, v = 1-a, a*(1-a)
            divided = [F(0)]+[(a**j-b**j)/(a-b) for j in range(1, 65)]
            self.assertEqual(divided[1:3], [1, 1])
            for degree in range(3, 65):
                self.assertEqual(divided[degree], divided[degree-1]-v*divided[degree-2])
                self.assertEqual(1-divided[degree], v*sum(divided[1:degree-1]))
                self.assertLessEqual(1-divided[degree], (degree-2)*v)
                if degree >= 5:
                    self.assertLess(1-divided[degree], (degree-2)*v)
            for budget in (F(0), F(1), F(2), F(9), F(100)):
                cubic = safe_subtraction_coefficients((0, budget))
                quartic = safe_subtraction_coefficients((0, 0, budget/2))
                self.assertEqual(semiprime_kernel(cubic), semiprime_kernel(quartic))
                actual_budget, lower, necessary = safe_subtraction_tradeoff((0, budget), a)
                self.assertEqual(actual_budget, budget)
                self.assertEqual(type_i_endpoint_coefficient(cubic), 1-budget/2)
                self.assertEqual(evaluate(semiprime_kernel(cubic), a), lower)
                self.assertGreater(necessary, 2)
                for degree in (5, 6, 10, 64):
                    penalties = (*([0]*(degree-2)), budget/(degree-2))
                    coefficients = safe_subtraction_coefficients(penalties)
                    self.assertEqual(type_i_endpoint_coefficient(coefficients), 1-budget/2)
                    value = evaluate(semiprime_kernel(coefficients), a)
                    self.assertGreaterEqual(value, lower)
                    if budget > 0:
                        self.assertGreater(value, lower)

    def test_safe_positive_endpoint_and_exact_deletion_cost(self):
        cases = ((), (100,), (0, 1), (5, 2), (17, 1, F(1, 2)),
                 (*([0]*62), F(1, 31)), (1, 2, 3, 4, 5))
        for penalties in cases:
            coefficients = safe_subtraction_coefficients(penalties)
            expected_budget = sum(j*F(c) for j, c in enumerate(penalties))
            for i in range(1, 40):
                a = F(1, 2)+F(i, 80)
                budget, lower, necessary = safe_subtraction_tradeoff(penalties, a)
                value = evaluate(semiprime_kernel(coefficients), a)
                self.assertEqual(budget, expected_budget)
                self.assertGreaterEqual(value, lower)
                if budget <= 2:
                    self.assertGreater(value, 0)
                    self.assertGreaterEqual(lower, 2*(1-a)**2*(2*a+1))
                if value <= 0:
                    self.assertGreaterEqual(budget, necessary)
                    self.assertLess(type_i_endpoint_coefficient(coefficients), 0)
        for a in (F(3, 5), F(2, 3), F(3, 4), F(9, 10)):
            necessary = 2/(a*(2*a-1))
            coefficients = safe_subtraction_coefficients((0, necessary))
            self.assertEqual(evaluate(semiprime_kernel(coefficients), a), 0)
            self.assertLess(type_i_endpoint_coefficient(coefficients), 0)

    def test_formal_triples_match_eight_divisors_and_expose_new_positive_loss(self):
        alternative = (0, 1, -100, 400, -500, 200)
        cases = ((0, 1), (0, 10, 0, -9), alternative, (0, -3, 7, -3))
        for coefficients in cases:
            for i in range(1, 18):
                for j in range(1, 20-i):
                    shares = (F(i, 20), F(j, 20), F(20-i-j, 20))
                    direct = F(0)
                    for removed in range(8):
                        argument = sum(shares[k] for k in range(3) if not removed & (1 << k))
                        direct += (-1)**removed.bit_count()*evaluate(coefficients, argument)
                    self.assertEqual(negative_triple_kernel(coefficients, shares), direct)
                    if coefficients == (0, 1):
                        self.assertEqual(direct, 0)
                    if coefficients == (0, 10, 0, -9):
                        self.assertEqual(direct, -54*shares[0]*shares[1]*shares[2])
        self.assertEqual(type_i_endpoint_coefficient(alternative), 1)
        self.assertEqual(evaluate(semiprime_kernel(alternative), F(3, 4)), -F(193, 64))
        self.assertEqual(negative_triple_kernel(alternative, (F(9, 10), F(1, 25), F(3, 50))),
                         F(7263, 15625))
        # These rational shares do not assert actual prime-factor locations.
        # A general polynomial passes coefficient validation but need not be
        # a member of the nonnegative subtraction family.
        with self.assertRaises(ValueError):
            safe_subtraction_coefficients((100, -400, 500, -200))

    def test_new_exact_domains_and_endpoint_normalization(self):
        for coefficients in ([0, 1], (0, 2), (False, 1), (0, 1.0)):
            with self.assertRaises(ValueError):
                type_i_endpoint_coefficient(coefficients)
        for a in (True, 0.75, F(1, 2), F(1), F(-1)):
            with self.assertRaises(ValueError):
                safe_subtraction_tradeoff((0, 9), a)
        for penalties in ([1], (True,), (1.0,), (-1,), (0,)*64):
            with self.assertRaises(ValueError):
                safe_subtraction_tradeoff(penalties, F(3, 4))
        for shares in ([F(1, 3)]*3, (F(1, 2), F(1, 2)), (0, F(1, 2), F(1, 2)),
                       (F(1, 2), F(1, 2), F(1, 2)), (True, F(1, 3), F(1, 3)),
                       (0.5, F(1, 4), F(1, 4))):
            with self.assertRaises(ValueError):
                negative_triple_kernel((0, 1), shares)
        for degree in range(1, 65):
            coefficients = (0, *([0]*(degree-1)), 1)
            self.assertEqual(type_i_endpoint_coefficient(coefficients),
                             F(1) if degree == 1 else F(degree, 2))


if __name__ == '__main__':
    unittest.main()
