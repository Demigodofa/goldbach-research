import unittest

from mobius_covariance_endpoint_probe import finite_endpoint_scan


class MobiusCovarianceEndpointProbeTests(unittest.TestCase):
    def test_grid_and_adversarial_receipts_are_well_formed(self):
        result = finite_endpoint_scan(32000)
        self.assertEqual(result["endpoint_count"], 25)
        self.assertEqual(result["window_count"], 276)
        self.assertGreater(result["prime_count"], 0)
        self.assertGreaterEqual(result["common_positive_window_count"], 0)
        self.assertLessEqual(result["common_positive_window_count"], 276)
        self.assertGreater(result["per_modulus_best_off_positive_count"], 0)
        self.assertLessEqual(result["per_modulus_best_off_positive_count"],
                             result["prime_count"])
        self.assertLess(result["individual_window_ratio_min"],
                        result["individual_window_ratio_max"])


if __name__ == "__main__":
    unittest.main()
