import json
import unittest
from pathlib import Path


class Q286WbssPointwiseAdverseDragTheoremTargetTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/q286-wbss-pointwise-adverse-drag-theorem-target.json"
        ).read_text(encoding="utf-8"))

    def test_receipt_demotes_finite_evidence_from_acceptance(self):
        receipt = self.load_receipt()

        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["pointwise_adverse_drag_theorem_proved"])
        self.assertFalse(
            receipt["fixed_modulus_equidistribution_theorem_proved"])
        self.assertTrue(receipt["universal_bound_open"])
        self.assertFalse(
            receipt["acceptance_condition"][
                "finite_evidence_is_acceptance_condition"])
        self.assertIn(
            "adverse_drag(N) < local_main(N)",
            receipt["acceptance_condition"]["required_universal_statement"])

    def test_definitions_are_unnormalized_and_pointwise(self):
        receipt = self.load_receipt()
        definitions = receipt["definitions"]

        self.assertEqual(definitions["moduli"], ["70", "130", "154", "286"])
        self.assertIn("A_-(N)=sum_d max(0,-E_d(N))",
                      definitions["adverse_drag"])
        self.assertIn("A_-(N) < M(N)",
                      definitions["sufficient_pointwise_inequality"])
        self.assertIn("unnormalized and pointwise",
                      receipt["acceptance_condition"][
                          "normalization_boundary"])

    def test_finite_calibration_combines_horizon_and_fresh_rows(self):
        receipt = self.load_receipt()
        summary = receipt["finite_calibration"]["summary"]

        self.assertEqual(summary["row_count"], 348)
        self.assertEqual(summary["target_minimum"], 1036248)
        self.assertEqual(summary["target_maximum"], 1155862)
        self.assertEqual(summary["positive_actual_count"], 348)
        self.assertEqual(summary["adverse_drag_not_below_local_main_count"],
                         0)
        self.assertEqual(summary["lambda_phi_below_one_count"], 348)

    def test_tightest_known_adverse_drag_row_is_fresh_row(self):
        receipt = self.load_receipt()
        row = receipt["finite_calibration"]["summary"][
            "tightest_adverse_drag_row"]

        self.assertEqual(row["target"], 1124642)
        self.assertEqual(row["source"],
                         "frozen_component_envelope_fresh_holdout")
        self.assertAlmostEqual(row["adverse_drag_ratio"],
                               0.23148438379145228,
                               places=12)
        self.assertAlmostEqual(row["adverse_only_expectation"],
                               0.6835668462365216,
                               places=12)

    def test_fixed_component_constants_are_explicitly_rejected(self):
        receipt = self.load_receipt()
        falsifier = receipt["finite_calibration"][
            "fresh_fixed_component_constant_falsifier"]

        self.assertTrue(
            falsifier["individual_frozen_component_suprema_falsified"])
        self.assertEqual(
            falsifier["rows_with_any_modulus_exceeding_frozen_supremum"], 2)
        self.assertEqual(falsifier["modulus_286_exceeding_row_count"], 2)
        self.assertEqual(
            falsifier["modulus_286_fresh_maximum_row"]["target"], 1124642)


if __name__ == "__main__":
    unittest.main()
