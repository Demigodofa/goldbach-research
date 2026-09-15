import json
import unittest
from pathlib import Path


class Q286WbssMod286BandlimitedResidualAuditTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/q286-wbss-mod286-bandlimited-residual-audit.json"
        ).read_text(encoding="utf-8"))

    def test_receipt_preserves_boundaries(self):
        receipt = self.load_receipt()

        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["bandlimited_character_theorem_proved"])
        self.assertFalse(receipt["signed_projection_theorem_proved"])
        self.assertTrue(
            receipt["one_sided_residual_absorption_candidate_supported"])
        self.assertIn("finite q286-WBSS top-20 Fourier residual diagnostic",
                      receipt["status_boundary"])

    def test_top20_split_shape(self):
        receipt = self.load_receipt()
        spectrum = receipt["coefficient_spectrum"]

        self.assertEqual(spectrum["conjugacy_group_count"], 25)
        self.assertEqual(spectrum["top_group_count"], 20)
        self.assertEqual(spectrum["residual_group_count"], 5)
        self.assertGreater(spectrum["top20_energy_share"], 0.87)
        self.assertLess(spectrum["residual_energy_share"], 0.14)

    def test_top20_main_drag_is_sign_stable(self):
        receipt = self.load_receipt()
        rows = receipt["row_summary"]

        self.assertEqual(rows["row_count"], 196)
        self.assertEqual(
            rows["total_interaction_component"]["negative_count"], 196)
        self.assertEqual(
            rows["bandlimited_top20_component"]["negative_count"], 196)
        self.assertLess(
            rows["bandlimited_plus_residual_error_summary"]["maximum"],
            1e-12)

    def test_one_sided_residual_absorption_is_small(self):
        receipt = self.load_receipt()
        rows = receipt["row_summary"]

        self.assertEqual(rows["positive_residual_row_count"], 24)
        self.assertEqual(rows["negative_residual_row_count"], 172)
        self.assertEqual(rows["pushback_lt_one_count"], 196)
        self.assertEqual(rows["pushback_lt_013_count"], 196)
        self.assertLess(
            rows["pushback_to_main_drag_ratio_summary"]["maximum"], 0.13)
        self.assertLess(
            rows["pushback_lt_one_eighth_count"], 196)

    def test_symmetric_abs_residual_is_near_sharp_but_passes(self):
        receipt = self.load_receipt()
        rows = receipt["row_summary"]

        self.assertEqual(rows["absolute_residual_lt_main_drag_count"], 196)
        self.assertGreater(
            rows["absolute_residual_to_main_drag_ratio_summary"]["maximum"],
            0.98)
        self.assertLess(
            rows["absolute_residual_to_main_drag_ratio_summary"]["maximum"],
            1.0)


if __name__ == "__main__":
    unittest.main()
