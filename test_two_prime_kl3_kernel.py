"""New exact checks for the two-prime eight-factor mechanism and its scope."""
from fractions import Fraction as F
from itertools import product
import unittest

from all_moduli_balanced_kernel import complete_exact
from two_prime_kl3_kernel import (
    completed_eight_exact, completed_eight_crt, toy_crt_values,
    diagonal_subtraction_exact, transform_zero_extension_prediction,
    two_prime_budget,
)


def fixture(p, seed=1):
    # Deliberately complex, asymmetric Gaussian integers: dropping bars or
    # using an ordinary-Kloosterman CRT twist must not pass accidentally.
    return ((0, 0),)+tuple((1+(i*seed+1) % 3, (i*i+seed) % 5-2)
                            for i in range(1, p))


class TwoPrimeKl3KernelTests(unittest.TestCase):
    def test_eight_factor_crt_with_complex_bars_and_rank_three_twists(self):
        wrong_twist_detected = False
        for p1, p2 in ((3, 5), (3, 7), (5, 7)):
            local = {p1: fixture(p1), p2: fixture(p2, 2)}
            values = toy_crt_values(local)
            for b, h1, h2 in (((0, 1, 2, 3), 1, 2),
                              ((0, 1, 0, 1), 2, -2),
                              ((1, 1, 2, 3), 0, 1)):
                direct = completed_eight_exact(values, b, h1, h2)
                self.assertEqual(direct, completed_eight_crt(local, b, h1, h2))
                wrong = completed_eight_crt(local, b, h1, h2, twist_power=1)
                wrong_twist_detected |= direct != wrong
        self.assertTrue(wrong_twist_detected)

    def test_fourier_diagonal_subtraction_including_equal_source_twists(self):
        for p in (3, 5, 7):
            for h1, h2 in product(range(p), repeat=2):
                for b in ((0, 1, 2, 3), (0, 1, 0, 1)):
                    left, right = diagonal_subtraction_exact(fixture(p), b, h1, h2)
                    self.assertEqual(left, right)
        # At composite q, s1!=s2 and gcd(s1-s2,q)=1 differ. The proof must
        # remove the local diagonal prime by prime, not just once modq.
        values = toy_crt_values({3: fixture(3), 5: fixture(5, 2)})
        mismatch = any(left != right for left, right in (
            diagonal_subtraction_exact(values, (0, 1, 0, 1), h1, h2)
            for h1, h2 in ((0, 0), (1, 2), (2, -2))))
        self.assertTrue(mismatch)

    def test_small_shift_box_synchronizes_rank_three_diagonals(self):
        for p1, p2, size in ((5, 7, 4), (7, 11, 6)):
            count = 0
            for b in product(range(1, size+1), repeat=4):
                literal = sorted(b[:2]) == sorted(b[2:])
                for p in (p1, p2):
                    modular = sorted(v % p for v in b[:2]) == sorted(v % p for v in b[2:])
                    self.assertEqual(literal, modular)
                count += literal
            self.assertEqual(count, 2*size*size-size)
        # Exceeding the smaller prime permits a diagonal at one prime only.
        b = (1, 2, 6, 2)
        self.assertEqual(sorted(v % 5 for v in b[:2]), sorted(v % 5 for v in b[2:]))
        self.assertNotEqual(sorted(v % 7 for v in b[:2]), sorted(v % 7 for v in b[2:]))

    def test_literal_zero_extension_correction_in_the_model_transform(self):
        for q in (15, 21, 35):
            for h, l, t in product((1, 2), (0, 1, 3, 5, 7), (0, 1, 3, 5, 7, 15)):
                direct = tuple(F(v, q) for v in complete_exact(q, h, l, t))
                self.assertEqual(direct, transform_zero_extension_prediction(q, h, l, t))
        for q, h in ((25, 1), (30, 1), (15, 3)):
            with self.assertRaises(ValueError):
                transform_zero_extension_prediction(q, h, 1, 1)

    def test_exact_varying_length_and_full_model_budgets(self):
        for sigma in (F(0), F(1, 256), F(1, 128)):
            result = two_prime_budget(sigma)
            self.assertEqual(max(result['moment_terms']), result['moment'])
            self.assertEqual(result['core'], result['expected_core'])
            self.assertLess(result['short_shift'], F(2, 5))
            self.assertLess(result['core'], F(1, 2)+sigma)
        self.assertEqual(two_prime_budget()['core'], F(31, 64))
        cap = two_prime_budget(0, F(1, 4096), F(1, 4096))
        self.assertEqual(cap['model'], F(4071, 4096))
        self.assertLessEqual(cap['raw_model'], cap['model'])
        self.assertLess(cap['correction'], cap['model'])
        self.assertLess(cap['axes'], cap['model'])
        # Actual padded X exponent: q~Y^1/2, so decorations in log_q
        # are twice their log_Y size, with a strict margin for tails.
        self.assertLess(2*F(1, 4096), F(1, 128))
        for bad in (True, 0.001, F(1, 64), -1):
            with self.assertRaises(ValueError):
                two_prime_budget(bad)


if __name__ == '__main__':
    unittest.main()
