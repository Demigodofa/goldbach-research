import json
import unittest
from pathlib import Path


EVIDENCE = Path(
    "evidence/"
    "mobius-moment-square-degree5-puncture-reachability-audit.json")


class MobiusMomentSquareDegree5PunctureReachabilityAuditTests(
        unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = json.loads(EVIDENCE.read_text(encoding="utf-8"))
        cls.summary = cls.receipt["puncture_summaries"][0]

    def test_receipt_preserves_boundaries(self):
        self.assertEqual(
            self.receipt["status"],
            "AUDIT_degree5_puncture_source_reachability")
        self.assertTrue(self.receipt["finite_reachability_audit_only"])
        self.assertTrue(self.receipt["finite_diagnostic_only"])
        self.assertFalse(self.receipt["goldbach_proved"])
        self.assertFalse(
            self.receipt["source_admissible_window_theorem_proved"])
        self.assertFalse(self.receipt["endpoint_swap_theorem_proved"])

    def test_start_one_is_unreachable_from_source_mapping(self):
        summary = self.summary

        self.assertEqual(summary["scale_modulus"], 149)
        self.assertEqual(summary["prime_modulus"], 163)
        self.assertEqual(summary["label"], "00,12")
        self.assertEqual(summary["row_count"], 32)
        self.assertEqual(summary["ell_freeze"], 48)
        self.assertEqual(summary["failure_start"], 1)
        self.assertEqual(summary["canonical_source_start"], 32)
        self.assertEqual(summary["translated_sweep_start_range"], [0, 64])
        self.assertTrue(summary["failure_start_in_translated_sweep"])
        self.assertFalse(summary["reachable_from_original_source_mapping"])
        self.assertEqual(summary["reachability"], "UNREACHABLE")

    def test_explicit_window_calculation_is_recorded(self):
        summary = self.summary

        self.assertEqual(summary["failure_start_window_rows_inclusive"],
                         [1, 32])
        self.assertEqual(summary["source_start_window_rows_inclusive"],
                         [32, 63])
        self.assertEqual(summary["prime_modulus_minus_scale_modulus"], 14)
        self.assertFalse(summary["p_minus_M_used_to_select_start"])
        self.assertIn("1!=32", summary["calculation"])


if __name__ == "__main__":
    unittest.main()
