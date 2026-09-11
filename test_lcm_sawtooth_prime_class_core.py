import unittest

import numpy as np

from lcm_sawtooth_prime_class_core import (
    _canonical_periodic_geometric_sum,
    prime_class_core_receipt,
)


class PrimeClassCoreTests(unittest.TestCase):
    def test_canonical_geometric_sum_discards_complete_periods(self):
        numerators = np.asarray((1, 2, 4))
        first = _canonical_periodic_geometric_sum(18, 7, numerators)
        second = _canonical_periodic_geometric_sum(18 + 5 * 7, 7, numerators)
        self.assertLess(float(np.max(np.abs(first - second))), 1e-12)

    def test_project_complete_class_reinforcement_gate(self):
        receipt = prime_class_core_receipt()
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["reduced_residue_class_count"], 2880)
        self.assertEqual(receipt["minimum_reinforcement_fraction"], .25)
        self.assertLess(
            receipt["maximum_source_packet_core_relative_error"], 1e-12)
        self.assertEqual(
            receipt["maximum_period_representative_absolute_error"], 0.0)
        self.assertTrue(receipt[
            "normalized_arithmetic_core_periodicity_proved"])
        self.assertAlmostEqual(
            receipt["complete_class_reinforcement_fraction"],
            .04768611334520251, places=10)
        self.assertAlmostEqual(
            receipt["positive_signed_core_class_fraction"],
            .47256944444444443, places=10)
        self.assertTrue(receipt[
            "direction_polynomial_product_positive_on_representatives"])
        self.assertGreater(
            receipt["minimum_direction_polynomial_product"], 0)
        self.assertFalse(receipt[
            "prime_class_reinforcement_hypothesis_passes"])
        self.assertFalse(receipt["signed_prime_correlation_proved"])

    def test_guards(self):
        with self.assertRaises(ValueError):
            prime_class_core_receipt(families=((77, 65, 1),))
        with self.assertRaises(ValueError):
            prime_class_core_receipt(
                families=((77, 65, 1), (143, 33, 2)))
        with self.assertRaises(ValueError):
            prime_class_core_receipt(minimum_reinforcement_fraction=0)


if __name__ == "__main__":
    unittest.main()
