import json
import unittest
from pathlib import Path


class PostQ286MobiusFrontierReconciliationTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/post-q286-mobius-frontier-reconciliation.json"
        ).read_text(encoding="utf-8"))

    def test_receipt_reconciles_frontier_without_claiming_proof(self):
        receipt = self.load_receipt()

        self.assertEqual(
            receipt["status"],
            "TARGET_mobius_six_coordinate_active_full_lower_frame")
        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["q286_reactivated"])
        self.assertFalse(receipt["mobius_covariance_theorem_proved"])
        self.assertFalse(receipt["signed_prime_correlation_proved"])

    def test_boundary_operator_step_is_already_satisfied(self):
        receipt = self.load_receipt()
        operator = receipt["boundary_operator_step_already_satisfied"]

        self.assertTrue(operator["exact_conductor_packet_identity_proved"])
        self.assertEqual(operator["quadratic_log_conductor_span_rank"], 3)
        self.assertGreater(operator["sharp_row_varying_quadratic_span_ratio"],
                           operator["actual_row_varying_energy_ratio"])
        self.assertFalse(
            operator["uniform_conductor_operator_subpower_bound_proved"])
        self.assertIn("already present", operator["decision"])

    def test_six_coordinate_frame_is_the_active_frontier(self):
        receipt = self.load_receipt()
        frame = receipt["six_coordinate_lower_frame_evidence"]
        decision = receipt["route_decision"]

        self.assertEqual(frame["scale_modulus"], 127)
        self.assertTrue(frame["one_half_lower_frame_certified"])
        self.assertGreaterEqual(frame["gershgorin_lower_frame_bound"], 0.5)
        self.assertLessEqual(frame["gershgorin_lower_frame_bound"],
                             frame["exact_smallest_generalized_eigenvalue"])
        self.assertFalse(frame["uniform_active_full_lower_frame_proved"])
        self.assertIn("six-coordinate active/full lower-frame",
                      decision["active_frontier"])
        self.assertIn(
            "post-q286 wording that says the boundary operator still needs derivation",
            decision["sleep_or_reservoir"])

    def test_axial_response_is_candidate_compression_not_theorem(self):
        receipt = self.load_receipt()
        axial = receipt["axial_schur_response_evidence"]

        self.assertLess(axial["determinant_axial_distance"], 0.02)
        self.assertLess(axial["projective_moment_curve_distance"], 1e-3)
        self.assertGreater(axial["actual_selector_angle_degrees"], 15)
        self.assertLess(axial["nonaxial_error_over_schur_margin"], 1.0)
        self.assertFalse(axial["uniform_determinant_lower_bound_proved"])
        self.assertFalse(axial["effective_log_parameter_formula_proved"])

    def test_prime_block_quadratic_scan_remains_finite_evidence(self):
        receipt = self.load_receipt()
        block = receipt["prime_block_quadratic_span_evidence"]

        self.assertEqual(block["scale_modulus"], 101)
        self.assertGreater(block["prime_count"], 1)
        self.assertLess(
            block["aggregate_prime_block_sharp_varying_span_ratio"],
            block["maximum_sharp_varying_span_ratio"])
        self.assertFalse(block["row_varying_quadratic_span_bound_proved"])


if __name__ == "__main__":
    unittest.main()
