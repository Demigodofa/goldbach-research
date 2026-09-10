import unittest

from active_centering_schur_bound import (
    near_cutoff_centering_schur_bound,
    row_centering_schur_bound,
)


class ActiveCenteringSchurBoundTests(unittest.TestCase):
    def test_entry_majorant_dominates_exact_centering_matrix(self):
        receipt = row_centering_schur_bound(1009, 5, 9, 8, compare_exact=True)
        self.assertLessEqual(
            receipt["exact_centering_schur_row_sum"],
            receipt["proved_centering_schur_bound"])
        self.assertFalse(receipt["shifted_rows_proved"])

    def test_project_range_has_theorem_receipt(self):
        receipt = near_cutoff_centering_schur_bound(32000)
        self.assertTrue(receipt["centering_o_one_theorem"])
        self.assertFalse(receipt["shifted_rows_proved"])

    def test_rejects_composite_modulus(self):
        with self.assertRaisesRegex(ValueError, "prime"):
            row_centering_schur_bound(1001, 5, 9, 8)


if __name__ == "__main__":
    unittest.main()
