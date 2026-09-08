"""Exact CRT projection controls; none of the model means are Goldbach counts."""
from fractions import Fraction
from math import gcd, prod
import unittest

from exceptional_character_model import character_values
from joint_residue_model import (coprime_product_profile, crt_pair_floor,
                                 joint_product_profile, unit_projection)
from product_resolution import atomic_cap_distance, field_product_pairs, jacobi_pair_floor
from redistribution import trial_prime


def uniform(modulus):
    return tuple(int(gcd(a, modulus) == 1) for a in range(modulus))


def character_density(modulus, amplitude=1):
    chi = character_values(modulus)
    return tuple(1+amplitude*c if c else 0 for c in chi)


def residue_pair_mean(values, target):
    modulus = len(values)
    phi = sum(gcd(a, modulus) == 1 for a in range(modulus))
    return sum((values[a]*values[(target-a) % modulus] for a in range(modulus)),
               Fraction(0))/phi


class JointResidueTests(unittest.TestCase):
    def test_all_proper_joint_projections_cannot_determine_positivity(self):
        for modulus in (21, 273):
            target = 2*(modulus//3)
            density = character_density(modulus)
            g, pairs = joint_product_profile(density, density, target)
            flat, flat_pairs = joint_product_profile(uniform(modulus), uniform(modulus), target)
            self.assertEqual(g, density)
            self.assertEqual(pairs, 0)
            self.assertEqual(flat, uniform(modulus))
            self.assertEqual(flat_pairs, Fraction(1, 2))
            for divisor in range(1, modulus):
                if modulus % divisor:
                    continue
                projected = unit_projection(g, divisor)
                self.assertEqual(projected, uniform(divisor))
                self.assertEqual(projected, unit_projection(flat, divisor))
                self.assertEqual(residue_pair_mean(projected, target),
                                 Fraction(1, 2) if divisor % 3 == 0 else 1)
        # The model's zero at14 is not an absence of an actual prime pair.
        self.assertEqual(3+11, 14)

    def test_sharp_positive_floor_and_inverse_distance(self):
        # In U_5, u=+1 on {1,2} and -1 on {3,4}; a skew four-cycle.
        u5 = (0, 1, 1, -1, -1)
        chi3 = (0, 1, -1)
        first15 = tuple(1+chi3[a % 3]*u5[a % 5] if gcd(a, 15) == 1 else 0
                        for a in range(15))
        _, pairs15 = joint_product_profile(first15, first15, 10)
        self.assertEqual(pairs15, Fraction(1, 4))
        chi = character_values(21)
        phi = sum(bool(c) for c in chi)
        for b in (0, Fraction(1, 2), Fraction(3, 4), Fraction(-3, 4), Fraction(7, 8), 1):
            first, second = character_density(21), character_density(21, b)
            g, pairs = joint_product_profile(first, second, 14)
            self.assertEqual(g, second)
            self.assertEqual(pairs, (1-b*b)/Fraction(2))
            if pairs < Fraction(1, 4):
                sign = 1 if b > 0 else -1
                nearest = character_density(21, sign)
                distance = Fraction(sum(abs(a-c) for a, c in zip(second, nearest)), phi)
                self.assertEqual(distance, 1-abs(b))
                self.assertEqual((1-distance)**2, 1-2*pairs)

    def test_asymmetric_nonbinary_inputs_and_independent_crt_reduction(self):
        checked_inverse = 0
        for primes in ((5,), (7,), (5, 7)):
            q = prod(primes)
            modulus = 3*q
            units_q = [a for a in range(q) if gcd(a, q) == 1]
            chi_q = character_values(q)
            chi_d = character_values(modulus)
            local = []
            for shift in (0, 1):
                local.append(tuple(prod(1 if (a % p-1+shift) % (p-1) < (p-1)//2 else -1
                                        for p in primes) if gcd(a, q) == 1 else 0
                                   for a in range(q)))
            profiles = (local[0], local[1], chi_q,
                        tuple((9*c+h)/Fraction(10) for c, h in zip(chi_q, local[0])))
            for u1, u2 in ((profiles[0], profiles[1]), (profiles[2], profiles[3]),
                           (profiles[3], profiles[1])):
                def lift(u):
                    return tuple(1+(1 if a % 3 == 1 else -1)*u[a % q]
                                 if gcd(a, modulus) == 1 else 0 for a in range(modulus))
                first, second = lift(u1), lift(u2)
                g, pairs = joint_product_profile(first, second, 2*q)
                # Independent inverse-product sum only on the Q-coordinate.
                w = {v: sum((u1[a]*u2[v*pow(a, -1, q) % q] for a in units_q),
                            Fraction(0))/len(units_q) for v in units_q}
                self.assertEqual(sum(w.values()), 0)
                for a in range(modulus):
                    expected = (1+(1 if a % 3 == 1 else -1)*w[a % q]
                                if gcd(a, modulus) == 1 else 0)
                    self.assertEqual(g[a], expected)
                correlation = sum(w[v]*w[-v % q] for v in units_q)/len(units_q)
                self.assertEqual(2*pairs, 1+correlation)
                if chi_q[-1] == 1:
                    self.assertGreaterEqual(pairs, Fraction(1, 4))
                else:
                    phi = 2*len(units_q)
                    a1, a2 = (Fraction(sum(v*c for v, c in zip(f, chi_d)), phi)
                              for f in (first, second))
                    x, y = a1*a1, a2*a2
                    self.assertGreaterEqual(2*pairs, 1-x*y-(1-x)*(1-y)/2)
                    if pairs < Fraction(1, 4):
                        checked_inverse += 1
                        for f, coefficient in ((first, a1), (second, a2)):
                            self.assertGreaterEqual(coefficient*coefficient, 1-2*pairs)
                            nearest = character_density(modulus, 1 if coefficient > 0 else -1)
                            distance = Fraction(sum(abs(a-b) for a, b in zip(f, nearest)), phi)
                            self.assertEqual(distance, 1-abs(coefficient))
                            self.assertLessEqual(distance, 2*pairs)
        self.assertGreaterEqual(checked_inverse, 2)

    def test_projection_towers_and_single_prime_premise_is_insufficient(self):
        density = character_density(273)
        for d1, d2 in ((91, 7), (39, 3), (21, 7)):
            self.assertEqual(unit_projection(unit_projection(density, d1), d2),
                             unit_projection(density, d2))
        self.assertEqual(unit_projection(uniform(9), 3), uniform(3))
        # D=3*7*11 has chi_Q(-1)=+1, but a lower-conductor interaction
        # chi_3*chi_7 defeats the positive floor if only single primes are checked.
        chi21 = character_values(21)
        lower = tuple(1+chi21[a % 21] if gcd(a, 231) == 1 else 0 for a in range(231))
        for p in (3, 7, 11):
            self.assertEqual(unit_projection(lower, p), uniform(p))
        self.assertNotEqual(unit_projection(lower, 21), uniform(21))
        # lower*lower=lower by multiplicative character orthogonality.
        self.assertEqual(residue_pair_mean(lower, 154), 0)
        with self.assertRaisesRegex(ValueError, "proper-divisor"):
            joint_product_profile(lower, lower, 154)

    def test_coprime_composite_target_bound_without_uniform_marginals(self):
        for modulus, primes in ((7, (7,)), (77, (7, 11)), (91, (7, 13)), (143, (11, 13))):
            units = [a for a in range(modulus) if gcd(a, modulus) == 1]
            first, second = [0]*modulus, [0]*modulus
            for i, a in enumerate(units):
                first[a] = 2*int(a % 7 in (1, 2, 3) if modulus % 7 == 0 else i < len(units)//2)
                second[a] = Fraction(2*int(i < len(units)//2)+1, 2)
            first, second = tuple(first), tuple(second)
            g, pair2 = coprime_product_profile(first, second, 2)
            self.assertEqual(pair2, residue_pair_mean(g, 2))
            if modulus == 77:
                self.assertNotEqual(unit_projection(first, 7), uniform(7))
            if modulus == 7:
                self.assertEqual((g, pair2),
                                 (field_product_pairs(first[1:], second[1:])[0],
                                  field_product_pairs(first[1:], second[1:])[1][2]))
                self.assertEqual(crt_pair_floor(7), jacobi_pair_floor(7))
            for a in (1, 2, modulus-1):
                direct = sum((first[b]*second[a*pow(b, -1, modulus) % modulus] for b in units),
                             Fraction(0))/len(units)
                self.assertEqual(g[a], direct)
            p0 = min(primes)
            theta = Fraction(prod(p-2 for p in primes), len(units))
            for target in units:
                value = residue_pair_mean(g, target)
                self.assertGreaterEqual(value, crt_pair_floor(modulus))
                self.assertGreater(value, 0)
                residual = (p0-2)*abs(value-theta)/theta-2
                if residual > 0:
                    self.assertLessEqual(residual*residual, p0)

    def test_local_caps_are_not_global_caps_and_atomic_resolution_gap(self):
        modulus, primes = 1001, (7, 11, 13)
        local_chi = [character_values(p) for p in primes]
        high_density = tuple(4*int(len({chi[a % p] for p, chi in zip(primes, local_chi)}) == 1)
                             if gcd(a, modulus) == 1 else 0 for a in range(modulus))
        phi = prod(p-1 for p in primes)
        self.assertEqual(sum(high_density), phi)
        self.assertEqual(max(high_density), 4)
        for p in primes:
            for residue in range(1, p):
                conditional = Fraction(sum(v for a, v in enumerate(high_density) if a % p == residue),
                                       phi//(p-1))
                self.assertEqual(conditional, 1)
        with self.assertRaisesRegex(ValueError, "cap2"):
            coprime_product_profile(high_density, high_density, 2)
        for high, z, modulus, primes in ((26, 2, 77, (7, 11)),
                                         (124, 4, 1001, (7, 11, 13)),
                                         (500, 7, 1001, (7, 11, 13))):
            self.assertGreater(modulus, 2*high)
            self.assertLess(high, (z+1)**3)
            phi = prod(p-1 for p in primes)
            self.assertGreaterEqual(phi**4, modulus**3)
            atoms = [p for p in range(z+1, high//(z+1)+1)
                     if trial_prime(p) and gcd(p, modulus) == 1]
            self.assertGreater(len(atoms), 0)
            self.assertEqual(len(atoms), len({p % modulus for p in atoms}))
            self.assertGreater(Fraction(phi, len(atoms)), 2)
            distance = atomic_cap_distance(phi, len(atoms))
            self.assertGreater(distance, 0)
            # Exact twelfth-power version of distance>2*(1-2^(1/4)*H^(-1/12)).
            self.assertLess(high*(1-distance/2)**12, 8)

    def test_input_coordinates_exactness_and_band_checks(self):
        first = character_density(21)
        for bad in ([*first], (), (0, 1), (0, True, 1), (0, 1.0, 1),
                    (1, 0, 1), (0, 0, 0), (0, 3, -1)):
            with self.assertRaises(ValueError):
                unit_projection(bad, 1)
        for divisor in (True, 0, 2, 3.0):
            with self.assertRaises(ValueError):
                unit_projection(first, divisor)
        for modulus in (3, 7, 9, 45, 75):
            with self.assertRaises(ValueError):
                joint_product_profile(uniform(modulus), uniform(modulus), 2*(modulus//3))
        for target in (True, -14, 7, 16, 42, 14.0):
            with self.assertRaises(ValueError):
                joint_product_profile(first, first, target)
        with self.assertRaises(ValueError):
            joint_product_profile(first, uniform(15), 14)
        self.assertEqual(unit_projection(first, 21), first)
        self.assertEqual(unit_projection(first, 1), (1,))
        self.assertEqual(joint_product_profile(first, first, 28)[1], 0)
        for modulus in (True, 3, 5, 21, 49, 7.0):
            with self.assertRaises(ValueError):
                crt_pair_floor(modulus)
        for denominator in (True, 0, 1.0):
            with self.assertRaises(ValueError):
                crt_pair_floor(77, denominator=denominator)
        self.assertEqual(crt_pair_floor(77, denominator=1), 0)
        for target in (True, -2, 0, 7, 11, 2.0):
            with self.assertRaises(ValueError):
                coprime_product_profile(uniform(77), uniform(77), target)
        with self.assertRaises(ValueError):
            coprime_product_profile(first, first, 2)
        with self.assertRaises(ValueError):
            coprime_product_profile(uniform(7), uniform(77), 2)


if __name__ == "__main__":
    unittest.main()
