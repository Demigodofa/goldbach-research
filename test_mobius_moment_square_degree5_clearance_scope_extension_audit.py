import json
import unittest
from pathlib import Path


EVIDENCE = Path(
    "evidence/"
    "mobius-moment-square-degree5-clearance-scope-extension-audit.json")


class MobiusMomentSquareDegree5ClearanceScopeExtensionAuditTests(
        unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = json.loads(EVIDENCE.read_text(encoding="utf-8"))

    def test_receipt_preserves_boundaries(self):
        self.assertEqual(
            self.receipt["status"],
            "AUDIT_clearance_scope_extension_m383")
        self.assertTrue(self.receipt["finite_scope_extension_audit_only"])
        self.assertTrue(self.receipt["finite_diagnostic_only"])
        self.assertFalse(
            self.receipt["replacement_family_payment_theorem_proved"])
        self.assertFalse(self.receipt["near_adverse_upper_bound_proved"])
        self.assertFalse(self.receipt["goldbach_proved"])

    def test_m383_adds_only_near_threshold_adverse_rows(self):
        m383 = self.receipt["m383_holdout_scope"]
        classification = self.receipt["classification"]

        self.assertEqual(m383["scale_modulus"], 383)
        self.assertEqual(m383["prime_modulus"], 599)
        self.assertEqual(m383["weakest_label"], "00,12")
        self.assertEqual(
            m383["negative_denominator_family_counts"],
            {"far_3_plus": 0, "middle_2_to_3": 0, "near_1_to_2": 3})
        self.assertEqual(m383["middle_far_negative_row_count"], 0)
        self.assertFalse(
            classification["m383_adds_middle_far_adverse_example"])
        self.assertTrue(classification["near_threshold_adverse_rows_increased"])

    def test_extended_scope_still_has_single_middle_far_exemplar(self):
        extended = self.receipt["extended_source_scope"]
        classification = self.receipt["classification"]

        self.assertEqual(extended["checked_block_count"], 7)
        self.assertEqual(
            extended["negative_denominator_family_counts"],
            {"far_3_plus": 0, "middle_2_to_3": 1, "near_1_to_2": 20})
        self.assertEqual(extended["middle_far_negative_row_count"], 1)
        self.assertEqual(
            extended["known_middle_far_exception"]["scale_modulus"], 229)
        self.assertEqual(
            extended["known_middle_far_exception"]["prime_modulus"], 379)
        self.assertEqual(
            extended["known_middle_far_exception"]["largest_middle_negative"][
                "reduced_denominator"],
            46189)
        self.assertTrue(
            classification[
                "extended_scope_still_single_q46189_middle_far_exemplar"])

    def test_m383_ratio_and_next_action_are_pinned(self):
        m383 = self.receipt["m383_holdout_scope"]
        action = self.receipt["candidate_next_action"]

        self.assertAlmostEqual(
            m383["near_negative_over_middle_far_positive"],
            0.0007470818732461599)
        self.assertEqual(
            action["name"], "symbolic Q46189 or targeted middle/far search")
        self.assertIn("Do not keep extending adjacent tight blocks",
                      action["smallest_next_test"])


if __name__ == "__main__":
    unittest.main()
