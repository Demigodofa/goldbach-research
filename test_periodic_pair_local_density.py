import itertools
import unittest
from collections import Counter
from fractions import Fraction as F
from math import prod

from periodic_pair_local_density import (
    admissible_residues,
    affine_mass_split,
    local_pair_product,
    periodic_density,
)


class PeriodicPairLocalDensityTests(unittest.TestCase):
    def test_crt_against_direct_enumeration_for_every_small_even_class(self):
        for period, modulus in ((1, 30), (6, 30), (10, 210), (30, 210)):
            weight = tuple(F((s * s + 3 * s) % 11 - 5, 7)
                           for s in range(period))
            for target in range(0, 2 * modulus, 2):
                with self.subTest(period=period, modulus=modulus, target=target):
                    direct, factored = periodic_density(target, period, modulus, weight)
                    self.assertEqual(direct, factored)

    def test_q286_assembled_period_with_new_sieve_primes(self):
        period = 10010
        weight = tuple(F(s % 19 - 7, 11) for s in range(period))
        for target in (0, 4124, 8856, 1038176):
            direct, factored = periodic_density(target, period, period * 3 * 17, weight)
            self.assertEqual(direct, factored)

    def test_each_admissible_residue_has_identical_local_density(self):
        for s in admissible_residues(22, 30):
            weight = tuple(int(r == s) for r in range(30))
            direct, factored = periodic_density(22, 30, 210, weight)
            self.assertEqual(direct, factored)
            self.assertEqual(direct, local_pair_product(22, 210)
                             / len(admissible_residues(22, 30)))

    def test_four_q286_moduli_share_the_same_uniform_mass_direction(self):
        for target in (0, 4124, 8856, 1038176):
            allowed = admissible_residues(target, 10010)
            for modulus in (70, 130, 154, 286):
                counts = Counter(s % modulus for s in allowed)
                small = admissible_residues(target, modulus)
                self.assertEqual(set(counts), set(small))
                self.assertEqual(set(counts.values()), {len(allowed) // len(small)})
                self.assertEqual(len(allowed) % len(small), 0)

    def test_zero_local_mean_has_zero_model_density(self):
        allowed = admissible_residues(22, 30)
        weight = [F(0)] * 30
        weight[allowed[0]], weight[allowed[-1]] = F(1), F(-1)
        self.assertEqual(periodic_density(22, 30, 210, weight), (0, 0))

    def test_even_local_products_are_bounded_below_independently_of_pairs(self):
        modulus = 2 * 3 * 5 * 7 * 11 * 13 * 17
        for target in range(0, 200, 2):
            self.assertGreaterEqual(local_pair_product(target, modulus), 1)
        for stop in (2, 3, 17, 100):
            telescoping = prod((1 - F(1, k * k) for k in range(2, stop + 1)),
                               start=F(1))
            self.assertEqual(telescoping, F(stop + 1, 2 * stop))

    def test_affine_identity_for_nonuniform_reference_and_signed_weights(self):
        reference = (F(1, 6), F(1, 3), F(1, 2))
        weight = (-3, 2, 5)
        for mass in itertools.product(range(3), repeat=3):
            row = affine_mass_split(mass, reference, F(13, 7), weight)
            self.assertEqual(row["witness"], row["reconstructed_witness"])
            self.assertEqual(sum(row["centered"]), 0)
            self.assertEqual(row["scalar_error"], row["total"] - F(13, 7))

    def test_centered_channels_cannot_detect_any_uniform_mass_deficit(self):
        reference = (F(1, 6), F(1, 3), F(1, 2))
        weight = (-3, 2, 5)
        for total in (F(0), F(1, 2), F(3), F(10)):
            row = affine_mass_split(tuple(total * u for u in reference),
                                    reference, 3, weight)
            self.assertEqual(row["centered"], (0, 0, 0))
            self.assertEqual(row["witness"], row["mean"] * total)
            self.assertEqual(row["scalar_error"], total - 3)

    def test_affine_adverse_gate_is_not_weaker_than_original_raw_gate(self):
        mean, baseline = F(5, 3), F(7, 2)
        for total in (F(0), F(1), baseline, F(9)):
            for channels in itertools.product((-2, 0, 3), repeat=3):
                adverse = sum(max(0, -value) for value in channels)
                scalar_adverse = max(0, -mean * (total - baseline))
                gap = mean * baseline - scalar_adverse - adverse
                self.assertEqual(gap, mean * min(total, baseline) - adverse)
                self.assertLessEqual(gap, mean * total - adverse)

    def test_invalid_domains_do_not_silently_use_squarefree_formula(self):
        for period, modulus, weight in ((4, 12, [1] * 4),
                                        (6, 10, [1] * 6), (6, 30, [1] * 5)):
            with self.assertRaises(ValueError):
                periodic_density(22, period, modulus, weight)
        with self.assertRaises(ValueError):
            periodic_density(21, 2, 6, [1, 1])
        with self.assertRaises(ValueError):
            affine_mass_split([0], [F(1, 2)], 3, [1])


if __name__ == "__main__":
    unittest.main()
