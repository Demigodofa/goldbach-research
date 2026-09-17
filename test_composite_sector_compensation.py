"""Exact sector and power-correction guards, not asymptotic extrapolation."""

import unittest
from fractions import Fraction as F
from math import gcd

from complementary_divisor_correlation import central_interval
from composite_sector_compensation import (
    composite_main_floor, power_free_sector_identity, prime_composite_vectors,
)
from cutoff_normalized_remainder import cutoff_log_vectors
from major_arc_kernel import _factorization


def value(vector):
    # Arbitrary exact additive log-prime assignment; tests algebra only.
    return sum(p * c for p, c in vector)


def fixture(target, cutoff):
    return {n: {key: v if key == 'P' else value(v)
                for key, v in prime_composite_vectors(n, cutoff).items()}
            for n in central_interval(target)}


def correlate(rows, target, left, right):
    return sum(row[left] * rows[target-n][right] for n, row in rows.items())


class CompositeSectorCompensationTests(unittest.TestCase):
    def test_exact_prime_and_composite_vector_split(self):
        for n in (11, 12, 13, 15, 16, 25, 27, 30, 49):
            row = prime_composite_vectors(n, 7)
            self.assertEqual(value(row['D']), value(row['D_prime']) + value(row['D_composite']))
            self.assertEqual(value(row['D_composite']), value(row['Q']) - value(row['B']))
            self.assertEqual(value(row['B']), (1-row['P'])*value(row['A']))

    def test_proper_powers_are_composites_not_zero_mangoldt(self):
        row = prime_composite_vectors(25, 7)
        self.assertEqual(row['P'], 0)
        self.assertEqual(row['Q'], ((5, 1),))
        self.assertNotEqual(row['D_composite'], tuple((p, -c) for p, c in row['B']))
        self.assertEqual(prime_composite_vectors(30, 7)['Q'], ())

    def test_exact_three_sector_recombination(self):
        for target, cutoff in ((30, 7), (50, 7), (60, 7), (84, 11)):
            rows = fixture(target, cutoff)
            c = lambda l, r: correlate(rows, target, l, r)
            self.assertEqual(c('D_prime', 'D_composite'), c('D_composite', 'D_prime'))
            self.assertEqual(c('D', 'D'), c('D_prime', 'D_prime')
                             + 2*c('D_prime', 'D_composite') + c('D_composite', 'D_composite'))

    def test_sector_formulas_retain_actual_pair_unknowns(self):
        for target, cutoff in ((30, 7), (50, 7), (60, 7), (84, 11)):
            rows = fixture(target, cutoff)
            c = lambda l, r: correlate(rows, target, l, r)
            a = value(_factorization(cutoff))
            parts = power_free_sector_identity(c('A', 'A'), c('P', 'A'),
                        c('Lambda_prime', 'A'), c('P', 'P'),
                        c('Lambda_prime', 'P'), c('Lambda_prime', 'Lambda_prime'), a)
            self.assertEqual(parts['pp'], c('D_prime', 'D_prime'))
            self.assertEqual(parts['pc'] + c('D_prime', 'Q'), c('D_prime', 'D_composite'))
            self.assertEqual(parts['cc'] - 2*c('B', 'Q') + c('Q', 'Q'),
                             c('D_composite', 'D_composite'))

    def test_proper_power_pair_correction_need_not_vanish(self):
        rows, target = fixture(50, 7), 50
        correction = -2*correlate(rows, target, 'B', 'Q') + correlate(rows, target, 'Q', 'Q')
        self.assertNotEqual(correction, 0)
        self.assertEqual(correlate(rows, target, 'D_composite', 'D_composite'),
                         correlate(rows, target, 'B', 'B') + correction)

    def test_no_free_full_gap_margin_from_sector_positivity(self):
        # Basis substitutions test the formal linear identity for all moments.
        for basis in range(6):
            values = [F(int(i == basis)) for i in range(6)]
            aa, pa, lap, z, m, t = values
            parts = power_free_sector_identity(*values, F(7, 3))
            self.assertEqual(parts['pp'] + 2*parts['pc'] + parts['cc'], t - 2*lap + aa)
        # Put the two proved H mains in: the remainder is T-H, not T+margin.
        parts = power_free_sector_identity(1, F(2, 3), 1, 0, 0, 0, F(1, 2))
        self.assertGreater(parts['cc'], 0)
        self.assertEqual(parts['pp'] + 2*parts['pc'] + parts['cc'], -1)

    def test_nonreduced_prime_progressions_are_empty_but_powers_survive(self):
        target, cutoff = 50, 7
        for d in range(1, cutoff+1):
            if gcd(d, target) == 1:
                continue
            primes = [m for m in central_interval(target) if (m-target) % d == 0
                      and _factorization(m) == ((m, 1),)]
            self.assertEqual(primes, [])
        self.assertEqual((25-target) % 5, 0)
        self.assertNotEqual(cutoff_log_vectors(target-25, cutoff)[0], ())

    def test_main_margin_floor_and_fixed_gap_boundary(self):
        theta = F(1, 3)
        self.assertEqual(composite_main_floor(theta, F(0)), 1-2*theta)
        self.assertEqual(composite_main_floor(theta, F(1, 10)), F(7, 27))
        self.assertGreater(composite_main_floor(theta, F(1, 10)), 0)
        self.assertEqual(composite_main_floor(theta, 1-2*theta), 0)
        self.assertLess(composite_main_floor(theta, F(1, 2)), 0)

    def test_strict_central_endpoints_and_ordered_midpoint(self):
        self.assertEqual(list(central_interval(12)), [5, 6, 7])
        rows = fixture(14, 3)
        self.assertEqual(correlate(rows, 14, 'P', 'P'), 1)
        self.assertEqual(rows[7]['P'], 1)

    def test_validation(self):
        for args in ((7, 7), (7, 11), (1, 1), (12, 0), (True, 1)):
            with self.assertRaises(ValueError):
                prime_composite_vectors(*args)
        for args in ((F(1, 2), F(0)), (F(0), F(0)),
                     (F(1, 3), F(1)), (F(1, 3), 0.1)):
            with self.assertRaises(ValueError):
                composite_main_floor(*args)
        with self.assertRaises(ValueError):
            power_free_sector_identity(1, 2, 3, 4, 5, 6, 0.5)


if __name__ == '__main__':
    unittest.main()
