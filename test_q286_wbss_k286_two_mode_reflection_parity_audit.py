import json
import unittest
from pathlib import Path


class Q286WbssK286TwoModeReflectionParityAuditTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/q286-wbss-k286-two-mode-reflection-parity-audit.json"
        ).read_text(encoding="utf-8"))

    def test_receipt_is_audit_not_proof(self):
        receipt = self.load_receipt()

        self.assertEqual(
            receipt["status"],
            "AUDIT_k286_two_mode_reflection_parity_not_proof")
        self.assertTrue(receipt["reflection_odd_null_identity_checked"])
        self.assertTrue(
            receipt["reflection_fails_as_universal_two_mode_simplifier"])
        self.assertFalse(receipt["zero_mass_check_is_logical_bridge"])
        self.assertFalse(receipt["l2_target_non_circular_confirmed"])
        self.assertFalse(receipt["binary_prime_moment_theorem_proved"])
        self.assertFalse(receipt["raw_adverse_drag_bound_proved"])
        self.assertFalse(receipt["universal_pointwise_bound_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_combined_two_mode_reflection_numbers_are_pinned(self):
        receipt = self.load_receipt()
        summary = receipt["combined_top_two_scaled"]["summary"]

        self.assertAlmostEqual(
            summary["even_energy_fraction_summary"]["minimum"],
            0.399466343237569,
            places=12)
        self.assertAlmostEqual(
            summary["even_energy_fraction_summary"]["maximum"],
            1.0,
            places=12)
        self.assertAlmostEqual(
            summary["even_energy_fraction_summary"]["mean"],
            0.50010368361382,
            places=12)
        self.assertAlmostEqual(
            summary["odd_energy_fraction_summary"]["maximum"],
            0.600533656762431,
            places=12)
        self.assertEqual(
            summary["worst_even_residue"]["target_residue_mod_286"], 0)
        self.assertEqual(
            summary["best_odd_residue"]["target_residue_mod_286"], 110)
        self.assertAlmostEqual(
            summary["worst_even_residue"]["reflection_even_l2"],
            50.09192896531902,
            places=12)
        self.assertAlmostEqual(
            summary["best_odd_residue"]["reflection_odd_l2"],
            38.69344488270867,
            places=12)

    def test_each_mode_has_exact_reflection_decomposition(self):
        receipt = self.load_receipt()

        self.assertEqual(len(receipt["mode_rows"]), 2)
        for mode in receipt["mode_rows"]:
            summary = mode["summary"]
            self.assertEqual(
                summary["even_energy_fraction_summary"]["count"], 143)
            self.assertEqual(
                summary["odd_energy_fraction_summary"]["count"], 143)
            self.assertEqual(
                summary["worst_even_residue"][
                    "target_residue_mod_286"], 0)
            self.assertLess(summary["max_reconstruction_error"], 1e-12)
            self.assertEqual(
                summary["max_reflection_odd_pair_sum_error"], 0.0)
            self.assertEqual(
                summary["max_reflection_even_pair_difference_error"], 0.0)

    def test_decision_preserves_bridge_boundary(self):
        receipt = self.load_receipt()

        self.assertIn("not a universal simplifier", receipt["decision"])
        self.assertIn("pointwise unnormalized analytic estimate",
                      receipt["decision"])
        self.assertIn("no non-circular L2 target",
                      receipt["status_boundary"])
        self.assertIn("no raw adverse-drag bound",
                      receipt["status_boundary"])


if __name__ == "__main__":
    unittest.main()
