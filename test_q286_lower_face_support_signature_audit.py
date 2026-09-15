import json
import unittest
from pathlib import Path


class Q286LowerFaceSupportSignatureAuditTests(unittest.TestCase):
    def test_support_signature_receipt_preserves_boundaries(self):
        receipt = json.loads(Path(
            "evidence/q286-lower-face-support-signature-audit.json"
        ).read_text(encoding="utf-8"))

        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(
            receipt["lower_face_support_signature_theorem_proved"])
        self.assertIn("finite lower-face support signature",
                      receipt["status_boundary"])
        self.assertEqual(receipt["curiosity_status"], "aha-candidate")

    def test_post_discovery_support_geometry(self):
        receipt = json.loads(Path(
            "evidence/q286-lower-face-support-signature-audit.json"
        ).read_text(encoding="utf-8"))
        summary = receipt["summary"]
        post = summary["post_discovery_rows"]

        self.assertEqual(summary["target_row_count"], 230)
        self.assertEqual(summary["post_discovery_target_count"], 196)
        self.assertEqual(post["complete_support_rows"], 196)
        self.assertEqual(post["support_size_histogram"], {"2": 196})
        self.assertEqual(summary["post_complement_closed_support_rows"], 196)
        self.assertTrue(receipt["dominant_negative_full_face_supported"])
        self.assertGreaterEqual(post["all_full_negative_rows"], 150)
        self.assertGreaterEqual(post["positive_f3_compensator_rows"], 190)
        self.assertGreater(
            post["negative_full_lower_mass_fraction_summary"]["minimum"],
            0.9)
        self.assertLess(
            post["actual_mass_on_extracted_support_summary"]["maximum"],
            0.02)

    def test_simple_residue_signature_is_not_supported(self):
        receipt = json.loads(Path(
            "evidence/q286-lower-face-support-signature-audit.json"
        ).read_text(encoding="utf-8"))
        post = receipt["summary"]["post_discovery_rows"]

        self.assertFalse(receipt["simple_residue_signature_supported"])
        self.assertGreaterEqual(
            post["support_signature_unique_counts"]["286"], 100)
        self.assertLess(post["top_support_signature_share_mod_286"], 0.1)


if __name__ == "__main__":
    unittest.main()
