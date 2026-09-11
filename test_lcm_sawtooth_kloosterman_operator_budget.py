import unittest

from lcm_sawtooth_kloosterman_operator_budget import (
    kloosterman_operator_budget_receipt,
)


class KloostermanOperatorBudgetTests(unittest.TestCase):
    def test_frequency_triangle_loses_local_saving(self):
        receipt = kloosterman_operator_budget_receipt()
        self.assertEqual(receipt["active_left_frequency_count"], 2989)
        self.assertEqual(receipt["active_right_frequency_count"], 3025)
        expected_ratios = {
            140: 67.54998119812704,
            154: 60.9939339483342,
            156: 133.15224722372224,
            182: 60.37858189924492,
            240: 154.4261253278829,
        }
        for lag, expected in expected_ratios.items():
            row = receipt["rows"][lag]
            self.assertAlmostEqual(
                row["bound_to_absolute_mode_mass_ratio"], expected, places=9)
            self.assertFalse(
                row["frequency_triangle_operator_bound_is_useful"])
        self.assertFalse(
            receipt["all_frequency_triangle_operator_bounds_are_useful"])
        self.assertFalse(receipt["cross_frequency_cancellation_estimate_proved"])
        self.assertFalse(receipt["signed_prime_correlation_proved"])

    def test_guards(self):
        with self.assertRaises(ValueError):
            kloosterman_operator_budget_receipt(lags=(1,))
        with self.assertRaises(ValueError):
            kloosterman_operator_budget_receipt(
                maximum_useful_bound_fraction=0)
        with self.assertRaises(ValueError):
            kloosterman_operator_budget_receipt(period=12)
        with self.assertRaises(ValueError):
            kloosterman_operator_budget_receipt(
                families=((55, 91), (143, 35)), lags=(140,))


if __name__ == "__main__":
    unittest.main()
