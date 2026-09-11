import unittest

from lcm_sawtooth_high_d_assignment import (
    high_d_assignment_expansion,
    high_d_residual_geometry_probe,
    residual_bessel_probe,
    three_way_prime_assignments,
)


class LcmSawtoothHighDAssignmentTests(unittest.TestCase):
    def test_three_way_assignments_are_unique_and_complete(self):
        for value, omega in ((1, 0), (2, 1), (6, 2), (30, 3), (210, 4)):
            assignments = three_way_prime_assignments(value)
            self.assertEqual(len(assignments), 3 ** omega)
            self.assertEqual(len(set(assignments)), len(assignments))
            for left, right, common in assignments:
                self.assertEqual(left * right * common, value)

    def test_assignment_expansion_matches_direct_structured_sum(self):
        for target in (6, 30, 42, 70, 210):
            receipt = high_d_assignment_expansion(
                101, 70, 4, 20, target)
            self.assertAlmostEqual(
                receipt["direct_structured_sum"],
                receipt["assignment_expanded_sum"], places=8)
            self.assertLessEqual(
                receipt["maximum_residual_lcm"],
                receipt["residual_lcm_upper_bound"] + 1e-12)
            self.assertTrue(receipt["three_way_assignment_identity_proved"])
            self.assertTrue(receipt["residual_lcm_bound_proved"])
            self.assertFalse(receipt["high_d_structured_sum_bound_proved"])

    def test_high_d_geometry_partitions_monotonically(self):
        receipt = high_d_residual_geometry_probe(101, 70, 4, 20)
        fractions = tuple(
            receipt["energy_fraction_by_maximum_residual_lcm"].values())
        self.assertEqual(tuple(sorted(fractions)), fractions)
        self.assertGreater(receipt["high_d_entry_count"], 0)
        self.assertTrue(receipt["three_way_residual_geometry_measured"])

    def test_nonsquarefree_target_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "squarefree"):
            high_d_assignment_expansion(101, 70, 4, 20, 12)

    def test_residual_bessel_matches_complete_factorization(self):
        from lcm_sawtooth_exact_gcd_factorization import (
            lcm_sawtooth_exact_gcd_factorization_probe)
        bessel = residual_bessel_probe(101, 70, 4, 20)
        exact = lcm_sawtooth_exact_gcd_factorization_probe(101, 70, 4, 20)
        self.assertAlmostEqual(
            bessel["complete_period_energy"],
            exact["exact_signed_complete_energy"], places=7)
        self.assertAlmostEqual(
            bessel["diagonal_energy"],
            exact["complete_period_diagonal_energy"], places=7)
        self.assertAlmostEqual(bessel["numerator_component_error"], 0.0)
        self.assertAlmostEqual(bessel["denominator_component_error"], 0.0)
        self.assertGreater(
            bessel["maximum_positive_weight_residual_support_count"], 0)
        self.assertLessEqual(
            bessel["maximum_positive_weight_residual_support_count"],
            bessel["maximum_all_coordinate_residual_support_count"])
        self.assertTrue(
            bessel["exact_residual_bessel_reformulation_proved"])
        self.assertFalse(bessel["residual_bessel_subpower_bound_proved"])


if __name__ == "__main__":
    unittest.main()
