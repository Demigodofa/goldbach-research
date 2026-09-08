"""Tiny exact Fourier checks, not a repetition of the frozen range experiment."""
from fractions import Fraction
from itertools import product
import unittest

from reflected_wheel_model import reflection_orbits
from reflection_fourier_gap import quarter_fourier, reflection_variance_quarter


def multiply(left, right):
    a, b = left
    c, d = right
    return a*c-b*d, a*d+b*c


def convolve(left, right):
    result = [Fraction(0)]*(len(left)+len(right)-1)
    for a, x in enumerate(left):
        for b, y in enumerate(right):
            result[a+b] += x*y
    return tuple(result)


def outcomes(center, wheel, p):
    orbits = reflection_orbits(center, wheel)
    for choices in product((0, 1, 2), repeat=len(orbits)):
        flags = [0]*center
        weight = Fraction(1)
        for (a, b), choice in zip(orbits, choices):
            weight *= (1-2*p, p, p)[choice]
            if choice:
                flags[(a, b)[choice-1]] = 1
        yield tuple(flags), weight


def unit_flags(center, wheel):
    flags = [0]*center
    for a, b in reflection_orbits(center, wheel):
        flags[a] = flags[b] = 1
    return tuple(flags)


class ReflectionFourierGapTests(unittest.TestCase):
    def test_exact_centered_moments_over_all_tiny_orbit_outcomes(self):
        for center, wheel in ((8, 2), (12, 2), (24, 6)):
            units = unit_flags(center, wheel)
            orbit_count = len(reflection_orbits(center, wheel))
            for p in (0, Fraction(1, 4), Fraction(1, 3), Fraction(1, 2)):
                means = [[Fraction(0), Fraction(0)] for _ in range(4)]
                seconds = [Fraction(0)]*4
                mass = Fraction(0)
                for flags, weight in outcomes(center, wheel, p):
                    mass += weight
                    residual = tuple(a-p*u for a, u in zip(flags, units))
                    for k, (real, imaginary) in enumerate(quarter_fourier(residual)):
                        means[k][0] += weight*real
                        means[k][1] += weight*imaginary
                        seconds[k] += weight*(real*real+imaginary*imaginary)
                self.assertEqual(mass, 1)
                self.assertEqual(means, [[0, 0]]*4)
                self.assertEqual(tuple(seconds), reflection_variance_quarter(center, wheel, p))
                self.assertEqual(seconds[0], 2*orbit_count*p*(1-2*p))
                if p:
                    self.assertNotEqual(seconds[0], 2*orbit_count*p*(1-p))

    def test_signed_pair_error_and_fourier_convolution_algebra(self):
        center, wheel, p = 12, 2, Fraction(1, 4)
        units = unit_flags(center, wheel)
        model = tuple(2*x for x in units)
        self.assertEqual(convolve(model, model)[center], 2*center)
        for flags, _ in outcomes(center, wheel, p):
            actual = tuple(8*x for x in flags)
            residual = tuple(f-m for f, m in zip(actual, model))
            sum_weight = tuple(f+m for f, m in zip(actual, model))
            error = tuple(x-y for x, y in zip(convolve(actual, actual), convolve(model, model)))
            self.assertEqual(error[center], -2*center)
            self.assertEqual(error, convolve(residual, sum_weight))
            self.assertEqual(quarter_fourier(error),
                             tuple(multiply(v, s) for v, s in
                                   zip(quarter_fourier(residual), quarter_fourier(sum_weight))))

    def test_prefix_perturbation_budget_at_exact_fourier_frequencies(self):
        center, wheel, through = 12, 2, 3
        for flags, _ in outcomes(center, wheel, Fraction(1, 3)):
            for prefix in product((0, 1), repeat=through):
                changed = list(flags)
                for a, included in enumerate(prefix, 1):
                    changed[a] = included
                    if included:
                        changed[center-a] = 0
                difference = tuple(a-b for a, b in zip(changed, flags))
                changed_count = sum(abs(value) for value in difference)
                self.assertLessEqual(changed_count, 2*through)
                self.assertEqual(convolve(tuple(changed), tuple(changed))[center], 0)
                for real, imaginary in quarter_fourier(difference):
                    self.assertLessEqual(real*real+imaginary*imaginary, changed_count**2)

    def test_fourier_convention_and_exact_input_semantics(self):
        self.assertEqual(quarter_fourier((0, 1)), ((1, 0), (0, 1), (-1, 0), (0, -1)))
        self.assertEqual(quarter_fourier(()), ((0, 0),)*4)
        for bad in ((True,), (0.5,), (1, complex(0, 1))):
            with self.assertRaises(ValueError):
                quarter_fourier(bad)
        for p in (True, 0.5, Fraction(-1, 3), Fraction(2, 3)):
            with self.assertRaises(ValueError):
                reflection_variance_quarter(12, 2, p)
        for h, q in ((True, 2), (12, 3), (10, 2), (12, 0)):
            with self.assertRaises(ValueError):
                reflection_variance_quarter(h, q, Fraction(1, 4))
        self.assertIn("do not certify", quarter_fourier.__doc__)


if __name__ == "__main__":
    unittest.main()
