import json
import unittest
from pathlib import Path


class Q286ConeDualityL1UniformityCandidateTests(unittest.TestCase):
    def test_receipt_records_l1_candidate_demotion(self):
        path = Path("evidence/q286-cone-duality-l1-uniformity-candidate.json")
        receipt = json.loads(path.read_text(encoding="utf-8"))
        summary = receipt["summary"]
        self.assertEqual(summary["selected_target_count"], 7)
        self.assertEqual(summary["selected_residue_count"], 7)
        self.assertEqual(summary["lp_feasible_bad_residue_count"], 7)
        self.assertEqual(summary["lp_infeasible_bad_residue_count"], 0)
        self.assertEqual(
            summary["actual_targets_passing_l1_uniformity_certificate"], [])
        self.assertEqual(
            summary["actual_target_certificate_pass_count"], 0)
        self.assertLess(summary["maximum_reconstruction_error"], 1e-12)
        self.assertAlmostEqual(
            summary["minimum_bad_l1_summary"]["minimum"],
            0.05724560696825869)
        self.assertGreater(
            summary["actual_l1_summary"]["minimum"],
            summary["minimum_bad_l1_summary"]["maximum"])
        self.assertFalse(receipt["goldbach_proved"])


if __name__ == "__main__":
    unittest.main()

