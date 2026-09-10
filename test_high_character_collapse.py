import unittest
from fractions import Fraction as F
from math import gcd

from high_character_collapse import (gauss_collapse, high_projector,
                                     nonprincipal_orthogonality,
                                     source_target_after_collapse)


class HighCharacterCollapseTests(unittest.TestCase):
    def test_nonprincipal_character_orthogonality_exactly(self):
        for m in (3, 5, 7, 11, 13, 17, 19):
            for p in range(1, m):
                for a in range(1, m):
                    expected = m - 2 if p == a else -1
                    self.assertEqual(nonprincipal_orthogonality(m, p, a),
                                     expected)

    def test_prime_gauss_family_collapses_to_additive_phase(self):
        for m in (3, 5, 7, 11, 13, 17):
            for p in range(1, m):
                for c in range(1, m):
                    self.assertEqual(*gauss_collapse(m, p, c))

    def test_high_projector_is_full_minus_low(self):
        for d, m in ((1, 5), (2, 5), (3, 5), (4, 7), (5, 7)):
            q = d * m
            units = [value for value in range(1, q + 1)
                     if gcd(value, q) == 1]
            for p in units:
                for residue in units:
                    expected = (F(int((p - residue) % q == 0))
                                - F(int((p - residue) % d == 0), m - 1))
                    self.assertEqual(high_projector(d, m, residue, p),
                                     expected)

    def test_high_projector_has_zero_residue_mean(self):
        for d, m in ((1, 5), (2, 5), (3, 5), (4, 7), (5, 7)):
            q = d * m
            units = [value for value in range(1, q + 1)
                     if gcd(value, q) == 1]
            for p in units:
                self.assertEqual(sum(high_projector(d, m, a, p)
                                     for a in units), 0)

    def test_no_cancellation_estimate_is_smuggled_in(self):
        target = source_target_after_collapse()
        self.assertTrue(target["high_family_equals_full_minus_low"])
        self.assertTrue(target["ordinary_additive_prime_phase_remains"])
        self.assertFalse(target["kloosterman_sum_created_by_orthogonality"])
        self.assertFalse(target["joint_m_h_cancellation_proved"])
        self.assertFalse(target["endpoint_and_mask_leakage_paid"])


if __name__ == "__main__":
    unittest.main()
