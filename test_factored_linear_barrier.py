"""Exact selected-target identities and interval checks for the plug-in gap."""
from fractions import Fraction
import unittest

from cubic_batch import _build_survivors
from cubic_sieve import exact_floor_cuberoot
from factored_linear_barrier import factored_bound, linear_plugin_coefficient, log_enclosure
from redistribution import trial_prime


def liouville_by_multiplicity(n):
    multiplicity = 0
    p = 2
    while p*p <= n:
        while n % p == 0:
            n //= p
            multiplicity += 1
        p += 1
    multiplicity += n > 1
    return -1 if multiplicity % 2 else 1


class FactoredLinearBarrierTests(unittest.TestCase):
    def test_selected_actual_survivors_liouville_and_diagonal(self):
        for target in (6, 8, 12, 24, 26, 30, 50, 98, 126, 242, 264, 338, 1000):
            high = target-3
            z = exact_floor_cuberoot(high)
            limit = max(z, high//(z+1))
            small = [p for p in range(3, limit+1, 2) if trial_prime(p)]
            a, c, _ = _build_survivors(small, z, high)
            lower, t, m, diagonal = factored_bound(target, a, c)
            signed = 0
            prime_survivor = 0
            true_g = 0
            cc = 0
            for i, n in enumerate(range(3, target-2, 2)):
                j = len(a)-1-i
                self.assertEqual(a[i]-c[i], int(trial_prime(n)))
                self.assertEqual(a[i]-2*c[i], -liouville_by_multiplicity(n)*a[i])
                signed -= liouville_by_multiplicity(n)*a[i]*a[j]
                prime_survivor += trial_prime(n)*a[j]
                true_g += trial_prime(n) and trial_prime(target-n)
                cc += c[i]*c[j]
            self.assertEqual(lower, signed+diagonal)
            self.assertEqual(lower, 2*t-m+diagonal)
            self.assertEqual(t, prime_survivor)
            self.assertEqual(lower, true_g-cc+diagonal)
            if target in (50, 98, 242, 338):
                self.assertEqual(diagonal, 1)
        self.assertEqual(liouville_by_multiplicity(121), 1)

    def test_rational_log_enclosures_are_nested_and_certify_gap(self):
        self.assertEqual(log_enclosure(1), (0, 0))
        # A two-term rational enclosure already proves the needed log2 bound.
        low2, high2 = log_enclosure(2, 2)
        self.assertGreater(low2, Fraction(2, 3))
        self.assertLess(high2, Fraction(25, 36))
        for x in (Fraction(9, 8), Fraction(4, 3), Fraction(3, 2), Fraction(7, 4), 2):
            low, high = log_enclosure(x, 1)
            for terms in (2, 4, 8, 12):
                next_low, next_high = log_enclosure(x, terms)
                self.assertLessEqual(low, next_low)
                self.assertLessEqual(next_high, high)
                self.assertLessEqual(next_low, next_high)
                low, high = next_low, next_high
        # Independent logarithm identity log(4/3)+log(3/2)=log2.
        a, b = log_enclosure(Fraction(4, 3))
        c, d = log_enclosure(Fraction(3, 2))
        e, f = log_enclosure(2)
        self.assertLessEqual(a+c, f)
        self.assertGreaterEqual(b+d, e)

    def test_level_threshold_and_negative_certificate_not_actual_bound(self):
        for u in (2, Fraction(9, 4), Fraction(5, 2), Fraction(11, 4), 3):
            for theta in (Fraction(1, 2), Fraction(2, 3), Fraction(3, 4),
                          Fraction(9, 10), 1):
                low, high = linear_plugin_coefficient(u, theta)
                self.assertLessEqual(low, high)
                self.assertLess(high, Fraction(-121, 1296))
                if theta*u <= 2:
                    t_low, t_high = log_enclosure(u-1)
                    self.assertEqual((low, high), (-(1+t_high)**2, -(1+t_low)**2))
            # At the limiting endpoint, compare the direct plug-in with
            # the independently simplified negative-square enclosure.
            low, high = linear_plugin_coefficient(u, 1)
            t_low, t_high = log_enclosure(u-1)
            self.assertLessEqual(low, -(1-t_low)**2)
            self.assertGreaterEqual(high, -(1-t_high)**2)
        self.assertEqual(linear_plugin_coefficient(2, 1), (-1, -1))
        self.assertIn("NOT actual L/K", linear_plugin_coefficient.__doc__)

    def test_input_meaning_and_rejected_unsafe_ranges(self):
        for x in (True, 0.5, Fraction(1, 2), Fraction(5, 2)):
            with self.assertRaises(ValueError):
                log_enclosure(x)
        for terms in (True, 0, 129, 1.0):
            with self.assertRaises(ValueError):
                log_enclosure(2, terms)
        for u, theta in ((True, 1), (3.0, 1), (Fraction(7, 2), 1),
                         (3, 0), (3, Fraction(11, 10))):
            with self.assertRaises(ValueError):
                linear_plugin_coefficient(u, theta)
        for target, a, c in ((True, bytearray([1]), bytearray([0])),
                             (6, bytearray([0]), bytearray([1])),
                             (8, bytearray([1]), bytearray([0])),
                             (6, bytearray([2]), bytearray([0]))):
            with self.assertRaises(ValueError):
                factored_bound(target, a, c)
        self.assertIn("not establish primality", factored_bound.__doc__)


if __name__ == "__main__":
    unittest.main()
