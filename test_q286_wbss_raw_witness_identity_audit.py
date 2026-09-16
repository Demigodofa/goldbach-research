import json
import unittest
from pathlib import Path


class Q286WbssRawWitnessIdentityAuditTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/q286-wbss-raw-witness-identity-audit.json"
        ).read_text(encoding="utf-8"))

    def test_receipt_preserves_proof_boundaries(self):
        receipt = self.load_receipt()

        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["raw_witness_theorem_proved"])
        self.assertFalse(receipt["positive_mass_theorem_proved"])
        self.assertFalse(receipt["pointwise_adverse_drag_theorem_proved"])
        self.assertTrue(receipt["universal_bound_open"])
        self.assertIn("finite rows are calibration",
                      receipt["status_boundary"])

    def test_raw_bridge_is_stated_without_normalized_mass_assumption(self):
        receipt = self.load_receipt()
        definitions = receipt["definitions"]

        self.assertIn("If T_N=0", definitions["raw_witness"])
        self.assertIn("raw sum is empty and equals 0",
                      definitions["raw_witness"])
        self.assertIn("forces at least one strict-central prime pair",
                      definitions["noncircular_bridge"])
        self.assertIn(
            "W_phi(N)>0",
            receipt["candidate"]["smallest_next_theorem_target"])

    def test_finite_rows_scale_to_positive_raw_witnesses(self):
        receipt = self.load_receipt()
        summary = receipt["finite_calibration"]["summary"]

        self.assertEqual(summary["row_count"], 348)
        self.assertEqual(summary["target_minimum"], 1036248)
        self.assertEqual(summary["target_maximum"], 1155862)
        self.assertEqual(summary["zero_pair_count_rows"], 0)
        self.assertEqual(summary["zero_total_weight_rows"], 0)
        self.assertEqual(summary["positive_raw_witness_count"], 348)
        self.assertEqual(summary["positive_raw_adverse_gate_gap_count"], 348)
        self.assertEqual(summary["pair_count_mismatch_count"], 0)

    def test_raw_reconstruction_errors_are_small(self):
        receipt = self.load_receipt()
        summary = receipt["finite_calibration"]["summary"]

        self.assertLess(
            summary["raw_formula_reconstruction_error_summary"]["maximum"],
            1e-8)
        self.assertLess(
            summary[
                "raw_adverse_gap_reconstruction_error_summary"]["maximum"],
            1e-8)

    def test_tightest_raw_rows_are_pinned(self):
        receipt = self.load_receipt()
        summary = receipt["finite_calibration"]["summary"]

        raw_witness_row = summary["minimum_raw_witness_row"]
        raw_gap_row = summary["minimum_raw_adverse_gate_gap_row"]
        min_weight_row = summary["minimum_total_weight_row"]

        self.assertEqual(raw_witness_row["target"], 1059514)
        self.assertEqual(raw_gap_row["target"], 1059514)
        self.assertEqual(min_weight_row["target"], 1042424)
        self.assertAlmostEqual(raw_witness_row["raw_witness"],
                               286929.1729900493,
                               places=6)
        self.assertAlmostEqual(raw_gap_row["raw_adverse_gate_gap"],
                               286929.1729900494,
                               places=6)
        self.assertAlmostEqual(min_weight_row["total_weight"],
                               443620.45738706784,
                               places=6)


if __name__ == "__main__":
    unittest.main()
