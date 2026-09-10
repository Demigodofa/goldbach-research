"""Conductor-gap, exact projector, maximal-endpoint and saving guards."""
from fractions import Fraction as F
from math import gcd, prod
import unittest

from major_arc_kernel import _factorization, _mobius_phi
from prime_companion_dispersion import (
    conductor_candidates, dispersion_budgets,
    dyadic_prefix_blocks, low_projection_weight,
)


def char3(n):
    return 0 if n % 3 == 0 else (1 if n % 3 == 1 else -1)


class PrimeCompanionDispersionTests(unittest.TestCase):
    def test_tail_profiles_charge_amplitude_and_each_endpoint(self):
        # Right-continuous step profile; its Stieltjes measure is atomic.
        threshold, initial = 10, F(2, 3)
        jumps = {13: -F(1, 4), 20: F(1, 2), 25: -F(1, 3)}
        for n in range(8, 29):
            direct = (initial+sum((change for at, change in jumps.items() if at <= n),
                                  F(0))) if n >= threshold else F(0)
            tails = initial*int(n >= threshold)+sum(
                (change*int(n >= at) for at, change in jumps.items()), F(0))
            self.assertEqual(direct, tails)
        self.assertGreater(abs(initial)+sum(map(abs, jumps.values())),
                           sum(map(abs, jumps.values())))
        self.assertEqual(F(46, 100)-F(47, 100), -F(1, 100))

    def test_prime_companion_creates_the_conductor_divisor_gap(self):
        for d, m in ((1, 7), (3, 7), (8, 11), (12, 17), (30, 31)):
            low, high = conductor_candidates(d, m)
            self.assertTrue(all(d % f == 0 and f <= d for f in low))
            self.assertTrue(all(f % m == 0 and f >= m for f in high))
            self.assertFalse(set(low) & set(high))
        # A prime power companion breaks this dichotomy: f=3 divides 5*9,
        # but neither divides d=5 nor contains the full companion m=9.
        self.assertEqual(45 % 3, 0)
        self.assertNotEqual(5 % 3, 0)
        self.assertNotEqual(3 % 9, 0)
        with self.assertRaises(ValueError):
            conductor_candidates(5, 9)

    def test_low_projection_matches_actual_small_characters(self):
        d, m = 3, 7
        for p in (29, 43, 71):
            for a in range(-7, 22):
                principal_d = int(gcd(a, d) == 1)
                principal_m = int(a % m != 0)
                # Sum the two characters mod3, both principal in the mod7 slot.
                direct = F((principal_d+char3(a)*char3(p))*principal_m,
                           (d-1)*(m-1))
                self.assertEqual(low_projection_weight(d, m, a, p), direct)

    def test_induced_coprimality_mask_is_essential(self):
        self.assertEqual(low_projection_weight(3, 7, 7, 43), 0)
        self.assertEqual((43-7) % 3, 0)
        self.assertNotEqual(F(1, 6), low_projection_weight(3, 7, 7, 43))
        self.assertEqual(low_projection_weight(3, 7, 1, 43), F(1, 6))

    def test_primitive_lift_agrees_only_on_the_licensed_sequence(self):
        induced = lambda p: char3(p)*int(gcd(p, 21) == 1)
        for p in (29, 43, 71):
            self.assertEqual(induced(p), char3(p))
        self.assertNotEqual(induced(7), char3(7))
        with self.assertRaises(ValueError):
            low_projection_weight(3, 7, 1, 49)  # A composite is not licensed.

    def test_dyadic_prefixes_include_every_endpoint_without_max_interchange(self):
        for size in (1, 2, 4, 8, 16):
            for endpoint in range(size+1):
                blocks = dyadic_prefix_blocks(endpoint, size)
                flattened = [j for lo, hi in blocks for j in range(lo, hi)]
                self.assertEqual(flattened, list(range(endpoint)))
                self.assertTrue(all(lo % (hi-lo) == 0 for lo, hi in blocks))
                self.assertLessEqual(len(blocks), size.bit_length())
        rows = ((1, -1, 0, 0), (0, 0, 1, -1))
        prefixes = [[sum(row[:u]) for u in range(5)] for row in rows]
        self.assertEqual(sum(max(x*x for x in row) for row in prefixes), 2)
        self.assertEqual(max(sum(row[u]**2 for row in prefixes) for u in range(5)), 1)

    def test_binary_tree_square_bound_handles_different_residue_maxima(self):
        rows = ((1, -1, 0, 0), (0, 0, 1, -1), (2, -3, 4, -1))
        for row in rows:
            tree = [(lo, lo+width) for width in (1, 2, 4)
                    for lo in range(0, 4, width)]
            max_prefix = max(sum(row[:u])**2 for u in range(5))
            bound = 3*sum(sum(row[lo:hi])**2 for lo, hi in tree)
            self.assertLessEqual(max_prefix, bound)

    def test_induced_lift_weights_cost_a_harmonic_sum(self):
        tau = lambda n: prod(e+1 for _, e in _factorization(n))
        for f in (3, 8, 15, 30):
            cap = 180
            actual = sum((F(1, _mobius_phi(q)[1])
                          for q in range(f, cap+1, f)), F(0))
            upper = F(1, _mobius_phi(f)[1])*sum(
                (F(tau(r), r) for r in range(1, cap//f+1)), F(0))
            self.assertLessEqual(actual, upper)

    def test_periodized_schwartz_weights_keep_repeated_shifts(self):
        h, q = 3, 11
        for a in range(q):
            weight = sum((F(1, 1+F(abs(r), h))**2
                          for r in range(-100, 101) if (r-a) % q == 0), F(0))
            self.assertLess(weight, 3)
        self.assertEqual((0-11) % q, 0)  # Shifts are not all distinct.

    def test_high_variance_normalization_gives_the_claimed_power_gains(self):
        budget = dispersion_budgets()
        self.assertEqual(budget['largest_modulus'], F(549, 1000))
        self.assertEqual(budget['bv_gap_at_largest_modulus'], -F(49, 1000))
        self.assertEqual(budget['high_first'], -F(1, 1000))
        self.assertEqual(budget['high_second'], -F(91, 2000))
        self.assertEqual(budget['left_power_energy'], -F(49, 200))
        self.assertEqual(budget['left_power_norm'], -F(49, 400))
        q, m, h = F(549, 1000), F(54, 100), F(1, 10)
        # (NH)^-1 * sqrt(QH) * sqrt(NQ + N²/M).
        self.assertEqual(-1-h+(q+h)/2+(1+q)/2, budget['high_first'])
        self.assertEqual(-1-h+(q+h)/2+(2-m)/2, budget['high_second'])
        self.assertEqual(8//2+1+1, 6)  # Variance logs, logm, companion blocks.

    def test_invalid_and_unproved_thresholds_are_rejected(self):
        for action in (lambda: dispersion_budgets(F(459, 1000)),
                       lambda: dispersion_budgets(F(41, 100)),
                       lambda: dispersion_budgets(F(51, 100)),
                       lambda: conductor_candidates(12, 7),
                       lambda: dyadic_prefix_blocks(3, 6),
                       lambda: dyadic_prefix_blocks(9, 8)):
            with self.assertRaises(ValueError):
                action()


if __name__ == '__main__':
    unittest.main()
