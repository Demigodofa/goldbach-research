import json
import unittest
from pathlib import Path


class Q286WbssMod286InteractionAuditTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/q286-wbss-mod286-interaction-audit.json"
        ).read_text(encoding="utf-8"))

    def test_receipt_preserves_boundaries(self):
        receipt = self.load_receipt()

        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["interaction_theorem_proved"])
        self.assertFalse(receipt["signed_projection_theorem_proved"])
        self.assertIn("finite mod-286 coefficient-interaction diagnostic",
                      receipt["status_boundary"])

    def test_coefficient_is_almost_all_interaction(self):
        receipt = self.load_receipt()
        summary = receipt["coefficient_decomposition_summary"]

        self.assertEqual(summary["residue_count"], 120)
        self.assertGreater(summary["interaction_variance_share"], 0.999)
        self.assertLess(summary["additive_variance_share"], 0.001)
        self.assertLess(summary["max_abs_decomposition_residual"], 1e-12)

    def test_actual_drag_is_interaction_dominated(self):
        receipt = self.load_receipt()
        row_summary = receipt["row_summary"]

        self.assertEqual(row_summary["row_count"], 196)
        self.assertEqual(
            row_summary["total_mod286_signed_error"]["negative_count"], 196)
        self.assertEqual(
            row_summary["interaction_component"]["negative_count"], 196)
        self.assertLess(
            row_summary["component_reconstruction_abs_error_summary"][
                "maximum"], 1e-10)

    def test_one_factor_marginals_are_small_and_mixed(self):
        receipt = self.load_receipt()
        row_summary = receipt["row_summary"]

        self.assertGreater(
            row_summary["mod11_marginal_component"]["negative_count"], 0)
        self.assertGreater(
            row_summary["mod11_marginal_component"]["positive_count"], 0)
        self.assertGreater(
            row_summary["mod13_marginal_component"]["negative_count"], 0)
        self.assertGreater(
            row_summary["mod13_marginal_component"]["positive_count"], 0)
        self.assertLess(
            abs(row_summary["additive_marginal_component"]["summary"][
                "maximum"]), 0.004)
        self.assertLess(
            abs(row_summary["additive_marginal_component"]["summary"][
                "minimum"]), 0.004)


if __name__ == "__main__":
    unittest.main()
