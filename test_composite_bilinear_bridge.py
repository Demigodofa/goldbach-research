"""Exact identities only; these tests do not prove the bilinear hypothesis."""
from fractions import Fraction as F
from math import gcd
import unittest

from composite_bilinear_bridge import (exceptional_multiple_witness,
                                      rough_normalization, vaughan_parts)
from exceptional_character_model import character_values
from redistribution import trial_prime


class CompositeBilinearTests(unittest.TestCase):
    def test_formal_vaughan_identity_for_dense_signed_rational_inputs(self):
        for limit in (1, 2, 12, 60):
            values = [0, 0]+[F((-1)**n*(n % 7), n % 3+1) for n in range(2, limit+1)]
            for u, v in ((1, 1), (limit, 1), (1, limit), (limit, limit),
                         (max(1, limit//3), max(1, limit//4))):
                a, b, c, d = vaughan_parts(values, u, v)
                self.assertEqual([a[n]+b[n]-c[n]+d[n] for n in range(limit+1)], values)
                # The last term has two factors respectively>u and>v.
                self.assertTrue(all(not d[n] for n in range(min(limit+1, (u+1)*(v+1)))))

    def test_prime_power_terms_are_not_erased_and_prime_indices_have_no_last_term(self):
        limit = 200
        values = [0]*(limit+1)
        for p in range(2, limit+1):
            if trial_prime(p):
                power = p
                while power <= limit:
                    values[power] = p  # Formal exact weight replacing log p.
                    power *= p
        a, b, c, d = vaughan_parts(values, 5, 7)
        reconstructed = [a[n]+b[n]-c[n]+d[n] for n in range(limit+1)]
        self.assertEqual(reconstructed, values)
        self.assertEqual((reconstructed[9], reconstructed[25], reconstructed[49]), (3, 5, 7))
        self.assertTrue(all(d[p] == 0 for p in range(2, limit+1) if trial_prime(p)))
        weights = [F((n % 5)-2, 3) for n in range(limit+1)]
        self.assertEqual(sum(weights[n]*reconstructed[n] for n in range(limit+1)),
                         sum(weights[n]*values[n] for n in range(limit+1)))

    def test_local_normalization_against_independent_complete_residue_counts(self):
        for cutoff in (2, 3, 5, 7):
            modulus = 1
            for p in range(2, cutoff+1):
                if trial_prime(p):
                    modulus *= p
            units = sum(gcd(a, modulus) == 1 for a in range(modulus))
            for target in range(6, 42, 2):
                c, v, singular = rough_normalization(target, cutoff)
                paired = sum(gcd(a, modulus) == gcd(target-a, modulus) == 1
                             for a in range(modulus))
                self.assertEqual(c, F(modulus, units))
                self.assertEqual(c*v, singular)
                self.assertEqual(singular, F(paired*modulus, units*units))

    def test_input_meanings_and_exact_type_checks(self):
        for values in ((), [], [0], [0, 1], [0, False], [0, 0, 0.5]):
            with self.assertRaises(ValueError):
                vaughan_parts(values, 1, 1)
        for u, v in ((True, 1), (0, 1), (1, 4), (1, 1.0)):
            with self.assertRaises(ValueError):
                vaughan_parts([0, 0, 1], u, v)
        for target, cutoff in ((7, 2), (True, 2), (6, True), (6, 1), (6, 3.0)):
            with self.assertRaises(ValueError):
                rough_normalization(target, cutoff)
        self.assertIn("NOT asserted to be Lambda", vaughan_parts.__doc__)

    def test_exceptional_offsets_against_complete_character_correlations(self):
        observed = set()
        for conductor, sign in ((29, 1), (31, 1), (33, 1), (35, 1), (40, 1),
                                (40, -1), (60, 1), (65, 1), (120, 1),
                                (120, -1), (280, 1), (280, -1), (385, 1)):
            target, offset = exceptional_multiple_witness(conductor, two_sign=sign)
            self.assertGreaterEqual(target, conductor**12)
            self.assertLess(target, conductor**12+2*conductor)
            self.assertEqual(target % (2*conductor), 0)
            self.assertGreater(F(target, 4), conductor**10)
            chi = character_values(conductor, two_sign=sign)
            units = sum(value != 0 for value in chi)
            correlation = sum(chi[a]*chi[(target-a) % conductor]
                              for a in range(conductor))
            self.assertEqual(offset, F(correlation, 4*units))
            self.assertEqual(offset, F(chi[-1], 4))
            observed.add(offset)
        self.assertEqual(observed, {F(-1, 4), F(1, 4)})
        # The positive discrepancy also occurs when the suppression family
        # is empty. These are formal residue controls, not detected zeros.
        self.assertEqual(exceptional_multiple_witness(29)[1], F(1, 4))
        self.assertEqual(exceptional_multiple_witness(31)[1], F(-1, 4))

    def test_exceptional_witness_rejects_invalid_conductors_and_claims_no_zero(self):
        for conductor in (True, 24, 25, 27, 30, 32, 36, 40.0, 45):
            with self.assertRaises(ValueError):
                exceptional_multiple_witness(conductor)
        for conductor, sign in ((31, -1), (40, True), (40, 0)):
            with self.assertRaises(ValueError):
                exceptional_multiple_witness(conductor, two_sign=sign)
        self.assertIn("not an actual computed J_N value", exceptional_multiple_witness.__doc__)


if __name__ == "__main__":
    unittest.main()
