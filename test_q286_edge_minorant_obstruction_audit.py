import json
import unittest
from pathlib import Path


class Q286EdgeMinorantObstructionAuditTests(unittest.TestCase):
    def test_minorant_obstruction_preserves_boundaries(self):
        receipt = json.loads(Path(
            "evidence/q286-edge-minorant-obstruction-audit.json"
        ).read_text(encoding="utf-8"))

        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["coefficientwise_minorant_theorem_proved"])
        self.assertTrue(receipt["pointwise_minorant_candidate_falsified"])
        self.assertIn("finite edge-minorant obstruction",
                      receipt["status_boundary"])

    def test_pointwise_minorant_fails_but_signed_distribution_rescues(self):
        receipt = json.loads(Path(
            "evidence/q286-edge-minorant-obstruction-audit.json"
        ).read_text(encoding="utf-8"))
        summary = receipt["summary"]
        post = summary["post_discovery_rows"]

        self.assertEqual(summary["target_row_count"], 230)
        self.assertEqual(summary["post_discovery_target_count"], 196)
        self.assertEqual(post["pointwise_minorant_pass_count"], 0)
        self.assertEqual(post["support_orbits_negative_count"], 196)
        self.assertLess(
            post["minimum_pointwise_rescue_coefficient_summary"]["maximum"],
            0.0)
        self.assertGreater(
            post["positive_to_negative_rescue_ratio_summary"]["minimum"],
            1.0)
        self.assertGreater(
            post["rescue_margin_from_signed_parts_summary"]["minimum"],
            0.0)
        self.assertLess(
            post["signed_part_identity_error_summary"]["maximum"], 1e-10)

    def test_tightest_signed_part_row_is_recorded(self):
        receipt = json.loads(Path(
            "evidence/q286-edge-minorant-obstruction-audit.json"
        ).read_text(encoding="utf-8"))
        weakest = receipt[
            "summary"]["weakest_post_discovery_signed_part_rows"][0]

        self.assertEqual(weakest["target"], 94856)
        self.assertFalse(weakest["pointwise_minorant_pass"])
        self.assertGreater(
            weakest["positive_to_negative_rescue_ratio"], 1.0)
        self.assertLess(
            weakest["positive_to_negative_rescue_ratio"], 1.02)


if __name__ == "__main__":
    unittest.main()
