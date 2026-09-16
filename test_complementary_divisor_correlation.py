"""Exact identity/bound tests, not finite evidence for the open remainder."""

import unittest
from fractions import Fraction as F
from math import lcm, log

from complementary_divisor_correlation import (
    central_interval, central_progression_count, centered_square_block,
    complementary_cell, complementary_expansion, divisor_value,
    frozen_mobius_log_vector,
)
from major_arc_kernel import _factorization, _mobius_phi
from unexceptional_vaughan_gate import mangoldt_log_vector


class ComplementaryDivisorTests(unittest.TestCase):
    def test_strict_endpoints_and_reflection(self):
        self.assertEqual(tuple(central_interval(12)), (5, 6, 7))
        self.assertEqual(tuple(central_interval(10)), (4, 5, 6))
        for n in (6, 8, 10, 12, 32, 100):
            self.assertEqual(tuple(central_interval(n)),
                             tuple(sorted(n - x for x in central_interval(n))))

    def test_crt_compatibility_and_non_coprime_divisors(self):
        self.assertIsNone(complementary_cell(14, 6, 9))
        self.assertEqual(complementary_cell(18, 6, 9), (18, 0))
        self.assertEqual(complementary_cell(14, 4, 6), (12, 8))
        self.assertEqual(complementary_cell(14, 4, 2), (4, 0))

    def test_lcm_only_compression_loses_target_residue(self):
        empty = complementary_cell(32, 2, 15)
        occupied = complementary_cell(32, 6, 5)
        self.assertEqual(empty, (30, 2))
        self.assertEqual(occupied, (30, 12))
        self.assertEqual(central_progression_count(32, *empty), 0)
        self.assertEqual(central_progression_count(32, *occupied), 1)

    def test_progression_error_including_equality_at_open_endpoints(self):
        self.assertEqual(central_progression_count(12, 4, 0) - F(12, 12), -1)
        for n in (6, 10, 12, 32, 100):
            for q in range(1, 18):
                for r in range(q):
                    count = central_progression_count(n, q, r)
                    direct = sum(x % q == r for x in central_interval(n))
                    self.assertEqual(count, direct)
                    self.assertLessEqual(abs(count - F(n, 3 * q)), 1)

    def test_bilinear_expansion_with_signed_rational_coefficients(self):
        left = {1: F(3, 2), 2: -2, 5: F(4, 7), 6: 3}
        right = {1: -1, 3: F(5, 9), 4: 2, 7: -5}
        for n in (6, 10, 12, 32, 100):
            result = complementary_expansion(n, left, right)
            direct = sum((divisor_value(x, left) * divisor_value(n - x, right)
                          for x in central_interval(n)), F(0))
            self.assertEqual(result.correlation, direct)
            self.assertEqual(result.correlation,
                             F(n, 3) * result.density + result.discrepancy)
            self.assertLessEqual(abs(result.discrepancy), result.discrepancy_bound)

    def test_source_block_is_centered_square_not_complementary_product(self):
        c = {2: -2, 3: F(5, 4), 5: -1, 6: 3}
        mean = sum((F(ca) * cb / lcm(a, b) for a, ca in c.items()
                    for b, cb in c.items()), F(0))
        for m, ell in ((11, 2), (13, 5), (17, 3)):
            direct = sum((divisor_value(m * ell + t, c) ** 2
                          for t in range(1, m)), F(0)) - (m - 1) * mean
            self.assertEqual(centered_square_block(m, ell, c), direct)

    def test_full_frozen_sum_is_lambda_independent_of_scale(self):
        for n in range(2, 91):
            for scale in (1, 17, 100):
                self.assertEqual(frozen_mobius_log_vector(n, scale),
                                 mangoldt_log_vector(n))
        self.assertEqual(frozen_mobius_log_vector(1, 17), ((17, 1),))

    def test_block_mapping_matches_original_arithmetic_code(self):
        from lcm_sawtooth_incomplete_covariance import _cyclic_discrepancy
        from lcm_sawtooth_structured_divisor_sum import _coefficient_data
        m, freeze, row = 17, 5, 4
        _, _, c, k = _coefficient_data(m, freeze, 2, 7)
        original = sum(value * _cyclic_discrepancy(m, row, q) for q, value in k.items())
        direct = sum(sum(value for a, value in c.items() if (m * row + t) % a == 0) ** 2
                     for t in range(1, m)) - (m - 1) * sum(value / q for q, value in k.items())
        self.assertAlmostEqual(original, direct, places=10)

    def test_middle_band_freezing_needs_its_correction(self):
        self.assertNotEqual(frozen_mobius_log_vector(30, 30, 2, 7),
                            frozen_mobius_log_vector(30, 17, 2, 7))
        self.assertEqual(frozen_mobius_log_vector(31, 100, 2, 7), ())

    def test_divisor_switch_preserves_coefficients_and_squarefree_sign(self):
        def switched(n, scale, lower, upper, factor_squarefree=False):
            vector = {}
            for b in range(1, n + 1):
                if n % b or not lower < n // b <= upper:
                    continue
                mu = (_mobius_phi(n)[0] * _mobius_phi(b)[0]
                      if factor_squarefree else _mobius_phi(n // b)[0])
                for number, sign in ((scale, 1), (b, 1), (n, -1)):
                    for p, power in _factorization(number):
                        vector[p] = vector.get(p, 0) + mu * sign * power
            return tuple(sorted((p, c) for p, c in vector.items() if c))

        for n in (30, 42, 60, 72):
            for lower, upper in ((2, 7), (7, n)):
                direct = frozen_mobius_log_vector(n, 100, lower, upper)
                self.assertEqual(switched(n, 100, lower, upper), direct)
                if _mobius_phi(n)[0]:
                    self.assertEqual(switched(n, 100, lower, upper, True), direct)
        self.assertEqual(frozen_mobius_log_vector(12, 100, 2, 7), ((2, -1),))
        self.assertEqual(switched(12, 100, 2, 7, True), ())

    def test_two_by_two_split_with_exact_log_linear_substitution(self):
        # log(p) -> p preserves every tested log-linear identity exactly.
        def value(vector):
            return sum(p * power for p, power in vector)

        n, b = 100, 7
        short = {x: value(frozen_mobius_log_vector(x, n, upper=b))
                 for x in central_interval(n)}
        long = {x: value(frozen_mobius_log_vector(x, n, lower=b, upper=n))
                for x in central_interval(n)}
        lam = {x: value(mangoldt_log_vector(x)) for x in central_interval(n)}
        aa = sum(short[x] * short[n - x] for x in short)
        ar = sum(short[x] * long[n - x] for x in short)
        ra = sum(long[x] * short[n - x] for x in short)
        rr = sum(long[x] * long[n - x] for x in short)
        self.assertEqual(ar, ra)
        self.assertEqual(aa + 2 * ar + rr, sum(lam[x] * lam[n - x] for x in lam))

    def test_actual_logs_and_prime_power_subtraction(self):
        n, b = 50, 7
        def evaluate(vector):
            return sum(c * log(p) for p, c in vector)
        interval = central_interval(n)
        short = {x: evaluate(frozen_mobius_log_vector(x, n, upper=b)) for x in interval}
        long = {x: evaluate(frozen_mobius_log_vector(x, n, lower=b, upper=n)) for x in interval}
        prime = {x: log(x) if _factorization(x) == ((x, 1),) else 0.0 for x in interval}
        lam = {x: evaluate(mangoldt_log_vector(x)) for x in interval}
        c = {a: _mobius_phi(a)[0] * log(n / a) for a in range(1, b + 1)}
        density = sum(c[a] * c[d] / lcm(a, d) for a in c for d in c
                      if complementary_cell(n, a, d) is not None)
        aa = sum(short[x] * short[n - x] for x in interval)
        error = aa - n * density / 3
        ar = sum(short[x] * long[n - x] for x in interval)
        rr = sum(long[x] * long[n - x] for x in interval)
        powers = sum(lam[x] * lam[n - x] - prime[x] * prime[n - x] for x in interval)
        total = sum(prime[x] * prime[n - x] for x in interval)
        self.assertGreater(powers, 0)
        self.assertLessEqual(abs(error), b ** 2 * log(n) ** 2)
        self.assertAlmostEqual(total, n * density / 3 + error + 2 * ar + rr - powers, places=10)

    def test_empty_coefficients_and_validation(self):
        self.assertEqual(complementary_expansion(12, {}).correlation, 0)
        for invalid in (0, 4, 9, 12.0, True):
            with self.assertRaises(ValueError):
                central_interval(invalid)
        with self.assertRaises(ValueError):
            complementary_expansion(12, {2: 0.5})
        with self.assertRaises(ValueError):
            complementary_cell(12, 0, 2)


if __name__ == "__main__":
    unittest.main()
