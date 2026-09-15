import json
import unittest
from pathlib import Path


class Q286WbssMultiplicativeCharacterL2ObservedMomentTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/"
            "q286-wbss-multiplicative-character-l2-observed-moment-audit.json"
        ).read_text(encoding="utf-8"))

    def test_receipt_is_finite_diagnostic_not_proof(self):
        receipt = self.load_receipt()

        self.assertEqual(
            receipt["status"],
            "HOLD_l2_cap_requires_boundary_or_stronger_theorem")
        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["aggregate_character_l2_bound_proved"])
        self.assertFalse(receipt["pointwise_adverse_drag_theorem_proved"])
        self.assertFalse(receipt["acceptance_condition"][
            "non_circular_bridge_confirmed"])

    def test_zero_mass_check_passes(self):
        receipt = self.load_receipt()
        zero = receipt["zero_mass_check"]

        self.assertEqual(zero["zero_pair_count"], 0)
        self.assertEqual(zero["zero_actual_mass_count"], 0)
        self.assertEqual(zero["nonunit_actual_mass_sum_count"], 0)
        self.assertEqual(zero["nonunit_uniform_mass_sum_count"], 0)

    def test_checked_rows_violate_global_and_row_local_caps(self):
        receipt = self.load_receipt()
        summary = receipt["summary"]

        self.assertEqual(summary["row_count"], 348)
        self.assertEqual(summary["global_min_cap_exceeding_row_count"], 301)
        self.assertEqual(summary["row_local_cap_exceeding_row_count"], 120)
        self.assertEqual(summary["max_target_exceeding_row_local_cap"],
                         1155862)

    def test_worst_row_values_are_stable(self):
        receipt = self.load_receipt()
        row = receipt["summary"]["largest_row_local_ratio_row"]

        self.assertEqual(row["target"], 1089544)
        self.assertAlmostEqual(row["aggregate_character_moment_l2"],
                               0.20982859176041493,
                               places=12)
        self.assertAlmostEqual(row["row_local_l2_cap"],
                               0.13475610600578378,
                               places=12)
        self.assertAlmostEqual(row["ratio_to_row_local_l2_cap"],
                               1.5570989543984672,
                               places=12)

    def test_decision_names_threshold_or_stronger_theorem(self):
        receipt = self.load_receipt()

        self.assertIn("threshold beyond the finite violations",
                      receipt["decision"])
        self.assertIn("stronger structured moment theorem",
                      receipt["decision"])


if __name__ == "__main__":
    unittest.main()
