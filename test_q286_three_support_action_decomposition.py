import json
import unittest
from pathlib import Path


class Q286ThreeSupportActionDecompositionTests(unittest.TestCase):
    def test_three_support_decomposition_keeps_tail_explicit(self):
        path = Path("evidence/q286-three-support-action-decomposition.json")
        receipt = json.loads(path.read_text(encoding="utf-8"))

        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["three_support_action_reduction_proved"])
        self.assertFalse(receipt["signed_prime_correlation_estimate_proved"])
        self.assertTrue(receipt["support_action_decomposition_measured"])

        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["tested_target_count"], 10)
        self.assertEqual(
            receipt["top_three_support_labels"], ["11x13", "7x11", "5x7"])
        self.assertEqual(receipt["top_three_natural_moduli"], [286, 154, 70])
        self.assertGreater(receipt["top_three_energy_fraction"], 0.99)
        self.assertLess(
            receipt["maximum_support_reconstruction_relative_error"], 1e-12)

        self.assertGreaterEqual(
            receipt["principal_plus_top_three_positive_count"],
            receipt["full_action_positive_count"] - 1)
        self.assertLessEqual(
            receipt["tail_changes_sign_decision_count"], 1)

        for row in receipt["rows"]:
            rebuilt = (
                row["principal_plus_top_three_to_principal_ratio"]
                + row["tail_centered_to_principal_ratio"])
            self.assertAlmostEqual(
                rebuilt,
                row["full_action_to_principal_ratio"],
                places=10)

        self.assertIn("E_286", receipt["decision"]
                      + receipt["candidate_mechanism"]
                      + receipt["status_boundary"])


if __name__ == "__main__":
    unittest.main()
