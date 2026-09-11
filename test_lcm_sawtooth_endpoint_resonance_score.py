import unittest

from lcm_sawtooth_endpoint_resonance_score import (
    endpoint_reduced_denominator,
    endpoint_resonance_score_receipt,
)


class LcmSawtoothEndpointResonanceScoreTests(unittest.TestCase):
    def test_endpoint_denominator_reduction_handles_common_factor(self):
        self.assertEqual(endpoint_reduced_denominator(210, 323, -1, 1),
                         67830)
        self.assertEqual(endpoint_reduced_denominator(6, 10, 1, 1), 15)

    def test_endpoint_score_is_exactly_grouped_and_finite(self):
        receipt = endpoint_resonance_score_receipt(
            101, 10, 10, 12, 3, 12)
        self.assertEqual(receipt["endpoint_frequency_count"] % 2, 0)
        self.assertGreaterEqual(
            receipt["endpoint_near_Q_weighted_square_score"], 0)
        self.assertGreaterEqual(
            receipt["high_Q_endpoint_ordered_pair_count"],
            receipt["near_high_Q_ordered_pair_count"])
        self.assertGreaterEqual(
            receipt["maximum_near_exact_Q_ordered_pair_multiplicity"], 0)
        self.assertTrue(
            0 <= receipt["near_high_Q_ordered_pair_fraction"] <= 1)
        self.assertTrue(
            0 <= receipt["near_high_Q_coefficient_weight_fraction"] <= 1)
        self.assertTrue(
            0 <= receipt[
                "row_count_scaled_near_Q_squared_product_weight_fraction"]
            <= receipt["ell_range"][1] - receipt["ell_range"][0] + 1)
        self.assertLess(
            receipt["packet_grouping_error_over_complete"], 1e-12)
        self.assertLess(
            receipt["endpoint_near_imaginary_error_over_complete"], 1e-12)
        self.assertTrue(receipt["finite_endpoint_resonance_score"])
        self.assertFalse(receipt["endpoint_score_controls_all_modes_proved"])

    def test_invalid_first_row_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "ell_first"):
            endpoint_resonance_score_receipt(101, 0, 10, 12, 3, 12)

    def test_m509_endpoint_score_is_led_by_the_67830_resonance(self):
        receipt = endpoint_resonance_score_receipt(
            509, 46, 46, 69, 4, 20)
        denominator, contribution = receipt[
            "largest_endpoint_near_packets"][0]
        self.assertEqual(denominator, 67830)
        self.assertAlmostEqual(contribution.real, -0.07159152525511893)
        self.assertLess(abs(contribution.imag), 1e-12)


if __name__ == "__main__":
    unittest.main()
