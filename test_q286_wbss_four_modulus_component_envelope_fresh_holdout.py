import json
import unittest
from pathlib import Path


class Q286WbssFourModulusComponentEnvelopeFreshHoldoutTests(
        unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/"
            "q286-wbss-four-modulus-component-envelope-fresh-holdout.json"
        ).read_text(encoding="utf-8"))

    def test_receipt_preserves_boundaries(self):
        receipt = self.load_receipt()

        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["per_modulus_supremum_theorem_proved"])
        self.assertFalse(
            receipt["one_sided_signed_concentration_theorem_proved"])
        self.assertFalse(
            receipt["fixed_modulus_equidistribution_theorem_proved"])
        self.assertFalse(receipt["universal_negative_drag_bound_proved"])
        self.assertTrue(receipt["universal_bound_open"])

    def test_frozen_sum_envelope_survives_fresh_holdout(self):
        receipt = self.load_receipt()
        summary = receipt["holdout"]["summary"]

        self.assertTrue(
            receipt["frozen_componentwise_envelope_survives_fresh_holdout"])
        self.assertEqual(summary["row_count"], 116)
        self.assertEqual(summary["actual_positive_count"], 116)
        self.assertEqual(summary["lambda_budget_failure_count"], 0)
        self.assertEqual(
            summary["frozen_componentwise_envelope_positive_count"], 116)
        self.assertEqual(
            summary["frozen_componentwise_envelope_nonpositive_count"], 0)
        self.assertEqual(receipt["holdout"]["target_minimum"], 1116328)
        self.assertEqual(receipt["holdout"]["target_maximum"], 1155862)

    def test_literal_individual_component_suprema_are_falsified(self):
        receipt = self.load_receipt()
        excess = receipt["holdout"]["modulus_excess_summary"]

        self.assertFalse(
            receipt[
                "individual_frozen_component_suprema_survive_fresh_holdout"])
        self.assertTrue(
            receipt["individual_frozen_component_suprema_falsified"])
        self.assertEqual(excess["70"]["exceeding_row_count"], 0)
        self.assertEqual(excess["130"]["exceeding_row_count"], 0)
        self.assertEqual(excess["154"]["exceeding_row_count"], 0)
        self.assertEqual(excess["286"]["exceeding_row_count"], 2)
        self.assertEqual(excess["286"]["fresh_maximum_row"]["target"],
                         1124642)
        self.assertAlmostEqual(
            excess["286"]["fresh_maximum_row"]["fresh_adverse_value"],
            0.12551431368886537,
            places=12)

    def test_tightest_frozen_envelope_row_is_recorded(self):
        receipt = self.load_receipt()
        row = receipt["holdout"]["summary"][
            "tightest_frozen_componentwise_envelope_row"]

        self.assertEqual(row["target"], 1118256)
        self.assertAlmostEqual(row["local_uniform_main_term"],
                               0.717245423802844,
                               places=12)
        self.assertAlmostEqual(
            row["frozen_componentwise_envelope_expectation"],
            0.38515813641492663,
            places=12)
        self.assertAlmostEqual(row["frozen_componentwise_envelope_ratio"],
                               0.4630037032891566,
                               places=12)

    def test_largest_rowwise_drag_and_lambda_rows_match(self):
        receipt = self.load_receipt()
        summary = receipt["holdout"]["summary"]

        self.assertEqual(
            summary["largest_rowwise_negative_drag_ratio_row"]["target"],
            1124642)
        self.assertAlmostEqual(
            summary["largest_rowwise_negative_drag_ratio_row"][
                "negative_drag_ratio"],
            0.23148438379145228,
            places=12)
        self.assertEqual(summary["largest_lambda_row"]["target"], 1124642)
        self.assertAlmostEqual(summary["largest_lambda_row"]["lambda_phi"],
                               0.18795270138709522,
                               places=12)


if __name__ == "__main__":
    unittest.main()
