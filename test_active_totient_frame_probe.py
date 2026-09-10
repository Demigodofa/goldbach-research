import unittest

from active_totient_frame_probe import (
    finite_active_totient_frame,
    single_modulus_active_totient_frame,
)


class ActiveTotientFrameProbeTests(unittest.TestCase):
    def test_aggregate_receipt_is_ordered(self):
        receipt = finite_active_totient_frame(32000, modulus_limit=3)
        self.assertGreaterEqual(
            receipt["largest_active_over_frame_eigenvalue"],
            receipt["mobius_active_over_frame"])
        self.assertGreaterEqual(
            receipt["active_frame_schur_row_sum_max"],
            receipt["largest_active_over_frame_eigenvalue"])
        self.assertFalse(receipt["active_totient_frame_bound_proved"])

    def test_single_modulus_receipt(self):
        receipt = single_modulus_active_totient_frame(1009, 5, 9, 3, 8)
        self.assertEqual(len(receipt["divisors"]), 5)
        self.assertGreaterEqual(
            receipt["active_frame_schur_row_sum_max"],
            receipt["active_frame_diagonal_max"])


if __name__ == "__main__":
    unittest.main()
