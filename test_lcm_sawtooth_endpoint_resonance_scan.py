import unittest

from lcm_sawtooth_endpoint_resonance_scan import (
    endpoint_resonance_scan_receipt,
)


class LcmSawtoothEndpointResonanceScanTests(unittest.TestCase):
    def test_scan_returns_finite_rank_comparison(self):
        receipt = endpoint_resonance_scan_receipt(
            (101, 103, 107), 10, 10, 12, 3, 12, 1)
        self.assertEqual(receipt["fixture_count"], 3)
        self.assertEqual(len(receipt["rows"]), 3)
        self.assertEqual(len(receipt["full_quotient_leaders"]), 1)
        self.assertEqual(len(receipt["endpoint_score_leaders"]), 1)
        self.assertTrue(-1 <= receipt["raw_pearson_correlation"] <= 1)
        self.assertTrue(-1 <= receipt["spearman_rank_correlation"] <= 1)
        self.assertTrue(receipt["finite_endpoint_score_scan"])
        self.assertFalse(
            receipt["endpoint_score_predicts_uniform_row_bound_proved"])

    def test_duplicate_moduli_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "distinct"):
            endpoint_resonance_scan_receipt(
                (101, 101), 10, 10, 12, 3, 12, 1)


if __name__ == "__main__":
    unittest.main()
