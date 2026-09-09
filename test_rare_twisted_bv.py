"""Exact conductor and residue controls; no numerical BV or zero assertion."""
from fractions import Fraction as F
from math import gcd, lcm
import unittest

from exceptional_character_model import character_values
from major_arc_kernel import _mobius_phi
from rare_twisted_bv import inflation_fibres, suppressed_prime_progression, twist_primitive_character


class RareTwistedBVTests(unittest.TestCase):
    def test_primitive_twist_involution_and_conductor_cancellation(self):
        inputs = ((1, 1), (3, 1), (4, 1), (5, 1), (8, 1), (8, -1),
                  (11, 1), (15, 1), (31, 1), (33, 1), (40, 1), (40, -1))
        for conductor, sign in ((31, 1), (33, 1), (40, 1), (40, -1), (105, 1)):
            signatures = set()
            fixed = character_values(conductor, two_sign=sign)
            for incoming, incoming_sign in inputs:
                period, transformed, values = twist_primitive_character(
                    conductor, incoming, two_sign=sign, incoming_two_sign=incoming_sign)
                original = (1,) if incoming == 1 else character_values(incoming, two_sign=incoming_sign)
                self.assertEqual(period, lcm(conductor, incoming))
                self.assertEqual(period % transformed, 0)
                self.assertTrue(all(values[a % transformed] == fixed[a % conductor]*original[a % incoming]
                                    for a in range(period) if gcd(a, period) == 1))
                self.assertNotIn((transformed, values), signatures)
                signatures.add((transformed, values))
                transformed_sign = 1
                if transformed > 1 and character_values(transformed) != values:
                    transformed_sign = -1
                    self.assertEqual(character_values(transformed, two_sign=-1), values)
                _, back, back_values = twist_primitive_character(
                    conductor, transformed, two_sign=sign, incoming_two_sign=transformed_sign)
                self.assertEqual((back, back_values), (incoming, original))
        self.assertEqual(twist_primitive_character(31, 31)[1:], (1, (1,)))
        self.assertEqual(twist_primitive_character(105, 3)[1], 35)
        self.assertEqual(twist_primitive_character(40, 40, incoming_two_sign=-1)[1], 4)

    def test_complex_quartic_twists_remain_distinct_and_involutive(self):
        # Exact Gaussian integer coordinates: no rounded roots of unity.
        zero, one = (0, 0), (1, 0)
        characters = ((zero, one, one, one, one),
                      (zero, one, (-1, 0), (-1, 0), one),
                      (zero, one, (0, 1), (0, -1), (-1, 0)),
                      (zero, one, (0, -1), (0, 1), (-1, 0)))
        fixed = character_values(35)
        units = [a for a in range(35) if gcd(a, 35) == 1]
        signatures = set()
        for incoming, expected_conductor in zip(characters, (35, 7, 35, 35)):
            transformed = tuple(tuple(fixed[a]*component for component in incoming[a % 5])
                                for a in units)
            self.assertNotIn(transformed, signatures)
            signatures.add(transformed)
            self.assertEqual(tuple(tuple(fixed[a]*component for component in value)
                                   for a, value in zip(units, transformed)),
                             tuple(incoming[a % 5] for a in units))
            possible = []
            for divisor in (1, 5, 7, 35):
                buckets = {}
                for a, value in zip(units, transformed):
                    buckets.setdefault(a % divisor, set()).add(value)
                if all(len(values) == 1 for values in buckets.values()):
                    possible.append(divisor)
            self.assertEqual(min(possible), expected_conductor)

    def test_inflation_fibres_and_totient_weight_capacity(self):
        for conductor in (1, 31, 33, 40, 105):
            fibres = inflation_fibres(conductor, 160)
            self.assertEqual(sorted(d for _, ds in fibres for d in ds), list(range(1, 161)))
            divisor_count = sum(conductor % d == 0 for d in range(1, conductor+1))
            saw_multiple = False
            for ell, ds in fibres:
                self.assertLessEqual(len(ds), divisor_count)
                phi_ell = _mobius_phi(ell)[1]
                saw_multiple |= len(ds) > 1
                for d in ds:
                    self.assertEqual(lcm(conductor, d), ell)
                    self.assertEqual(conductor % (ell//d), 0)
                    self.assertLessEqual(F(phi_ell, _mobius_phi(d)[1]), conductor)
                self.assertLessEqual(sum((F(1, _mobius_phi(d)[1]) for d in ds), F(0)),
                                     F(conductor*divisor_count, phi_ell))
            if conductor > 1:
                self.assertTrue(saw_multiple)

    def test_modulus_three_filter_exactly_recovers_allowed_positive_units(self):
        for conductor, target, sign in ((31, 62, 1), (33, 22, 1), (33, 66, 1),
                                        (40, 20, 1), (40, 40, -1), (120, 20, 1)):
            chi = character_values(conductor, two_sign=sign)
            try:
                b, residue, coefficient = suppressed_prime_progression(conductor, target, two_sign=sign)
            except ValueError:
                # 33,66 is deliberately outside F_D; it must not borrow the rule.
                self.assertEqual((conductor, target), (33, 66))
                continue
            self.assertIn(b, (1, 3))
            self.assertEqual(coefficient, F(1, 2*_mobius_phi(b)[1]))
            for a in range(conductor):
                if chi[a] == 0:
                    continue
                direct = int(chi[a] == 1 and gcd(target-a, conductor) == 1)
                projected = int(a % b == residue)*F(1+chi[a], 2)
                self.assertEqual(projected, direct)
        self.assertEqual(suppressed_prime_progression(33, 22), (3, 2, F(1, 4)))
        self.assertEqual(suppressed_prime_progression(31, 62), (1, 0, F(1, 2)))

    def test_domain_and_finite_verifier_limits(self):
        for args in ((True, 1), (25, 1), (31, True), (31, 2), (31, 0),
                     (31, 1.0), (1009, 1013), (10001, 1)):
            with self.assertRaises(ValueError):
                twist_primitive_character(*args)
        for incoming_sign in (True, -1):
            with self.assertRaises(ValueError):
                twist_primitive_character(31, incoming_two_sign=incoming_sign)
        for args in ((0, 10), (31, 0), (True, 10), (31, 1.0), (1001, 10), (31, 10001)):
            with self.assertRaises(ValueError):
                inflation_fibres(*args)
        for args in ((24, 0), (25, 0), (31, 2), (33, 11)):
            with self.assertRaises(ValueError):
                suppressed_prime_progression(*args)


if __name__ == "__main__":
    unittest.main()
