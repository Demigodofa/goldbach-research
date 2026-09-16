import json
import unittest
from pathlib import Path


class Q286WbssSourceTheoremFitAuditTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/q286-wbss-source-theorem-fit-audit.json"
        ).read_text(encoding="utf-8"))

    def test_receipt_is_not_a_proof(self):
        receipt = self.load_receipt()

        self.assertEqual(
            receipt["status"],
            "SOURCE_FIT_no_existing_direct_pointwise_bridge")
        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["strict_raw_gap_theorem_proved"])
        self.assertFalse(receipt["external_pointwise_bridge_found"])
        self.assertFalse(receipt["binary_prime_convolution_theorem_proved"])
        self.assertTrue(receipt["universal_bound_open"])

    def test_required_theorem_shape_is_pointwise_raw_and_strict_central(self):
        receipt = self.load_receipt()
        required = receipt["required_theorem_shape"]

        self.assertIn("every sufficiently large", required["pointwise"])
        self.assertIn("unnormalized", required["raw"])
        self.assertIn("q286-WBSS coefficient", required["weighted"])
        self.assertIn("N/3 < p < 2N/3", required["strict_central"])
        self.assertIn("explicit threshold", required["finite_remainder"])

    def test_external_sources_do_not_fit_direct_bridge(self):
        receipt = self.load_receipt()
        table = {
            item["id"]: item
            for item in receipt["source_fit_table"]
        }

        self.assertEqual(
            table["BMOR_2018_AP_prime_counts"]["fit_to_q286_raw_gap"],
            "insufficient")
        self.assertEqual(
            table["Salmensuu_2021_binary_AP_Goldbach_almost_all"][
                "fit_to_q286_raw_gap"],
            "insufficient_as_direct_bridge")
        self.assertEqual(
            table["Halupczok_2012_AP_Goldbach_mean_value"][
                "fit_to_q286_raw_gap"],
            "insufficient_as_direct_bridge")
        self.assertEqual(
            receipt["fit_summary"]["external_direct_bridge_count"],
            0)

    def test_internal_best_target_is_character_l2_not_source_theorem(self):
        receipt = self.load_receipt()
        table = {
            item["id"]: item
            for item in receipt["source_fit_table"]
        }

        self.assertEqual(
            receipt["fit_summary"]["internal_best_target"],
            "q286_active_character_L2_payment")
        self.assertEqual(
            table["q286_active_character_L2_payment"][
                "fit_to_q286_raw_gap"],
            "best_current_internal_target")
        self.assertGreater(receipt["fit_summary"]["character_l2_cap"], 0.1)

    def test_next_candidate_has_falsifier_and_sleep_conditions(self):
        receipt = self.load_receipt()

        self.assertIn(
            "fixed-finite-modulus weighted circle-method bridge",
            receipt["candidate"]["name"])
        self.assertIn(
            "unproved pointwise lower bound",
            receipt["candidate"]["falsifier"])
        self.assertIn(
            "exact raw character-expanded theorem target",
            receipt["decision"])
        self.assertIn(
            "one-dimensional AP marginals",
            " ".join(receipt["sleep_conditions"]))


if __name__ == "__main__":
    unittest.main()
