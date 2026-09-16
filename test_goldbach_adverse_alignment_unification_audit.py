import json
import unittest
from pathlib import Path


EVIDENCE = Path("evidence/goldbach-adverse-alignment-unification-audit.json")


class GoldbachAdverseAlignmentUnificationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = json.loads(EVIDENCE.read_text(encoding="utf-8"))

    def test_preserves_proof_boundaries(self):
        self.assertEqual(
            self.receipt["status"],
            "AUDIT_goldbach_adverse_alignment_unification")
        self.assertTrue(self.receipt["combined_as_shared_language_only"])
        self.assertFalse(self.receipt["merged_numeric_formula_established"])
        self.assertFalse(self.receipt["adverse_alignment_theorem_proved"])
        self.assertFalse(self.receipt["goldbach_proved"])

    def test_schema_contains_both_instantiations(self):
        self.assertIn("A_D(N)", self.receipt["shared_schema"]["formula_template"])
        self.assertIn("q286_instantiation", self.receipt)
        self.assertIn("q46189_instantiation", self.receipt)
        self.assertEqual(
            self.receipt["q286_instantiation"]["channels"],
            ["70", "130", "154", "286"],
        )
        self.assertIn(
            "source-block",
            self.receipt["q46189_instantiation"]["channels"],
        )

    def test_q46189_is_diagnostic_not_theorem_ready(self):
        q46189 = self.receipt["q46189_instantiation"]
        self.assertEqual(q46189["best_input_feature"]["feature"],
                         "missing_count")
        self.assertEqual(q46189["best_matrix_feature"]["feature"],
                         "tension_sum")
        self.assertIn("not theorem-ready", q46189["current_strength"])

    def test_next_action_returns_to_q286_raw_definition(self):
        action = self.receipt["candidate_next_action"]
        self.assertEqual(action["name"],
                         "q286 raw adverse-envelope definition audit")
        self.assertIn("actually raw", action["mechanism"])
        self.assertIn("hidden normalization", action["falsifier"])


if __name__ == "__main__":
    unittest.main()
