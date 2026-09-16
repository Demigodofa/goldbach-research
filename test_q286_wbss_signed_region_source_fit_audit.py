import json
import unittest
from pathlib import Path


class Q286WbssSignedRegionSourceFitAuditTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/q286-wbss-signed-region-source-fit-audit.json"
        ).read_text(encoding="utf-8"))

    def test_receipt_is_source_fit_hold_not_proof(self):
        receipt = self.load_receipt()

        self.assertEqual(
            receipt["status"],
            "SOURCE_FIT_no_existing_signed_region_pointwise_bridge")
        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["external_pointwise_bridge_found"])
        self.assertFalse(
            receipt["signed_negative_region_distribution_theorem_proved"])
        self.assertFalse(receipt["raw_adverse_drag_theorem_proved"])
        self.assertFalse(receipt["universal_pointwise_bound_proved"])

    def test_required_shape_is_raw_pointwise_and_weighted(self):
        receipt = self.load_receipt()
        shape = receipt["required_theorem_shape"]

        self.assertIn("every sufficiently large covered even N",
                      shape["quantifier"])
        self.assertIn("sum_{u:phi(u)>0}", shape["raw_inequality"])
        self.assertIn("N/3 < p < 2N/3", shape["strict_central"])
        self.assertIn("both p and N-p prime", shape["binary"])
        self.assertIn("normalization", " ".join(shape.keys()))
        self.assertIn("raw strict positivity",
                      shape["normalization_boundary"])

    def test_source_table_has_no_external_direct_bridge(self):
        receipt = self.load_receipt()
        rows = {row["id"]: row for row in receipt["source_fit_table"]}

        self.assertEqual(receipt["fit_summary"]["evaluated_source_count"], 5)
        self.assertEqual(
            receipt["fit_summary"]["external_direct_bridge_count"], 0)
        self.assertEqual(
            rows["BMOR_2018_AP_prime_counts"][
                "fit_to_signed_region_obligation"],
            "insufficient")
        self.assertEqual(
            rows["Salmensuu_2021_binary_AP_Goldbach_almost_all"][
                "fit_to_signed_region_obligation"],
            "insufficient_as_direct_bridge")
        self.assertEqual(
            rows["Halupczok_2012_AP_Goldbach_mean_value"][
                "fit_to_signed_region_obligation"],
            "insufficient_as_direct_bridge")
        self.assertEqual(
            rows["q286_signed_region_shape_target"][
                "fit_to_signed_region_obligation"],
            "exact_target_not_theorem")

    def test_summary_preserves_threshold_context(self):
        receipt = self.load_receipt()
        summary = receipt["fit_summary"]

        self.assertAlmostEqual(
            summary["shape_threshold_minimum"],
            0.48729403831397616,
            places=12)
        self.assertAlmostEqual(
            summary["minimum_local_uniform_shape_margin"],
            0.10534041937277128,
            places=12)
        self.assertTrue(summary["robust_sign_mass_route_sleeping"])

    def test_decision_names_surviving_work_and_sleep_conditions(self):
        receipt = self.load_receipt()

        self.assertIn("bespoke fixed-modulus signed circle-method target",
                      receipt["decision"])
        self.assertIn("T_N>0 first", receipt["decision"])
        self.assertIn("one-dimensional AP marginals",
                      receipt["sleep_conditions"][0])
        self.assertIn("character_moment_target",
                      receipt["surviving_work"])
        self.assertIn("region_correlation_target",
                      receipt["surviving_work"])


if __name__ == "__main__":
    unittest.main()
