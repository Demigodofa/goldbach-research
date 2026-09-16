import json
import unittest
from pathlib import Path


EVIDENCE = Path("evidence/goldbach-bridge-acceptance-gate-audit.json")


class GoldbachBridgeAcceptanceGateAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = json.loads(EVIDENCE.read_text(encoding="utf-8"))

    def test_receipt_is_gate_not_proof(self):
        receipt = self.receipt

        self.assertEqual(
            receipt["status"],
            "GATE_current_goldbach_bridge_acceptance")
        self.assertFalse(receipt["aggregate_l2_theorem_proved"])
        self.assertFalse(receipt["source_window_theorem_proved"])
        self.assertFalse(receipt["raw_adverse_drag_theorem_proved"])
        self.assertFalse(receipt["pointwise_adverse_drag_theorem_proved"])
        self.assertFalse(receipt["q286_threshold_theorem_proved"])
        self.assertFalse(receipt["strict_central_goldbach_theorem_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_l2_state_separates_zero_mass_from_bridge(self):
        l2 = self.receipt["zero_mass_l2_status"]

        self.assertTrue(
            l2["zero_mass_arithmetic_sanity_confirmed_on_checked_rows"])
        self.assertTrue(l2["raw_strict_l2_shape_is_noncircular"])
        self.assertFalse(l2["l2_logical_bridge_confirmed"])
        self.assertEqual(l2["observed_row_local_cap_violations"], 120)
        self.assertEqual(l2["observed_global_min_cap_violations"], 301)

    def test_pointwise_adverse_drag_is_live_gate_but_unproved(self):
        pointwise = self.receipt["pointwise_adverse_drag_status"]

        self.assertFalse(pointwise["finite_evidence_is_acceptance_condition"])
        self.assertEqual(pointwise["checked_rows"], 348)
        self.assertEqual(pointwise["checked_rows_failing_adverse_below_local"], 0)
        self.assertAlmostEqual(
            pointwise["worst_checked_ratio"],
            0.23148438379145228,
            places=15)
        self.assertEqual(pointwise["worst_checked_target"], 1124642)
        self.assertTrue(pointwise["universal_bound_open"])

    def test_metric_soft_source_window_is_not_promoted_to_bridge(self):
        metric = self.receipt["metric_soft_source_window_status"]

        self.assertTrue(metric["broad_all_translation_quantifier_falsified"])
        self.assertTrue(metric["all_source_starts_pass"])
        self.assertEqual(metric["failing_translated_start_count"], 1)
        self.assertEqual(metric["source_start_failure_count"], 0)
        self.assertIn("not a logical bridge", metric["role"])

    def test_bridge_table_classifies_three_routes(self):
        rows = {row["route"]: row for row in self.receipt["bridge_table"]}

        self.assertEqual(set(rows), {
            "q286 raw adverse-drag",
            "q286 normalized/aggregate L2",
            "metric-soft source-admissible window",
        })
        self.assertEqual(
            rows["q286 raw adverse-drag"]["state"],
            "live_theorem_target")
        self.assertTrue(rows["q286 raw adverse-drag"]["non_circular_shape"])
        self.assertFalse(
            rows["q286 normalized/aggregate L2"][
                "logical_bridge_confirmed"])
        self.assertEqual(
            rows["metric-soft source-admissible window"][
                "finite_evidence_role"],
            "source-window/admissible-window diagnostic only")

    def test_acceptance_gate_rejects_finite_closeouts(self):
        gate = self.receipt["acceptance_gate"]

        self.assertFalse(gate["finite_evidence_is_acceptance_condition"])
        self.assertIn(
            "universal pointwise unnormalized estimate",
            gate["current_required_bridge"])
        self.assertIn(
            "checked-row zero-mass sanity alone",
            gate["invalid_closeouts"])
        self.assertIn(
            "source-window metric-soft dominance without a Goldbach "
            "implication theorem",
            gate["invalid_closeouts"])


if __name__ == "__main__":
    unittest.main()
