import json
import unittest
from pathlib import Path


class Q286UnnormalizedDualEdgeWitnessAuditTests(unittest.TestCase):
    def test_raw_witness_receipt_preserves_boundaries(self):
        receipt = json.loads(Path(
            "evidence/q286-unnormalized-dual-edge-witness-audit.json"
        ).read_text(encoding="utf-8"))

        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["unnormalized_edge_witness_theorem_proved"])
        self.assertFalse(receipt["normalization_gap_closed"])
        self.assertIn("finite unnormalized dual-edge witness",
                      receipt["status_boundary"])

    def test_post_discovery_raw_witnesses_are_positive(self):
        receipt = json.loads(Path(
            "evidence/q286-unnormalized-dual-edge-witness-audit.json"
        ).read_text(encoding="utf-8"))
        summary = receipt["summary"]
        post = summary["post_discovery_rows"]

        self.assertEqual(summary["target_row_count"], 230)
        self.assertEqual(summary["post_discovery_target_count"], 196)
        self.assertEqual(post["observed_strict_central_pair_rows"], 196)
        self.assertEqual(post["positive_raw_signed_witness_rows"], 196)
        self.assertGreater(
            post["raw_margin_after_rescue_summary"]["minimum"], 0.0)
        self.assertLess(
            post["raw_margin_identity_error_summary"]["maximum"], 1e-8)

    def test_tightest_raw_margin_is_recorded(self):
        receipt = json.loads(Path(
            "evidence/q286-unnormalized-dual-edge-witness-audit.json"
        ).read_text(encoding="utf-8"))
        tightest = receipt[
            "summary"]["tightest_post_discovery_raw_margin_rows"][0]

        self.assertEqual(tightest["target"], 94856)
        self.assertGreater(tightest["raw_margin_after_rescue"], 490.0)
        self.assertLess(tightest["raw_margin_after_rescue"], 491.0)
        self.assertAlmostEqual(
            tightest["raw_margin_after_rescue"],
            tightest["raw_full_signed_witness"],
            places=7)


if __name__ == "__main__":
    unittest.main()
