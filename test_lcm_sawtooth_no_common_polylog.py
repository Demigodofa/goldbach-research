import unittest

from lcm_sawtooth_no_common_polylog import three_state_harmonic_receipt


class LcmSawtoothNoCommonPolylogTests(unittest.TestCase):
    def test_exact_weight_is_bounded_by_triple_harmonic_sum(self):
        for limit in (1, 2, 10, 40):
            receipt = three_state_harmonic_receipt(limit)
            self.assertLessEqual(
                receipt["exact_squared_bound"],
                receipt["triple_harmonic_bound"] + 1e-12)
            self.assertLessEqual(
                receipt["triple_harmonic_bound"],
                receipt["log_six_bound"] + 1e-12)
            self.assertTrue(receipt["three_state_count_bound_proved"])
            self.assertTrue(
                receipt["no_common_polylog_bound_proved_under_d_gt_BV"])

    def test_rejects_invalid_limit(self):
        with self.assertRaises(ValueError):
            three_state_harmonic_receipt(0)


if __name__ == "__main__":
    unittest.main()
