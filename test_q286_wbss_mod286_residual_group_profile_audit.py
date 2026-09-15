import json
import unittest
from pathlib import Path


class Q286WbssMod286ResidualGroupProfileAuditTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/q286-wbss-mod286-residual-group-profile-audit.json"
        ).read_text(encoding="utf-8"))

    def test_receipt_preserves_boundaries(self):
        receipt = self.load_receipt()

        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["residual_group_theorem_proved"])
        self.assertFalse(receipt["signed_projection_theorem_proved"])
        self.assertTrue(receipt["single_residual_group_shortcut_demoted"])
        self.assertTrue(receipt["proper_fixed_residual_subset_shortcut_demoted"])
        self.assertIn("finite q286-WBSS residual Fourier group profile",
                      receipt["status_boundary"])

    def test_residual_groups_are_the_expected_five(self):
        receipt = self.load_receipt()
        groups = receipt["coefficient_spectrum"]["residual_groups"]

        self.assertEqual(receipt["coefficient_spectrum"][
            "residual_group_count"], 5)
        self.assertEqual(
            [group["representative"] for group in groups],
            [
                {"ell_mod_12": 1, "k_mod_10": 1},
                {"ell_mod_12": 9, "k_mod_10": 1},
                {"ell_mod_12": 10, "k_mod_10": 4},
                {"ell_mod_12": 2, "k_mod_10": 4},
                {"ell_mod_12": 9, "k_mod_10": 3},
            ],
        )

    def test_positive_residual_rows_are_not_single_group(self):
        receipt = self.load_receipt()
        rows = receipt["row_summary"]
        argmax_counts = rows["argmax_positive_residual_counts"]

        self.assertEqual(rows["row_count"], 196)
        self.assertEqual(rows["positive_residual_row_count"], 24)
        self.assertEqual(rows["negative_residual_row_count"], 172)
        self.assertEqual(set(argmax_counts.values()), {2, 6, 8})
        self.assertEqual(sum(argmax_counts.values()), 24)

    def test_no_proper_subset_recovers_signed_positive_residual_everywhere(self):
        receipt = self.load_receipt()
        profiles = receipt["row_summary"][
            "best_fixed_subset_profiles_on_positive_residual_rows"]

        self.assertEqual(profiles["size_1"]["touch_count"], 19)
        self.assertEqual(profiles["size_2"]["touch_count"], 23)
        self.assertEqual(profiles["size_3"]["touch_count"], 24)
        self.assertEqual(profiles["size_4"]["touch_count"], 24)
        self.assertLess(profiles["size_4"]["signed_positive_count"], 24)
        self.assertEqual(profiles["size_5"]["signed_positive_count"], 24)

    def test_group_reconstruction_is_exact_in_rows(self):
        receipt = self.load_receipt()
        rows = receipt["row_summary"]

        self.assertLess(
            rows["residual_five_group_component"]["summary"]["maximum"],
            0.058)
        self.assertGreater(
            rows["pushback_to_main_drag_ratio_summary"]["maximum"],
            0.125)
        self.assertLess(
            rows["pushback_to_main_drag_ratio_summary"]["maximum"],
            0.13)


if __name__ == "__main__":
    unittest.main()
