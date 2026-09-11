import unittest

import numpy as np

from lcm_sawtooth_prime_class_core import _canonical_periodic_geometric_sum
from lcm_sawtooth_ramanujan_class_mean import (
    _endpoint_geometric_sum,
    _ramanujan_sum,
    ramanujan_class_mean_receipt,
)


class RamanujanClassMeanTests(unittest.TestCase):
    def test_endpoint_root_sum_matches_complete_period_reduction(self):
        numerators = np.asarray((1, 2, 3, 4))
        endpoint = _endpoint_geometric_sum(23, 5, numerators)
        canonical = _canonical_periodic_geometric_sum(23, 5, numerators)
        self.assertLess(float(np.max(np.abs(endpoint - canonical))), 1e-12)

    def test_integer_ramanujan_sum_values(self):
        self.assertEqual(
            tuple(_ramanujan_sum(10, value) for value in (0, 1, 2, 5)),
            (4, 1, -1, -4))

    def test_project_leading_lag_ramanujan_reconstruction(self):
        receipt = ramanujan_class_mean_receipt()
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["unit_class_count"], 2880)
        self.assertEqual((receipt["lag"], receipt["inverse_lag"]), (182, 9828))
        self.assertGreater(
            receipt["maximum_endpoint_packet_relative_error"], 1e-12)
        self.assertLess(
            receipt["maximum_endpoint_packet_relative_error"], 2e-12)
        self.assertFalse(receipt["endpoint_packet_float_comparison_passes"])
        self.assertLess(
            receipt["endpoint_to_canonical_mean_relative_error"], 1e-12)
        self.assertLess(
            receipt["ramanujan_mean_reconstruction_relative_error"], 1e-12)
        self.assertLess(
            receipt["ramanujan_pair_reconstruction_relative_error"], 1e-12)
        self.assertTrue(receipt[
            "finite_periodic_dft_ramanujan_identity_passes"])
        self.assertFalse(receipt["source_term_ramanujan_reduction_proved"])
        self.assertAlmostEqual(
            receipt["canonical_direct_paired_common_reweighting"],
            -378954805.6330534, places=2)
        self.assertLess(
            receipt["ramanujan_pair_reconstruction_relative_error"],
            1e-12)
        self.assertFalse(receipt["signed_prime_correlation_proved"])

    def test_guards(self):
        with self.assertRaises(ValueError):
            ramanujan_class_mean_receipt(lag=0)
        with self.assertRaises(ValueError):
            ramanujan_class_mean_receipt(second_row_count=20)


if __name__ == "__main__":
    unittest.main()
