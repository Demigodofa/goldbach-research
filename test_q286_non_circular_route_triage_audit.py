import json
import unittest
from pathlib import Path


class Q286NonCircularRouteTriageAuditTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/q286-non-circular-route-triage-audit.json"
        ).read_text(encoding="utf-8"))

    def test_receipt_is_route_triage_not_proof(self):
        receipt = self.load_receipt()

        self.assertEqual(
            receipt["status"],
            "HOLD_component_pair_is_sharper_current_theorem_obligation")
        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["non_circular_bridge_confirmed"])
        self.assertFalse(receipt["pointwise_adverse_drag_theorem_proved"])
        self.assertFalse(receipt["component_pair_closure_theorem_proved"])
        self.assertFalse(receipt["fixed_conductor_channel_theorem_proved"])
        self.assertTrue(receipt["universal_bound_open"])

    def test_wbss_plain_l2_is_put_in_reservoir(self):
        receipt = self.load_receipt()
        wbss = receipt["wbss_plain_l2_route"]

        self.assertEqual(wbss["role"], "reservoir_until_changed_condition")
        self.assertFalse(wbss["non_circular_bridge_confirmed"])
        self.assertFalse(wbss["zero_mass_defect_found"])
        self.assertEqual(wbss["checked_rows"], 348)
        self.assertEqual(wbss["row_local_l2_cap_violations"], 120)
        self.assertEqual(wbss["global_min_l2_cap_violations"], 301)
        self.assertEqual(wbss["worst_row"]["target"], 1089544)

    def test_component_pair_route_is_sharper_current_target(self):
        receipt = self.load_receipt()
        component = receipt["component_pair_route"]

        self.assertEqual(component["role"],
                         "sharper_current_theorem_obligation")
        self.assertEqual(component["tail_target_count"], 3)
        self.assertEqual(component["positive_strict_margin_count"], 3)
        self.assertTrue(
            component["all_tail_targets_have_positive_strict_margin"])
        self.assertEqual(component["tightest_selected_margin_target"],
                         1379072)
        self.assertAlmostEqual(component["tightest_selected_margin"],
                               0.48379401372791037,
                               places=12)
        self.assertAlmostEqual(
            component["calibrated_normalized_real_channel_linf_bound"],
            0.05885324711081062,
            places=14)
        self.assertTrue(component["active_conductors_35_77_named_in_note"])

    def test_route_decision_names_next_non_circular_target(self):
        receipt = self.load_receipt()
        decision = receipt["route_decision"]

        self.assertIn("component-pair active-lane",
                      decision["next_best_non_circular_target"])
        self.assertIn("plain aggregate WBSS L2 finite cap checks",
                      decision["sleep_or_reservoir"])
        self.assertIn("active-selector rarity",
                      decision["smallest_next_test"])


if __name__ == "__main__":
    unittest.main()
