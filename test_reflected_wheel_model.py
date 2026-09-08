"""Independent finite checks; enumeration is not the asymptotic proof."""
from fractions import Fraction
from itertools import product
import math
import unittest

from reflected_wheel_model import (baseline_numerators, ordered_counts,
                                  reflection_orbits, sample_model, splice_prime_prefix)
from redistribution import trial_prime


def direct_counts(flags):
    points = [a for a, present in enumerate(flags) if present]
    result = [0]*(2*len(flags)-1)
    for a in points:
        for b in points:
            result[a+b] += 1
    return result


class ReflectedWheelTests(unittest.TestCase):
    def test_exact_convolution_against_all_binary_odd_sets(self):
        for bits in product((0, 1), repeat=7):
            flags = bytearray(14)
            flags[1::2] = bytes(bits)
            self.assertEqual(ordered_counts(flags), direct_counts(flags))

    def test_all_outcomes_have_forced_zero_and_exact_expected_other_counts(self):
        center, wheel, p = 12, 2, Fraction(1, 4)
        orbits = reflection_orbits(center, wheel)
        units = bytearray(center)
        for a, b in orbits:
            units[a] = units[b] = 1
        expected = [Fraction(0)]*(2*center-1)
        second = expected.copy()
        mass = Fraction(0)
        for choices in product((0, 1, 2), repeat=len(orbits)):
            flags = bytearray(center)
            weight = Fraction(1)
            for (a, b), choice in zip(orbits, choices):
                weight *= (1-2*p) if choice == 0 else p
                if choice:
                    flags[(a, b)[choice-1]] = 1
            counts = direct_counts(flags)
            self.assertEqual(counts[center], 0)
            mass += weight
            for k, value in enumerate(counts):
                expected[k] += weight*value
                second[k] += weight*value*value
        self.assertEqual(mass, 1)
        baseline = baseline_numerators(units, p)
        for k, numerator in enumerate(baseline):
            if k != center:
                self.assertEqual(expected[k], Fraction(numerator, p.denominator**2))
                self.assertLessEqual(second[k]-expected[k]**2, 12*center*p*p+4*p)
        self.assertGreater(baseline[center], 0)

    def test_wheel_and_reflection_are_preserved_without_using_primality(self):
        for center, wheel in [(120, 30), (840, 210), (64, 2)]:
            flags, units = sample_model(center, wheel, Fraction(2, 5), 0)
            self.assertEqual(ordered_counts(flags), direct_counts(flags))
            self.assertEqual(ordered_counts(flags)[center], 0)
            for a in range(1, center):
                self.assertEqual(bool(units[a]), math.gcd(a, wheel) == 1)
                self.assertLessEqual(flags[a], units[a])
                self.assertLessEqual(flags[a]+flags[center-a], 1)

    def test_true_prime_prefix_does_not_remove_the_forced_hole(self):
        center, through = 840, 200
        sampled, _ = sample_model(center, 210, Fraction(2, 5), 0)
        sampled.append(0)  # include the center index, as the splice contract requires
        original = sampled.copy()
        changed = splice_prime_prefix(sampled, center, through)
        self.assertEqual(sampled, original)
        for n in range(through+1):
            self.assertEqual(bool(changed[n]), trial_prime(n))
        counts = direct_counts(changed)
        self.assertEqual(counts[center], 0)
        for n in range(4, through+1, 2):
            self.assertEqual(counts[n], sum(trial_prime(a) and trial_prime(n-a)
                                            for a in range(2, n-1)))


if __name__ == "__main__":
    unittest.main()
