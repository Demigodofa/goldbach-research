import json
import unittest
from pathlib import Path


EVIDENCE = Path("evidence/q286-l2-vs-one-sided-adverse-separation-audit.json")


class Q286L2VsOneSidedAdverseSeparationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = json.loads(EVIDENCE.read_text(encoding="utf-8"))

    def test_preserves_boundaries(self):
        self.assertEqual(
            self.receipt["status"],
            "AUDIT_q286_l2_vs_one_sided_adverse_separation",
        )
        self.assertTrue(self.receipt["finite_separation_audit_only"])
        self.assertFalse(self.receipt["aggregate_l2_theorem_proved"])
        self.assertFalse(
            self.receipt["one_sided_adverse_projection_theorem_proved"])
        self.assertFalse(self.receipt["goldbach_proved"])

    def test_l2_violations_still_have_positive_adverse_gate(self):
        pop = self.receipt["population"]
        self.assertEqual(pop["joined_row_count"], 348)
        self.assertEqual(pop["row_local_l2_cap_violation_count"], 120)
        self.assertEqual(pop["global_min_l2_cap_violation_count"], 301)
        self.assertEqual(pop["raw_adverse_gate_failure_count"], 0)
        self.assertEqual(
            pop["row_local_l2_violations_with_positive_adverse_gate"],
            pop["row_local_l2_cap_violation_count"],
        )

    def test_l2_ratio_is_weak_adverse_proxy(self):
        sep = self.receipt["separation_metrics"]
        self.assertLess(
            abs(sep["pearson_row_l2_ratio_vs_raw_adverse_ratio"]),
            0.2,
        )
        self.assertEqual(
            sep["row_l2_violations_with_adverse_ratio_below_0_05"],
            77,
        )
        self.assertEqual(
            sep["row_l2_violations_with_adverse_ratio_below_0_10"],
            103,
        )

    def test_route_decision_demotes_symmetric_l2(self):
        decision = self.receipt["route_decision"]
        self.assertTrue(
            decision["symmetric_l2_is_too_strong_as_immediate_bridge"])
        self.assertIn("one-sided raw adverse projection",
                      decision["preferred_next_theorem_shape"])
        self.assertIn("reservoir", decision["l2_retained_as"])

    def test_extreme_row_is_recorded(self):
        row = self.receipt["extreme_rows"][
            "worst_adverse_ratio_among_row_l2_violations"]
        self.assertEqual(row["target"], 1124642)
        self.assertGreater(row["raw_adverse_gate_gap"], 0)
        self.assertTrue(row["exceeds_row_local_l2_cap"])


if __name__ == "__main__":
    unittest.main()
