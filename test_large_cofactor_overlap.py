"""Exact cofactor, multiplicity, resonance and analytic-budget guards."""
from cmath import exp
from fractions import Fraction as F
from math import comb, gcd, pi, prod
import unittest

from detector_prime_product_transfer import (
    convolution_log_vector, full_mobius_log_vector, truncated_mobius_coefficient,
)
from large_cofactor_overlap import (
    coprimality_mobius_weight, large_cofactor_budgets,
    large_cofactor_log_vector, modulus_weight_vector, reflected_frequency_support,
)
from major_arc_kernel import _factorization, _mobius_phi
from short_divisor_overlap import complement_cofactor_coefficients, dual_support_indices
from unexceptional_vaughan_gate import _divisors, mangoldt_log_vector


def add_vectors(*vectors):
    out = {}
    for vector in vectors:
        for p, value in vector:
            out[p] = out.get(p, 0)+value
    return tuple((p, value) for p, value in sorted(out.items()) if value)


def expanded_vector(k, lower, cutoff):
    terms = []
    for d in _divisors(k):
        if d <= cutoff:
            for m in _divisors(k//d):
                if k//m >= lower:
                    terms.append(tuple((p, _mobius_phi(d)[0]*c)
                                       for p, c in mangoldt_log_vector(m)))
    return add_vectors(*terms)


def spectral_fixture(q, base_spacing):
    """Poisson algebra fixture only; not actual chi or prime/zero data."""
    total = F(0)
    for e in _divisors(q):
        spacing = base_spacing/e
        for j in dual_support_indices(spacing):
            x = j*spacing
            spectral_value = 16*(x-1)**2*(2-x)**2
            total += _mobius_phi(e)[0]*spacing*spectral_value
    return total


class LargeCofactorOverlapTests(unittest.TestCase):
    def test_reflected_fourier_support_has_the_negative_sign_and_ratio(self):
        self.assertEqual(reflected_frequency_support(F(1)), (-F(2), -F(1)))
        self.assertEqual(reflected_frequency_support(F(3, 2)), (-F(4, 3), -F(1)))
        self.assertEqual(reflected_frequency_support(F(2, 3)), (-F(2), -F(3, 2)))
        for ratio in (F(1, 3), F(1, 2), F(2), F(3)):
            self.assertIsNone(reflected_frequency_support(ratio))

    def test_reflected_residues_keep_the_target_dependent_phase(self):
        for target in (101, 102):
            for q in (2, 6, 30):
                for shift in (-7, -1, 0, 1, 6):
                    self.assertEqual(coprimality_mobius_weight(q, target+shift),
                                     int(gcd(q, target+shift) == 1))
            # q=2, base dual spacing3: only e=2,ell=-1 is resonant.
            # This is Fourier phase geometry, not actual primes/zeros.
            e, ell = 2, -1
            shifted_main = -F(3, 2)*exp(-2j*pi*ell*target/e)
            expected = -F(3, 2)*(-1)**target
            self.assertAlmostEqual(shifted_main.real, float(expected), places=10)
            self.assertAlmostEqual(shifted_main.imag, 0, places=10)

    def test_expansion_keeps_the_actual_cofactor_endpoint(self):
        for k in (49, 121, 210, 31*101, 31*49):
            for lower in (7, 8, 31, 32, 100):
                self.assertEqual(large_cofactor_log_vector(k, lower, 5),
                                 expanded_vector(k, lower, 5))
        self.assertNotEqual(large_cofactor_log_vector(49, 7, 5),
                            large_cofactor_log_vector(49, 8, 5))

    def test_left_prime_powers_and_their_modulus_weights_remain(self):
        # n=31,m=49 is admissible and contributes a second log7.
        self.assertEqual(large_cofactor_log_vector(31*49, 30, 5),
                         ((7, F(2)), (31, F(1))))
        self.assertEqual(modulus_weight_vector(49, 1, 49), ((7, 1),))
        self.assertEqual(modulus_weight_vector(49, 1, 48), ())

    def test_modulus_multiplicity_is_bounded_by_log_q(self):
        for q in (4, 8, 12, 30, 49, 60, 360, 2310):
            full = add_vectors(*(mangoldt_log_vector(m) for m in _divisors(q)))
            self.assertEqual(full, _factorization(q))
            logarithm = dict(_factorization(q))
            for cutoff in (1, 5, q):
                weighted = modulus_weight_vector(q, cutoff, q)
                self.assertTrue(all(0 <= c <= logarithm[p] for p, c in weighted))

    def test_reduced_residue_inversion_includes_zero_and_negative_shifts(self):
        for q in (1, 2, 6, 12, 30, 49):
            for shift in (-30, -7, -1, 0, 1, 6, 30):
                self.assertEqual(coprimality_mobius_weight(q, shift),
                                 int(gcd(q, shift) == 1))

    def test_resonant_main_is_not_silently_annihilated(self):
        self.assertEqual(spectral_fixture(2, F(3)), -F(3, 2))
        self.assertEqual(spectral_fixture(6, F(3)), -F(1))
        for q in (1, 2, 6, 30):
            self.assertEqual(spectral_fixture(q, F(2*q+1)), 0)

    def test_elementary_totient_and_divisor_bounds_need_no_coprimality(self):
        tau = lambda n: prod(e+1 for _, e in _factorization(n))
        for d in (1, 2, 4, 6, 12, 30):
            for m in (1, 2, 8, 9, 12, 49):
                self.assertGreaterEqual(_mobius_phi(d*m)[1],
                                        _mobius_phi(d)[1]*_mobius_phi(m)[1])
                self.assertLessEqual(tau(d*m), tau(d)*tau(m))
                self.assertLessEqual(F(d*m, _mobius_phi(d*m)[1]), tau(d*m))
                tau4 = prod(comb(e+3, 3) for _, e in _factorization(d*m))
                self.assertLessEqual(tau(d*m)**2, tau4)

    def test_bv_and_resonance_error_budgets_are_separate(self):
        budget = large_cofactor_budgets()
        self.assertEqual(budget['modulus_exponent'], F(499, 1000))
        self.assertEqual(budget['bv_level_gap'], F(1, 1000))
        self.assertEqual(budget['main_error'], (-F(1, 10), 9))
        self.assertEqual(budget['freeze_error'], (-F(9, 10), 5))
        self.assertEqual(budget['cutoff_error'], (-F(2), 5))
        self.assertEqual(budget['opposite_prime_power_error'], (-F(1, 4), 4))
        self.assertEqual(budget['distribution_log_error'], -11)
        t, h = F(9, 10), F(1, 10)
        self.assertEqual((2*t-1)+(-1-t)+1+h, 0)  # BV, with multiplicity log.
        self.assertEqual((2*t-1)+(-1-t)+1, -h)   # Reduced-residue main.
        self.assertEqual((2*t-1)+(-1-2*t)+1+h, -t)  # Freezing.
        self.assertEqual(large_cofactor_budgets(F(3, 5))['modulus_exponent'],
                         F(409, 1000))

    def test_core_complement_identity_keeps_all_unpaid_short_terms(self):
        lower, cutoff = 100, 5
        h = {n: F(truncated_mobius_coefficient(n, cutoff), 2)
             for n in range(17, 33)}  # Rational fixture, not actual damping.
        for k in (101, 31*101, 31**3, 37*101):
            remainder = complement_cofactor_coefficients(k, cutoff, h)
            core = {n: c for n, c in remainder.items() if n < lower}
            self.assertEqual(add_vectors(mangoldt_log_vector(k),
                                         convolution_log_vector(k, h),
                                         convolution_log_vector(k, core),
                                         large_cofactor_log_vector(k, lower, cutoff)),
                             full_mobius_log_vector(k, cutoff))
        self.assertNotEqual(convolution_log_vector(31*101,
                            {n: c for n, c in complement_cofactor_coefficients(
                             31*101, cutoff, h).items() if n < lower}), ())

    def test_invalid_or_unlicensed_levels_are_rejected(self):
        for action in (lambda: large_cofactor_budgets(F(509, 1000)),
                       lambda: large_cofactor_budgets(F(41, 100)),
                       lambda: large_cofactor_budgets(F(1)),
                       lambda: large_cofactor_log_vector(49, 1, 5),
                       lambda: modulus_weight_vector(0, 5, 10),
                       lambda: reflected_frequency_support(F(0)),
                       lambda: coprimality_mobius_weight(6, F(1))):
            with self.assertRaises(ValueError):
                action()


if __name__ == '__main__':
    unittest.main()
