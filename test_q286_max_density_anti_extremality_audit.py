import json
import unittest
from pathlib import Path


class Q286MaxDensityAntiExtremalityAuditTests(unittest.TestCase):
    def test_max_density_cone_is_too_crude(self):
        path = Path("evidence/q286-max-density-anti-extremality-audit.json")
        receipt = json.loads(path.read_text(encoding="utf-8"))

        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["maximum_density_theorem_proved"])
        self.assertIn("maximum-density", receipt["status_boundary"])

        summary = receipt["summary"]
        self.assertEqual(summary["target_row_count"], 230)
        self.assertEqual(summary["residue_count"], 204)
        self.assertEqual(summary["lp_success_count"], 204)
        self.assertEqual(summary["actual_certificate_pass_count"], 0)
        self.assertEqual(summary["post_discovery_certificate_pass_count"], 0)

        bad_density = summary["minimum_bad_max_density_multiple_summary"]
        actual_density = summary["actual_max_orbit_density_multiple_summary"]
        ratio = summary["actual_to_minimum_bad_density_ratio_summary"]

        self.assertLess(bad_density["minimum"], 1.1)
        self.assertLess(bad_density["maximum"], 1.25)
        self.assertGreater(actual_density["minimum"], 3.0)
        self.assertGreater(ratio["minimum"], 2.9)

    def test_every_target_has_density_threshold_comparison(self):
        path = Path("evidence/q286-max-density-anti-extremality-audit.json")
        receipt = json.loads(path.read_text(encoding="utf-8"))

        for row in receipt["residue_rows"]:
            self.assertTrue(row["lp_success"])
            self.assertGreater(row["minimum_bad_max_density_multiple"], 1.0)
            self.assertLessEqual(row["bad_first_three"], -0.3 + 1e-8)
            self.assertLessEqual(row["bad_full"], 1e-8)

        for row in receipt["target_rows"]:
            self.assertTrue(row["actual_measure_available"])
            self.assertFalse(row["passes_max_density_certificate"])
            self.assertGreater(
                row["actual_max_orbit_density_multiple"],
                row["minimum_bad_max_density_multiple"])
            self.assertGreater(
                row["actual_to_minimum_bad_density_ratio"], 1.0)


if __name__ == "__main__":
    unittest.main()
