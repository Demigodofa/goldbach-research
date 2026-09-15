import json
import unittest
from pathlib import Path


class Q286WbssFourModulusEdgeCharacterAuditTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/q286-wbss-four-modulus-edge-character-audit.json"
        ).read_text(encoding="utf-8"))

    def test_receipt_preserves_boundaries(self):
        receipt = self.load_receipt()

        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["character_sum_bound_proved"])
        self.assertFalse(receipt["four_modulus_projection_theorem_proved"])
        self.assertFalse(receipt["signed_discrepancy_theorem_proved"])
        self.assertTrue(receipt["universal_bound_open"])
        self.assertFalse(receipt["residual_absorption_constant_universal"])
        self.assertIn("finite q286-WBSS CRT edge-character",
                      receipt["status_boundary"])
        self.assertIn("finite fixture fits", receipt["status_boundary"])

    def test_character_translation_is_verified(self):
        receipt = self.load_receipt()
        summary = receipt["summary"]

        self.assertTrue(receipt["edge_translation_verified"])
        self.assertLess(summary["maximum_parseval_error"], 1e-9)
        self.assertLess(summary["maximum_reconstruction_error"], 1e-9)
        self.assertEqual(summary["zero_axis_nonzero_edge_character_count"], 0)

    def test_nonzero_supports_match_factor_anova_checkpoint(self):
        receipt = self.load_receipt()

        self.assertEqual(receipt["summary"]["nonzero_support_keys"], [
            "empty", "5", "7", "11", "13",
            "5,7", "5,13", "7,11", "11,13",
        ])
        self.assertTrue(
            receipt["no_three_or_four_factor_character_obligations"])

    def test_edge_character_counts_name_the_hard_obligations(self):
        receipt = self.load_receipt()
        summary = receipt["summary"]

        self.assertEqual(summary["edge_character_counts"], {
            "5,7": 8,
            "5,13": 17,
            "7,11": 23,
            "11,13": 50,
        })
        self.assertEqual(
            summary["fully_nonprincipal_edge_character_count"], 98)
        self.assertEqual(summary["total_nonconstant_character_count"], 110)
        self.assertEqual(summary["nonzero_singleton_character_count"], 12)

    def test_each_binary_prime_obligation_has_no_principal_axis_terms(self):
        receipt = self.load_receipt()
        obligations = receipt["binary_prime_theorem_obligations"]

        self.assertEqual(
            [row["edge_key"] for row in obligations],
            ["5,7", "5,13", "7,11", "11,13"],
        )
        self.assertTrue(all(
            row["zero_axis_nonzero_character_count"] == 0
            for row in obligations))


if __name__ == "__main__":
    unittest.main()
