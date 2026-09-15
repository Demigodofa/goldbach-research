import json
import unittest
from pathlib import Path


class Q286SupportTailStabilityWindowAuditTests(unittest.TestCase):
    def test_later_windows_have_no_support_tail_sign_flips(self):
        path = Path("evidence/q286-support-tail-stability-window-audit.json")
        receipt = json.loads(path.read_text(encoding="utf-8"))

        self.assertTrue(receipt["support_tail_stability_window_measured"])
        self.assertFalse(receipt["tail_stable_threshold_proved"])
        self.assertFalse(receipt["signed_tail_control_theorem_proved"])
        self.assertFalse(receipt["goldbach_proved"])

        validation = receipt["validation_against_action_reference"]
        self.assertTrue(validation["matches_reference"])
        self.assertLess(validation["maximum_dominant_delta"], 1e-12)
        self.assertLess(validation["maximum_tail_delta"], 1e-12)
        self.assertLess(validation["maximum_full_delta"], 1e-12)

        aggregate = receipt["aggregate"]
        self.assertEqual(aggregate["target_count"], 85085)
        self.assertEqual(aggregate["tail_sign_change_count"], 0)
        self.assertEqual(aggregate["negative_tail_kill_count"], 0)
        self.assertEqual(aggregate["positive_tail_rescue_count"], 0)
        self.assertEqual(aggregate["full_action_nonpositive_count"], 0)
        self.assertEqual(
            aggregate["principal_plus_dominant_nonpositive_count"], 0)
        self.assertLess(aggregate["maximum_reconstruction_error"], 1e-12)

        windows = {row["name"]: row for row in receipt["windows"]}
        self.assertEqual(windows["checked_positive_suffix"]["target_count"],
                         80080)
        self.assertEqual(
            windows["fresh_next_arithmetic_cycle"]["target_count"], 5005)
        self.assertGreater(
            windows["checked_positive_suffix"][
                "negative_tail_erodes_positive_partial_count"],
            0,
        )
        self.assertEqual(
            receipt["candidate_status"],
            "supported_finite_tail_stability_candidate")


if __name__ == "__main__":
    unittest.main()
