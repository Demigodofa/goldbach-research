import json
import unittest
from pathlib import Path


class Q286ResidualSupportOrderRawScaleBridgeTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/q286-residual-support-order-raw-scale-bridge.json"
        ).read_text(encoding="utf-8"))

    def test_boundaries_are_preserved(self):
        receipt = self.load_receipt()

        self.assertEqual(
            receipt["status"],
            "CALIBRATION_raw_scale_bridge_verified_on_horizon")
        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["positive_mass_theorem_proved"])
        self.assertFalse(receipt["raw_pointwise_estimate_proved"])
        self.assertFalse(receipt["one_period_threshold_theorem_proved"])
        self.assertFalse(receipt["acceptance_condition"][
            "finite_evidence_is_acceptance_condition"])

    def test_scale_is_positive_on_checked_horizon(self):
        receipt = self.load_receipt()
        horizon = receipt["finite_horizon"]

        self.assertEqual(horizon["row_count"], 224)
        self.assertEqual(horizon["positive_scale_count"], 224)
        self.assertEqual(horizon["nonpositive_scale_targets"], [])
        self.assertEqual(horizon["sign_equivalence_failure_targets"], [])
        self.assertEqual(horizon["raw_domination_failure_targets"], [])

    def test_principal_mean_is_positive_real(self):
        receipt = self.load_receipt()
        identity = receipt["normalization_identity"]

        self.assertTrue(
            identity["principal_mean_positive_on_current_context"])
        self.assertGreater(identity["principal_mean_real"], 0.0)
        self.assertLess(identity["principal_mean_imag_to_real"], 1e-10)

    def test_tight_rows_are_exposed(self):
        receipt = self.load_receipt()
        horizon = receipt["finite_horizon"]
        tight = horizon["tight_raw_margin_row"]
        scale = horizon["smallest_positive_scale_row"]
        pair_count = horizon["smallest_pair_count_row"]

        self.assertEqual(tight["target"], 44168)
        self.assertGreater(tight["raw_pointwise_margin"], 0.0)
        self.assertEqual(scale["target"], 24148)
        self.assertGreater(scale["principal_scale"], 0.0)
        self.assertEqual(pair_count["target"], 24148)
        self.assertGreater(pair_count["ordered_central_prime_pair_count"], 0)

    def test_raw_margin_identity_error_is_tiny(self):
        receipt = self.load_receipt()
        error = receipt["finite_horizon"][
            "maximum_raw_margin_relative_reconstruction_error"]

        self.assertLess(error, 1e-15)


if __name__ == "__main__":
    unittest.main()
