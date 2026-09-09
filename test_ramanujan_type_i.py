"""Independent complete-period controls for the two-scale comparison."""
from fractions import Fraction as F
from math import gcd, lcm
import unittest

from exceptional_character_model import character_values
from major_arc_kernel import sampled_kernel
from ramanujan_type_i import mixed_pair_coefficients, progression_means
from signed_pair_main_term import pair_coefficients


def arrays(samples, conductor=None, sign=1, period=None):
    if period is None:
        period = lcm(conductor or 1, *(q for q in range(1, len(samples)) if samples[q]))
    chi = character_values(conductor, two_sign=sign) if conductor is not None else None
    phi_d = sum(bool(a) for a in chi) if chi is not None else 1
    principal = [sampled_kernel(n or period, 1, samples) for n in range(period)]
    exceptional = ([chi[n % conductor]*F(conductor, phi_d)*
                    sampled_kernel(n or period, conductor, samples) for n in range(period)]
                   if chi is not None else [F(0)]*period)
    return period, principal, exceptional


class RamanujanTypeITests(unittest.TestCase):
    def test_progression_means_against_direct_periods(self):
        samples = (0, 1, F(-2, 3), F(4, 5), F(1, 7), F(-3, 8), F(5, 9), 0, F(2, 3))
        for conductor, sign in ((None, 1), (3, 1), (4, 1), (5, 1), (8, 1), (8, -1)):
            period, principal, exceptional = arrays(samples, conductor, sign)
            for target in (0, 1, 2, 8, -10):
                for step in (1, 2, 3, 4, 5, 6, 8, 12, 24):
                    terms = period//gcd(period, step)
                    direct = tuple(sum(a[(target-step*k) % period] for k in range(terms))/terms
                                   for a in (principal, exceptional))
                    self.assertEqual(progression_means(target, step, samples, conductor,
                                                       two_sign=sign), direct)

    def test_full_divisor_density_including_nonreduced_and_prime_powers(self):
        samples = (0,)+(1,)*24
        for step in range(1, 25):
            phi = sum(gcd(a, step) == 1 for a in range(step))
            for target in range(0, 2*step+1):
                expected = F(step, phi) if gcd(target, step) == 1 else 0
                self.assertEqual(progression_means(target, step, samples), (expected, 0))
        # Finite truncation cannot silently be replaced by the full density.
        self.assertEqual(progression_means(2, 5, (0, 1))[0], 1)
        self.assertNotEqual(progression_means(2, 5, (0, 1))[0], F(5, 4))

    def test_character_resonance_requires_the_whole_Dq(self):
        for conductor, cofactor, sign in ((33, 2, 1), (40, 3, 1), (40, 3, -1)):
            samples = [F(0)]*(conductor*cofactor+1)
            samples[conductor*cofactor] = F(2, 3)
            samples = tuple(samples)
            period, _, exceptional = arrays(samples, conductor, sign)
            for target in (1, 2, conductor, 2*conductor):
                for step in (1, conductor, cofactor, conductor*cofactor, 2*conductor*cofactor):
                    terms = period//gcd(period, step)
                    expected = sum(exceptional[(target-step*k) % period] for k in range(terms))/terms
                    self.assertEqual(progression_means(target, step, samples, conductor,
                                                       two_sign=sign)[1], expected)
            self.assertEqual(progression_means(1, conductor, samples, conductor, two_sign=sign)[1], 0)
            self.assertNotEqual(progression_means(1, conductor*cofactor, samples, conductor,
                                                  two_sign=sign)[1], 0)

    def test_all_four_mixed_correlations_with_unequal_signed_cutoffs(self):
        for conductor, cofactor, sign in ((3, 2, 1), (33, 2, 1), (40, 3, 1), (40, 3, -1)):
            left = [F(0)]*(conductor*cofactor+2)
            right = [F(0)]*(conductor*cofactor+1)
            for index in (1, 2, 3, 5, conductor, conductor*cofactor):
                left[index] = F(index % 7-3, 5)
                right[index] = F(index % 5-2, 3)
            left[-1] = F(0)  # Different support lengths, not a changed common period.
            left[conductor], right[conductor] = F(2, 3), F(-3, 4)
            left, right = tuple(left), tuple(right)
            period = lcm(conductor, *(q for q in range(1, len(left)) if left[q]),
                         *(q for q in range(1, len(right)) if right[q]))
            _, pl, xl = arrays(left, conductor, sign, period)
            _, pr, xr = arrays(right, conductor, sign, period)
            for target in (0, 2, 8, 2*conductor, -2*conductor):
                direct = tuple(sum(a[n]*b[(target-n) % period] for n in range(period))/period
                               for a, b in ((pl, pr), (pl, xr), (xl, pr), (xl, xr)))
                u0, mixed, quadratic = mixed_pair_coefficients(target, left, right, conductor,
                                                               two_sign=sign)
                self.assertEqual(direct, (u0, mixed, mixed, quadratic))
                self.assertEqual(mixed_pair_coefficients(target, left, left, conductor,
                                                         two_sign=sign),
                                 pair_coefficients(target, left, conductor, two_sign=sign))

    def test_fine_plateau_leaves_one_coarse_cutoff_not_its_square(self):
        coarse = (0, 1, F(1, 3), F(2, 5), 0, F(3, 7), F(4, 9))
        fine = (0,)+(1,)*8
        for conductor in (None, 3):
            self.assertEqual(mixed_pair_coefficients(8, fine, coarse, conductor),
                             mixed_pair_coefficients(8, fine[:len(coarse)], coarse, conductor))
            self.assertNotEqual(mixed_pair_coefficients(8, fine, coarse, conductor),
                                pair_coefficients(8, coarse, conductor))
        # Omitting the conductor's boundary sample removes the exceptional term.
        self.assertNotEqual(mixed_pair_coefficients(8, (0, 1, 1, 1, 1),
                                                   (0, 1, 1, 1, 1), 4)[2], 0)
        self.assertEqual(mixed_pair_coefficients(8, (0, 1, 1, 1, 1), (0, 1, 1, 1), 4)[1:],
                         (0, 0))

    def test_input_meaning_rejects_inexact_values_and_invalid_characters(self):
        for target, step, samples, conductor, sign in (
                (True, 1, (0, 1), None, 1), (2, 0, (0, 1), None, 1),
                (2, True, (0, 1), None, 1), (2, 1, (0,), None, 1),
                (2, 1, (0, 0.5), None, 1), (2, 1, (0, True), None, 1),
                (2, 1, (0, 1), 9, 1), (2, 1, (0, 1), None, -1),
                (2, 1, (0, 1), 5, -1), (2, 1, (0, 1), 8, True)):
            with self.assertRaises(ValueError):
                progression_means(target, step, samples, conductor, two_sign=sign)
        for target, left, right, conductor, sign in (
                (1, (0, 1), (0, 1), None, 1), (True, (0, 1), (0, 1), None, 1),
                (2, (0, 1), (0, 0.5), None, 1), (2, (0,), (0, 1), None, 1),
                (2, (0, 1), (0, 1), 25, 1), (2, (0, 1), (0, 1), None, -1),
                (2, (0, 1), (0, 1), 8, True)):
            with self.assertRaises(ValueError):
                mixed_pair_coefficients(target, left, right, conductor, two_sign=sign)


if __name__ == "__main__":
    unittest.main()
