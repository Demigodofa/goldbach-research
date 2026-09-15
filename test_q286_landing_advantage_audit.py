import json
import unittest
from pathlib import Path


class Q286LandingAdvantageAuditTests(unittest.TestCase):
    def test_landing_advantage_splits_boundary_from_later_windows(self):
        path = Path("evidence/q286-landing-advantage-audit.json")
        receipt = json.loads(path.read_text(encoding="utf-8"))

        self.assertTrue(receipt["landing_advantage_measured"])
        self.assertFalse(receipt["q286_landing_advantage_theorem_proved"])
        self.assertFalse(receipt["goldbach_proved"])

        validation = receipt["validation_against_action_reference"]
        self.assertTrue(validation["matches_reference"])
        self.assertLess(validation["maximum_partial_delta"], 1e-12)
        self.assertLess(validation["maximum_tail_delta"], 1e-12)
        self.assertLess(validation["maximum_full_delta"], 1e-12)

        aggregate = receipt["aggregate"]
        self.assertEqual(aggregate["target_count"], 85198)
        self.assertEqual(aggregate["tail_sign_change_count"], 16)
        self.assertEqual(aggregate["negative_tail_kill_count"], 16)
        self.assertEqual(aggregate["positive_tail_rescue_count"], 0)
        self.assertLess(aggregate["maximum_full_reconstruction_error"], 1e-8)

        windows = {row["name"]: row for row in receipt["windows"]}
        self.assertEqual(windows["known_extremals"]["target_count"], 113)
        self.assertEqual(
            windows["known_extremals"]["negative_tail_kill_count"], 16)
        self.assertEqual(
            windows["checked_positive_suffix"]["negative_tail_kill_count"], 0)
        self.assertEqual(
            windows["fresh_next_arithmetic_cycle"][
                "negative_tail_kill_count"],
            0,
        )
        self.assertGreater(
            windows["checked_positive_suffix"][
                "full_positive_to_negative_drag_ratio_summary"]["minimum"],
            1.0,
        )
        self.assertGreater(
            windows["fresh_next_arithmetic_cycle"][
                "full_positive_to_negative_drag_ratio_summary"]["minimum"],
            1.0,
        )


if __name__ == "__main__":
    unittest.main()
