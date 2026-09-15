import json
import unittest
from pathlib import Path


class Q286ThreeSupportKnownExtremalsAuditTests(unittest.TestCase):
    def test_known_extremals_demote_tail_simplification(self):
        path = Path(
            "evidence/q286-three-support-known-extremals-audit.json")
        receipt = json.loads(path.read_text(encoding="utf-8"))

        self.assertTrue(receipt["known_extremals_audit_measured"])
        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["three_support_action_reduction_proved"])
        self.assertFalse(receipt["signed_prime_correlation_estimate_proved"])

        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["tested_target_count"], 113)
        self.assertEqual(
            receipt["top_three_support_labels"], ["11x13", "7x11", "5x7"])
        self.assertEqual(receipt["top_three_natural_moduli"], [286, 154, 70])
        self.assertGreater(receipt["top_three_energy_fraction"], 0.99)
        self.assertLess(
            receipt["maximum_support_reconstruction_relative_error"], 1e-12)

        self.assertFalse(
            receipt[
                "all_known_extremal_sign_decisions_preserved_by_top_three"])
        self.assertEqual(receipt["tail_changes_sign_decision_count"], 16)
        self.assertEqual(
            receipt["source_summaries"]["fresh_holdout_cycle_minimum"][
                "tail_changes_sign_decision_count"],
            0,
        )
        self.assertEqual(
            receipt["source_summaries"]["census_nonpositive_raw_action"][
                "tail_changes_sign_decision_count"],
            16,
        )

        self.assertIn("cannot be demoted", receipt["decision"])
        self.assertIn(
            "frequency stress skeleton",
            receipt["candidate_curiosity_mechanism"]["name"],
        )


if __name__ == "__main__":
    unittest.main()
