import json
import unittest
from pathlib import Path


class Q286WbssK286ZeroResidueComponentPhaseAuditTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/q286-wbss-k286-zero-residue-component-phase-audit.json"
        ).read_text(encoding="utf-8"))

    def test_receipt_is_component_phase_diagnostic_not_proof(self):
        receipt = self.load_receipt()

        self.assertEqual(
            receipt["status"],
            "DIAGNOSTIC_zero_residue_component_phase_nonalignment")
        self.assertFalse(receipt["component_nonalignment_theorem_proved"])
        self.assertFalse(receipt["phase_mode_theorem_proved"])
        self.assertFalse(
            receipt["coefficient_direction_nonalignment_theorem_proved"])
        self.assertFalse(receipt["universal_pointwise_raw_bound_proved"])
        self.assertFalse(receipt["q286_threshold_theorem_proved"])
        self.assertFalse(receipt["strict_central_goldbach_theorem_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_dominant_modulus_counts_are_pinned(self):
        receipt = self.load_receipt()
        summary = receipt["finite_diagnostic"]["summary"]

        self.assertEqual(summary["violating_row_count"], 18)
        self.assertEqual(
            summary["dominant_cauchy_threat_modulus_counts"],
            {"286": 18})
        self.assertEqual(
            summary["dominant_actual_adverse_modulus_counts"],
            {"130": 3, "154": 6, "286": 5, "70": 4})

    def test_aggregate_violating_row_summaries_are_pinned(self):
        receipt = self.load_receipt()
        summary = receipt["finite_diagnostic"]["summary"]

        threat = summary["aggregate_cauchy_threat_ratio_summary"]
        self.assertAlmostEqual(
            threat["minimum"], 1.0101218646296932, places=15)
        self.assertAlmostEqual(
            threat["mean"], 1.1189916481072606, places=15)
        self.assertAlmostEqual(
            threat["maximum"], 1.354153874306624, places=15)

        efficiency = summary["aggregate_directional_efficiency_summary"]
        self.assertAlmostEqual(
            efficiency["minimum"], 0.0007566063462656461, places=15)
        self.assertAlmostEqual(
            efficiency["mean"], 0.05468085899942172, places=15)
        self.assertAlmostEqual(
            efficiency["maximum"], 0.19440538748390473, places=15)

    def test_modulus_286_carries_threat_but_not_always_adverse_drag(self):
        receipt = self.load_receipt()
        row = receipt["finite_diagnostic"]["summary"]["by_modulus"]["286"]

        self.assertEqual(row["row_count"], 18)
        self.assertEqual(row["adverse_component_count"], 8)
        self.assertEqual(row["rescue_component_count"], 10)
        self.assertAlmostEqual(
            row["cauchy_threat_ratio_summary"]["mean"],
            0.7672836478772077,
            places=15)
        self.assertAlmostEqual(
            row["actual_adverse_drag_ratio_summary"]["mean"],
            0.029285134674525884,
            places=15)
        self.assertAlmostEqual(
            row["directional_efficiency_summary"]["mean"],
            0.03794725356022015,
            places=15)
        self.assertAlmostEqual(
            row["phase_cancellation_ratio_summary"]["mean"],
            0.15132464895023304,
            places=15)
        self.assertLess(
            row["phase_reconstruction_error_summary"]["maximum"],
            5e-17)

    def test_largest_threat_row_is_pinned(self):
        receipt = self.load_receipt()
        row = receipt["finite_diagnostic"]["summary"][
            "largest_aggregate_cauchy_threat_row"]

        self.assertEqual(row["target"], 1171456)
        self.assertEqual(row["target_residue"], 286)
        self.assertEqual(row["dominant_cauchy_threat_modulus"], "286")
        self.assertEqual(row["dominant_actual_adverse_modulus"], "286")
        self.assertAlmostEqual(
            row["aggregate_cauchy_threat_ratio_to_local_main"],
            1.354153874306624,
            places=15)
        self.assertAlmostEqual(
            row["raw_adverse_drag_ratio_to_local_main"],
            0.024989313695990587,
            places=15)
        self.assertAlmostEqual(
            row["directional_efficiency_actual_over_cauchy"],
            0.018453821364123796,
            places=15)

    def test_decision_names_phase_nonalignment_without_promotion(self):
        receipt = self.load_receipt()

        self.assertIn(
            "modulus 286 dominates the Cauchy norm threat",
            receipt["decision"])
        self.assertIn(
            "not an aggregate L2 estimate",
            receipt["decision"])
        self.assertIn(
            "Finite component/phase diagnostic only",
            receipt["status_boundary"])


if __name__ == "__main__":
    unittest.main()
