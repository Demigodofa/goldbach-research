import json
import unittest
from pathlib import Path


class Q286LowerFaceDualEdgeAuditTests(unittest.TestCase):
    def test_dual_edge_receipt_preserves_boundaries(self):
        receipt = json.loads(Path(
            "evidence/q286-lower-face-dual-edge-audit.json"
        ).read_text(encoding="utf-8"))

        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["lower_face_dual_edge_theorem_proved"])
        self.assertIn("finite lower-face dual-edge",
                      receipt["status_boundary"])
        self.assertEqual(receipt["curiosity_status"], "aha-candidate")

    def test_post_discovery_edges_are_valid_and_rescue(self):
        receipt = json.loads(Path(
            "evidence/q286-lower-face-dual-edge-audit.json"
        ).read_text(encoding="utf-8"))
        summary = receipt["summary"]
        post = summary["post_discovery_rows"]

        self.assertEqual(summary["target_row_count"], 230)
        self.assertEqual(summary["valid_edge_row_count"], 230)
        self.assertEqual(summary["post_discovery_target_count"], 196)
        self.assertEqual(
            summary["post_rows_with_edge_gap_rescue_ratio_above_one"], 196)
        self.assertLess(
            post["edge_formula_error_summary"]["maximum"], 1e-10)
        self.assertGreater(
            post["minimum_gap_over_all_orbits_summary"]["minimum"], -1e-10)
        self.assertGreater(
            post["edge_gap_rescue_ratio_summary"]["minimum"], 1.0)
        self.assertGreater(
            post["edge_gap_margin_after_rescue_summary"]["minimum"], 0.0)

    def test_tightest_row_is_near_sharp_but_positive(self):
        receipt = json.loads(Path(
            "evidence/q286-lower-face-dual-edge-audit.json"
        ).read_text(encoding="utf-8"))
        tightest = receipt[
            "summary"]["tightest_post_discovery_edge_rescue_rows"][0]

        self.assertEqual(tightest["target"], 94856)
        self.assertLess(tightest["edge_gap_rescue_ratio"], 1.003)
        self.assertGreater(tightest["edge_gap_rescue_ratio"], 1.0)
        self.assertAlmostEqual(
            tightest["edge_gap_margin_after_rescue"],
            tightest["actual_full"],
            places=8)


if __name__ == "__main__":
    unittest.main()
