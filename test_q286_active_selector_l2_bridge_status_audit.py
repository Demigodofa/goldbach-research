import json
import unittest

from tools.build_q286_active_selector_l2_bridge_status_audit import OUT


class Q286ActiveSelectorL2BridgeStatusAuditTest(unittest.TestCase):

    def test_receipt_answers_l2_non_circularity_without_promoting_theorem(self):
        self.assertTrue(OUT.exists())
        receipt = json.loads(OUT.read_text(encoding="utf-8"))
        status = receipt["non_circularity_classification"]
        self.assertTrue(status["valid_sufficient_implication"])
        self.assertTrue(status["non_circular_as_external_arithmetic_premise"])
        self.assertFalse(status["confirmed_by_current_work"])
        self.assertFalse(status["proves_strict_central_existence"])
        self.assertFalse(receipt["l2_discrepancy_theorem_proved"])
        self.assertFalse(receipt["active_selector_rarity_theorem_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_l2_thresholds_and_sample_stress_are_stable(self):
        receipt = json.loads(OUT.read_text(encoding="utf-8"))
        shape = receipt["l2_sufficient_theorem_shape"]
        self.assertAlmostEqual(
            shape["minimum_l2_relative_error_sufficient"],
            0.0059551615239434134)
        self.assertAlmostEqual(
            shape["maximum_l2_relative_error_sufficient"],
            0.017908306132142508)
        self.assertEqual(shape["even_target_residue_count"], 143)
        stress = receipt["sample_stress"]
        self.assertEqual(
            [row["target"] for row in
             stress["clear_rows_that_fail_l2_but_pass_signed_projection"]],
            [1240888, 1242118])
        self.assertEqual(stress["tail_sample_targets"], [1222142])
        row = next(row for row in stress["sample_rows"]
                   if row["target"] == 1242118)
        self.assertFalse(row["generic_l2_uniformity_certificate_holds"])
        self.assertTrue(row["signed_projection_certificate_holds"])
        self.assertAlmostEqual(row["l2_budget_utilization"],
                               2.9097499848440553)

    def test_post_failure_context_remains_denominator_evidence_only(self):
        receipt = json.loads(OUT.read_text(encoding="utf-8"))
        context = receipt["post_failure_context"]
        self.assertEqual(context["scanned_target_count"], 10010)
        self.assertEqual(context["active_selector_count"], 1)
        self.assertEqual(context["active_targets"], [650476])
        self.assertEqual(context["active_targets_not_in_source_summary"], [])


if __name__ == "__main__":
    unittest.main()
