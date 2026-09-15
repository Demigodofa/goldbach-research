import json
import unittest
from pathlib import Path


class Q286WbssFourModulusSpanIdentityAuditTests(unittest.TestCase):
    def test_receipt_preserves_boundaries(self):
        receipt = json.loads(Path(
            "evidence/q286-wbss-four-modulus-span-identity-audit.json"
        ).read_text(encoding="utf-8"))

        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["four_modulus_projection_theorem_proved"])
        self.assertFalse(receipt["signed_discrepancy_theorem_proved"])
        self.assertIn("finite algebraic span audit",
                      receipt["status_boundary"])

    def test_unit_level_four_modulus_identity_implies_all_even_residues(self):
        receipt = json.loads(Path(
            "evidence/q286-wbss-four-modulus-span-identity-audit.json"
        ).read_text(encoding="utf-8"))

        self.assertTrue(
            receipt["unit_level_identity_implies_all_even_target_residues"])
        self.assertEqual(receipt["even_target_residue_count"], 5005)
        self.assertEqual(
            receipt["implied_exact_even_target_residue_count"], 5005)

    def test_modulus_130_is_required_beyond_dominant_supports(self):
        receipt = json.loads(Path(
            "evidence/q286-wbss-four-modulus-span-identity-audit.json"
        ).read_text(encoding="utf-8"))
        unit = receipt["unit_level_summary"]

        self.assertGreater(
            unit["dominant_support_moduli"]["relative_l2_residual"], 1e-3)
        self.assertLess(
            unit["four_modulus_support"]["relative_l2_residual"], 1e-12)
        self.assertLess(
            unit["four_modulus_support"]["max_abs_residual"], 1e-10)

    def test_representative_target_orbits_inherit_four_modulus_span(self):
        receipt = json.loads(Path(
            "evidence/q286-wbss-four-modulus-span-identity-audit.json"
        ).read_text(encoding="utf-8"))
        summary = receipt["spot_target_residue_summary"]

        self.assertEqual(
            summary["four_modulus_support"]["exact_span_count"],
            len(receipt["spot_target_residues"]),
        )
        self.assertEqual(
            summary["dominant_support_moduli"]["span_failure_count"],
            len(receipt["spot_target_residues"]),
        )
        self.assertLess(
            summary["four_modulus_support"]["maximum_relative_l2_residual"],
            1e-10)


if __name__ == "__main__":
    unittest.main()
