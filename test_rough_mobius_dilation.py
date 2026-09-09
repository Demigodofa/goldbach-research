"""Exact reconstruction, signed cross terms and full moving-support guards."""
from fractions import Fraction as F
from math import gcd
import unittest

from major_arc_kernel import _factorization, _mobius_phi
from rough_mobius_dilation import block_energy, cofactor_rows, dilation_blocks
from specialized_sieve_coefficients import mobius_cofactor_terms


class RoughMobiusDilationTests(unittest.TestCase):
    def test_exact_prime_divisor_identity_with_different_factor_counts(self):
        values = {35: F(2, 3), 77: -2, 105: 5, 385: -3, 5005: F(7, 2)}
        blocks = dilation_blocks(values, 2)
        actual = sum(block_energy(rows)['sum'] for rows in blocks.values())
        direct = sum(_mobius_phi(r)[0]*value for r, value in values.items())
        self.assertEqual(actual, direct)
        for lower, rows in blocks.items():
            for s, prime_values in rows.items():
                for p, value in prime_values.items():
                    self.assertTrue(lower < p <= 2*lower)
                    self.assertEqual(gcd(p, s), 1)
                    self.assertEqual(value, values[p*s])
        # Omitting the exact denominator overcounts by omega(r).
        naive = sum(-_mobius_phi(s)[0]*sum(pv.values())
                    for rows in blocks.values() for s, pv in rows.items())
        self.assertNotEqual(naive, direct)

    def test_signed_cross_terms_can_cancel_and_can_reinforce(self):
        cancel = block_energy({3: {5: F(1), 7: F(-1)}})
        self.assertEqual((cancel['diagonal'], cancel['off_diagonal'], cancel['energy']),
                         (2, -2, 0))
        reinforce = block_energy({3: {5: F(1), 7: F(1)}})
        self.assertEqual((reinforce['diagonal'], reinforce['off_diagonal'],
                          reinforce['energy']), (2, 2, 4))
        self.assertGreater(reinforce['energy'], reinforce['diagonal'])
        for receipt in (cancel, reinforce):
            self.assertLessEqual(receipt['sum']**2, receipt['cauchy_bound_squared'])

    def test_full_localized_rows_and_coprime_pruning_keep_both_v_branches(self):
        x, y = 16004, 2
        weights = {10605: F(-3), 15015: F(5, 2), 10005: F(7)}
        rows = cofactor_rows(x, y, weights)
        self.assertTrue(any(v == 1 for _, v in rows))
        self.assertTrue(any(v > 1 for _, v in rows))
        direct = sum(sign*value for n, value in weights.items() if gcd(n, 2*x) == 1
                     for _, _, _, sign in mobius_cofactor_terms(n, y))
        expanded = F(0)
        for (t, v), values in rows.items():
            for lower, s_rows in dilation_blocks(values, y).items():
                receipt = block_energy(s_rows)
                expanded += receipt['sum']
                self.assertLessEqual(receipt['sum']**2, receipt['cauchy_bound_squared'])
                self.assertLessEqual(receipt['coefficient_norm'], F(x, t*v*lower))
                for s, pv in s_rows.items():
                    self.assertTrue(F(x, 4*t*v*lower) < s <= F(x, t*v*lower))
                    for p in pv:
                        n = t*v*p*s
                        self.assertEqual(gcd(n, 2*x), 1)
                        self.assertIn((t, p*s, v, _mobius_phi(p*s)[0]),
                                      mobius_cofactor_terms(n, y))
        self.assertEqual(expanded, direct)
        # A common factor with N is removed only by the proved summed estimate.
        self.assertTrue(cofactor_rows(16005, y, weights, coprime=False))
        self.assertEqual(cofactor_rows(16005, y, weights), {})

    def test_same_mask_four_term_centering_and_linked_prime_relation(self):
        N, c, p, q, s = 32008, 3, 5, 7, 11
        q1, q2 = N-c*p*s, N-c*q*s
        self.assertEqual(q*q1-p*q2, (q-p)*N)
        for mask_p, mask_q in ((1, 1), (0, 1), (1, 0)):
            a_p, a_q, b_p, b_q = 7, 11, F(3, 2), F(5, 2)
            self.assertEqual(mask_p*mask_q*(a_p-b_p)*(a_q-b_q),
                             mask_p*mask_q*(a_p*a_q-a_p*b_q-b_p*a_q+b_p*b_q))

    def test_forbidden_support_is_rejected_and_empty_rows_are_zero(self):
        for bad in ({1: 1}, {9: 1}, {15: 1}):
            with self.assertRaises(ValueError):
                dilation_blocks(bad, 3)
        with self.assertRaises(ValueError):
            block_energy({5: {5: 1}})
        with self.assertRaises(ValueError):
            cofactor_rows(100, 2, {50: 1})
        self.assertEqual(dilation_blocks({}, 2), {})
        self.assertEqual(block_energy({})['sum'], 0)


if __name__ == '__main__':
    unittest.main()
