import json
import unittest
from pathlib import Path


class Q286WbssProjectionUniformityObstructionAuditTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/q286-wbss-projection-uniformity-obstruction-audit.json"
        ).read_text(encoding="utf-8"))

    def test_receipt_preserves_boundaries(self):
        receipt = self.load_receipt()

        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["projection_uniformity_theorem_proved"])
        self.assertFalse(receipt["four_modulus_formula_falsified"])
        self.assertTrue(
            receipt["blunt_projected_linf_uniformity_bridge_demoted"])
        self.assertIn("finite four-modulus projected-uniformity obstruction",
                      receipt["status_boundary"])

    def test_post_discovery_rows_are_outside_blunt_budget(self):
        receipt = self.load_receipt()
        summary = receipt["summary"]["post_discovery_rows"]

        self.assertEqual(summary["row_count"], 196)
        self.assertEqual(summary["positive_actual_expectation_count"], 196)
        self.assertEqual(
            summary["inside_blunt_projection_error_budget_count"], 0)
        self.assertEqual(
            summary["outside_blunt_projection_error_budget_count"], 196)
        self.assertGreater(
            summary["max_abs_projection_error_summary"]["minimum"],
            receipt["projection_error_budget"])

    def test_projection_formula_replays_actual_expectation(self):
        receipt = self.load_receipt()
        summary = receipt["summary"]["post_discovery_rows"]

        self.assertLess(
            summary["projection_formula_abs_error_summary"]["maximum"],
            1e-10)

    def test_all_four_moduli_are_reported(self):
        receipt = self.load_receipt()
        moduli = set(
            receipt["summary"]["post_discovery_modulus_summaries"].keys())

        self.assertEqual(moduli, {"70", "130", "154", "286"})


if __name__ == "__main__":
    unittest.main()
