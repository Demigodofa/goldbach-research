"""Exact projection and composition guards; no prime-correlation experiment."""
from fractions import Fraction as F
from math import gcd, lcm
import unittest

from balanced_projection_transfer import (
    divisor_value, gcd_main, harmonic_projection, projection_budget,
    projection_divisors, projection_value, ramanujan_main,
)
from free_divisor_correlation import product_log_vector
from major_arc_kernel import ramanujan
from unexceptional_vaughan_gate import _divisors


class BalancedProjectionTransferTests(unittest.TestCase):
    def test_full_ramanujan_expansion_recovers_signed_divisor_sequence(self):
        coefficients = {6: F(2, 3), 10: F(-5, 7), 12: F(1, 2), 15: F(-3, 5)}
        full = harmonic_projection(coefficients, max(coefficients))
        for n in range(1, 61):
            self.assertEqual(projection_value(full, n), divisor_value(coefficients, n))
        # Prime-power moduli may contribute; squarefree restriction would fail.
        self.assertNotEqual(full[4], 0)

    def test_gcd_main_is_exact_and_truncation_has_an_explicit_tail(self):
        left = {6: F(2, 3), 10: F(-5, 7), 12: F(1, 2)}
        right = {9: F(3, 5), 10: F(7, 4), 15: F(-1, 3)}
        a, b = harmonic_projection(left, 15), harmonic_projection(right, 15)
        for target in (30, 31, 60, 98):
            full = ramanujan_main(a, b, target)
            self.assertEqual(full, gcd_main(left, right, target))
            tail = sum((a[q]*b[q]*ramanujan(q, target) for q in range(4, 16)), F(0))
            self.assertEqual(full-ramanujan_main(a[:4], b[:4], target), tail)
        self.assertNotEqual(ramanujan_main(a, b, 30), ramanujan_main(a[:4], b[:4], 30))

    def test_type_i_projection_conversion_is_exact_for_every_sample(self):
        samples = (F(0), F(1), F(-2, 3), F(3, 5), F(1, 4), F(-2, 7), F(1, 6))
        divisors = projection_divisors(samples)
        for n in range(1, 61):
            self.assertEqual(divisor_value(divisors, n), projection_value(samples, n))
        self.assertEqual(max(divisors), len(samples)-1)
        self.assertEqual(divisors[6], 1)

    def test_complete_means_match_without_an_extra_phi_factor(self):
        # These are the two distinct means needed by BP and PP.
        for q, r, target in ((4, 4, 12), (3, 4, 12), (6, 6, 30), (5, 5, 31)):
            period = lcm(q, r)
            direct = F(sum(ramanujan(q, n)*ramanujan(r, target-n) for n in range(period)), period)
            self.assertEqual(direct, ramanujan(q, target) if q == r else 0)
        for modulus, step, target in ((6, 12, 30), (6, 10, 30), (4, 6, 31), (5, 10, 31)):
            period = modulus//gcd(modulus, step)
            direct = F(sum(ramanujan(modulus, target-step*k) for k in range(period)), period)
            self.assertEqual(direct, ramanujan(modulus, target) if step % modulus == 0 else 0)

    def test_actual_logarithmic_coefficients_and_short_k_are_retained(self):
        # Check the projection linear map separately on actual log-prime coordinates.
        support = (9, 10, 12, 15, 18)
        for prime in (2, 3, 5):
            coefficients = {r: F(dict(product_log_vector(r, 2, 2)).get(prime, 0)) for r in support}
            full = harmonic_projection(coefficients, 18)
            for n in (18, 30, 36, 45, 60):
                self.assertEqual(projection_value(full, n), divisor_value(coefficients, n))
        # For a rough semiprime, all proper divisors have zero h; k=1 survives.
        for n, expected in ((77, ((7, -1), (11, -1))), (49, ((7, -1),))):
            self.assertEqual(product_log_vector(n, 3, 3), expected)
            for d in _divisors(n):
                if d < n:
                    self.assertEqual(product_log_vector(d, 3, 3), ())

    def test_projection_does_not_silently_become_the_prime_model(self):
        # Each negative log coordinate of actual h_77 gives H(1)=-1/77.
        actual_log_coordinate = harmonic_projection({77: F(-1)}, 6)
        self.assertEqual(actual_log_coordinate[1], F(-1, 77))
        self.assertNotEqual(actual_log_coordinate[1], 1)
        # Exact finite algebra of the actual residual decomposition, with arbitrary
        # nonconstant target masks; no smallness assertion is being tested here.
        target = 40
        a = {n: F((3*n) % 11-5) for n in range(1, target)}
        e = {n: F((5*n) % 13-6, 3) for n in range(1, target)}
        b = {n: divisor_value({6: F(-2), 10: F(3)}, n) for n in range(1, target)}
        samples = harmonic_projection({6: F(-2), 10: F(3)}, 3)
        p = {n: projection_value(samples, n) for n in range(1, target)}
        z = {n: b[n]-p[n] for n in a}
        h = {n: a[n]-b[n] for n in a}
        r = {n: e[n]-z[n] for n in a}
        def corr(left, right):
            return sum((F(n % 7, 5)*left[n]*right[target-n] for n in a), F(0))
        self.assertEqual(corr(a, e), corr(z, r)+corr(h, e)+corr(z, z)+corr(p, e))

    def test_all_projection_error_budgets_pass_and_tail_dominates(self):
        for delta in (F(1, 4800), F(1, 9600), F(1, 100000)):
            budget = projection_budget(delta)
            self.assertEqual(budget.saving, 2*delta)
            self.assertLess(budget.mixed_period, 1)
            self.assertLess(budget.projection_period, 1)
            self.assertEqual(budget.convolution, F(1983, 2000))
        with self.assertRaises(ValueError):
            projection_budget(F(1, 100))

    def test_exact_inputs_are_required(self):
        for coefficients, cutoff in (({}, 3), ({2: 0.5}, 3), ({True: F(1)}, 3), ({2: F(1)}, 0)):
            with self.assertRaises(ValueError):
                harmonic_projection(coefficients, cutoff)
        with self.assertRaises(ValueError):
            projection_divisors((F(1), F(2)))


if __name__ == '__main__':
    unittest.main()
