"""Finite controls for composing supports and transferring count bounds."""
from fractions import Fraction
import unittest

from cubic_batch import _build_survivors
from cubic_sieve import exact_floor_cuberoot
from prime_pair_transfer import count_difference_floor, dyadic_intervals
from redistribution import trial_prime


class PrimePairTransferTests(unittest.TestCase):
    def test_disjoint_dyadic_cover_and_necessary_cross_interval_pairs(self):
        found_cross_terms = False
        for upper, levels in ((31, 1), (96, 3), (101, 5), (128, 8)):
            intervals = dyadic_intervals(upper, levels)
            lower = Fraction(upper, 2**levels)
            blocks = [{n for n in range(1, upper+1) if a < n <= b} for a, b in intervals]
            for n in range(1, upper+1):
                self.assertEqual(sum(n in block for block in blocks), int(lower < n <= upper))
            self.assertLess(sum(b for _, b in intervals), 2*upper)
            for target in range(upper//2, upper+1):
                direct = sum(lower < n <= upper and lower < target-n <= upper
                             for n in range(1, upper+1))
                composed = sum(sum(target-n in second for n in first)
                               for first in blocks for second in blocks)
                self_only = sum(sum(target-n in block for n in block) for block in blocks)
                self.assertEqual(direct, composed)
                found_cross_terms |= self_only != direct
        self.assertTrue(found_cross_terms)

    def test_canonical_composites_embed_in_fixed_semiprime_set_and_trim_safely(self):
        for x in (28, 64, 126, 250):
            upper = 2*x
            primes = [p for p in range(3, upper+1, 2) if trial_prime(p)]
            prime_set = set(primes)
            z = exact_floor_cuberoot(x-3)
            semiprimes = {p*q for p in primes for q in primes
                          if z < p <= q and p*q <= upper}
            for target in (x, x+2, upper-2, upper):
                zm = exact_floor_cuberoot(target-3)
                a, c, _ = _build_survivors(primes, zm, target-3)
                composites = {3+2*i for i, value in enumerate(c) if value}
                self.assertEqual(composites,
                                 {3+2*i for i, value in enumerate(a) if value and not trial_prime(3+2*i)})
                self.assertTrue(composites <= semiprimes)
                g = sum(target-p in prime_set for p in primes)
                cc = sum(target-n in composites for n in composites)
                canonical_l = g-cc+int(target//2 in composites)
                for lower in (Fraction(target, 7), Fraction(target, 3), Fraction(5, 2)):
                    prime_pairs = [(p, target-p) for p in primes
                                   if target-p in prime_set and p > lower and target-p > lower]
                    semi_pairs = [(s, target-s) for s in semiprimes
                                  if target-s in semiprimes and s > lower and target-s > lower]
                    omitted = 2*(lower.numerator//lower.denominator)
                    self.assertGreaterEqual(canonical_l, len(prime_pairs)-len(semi_pairs)-omitted)
                    prime_weights = [Fraction(p % 7+2, 3)*Fraction(q % 7+2, 3) for p, q in prime_pairs]
                    semi_weights = [Fraction(s % 5+3, 4)*Fraction(t % 5+3, 4) for s, t in semi_pairs]
                    floor = count_difference_floor(sum(prime_weights), sum(semi_weights),
                                                   max(prime_weights, default=1),
                                                   min(semi_weights, default=1), omitted)
                    self.assertGreaterEqual(canonical_l, floor)

    def test_weight_inequality_direction_and_required_ratio(self):
        rho, gap, a = Fraction(49, 100), Fraction(7, 3), 4
        for semi_weight in (0, 1, 1000):
            prime_weight = rho*semi_weight+gap
            bound = count_difference_floor(prime_weight, semi_weight, a, 10, 5)
            self.assertGreaterEqual(bound, gap/a-5)
        # If rho*b<a the simplification is false. Retain that prerequisite.
        bound = count_difference_floor(rho*1000+gap, 1000, a, 8)
        self.assertLess(bound, gap/a)

    def test_input_meaning_and_fractional_endpoints(self):
        self.assertEqual(dyadic_intervals(7, 2), ((Fraction(7, 2), Fraction(7)),
                                                (Fraction(7, 4), Fraction(7, 2))))
        for upper, levels in ((True, 2), (0, 2), (8, 0), (8, True), (8, 65)):
            with self.assertRaises(ValueError):
                dyadic_intervals(upper, levels)
        for values in ((1.0, 2, 3, 4, 0), (True, 2, 3, 4, 0), (1, 2, 0, 4, 0),
                       (1, -2, 3, 4, 0), (1, 2, 3, 4, True), (1, 2, 3, 4, -1)):
            with self.assertRaises(ValueError):
                count_difference_floor(*values)
        self.assertIn("not primality", count_difference_floor.__doc__)


if __name__ == "__main__":
    unittest.main()
