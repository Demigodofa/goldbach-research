import json
import unittest
from pathlib import Path


class Q286LowerFaceOverlapAuditTests(unittest.TestCase):
    def test_actual_rows_avoid_lower_face_support(self):
        path = Path("evidence/q286-lower-face-overlap-audit.json")
        receipt = json.loads(path.read_text(encoding="utf-8"))

        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["lower_face_overlap_theorem_proved"])
        self.assertIn("lower-face overlap", receipt["status_boundary"])

        summary = receipt["summary"]
        self.assertEqual(summary["target_row_count"], 230)
        self.assertEqual(summary["valid_target_row_count"], 230)
        self.assertEqual(summary["post_discovery_target_count"], 196)

        post_overlap = (
            summary[
                "post_discovery_actual_mass_on_lower_face_support_summary"])
        post_tv = (
            summary["post_discovery_total_variation_from_lower_face_summary"])
        post_surplus = (
            summary["post_discovery_actual_surplus_above_lower_face_summary"])
        post_transport = (
            summary[
                "post_discovery_transport_positive_to_negative_ratio_summary"])

        self.assertLess(post_overlap["maximum"], 0.02)
        self.assertGreater(post_tv["minimum"], 0.98)
        self.assertGreater(post_surplus["minimum"], 3.0)
        self.assertGreater(post_transport["minimum"], 3.0)

    def test_transport_identities_hold(self):
        path = Path("evidence/q286-lower-face-overlap-audit.json")
        receipt = json.loads(path.read_text(encoding="utf-8"))

        transport_errors = receipt["summary"]["transport_error_summary"]
        self.assertLess(transport_errors["maximum"], 1e-8)

        for row in receipt["target_rows"]:
            self.assertGreaterEqual(row["lower_face_support_size"], 1)
            self.assertLess(
                row["actual_mass_on_lower_face_support"], 0.07)
            self.assertAlmostEqual(
                row["overlap_with_lower_face_measure"],
                1.0 - row["total_variation_from_lower_face"],
                places=8)
            self.assertAlmostEqual(
                row["actual_surplus_above_lower_face"],
                row["transport_full_surplus"],
                places=8)


if __name__ == "__main__":
    unittest.main()
