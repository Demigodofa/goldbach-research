import unittest

from lcm_sawtooth_endpoint_resonance_count import (
    project_endpoint_resonance_count_receipt,
)


class LcmSawtoothEndpointResonanceCountTests(unittest.TestCase):
    def test_complete_prime_block_count_is_reconstructed(self):
        receipt = project_endpoint_resonance_count_receipt(251)
        self.assertGreater(receipt["prime_count"], 0)
        self.assertGreater(
            receipt["high_Q_endpoint_ordered_pair_count"], 0)
        self.assertTrue(
            0 <= receipt["aggregate_near_pair_fraction"] <= 1)
        self.assertAlmostEqual(
            receipt["row_count_scaled_aggregate_near_pair_fraction"],
            receipt["row_count"] * receipt["aggregate_near_pair_fraction"])
        self.assertAlmostEqual(
            receipt[
                "row_count_scaled_aggregate_near_coefficient_weight_fraction"],
            receipt["row_count"]
            * receipt["aggregate_near_coefficient_weight_fraction"])
        self.assertGreaterEqual(
            receipt[
                "row_count_scaled_aggregate_near_Q_squared_product_weight_fraction"],
            0)
        self.assertGreaterEqual(
            receipt["maximum_near_exact_Q_ordered_pair_multiplicity"], 1)
        self.assertTrue(
            receipt["finite_complete_prime_block_endpoint_count"])
        self.assertFalse(
            receipt["uniform_endpoint_resonance_count_bound_proved"])

    def test_small_scale_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "at least 17"):
            project_endpoint_resonance_count_receipt(16)


if __name__ == "__main__":
    unittest.main()
