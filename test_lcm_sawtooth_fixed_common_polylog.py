import unittest

from lcm_sawtooth_fixed_common_polylog import (
    fixed_common_layer_polylog_receipt,
)


class LcmSawtoothFixedCommonPolylogTests(unittest.TestCase):
    def test_common_part_shortens_residual_and_preserves_condition(self):
        receipts = tuple(
            fixed_common_layer_polylog_receipt(
                128021 * 5311, 16, 404, 30030, common)
            for common in (1, 2, 6, 30))
        self.assertTrue(all(
            receipt[
                "fixed_common_layer_polylog_bound_proved_for_reported_range"]
            for receipt in receipts))
        self.assertEqual(
            tuple(receipt["residual_limit"] for receipt in receipts),
            (5, 2, 1, 1))
        self.assertTrue(all(
            not receipt["common_layer_diagonal_interference_bound_proved"]
            for receipt in receipts))
        self.assertEqual(
            tuple(receipt["fixed_common_base_to_no_common_factor"]
                  for receipt in receipts),
            (1, 2, 4, 8))
        self.assertTrue(all(
            receipt[
                "separated_base_energy_domination_proved_for_reported_range"]
            for receipt in receipts))

    def test_rejects_nondividing_common_part(self):
        with self.assertRaises(ValueError):
            fixed_common_layer_polylog_receipt(1000, 10, 100, 210, 4)

    def test_fixed_layer_condition_does_not_imply_base_domination(self):
        receipt = fixed_common_layer_polylog_receipt(1000, 10, 100, 210, 5)
        self.assertTrue(
            receipt["fixed_common_layer_polylog_bound_proved_for_reported_range"])
        self.assertFalse(
            receipt["fixed_common_base_domination_proved_for_reported_range"])


if __name__ == "__main__":
    unittest.main()
