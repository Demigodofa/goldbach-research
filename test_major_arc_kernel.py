"""Exact kernel controls, including the source majorant's square obstruction."""
from fractions import Fraction
from math import gcd
import unittest

from exceptional_character_model import character_values
from major_arc_kernel import radical, ramanujan, sampled_kernel
from redistribution import trial_prime


def prime_power_ramanujan(q, n):
    value = 1
    for p in range(2, q+1):
        if not trial_prime(p) or q % p:
            continue
        power = p
        while q % (power*p) == 0:
            power *= p
        if n % power == 0:
            value *= power-power//p
        elif n % (power//p) == 0:
            value *= -power//p
        else:
            return 0
    return value


class MajorArcKernelTests(unittest.TestCase):
    def test_ramanujan_divisor_formula_against_prime_power_evaluation(self):
        for q in range(1, 49):
            for n in range(-48, 49):
                self.assertEqual(ramanujan(q, n), prime_power_ramanujan(q, n))

    def test_radical_invariance_for_arbitrary_rational_cutoff_samples(self):
        samples = tuple(Fraction((k*7) % 11-5, k+1) for k in range(41))
        for n in (1, 4, 8, 9, 25, 27, 49, 72, 121, 225, 1000):
            for conductor in range(1, 13):
                self.assertEqual(sampled_kernel(n, conductor, samples),
                                 sampled_kernel(radical(n), conductor, samples))
                self.assertEqual(gcd(n, conductor) == 1, gcd(radical(n), conductor) == 1)

    def test_literal_squarefree_majorant_cannot_bound_the_kernel(self):
        # For R=2: G(0)=G(1)=1, G(2)=0, and the sample at log_2(3)
        # may be any nonnegative value. The printed H_R(25) is identically
        # zero because h_xi is stated to have squarefree support.
        self.assertNotEqual(radical(25), 25)
        literal_majorant_at_25 = 0
        for middle in (0, Fraction(1, 2), 1, 3):
            samples = (0, 1, 1, middle, 0)
            value = sampled_kernel(25, 1, samples)
            self.assertEqual(value, 2+Fraction(middle, 2))
            self.assertGreaterEqual(value, 2)
            self.assertGreater(value, literal_majorant_at_25)
        # Even after radical repair a unit constant is unjustified:
        # H_2(rad25)=4*log(2)/9 <4/9 <2. The analytic claim uses <<_G.
        self.assertLess(Fraction(4, 9), 2)

    def test_character_reconstruction_and_necessary_rough_support(self):
        # All primitive characters of conductors <=4: one each at1,3,4.
        characters = [(1, (1,), 1), (3, character_values(3), 2),
                      (4, character_values(4), 2)]
        for samples in ((0, 1, 1, Fraction(1, 3), 0), (0, 2, -1, 3, 4)):
            for n in range(1, 49):
                for m in (5, 7, 11, 13):
                    direct = sum(samples[q]*ramanujan(q, n-m) for q in range(1, 5))
                    reconstructed = sum(chi[n % r]*chi[m % r]*Fraction(r, phi)*
                                        sampled_kernel(n, r, samples)
                                        for r, chi, phi in characters)
                    self.assertEqual(direct, reconstructed)
        samples = (0, 1, 1)
        direct_at_nonrough_input = sum(samples[q]*ramanujan(q, 1-2) for q in (1, 2))
        self.assertEqual(direct_at_nonrough_input, 0)
        self.assertEqual(sampled_kernel(1, 1, samples), 2)

    def test_finite_sample_contract(self):
        for n in (0, -1, True):
            with self.assertRaises(ValueError):
                radical(n)
        for samples in ((0,), (0, 0.5), (0, True)):
            with self.assertRaises(ValueError):
                sampled_kernel(25, 1, samples)
        self.assertIn("does not certify", sampled_kernel.__doc__)


if __name__ == "__main__":
    unittest.main()
