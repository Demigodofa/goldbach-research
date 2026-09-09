"""Exact support and local-algebra tests; no exceptional-zero experiment."""
from fractions import Fraction as F
from math import gcd
import unittest

from prime_cutoff_bridge import (
    affine_log_coefficients, cutoff_witnesses, nonzero_mode_budget, source_multiplier,
)
from rare_divisor_calibration import lambda_w_identity


def _lambda_and_w(n, conductor):
    _, lam, twice_w, _ = lambda_w_identity(n, conductor)
    return lam, dict((p, coefficient/2) for p, coefficient in twice_w)


class PrimeCutoffBridgeTests(unittest.TestCase):
    def test_both_signs_and_both_weight_placements_by_complete_residues(self):
        for D, m, sign in ((31, 62, 1), (33, 22, 1), (40, 20, 1),
                           (40, 40, -1), (120, 20, 1)):
            for r in (5, 7, 13, 19):
                for a, c in ((1, 1), (7, 11), (13, 17)):
                    if gcd(r*a, c) != 1 or gcd(r*a*c, D) != 1:
                        continue
                    direct, predicted = affine_log_coefficients(D, m, r, a, c, two_sign=sign)
                    self.assertEqual(direct, predicted)
                    self.assertEqual(direct[:2], direct[2:4])

    def test_sign_changes_number_of_harmonic_cancellations(self):
        positive, _ = affine_log_coefficients(31, 62, 5, 1, 1)
        negative, _ = affine_log_coefficients(31, 62, 13, 1, 1)
        self.assertEqual(positive, (F(30, 31), F(-60, 31), F(30, 31), F(-60, 31), 0))
        self.assertEqual(negative, (F(30, 31), 0, F(30, 31), 0, F(60, 31)))
        signed, _ = affine_log_coefficients(31, 62, 5, 13, 7)
        self.assertLess(signed[0], 0)  # no boxwise absolute main recombination

    def test_three_exact_factorization_identities_from_divisor_convolution(self):
        x, n = 95, 91  # 5*19 and 7*13; target186 is suppressed modulo31
        witnesses = cutoff_witnesses(x, n, 31, 5, 13)
        self.assertEqual(witnesses, (('positive_first', 5, 19),
                                    ('positive_partner', 7, 13),
                                    ('negative_partner', 13, 7)))
        lam_x, _ = _lambda_and_w(x, 31)
        _, w_n = _lambda_and_w(n, 31)
        original = {p: F(lam_x, 2)*v for p, v in w_n.items()}
        self.assertEqual(original, {13: F(4)})  # common outside log(x) omitted
        for kind, r, q in witnesses:
            lam_q, w_q = _lambda_and_w(q, 31)
            if kind == 'positive_first':
                transformed = {p: lam_q*v for p, v in w_n.items()}
                self.assertEqual(r*q+n, x+n)
            elif kind == 'positive_partner':
                transformed = {p: lam_x*v for p, v in w_q.items()}
                self.assertEqual(x+r*q, x+n)
            else:
                transformed = {r: F(lam_x*lam_q, 2)}
                self.assertEqual(x+r*q, x+n)
            self.assertEqual(transformed, original)

    def test_union_cover_is_not_a_disjoint_partition(self):
        witnesses = cutoff_witnesses(95, 91, 31, 5, 13)
        self.assertEqual(len(witnesses), 3)
        # Each exact transformed summand equals the original nonzero weight.
        # Their sum is an upper bound, not an equality with the difference.
        _, w_n = _lambda_and_w(91, 31)
        self.assertGreater(len(witnesses)*w_n[13], w_n[13])

    def test_zero_weights_and_no_intermediate_factor_require_no_witness(self):
        self.assertEqual(cutoff_witnesses(97, 957, 31, 3, 29), ())  # three negatives in n
        self.assertEqual(cutoff_witnesses(95, 91, 31, 3, 4), ())    # both > old cutoff
        self.assertEqual(cutoff_witnesses(91, 95, 31, 5, 13), ())  # lambda(first)=0

    def test_strict_old_and_nonstrict_dynamic_endpoints_are_preserved(self):
        self.assertEqual(cutoff_witnesses(95, 91, 31, 5, 5),
                         (('positive_first', 5, 19),))
        with self.assertRaises(ValueError):
            cutoff_witnesses(95, 91, 31, 6, 13)

    def test_fixed_margin_and_invalid_inverse_guards(self):
        for theta in (F(1, 1000), F(1, 10), F(199, 1000)):
            exponent, margin = nonzero_mode_budget(theta)
            self.assertEqual(exponent+margin, 1)
            self.assertGreater(margin, F(1, 45))
        for theta in (F(0), F(1, 5), 0.1, True):
            with self.assertRaises(ValueError):
                nonzero_mode_budget(theta)
        for args in ((31, 62, 7, 1, 7), (31, 62, 31, 1, 1), (31, 2, 5, 1, 1)):
            with self.assertRaises(ValueError):
                affine_log_coefficients(*args)

    def test_squareful_and_shared_terms_cannot_use_squarefree_identities(self):
        for first, partner in ((95, 49*13), (95, 5*13)):
            with self.assertRaises(ValueError):
                cutoff_witnesses(first, partner, 31, 3, 13)

    def test_source_multiplier_has_no_missing_near_zero_residue_class(self):
        witnessed = set()
        for D, sign in ((31, 1), (33, 1), (40, 1), (40, -1), (105, 1), (120, 1)):
            for m in range(2, 2*D+1, 2):
                (A, B, C), actual, source = source_multiplier(D, m, two_sign=sign)
                self.assertEqual(actual, source)
                self.assertGreater(A, 0)
                self.assertLessEqual(actual, 2)
                if actual == 0:
                    self.assertEqual((B, C), (0, -A))
                else:
                    self.assertGreaterEqual(actual, F(2, 3))
                witnessed.add(actual)
        self.assertTrue({F(0), F(2, 3), F(1), F(2)} <= witnessed)
        self.assertEqual(source_multiplier(105, 42)[1], F(2, 3))


if __name__ == '__main__':
    unittest.main()
