"""Exact guards for the positive cofactor sieve and actual affine transfer."""
from fractions import Fraction as F
from itertools import product
from math import gcd, prod
import unittest

from rough_cofactor_sieve_bridge import (
    RHO, primes_below, upper_beta_data, pointwise_sieve_identity,
    euler_sieve_identity, weighted_progression_identity,
    affine_inverse_phase, transfer_budget,
)
from exceptional_character_model import character_values


class RoughCofactorBridgeTests(unittest.TestCase):
    def test_pointwise_upper_sieve_and_first_failed_prefixes(self):
        strict_excess = False
        for level, cutoff, beta in ((100, 10, 2), (1000, 19, 2),
                                    (10000, 14, 3), (27, 8, 2)):
            primes = primes_below(cutoff)
            weights, failures = upper_beta_data(level, cutoff, beta)
            self.assertTrue(all(d < level and abs(v) == 1 for d, v in weights.items()))
            self.assertTrue(all(len(prefix) % 2 for prefix in failures))
            for bits in product((0, 1), repeat=len(primes)):
                n = prod(p for p, bit in zip(primes, bits) if bit)
                for value in (n, n*n):
                    sigma, rough, remainder = pointwise_sieve_identity(value, level, cutoff, beta)
                    self.assertEqual(sigma, rough+remainder)
                    self.assertGreaterEqual(sigma, rough)
                    strict_excess = strict_excess or sigma > rough
        self.assertTrue(strict_excess)

    def test_source_sign_correction_has_exact_nonzero_witness(self):
        weights, _ = upper_beta_data(100, 10, 2)
        self.assertEqual(weights, {1: 1, 2: -1, 3: -1, 6: 1})
        total, euler, remainder = euler_sieve_identity(100, 10, 2)
        self.assertEqual((total, euler, remainder), (F(1, 3), F(8, 35), F(11, 105)))
        self.assertEqual(total, euler+remainder)
        self.assertNotEqual(total, euler-remainder)
        self.assertEqual(pointwise_sieve_identity(5, 100, 10, 2), (1, 0, 1))
        for densities in ({2: F(1), 3: F(0), 5: F(2, 5), 7: F(3, 7)},
                           {2: F(1, 3), 3: F(1, 4), 5: F(1, 6), 7: F(1, 8)}):
            total, euler, remainder = euler_sieve_identity(100, 10, 2, densities)
            self.assertEqual(total, euler+remainder)
            self.assertGreaterEqual(remainder, 0)

    def test_both_sieve_cutoffs_are_strict(self):
        weights, failures = upper_beta_data(27, 7, 2)
        self.assertNotIn(3, weights)  # 3^(beta+1) equals the level.
        self.assertIn((3,), failures)
        self.assertEqual(pointwise_sieve_identity(7, 27, 7, 2), (1, 1, 0))
        self.assertEqual(primes_below(2), ())

    def test_weighted_progression_formula_including_prime_power_moduli(self):
        coefficients = {2: 2, 3: F(4, 3), 5: F(4, 5), 7: F(4, 7)}
        for start, ell in product((1, 7, 20, 101), (1, 2, 4, 9, 12, 25, 49, 121, 840)):
            direct, expanded, density, floor_budget = weighted_progression_identity(start, ell, coefficients)
            self.assertEqual(direct, expanded)
            self.assertLessEqual(abs(direct-start*density), floor_budget)
            # Average over a full common period gives exactly the predicted density.
        for ell in (1, 4, 9, 25, 11):
            start = 2*3*5*7*ell
            direct, _, density, _ = weighted_progression_identity(start, ell, coefficients)
            self.assertEqual(direct, start*density)

    def test_trimmed_density_fits_upper_beta_function_class(self):
        for c, p in product((F(0), F(1), F(4), F(11, 2), F(20)), (2, 3, 5, 7, 11, 23)):
            cp = c/p if p >= max(c, 2) else F(0)
            gp = (1+cp)/(p+cp)
            self.assertGreaterEqual(gp, F(1, p))
            self.assertLessEqual(gp, F(2, p))

    def test_affine_local_density_charges_small_primes_of_cofactor(self):
        witnessed_small_cofactor_prime = False
        for p, cofactor, target in product((3, 5, 7, 11), (3, 5, 9, 35, 77), (2, 12, 26)):
            if gcd(cofactor, target) != 1:
                continue
            roots = sum(n*(target-cofactor*n) % p == 0 for n in range(p))
            self.assertEqual(roots, 1 if cofactor*target % p == 0 else 2)
            if cofactor % p == 0:
                ratio = F(p-1, p-2)
                self.assertLessEqual(ratio, 1+F(3, p))
                witnessed_small_cofactor_prime = True
        self.assertTrue(witnessed_small_cofactor_prime)

    def test_affine_crt_phase_and_periodic_character_factor(self):
        for conductor, modulus, d1, cofactor, small, target, frequency in (
                (5, 12, 5, 7, 5, 22, 3), (7, 15, 2, 11, 4, 30, 2),
                (5, 8, 3, 9, 7, 18, 6), (13, 9, 2, 5, 4, 24, 3)):
            chi = character_values(conductor)
            phase = affine_inverse_phase(conductor, d1, cofactor, small, modulus, target, frequency)
            b0 = target*pow(cofactor*d1*small, -1, modulus) % modulus
            self.assertEqual(phase, -frequency*b0*pow(conductor, -1, modulus) % modulus)
            # Exact additive numerators in Z/(D*q), avoiding floating roots of unity.
            for gamma in range(conductor):
                b = next(n for n in range(conductor*modulus)
                         if n % modulus == b0 and n % conductor == modulus*gamma % conductor)
                self.assertEqual(-frequency*b % (conductor*modulus),
                                 (phase*conductor-frequency*gamma*modulus) % (conductor*modulus))
                expected = chi[d1*b % conductor]*chi[(target-cofactor*d1*small*b) % conductor]
                formula = chi[d1*modulus*gamma % conductor]*chi[
                    (target-cofactor*d1*small*modulus*gamma) % conductor]
                self.assertEqual(expected, formula)
                for shift_m, shift_a in ((conductor, 0), (0, conductor)):
                    shifted = chi[d1*modulus*gamma % conductor]*chi[
                        (target-(cofactor+shift_m)*d1*(small+shift_a)*modulus*gamma) % conductor]
                    self.assertEqual(formula, shifted)

    def test_mobius_expansion_does_not_make_native_unit_mask_optional(self):
        # M=3 shares target=6 and q0=9. A l0=3 Mobius term permits it,
        # and its original congruence can have solutions; inverse(M) cannot.
        self.assertTrue(any(3*n % 9 == 6 for n in range(9)))
        with self.assertRaises(ValueError):
            affine_inverse_phase(5, 1, 3, 1, 9, 6, 1)
        for bad in ((2, 1, 1, 1, 8), (5, 3, 1, 1, 9), (5, 1, 1, 3, 9)):
            with self.assertRaises(ValueError):
                affine_inverse_phase(*bad, 6, 1)

    def test_all_transfer_index_frequency_and_density_costs_fit(self):
        budget = transfer_budget()
        self.assertGreater(budget['frequency_margin'], 0)
        self.assertGreater(budget['period_margin'], 0)
        self.assertLess(budget['model_exponent'], budget['gcd_tail_exponent'])
        self.assertLess(budget['gcd_tail_exponent'], budget['claimed_exponent'])
        self.assertLess(budget['claimed_exponent'], 1)
        self.assertLess(budget['harmonic_error_exponent'], 0)
        self.assertLess(budget['unit_modulus_frequency_exponent'], 0)
        scale = 1+2*RHO
        for b in (F(1, 5), F(13, 25)):
            for x in (F(0), (1-b)/2):
                self.assertLessEqual(b/scale+2*x/scale, 1)
                self.assertLessEqual(b/scale, F(13, 25))
                if b/scale < F(1, 5):
                    # Direct linear route for the slightly extended lower edge.
                    exponent = min(b/scale, x/scale)+F(3, 4)+3*F(1, 4096)
                    self.assertLess(exponent, 1-F(1, 4096))
        self.assertLess(transfer_budget(F(1, 100))['period_margin'], 0)


if __name__ == '__main__':
    unittest.main()
