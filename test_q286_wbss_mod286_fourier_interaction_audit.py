import json
import unittest
from pathlib import Path


class Q286WbssMod286FourierInteractionAuditTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/q286-wbss-mod286-fourier-interaction-audit.json"
        ).read_text(encoding="utf-8"))

    def test_receipt_preserves_boundaries(self):
        receipt = self.load_receipt()

        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["multiplicative_character_theorem_proved"])
        self.assertFalse(receipt["signed_projection_theorem_proved"])
        self.assertTrue(receipt["tiny_character_shortcut_demoted"])
        self.assertIn("finite mod-286 Fourier-interaction diagnostic",
                      receipt["status_boundary"])

    def test_spectrum_is_interaction_and_not_tiny(self):
        receipt = self.load_receipt()
        spectrum = receipt["coefficient_spectrum"]
        shares = spectrum["energy_share_by_top_group_count"]

        self.assertEqual(spectrum["residue_count"], 120)
        self.assertLess(spectrum["zero_axis_energy_share"], 1e-25)
        self.assertLess(shares["8"], 0.5)
        self.assertGreater(shares["20"], 0.85)
        self.assertLess(shares["20"], 0.9)
        self.assertGreater(shares["25"], 0.999)

    def test_small_truncations_do_not_close_sign(self):
        receipt = self.load_receipt()
        truncations = receipt["row_summary"]["truncations"]

        self.assertLess(
            truncations["top_8_conjugacy_groups"]["contribution"][
                "negative_count"], 196)
        self.assertEqual(
            truncations["top_10_conjugacy_groups"]["contribution"][
                "negative_count"], 196)
        self.assertLess(
            truncations["top_10_conjugacy_groups"][
                "contribution_to_total_ratio_summary"]["minimum"], 0.02)

    def test_twenty_groups_carry_half_drag_on_all_rows(self):
        receipt = self.load_receipt()
        row_summary = receipt["row_summary"]
        truncation = row_summary["truncations"]["top_20_conjugacy_groups"]

        self.assertEqual(row_summary["row_count"], 196)
        self.assertEqual(
            row_summary["total_interaction_component"]["negative_count"], 196)
        self.assertTrue(truncation["all_rows_negative"])
        self.assertTrue(truncation["all_rows_half_or_more_of_total_drag"])
        self.assertGreater(
            truncation["contribution_to_total_ratio_summary"]["minimum"], 0.5)


if __name__ == "__main__":
    unittest.main()
