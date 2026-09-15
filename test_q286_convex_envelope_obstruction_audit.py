import json
import unittest
from pathlib import Path


class Q286ConvexEnvelopeObstructionAuditTests(unittest.TestCase):
    def test_coefficient_hull_does_not_force_rescue(self):
        path = Path("evidence/q286-convex-envelope-obstruction-audit.json")
        receipt = json.loads(path.read_text(encoding="utf-8"))

        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["anti_extremality_theorem_proved"])
        self.assertIn(
            "coefficient-envelope",
            receipt["status_boundary"])

        summary = receipt["summary"]
        self.assertEqual(summary["target_row_count"], 230)
        self.assertEqual(summary["residue_count"], 204)
        self.assertEqual(
            summary["synthetic_tail_failure_residue_count"],
            summary["residue_count"])

        lower_tail = summary["minimum_full_on_tail_halfspace_summary"]
        self.assertLess(lower_tail["maximum"], 0.0)
        self.assertLess(lower_tail["mean"], -4.0)

        post_surplus = (
            summary[
                "post_discovery_actual_surplus_above_lower_envelope_summary"])
        self.assertEqual(post_surplus["count"], 196)
        self.assertGreater(post_surplus["minimum"], 3.0)

        positions = (
            summary["post_discovery_position_between_envelopes_summary"])
        self.assertGreater(positions["minimum"], 0.3)
        self.assertLess(positions["maximum"], 0.7)

    def test_rows_preserve_exact_lp_witnesses(self):
        path = Path("evidence/q286-convex-envelope-obstruction-audit.json")
        receipt = json.loads(path.read_text(encoding="utf-8"))

        for row in receipt["residue_rows"]:
            self.assertTrue(row["tail_and_full_failure_feasible"])
            witness = row["one_synthetic_tail_failure"]
            self.assertTrue(witness["success"])
            self.assertLessEqual(witness["first_three_value"], -0.3 + 1e-8)
            self.assertLessEqual(witness["full_value"], 1e-8)
            self.assertGreaterEqual(witness["support_size"], 1)

        for row in receipt["target_rows"]:
            lower = row["coefficient_lower_envelope"]
            upper = row["coefficient_upper_envelope"]
            self.assertTrue(lower["success"])
            self.assertTrue(upper["success"])
            self.assertGreater(
                row["actual_full"],
                lower["full_value"] - 1e-8)
            self.assertLess(
                row["actual_full"],
                upper["full_value"] + 1e-8)


if __name__ == "__main__":
    unittest.main()
