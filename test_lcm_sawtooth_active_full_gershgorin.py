import unittest

import numpy as np

from lcm_sawtooth_active_full_gershgorin import (
    coordinate_scaled_difference_gershgorin_receipt,
    project_aggregate_gershgorin_receipt,
    whitened_gershgorin_lower_frame_receipt,
)


class LcmSawtoothActiveFullGershgorinTests(unittest.TestCase):
    def test_diagonal_fixture_is_exact(self):
        full = np.diag((2.0, 8.0, 18.0))
        active = np.diag((1.5, 10.0, 36.0))
        receipt = whitened_gershgorin_lower_frame_receipt(active, full)
        np.testing.assert_allclose(
            sorted(receipt["gershgorin_lower_edges"]), (.75, 1.25, 2.0))
        self.assertAlmostEqual(
            receipt["gershgorin_lower_frame_bound"], .75)
        self.assertTrue(receipt["one_half_lower_frame_certified"])
        scaled = coordinate_scaled_difference_gershgorin_receipt(
            active, full)
        np.testing.assert_allclose(
            sorted(scaled["scaled_difference_gershgorin_edges"]),
            (.25, .75, 1.5))
        self.assertTrue(
            scaled["coordinate_scaled_gershgorin_certifies_candidate"])

    def test_m127_aggregate_certifies_one_half(self):
        receipt = project_aggregate_gershgorin_receipt(127)
        self.assertEqual(receipt["prime_count"], 24)
        self.assertAlmostEqual(
            receipt["gershgorin_lower_frame_bound"],
            .7454313024194685)
        self.assertAlmostEqual(
            receipt["exact_smallest_generalized_eigenvalue"],
            .8768802946823543)
        self.assertLessEqual(
            receipt["gershgorin_lower_frame_bound"],
            receipt["exact_smallest_generalized_eigenvalue"])
        self.assertTrue(receipt["one_half_lower_frame_certified"])
        self.assertFalse(receipt["uniform_entrywise_bound_proved"])
        scaled = receipt["coordinate_scaled_one_half_receipt"]
        self.assertAlmostEqual(
            scaled["scaled_difference_gershgorin_lower_edge"],
            -1.8462120978156262)
        self.assertFalse(
            scaled["coordinate_scaled_gershgorin_certifies_candidate"])

    def test_guards_singular_denominator(self):
        with self.assertRaises(ValueError):
            whitened_gershgorin_lower_frame_receipt(
                np.eye(2), np.diag((1.0, 0.0)))


if __name__ == "__main__":
    unittest.main()
