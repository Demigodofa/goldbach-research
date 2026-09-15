import json
import unittest
from pathlib import Path


class Q286SignedPairCorrelationDefinitionTests(unittest.TestCase):
    def test_definition_freezes_exact_bad_branch(self):
        path = Path("evidence/q286-signed-pair-correlation-definition.json")
        receipt = json.loads(path.read_text(encoding="utf-8"))
        self.assertFalse(receipt["goldbach_proved"])
        self.assertIn("bad_branch", receipt["definition"]["operators"])
        self.assertIn("nu_N=mu_N-u_a", receipt["definition"]["centered_discrepancy"])
        self.assertIn(
            "strict-central",
            receipt["definition"]["strict_central_weight"].lower())
        self.assertIn(
            "binary Goldbach-in-progressions",
            receipt["status_boundary"])

        summary = receipt["summary"]
        self.assertEqual(summary["selected_residue_count"], 7)
        self.assertLess(
            summary["uniform_first_three_abs_error_summary"]["maximum"],
            1e-12)
        self.assertGreater(
            summary["uniform_full_action_summary"]["minimum"],
            0.0)
        self.assertGreater(
            summary["first_three_full_centered_cosine_summary"]["minimum"],
            0.75)
        self.assertLess(
            summary["first_three_full_centered_cosine_summary"]["maximum"],
            0.9)

        for row in receipt["selected_operator_rows"]:
            bad = row["bad_branch_centered_inequalities"]
            self.assertEqual(
                bad["first_three_centered_action_at_most"],
                -0.3)
            self.assertAlmostEqual(
                bad["full_centered_action_at_most"],
                -row["uniform_full_action_to_principal"])
            self.assertEqual(
                row["negative_first_three_orbit_count"]
                + row["positive_first_three_orbit_count"]
                + row["zero_first_three_orbit_count"],
                row["reflection_orbit_count"])


if __name__ == "__main__":
    unittest.main()
