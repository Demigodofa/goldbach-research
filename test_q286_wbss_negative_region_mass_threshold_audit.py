import json
import unittest
from pathlib import Path


class Q286WbssNegativeRegionMassThresholdAuditTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/q286-wbss-negative-region-mass-threshold-audit.json"
        ).read_text(encoding="utf-8"))

    def test_receipt_is_theorem_obligation_not_proof(self):
        receipt = self.load_receipt()

        self.assertEqual(
            receipt["status"],
            "TARGET_signed_negative_region_correlation_obligation")
        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(
            receipt["signed_negative_region_distribution_theorem_proved"])
        self.assertFalse(receipt["raw_adverse_drag_theorem_proved"])
        self.assertFalse(receipt["positive_mass_theorem_proved"])
        self.assertFalse(receipt["universal_pointwise_bound_proved"])
        self.assertFalse(receipt["finite_evidence_acceptance_condition"])

    def test_crude_robust_threshold_is_too_strong(self):
        receipt = self.load_receipt()
        summary = receipt["summary"]

        self.assertEqual(summary["even_target_residue_count"], 5005)
        self.assertEqual(summary["local_uniform_robust_threshold_pass_count"],
                         0)
        self.assertAlmostEqual(
            summary["robust_sign_mass_threshold_summary"]["minimum"],
            0.0007147368046632611,
            places=15)
        self.assertAlmostEqual(
            summary["robust_sign_mass_threshold_summary"]["maximum"],
            0.0033012537800608146,
            places=15)
        self.assertLess(
            summary["uniform_margin_to_robust_threshold_summary"]["maximum"],
            0.0)

    def test_signed_shape_threshold_has_local_uniform_margin(self):
        receipt = self.load_receipt()
        summary = receipt["summary"]

        self.assertEqual(summary["local_uniform_shape_threshold_pass_count"],
                         5005)
        self.assertAlmostEqual(
            summary["shape_mass_threshold_summary"]["minimum"],
            0.48729403831397616,
            places=12)
        self.assertAlmostEqual(
            summary["shape_mass_threshold_summary"]["maximum"],
            0.6355852930606508,
            places=12)
        self.assertAlmostEqual(
            summary["uniform_margin_to_shape_threshold_summary"]["minimum"],
            0.10534041937277128,
            places=12)
        self.assertAlmostEqual(
            summary["negative_weight_fraction_summary"]["maximum"],
            0.47205387205387206,
            places=12)

    def test_raw_boundary_avoids_normalized_circularity(self):
        receipt = self.load_receipt()
        definitions = receipt["definitions"]
        obligation = receipt["theorem_obligation"]

        self.assertIn("W_phi(N)>0", definitions["raw_witness_boundary"])
        self.assertIn("strict-central mass",
                      definitions["raw_witness_boundary"])
        self.assertIn("sum_{u:phi(u)>0}",
                      obligation["raw_unormalized_form"])
        self.assertIn("conditional on T_N>0",
                      obligation["normalization_warning"])

    def test_candidate_and_decision_preserve_surviving_route(self):
        receipt = self.load_receipt()
        candidate = receipt["candidate"]

        self.assertEqual(candidate["novelty_label"], "new-to-this-task")
        self.assertIn("positive coefficient mass",
                      candidate["mechanism"])
        self.assertIn("robust sign-only theorem is too severe",
                      candidate["prediction"])
        self.assertIn("does not force q286 to sleep",
                      receipt["decision"])
        self.assertIn("theorem obligation, not a theorem",
                      receipt["decision"])


if __name__ == "__main__":
    unittest.main()
