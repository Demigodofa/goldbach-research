import json
import unittest
from pathlib import Path


class Q286WbssActiveCharacterCollapseAuditTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/q286-wbss-active-character-collapse-audit.json"
        ).read_text(encoding="utf-8"))

    def test_receipt_is_sleep_hold_not_proof(self):
        receipt = self.load_receipt()

        self.assertEqual(
            receipt["status"],
            "SLEEP_active_character_route_until_independent_raw_theorem_"
            "or_new_engine")
        self.assertFalse(receipt["active_character_moment_theorem_proved"])
        self.assertFalse(receipt["signed_weight_major_arc_estimate_proved"])
        self.assertFalse(receipt["raw_weighted_witness_theorem_proved"])
        self.assertFalse(receipt["positive_mass_theorem_proved"])
        self.assertFalse(receipt["q286_threshold_theorem_proved"])
        self.assertFalse(receipt["strict_central_goldbach_theorem_proved"])
        self.assertFalse(receipt["goldbach_proved"])
        self.assertIn("Logical dependency HOLD only",
                      receipt["status_boundary"])

    def test_raw_active_character_package_values_are_pinned(self):
        receipt = self.load_receipt()
        package = receipt["raw_active_character_package"]

        self.assertEqual(package["active_complex_character_count"], 122)
        self.assertEqual(package["active_real_channel_count"], 64)
        self.assertAlmostEqual(
            package["aggregate_character_l2"],
            5.525106448699807,
            places=12)
        self.assertAlmostEqual(
            package["normalized_l2_cap_when_mass_positive"],
            0.10930746469603118,
            places=15)
        self.assertAlmostEqual(
            package["minimum_local_factor_M"],
            0.6039353780830684,
            places=15)

    def test_route_classification_separates_raw_from_conditional(self):
        receipt = self.load_receipt()
        rows = {row["id"]: row for row in receipt["route_classification"]}

        self.assertEqual(
            rows["direct_signed_sum_W_phi_positive"]["logical_status"],
            "valid_but_goldbach_strength")
        self.assertTrue(
            rows["direct_signed_sum_W_phi_positive"][
                "creates_support_if_proved"])
        self.assertEqual(
            rows["raw_aggregate_L2_less_than_TN_main"]["logical_status"],
            "non_circular_shape_but_theorem_missing")
        self.assertEqual(
            rows["P0_scaled_major_arc_replacement"]["logical_status"],
            "possible_raw_theorem_but_unproved")
        self.assertEqual(
            rows["normalized_character_distribution_after_TN_positive"][
                "logical_status"],
            "conditional_decoration")
        self.assertFalse(
            rows["normalized_character_distribution_after_TN_positive"][
                "creates_support_if_proved"])

    def test_source_fit_closure_blocks_named_source_retry(self):
        receipt = self.load_receipt()
        closure = receipt["source_fit_closure"]

        self.assertEqual(closure["checked_source_count"], 4)
        self.assertEqual(closure["direct_raw_pointwise_bridge_count"], 0)
        self.assertEqual(closure["bauer_wang_fit"], "insufficient")
        self.assertFalse(closure["bauer_wang_reactivates_lane"])
        self.assertIn("not another metadata-level source fit",
                      closure["meaning"])

    def test_logical_implications_name_collapse(self):
        receipt = self.load_receipt()
        implications = receipt["logical_implications"]

        self.assertTrue(
            implications[
                "W_phi_positive_implies_strict_central_support"])
        self.assertTrue(
            implications[
                "raw_L2_strict_inequality_implies_strict_central_support"])
        self.assertTrue(implications["normalized_L2_requires_support_first"])
        self.assertFalse(
            implications["principal_local_factor_creates_support_by_itself"])
        self.assertIn("does not lower current core",
                      receipt["decision"])


if __name__ == "__main__":
    unittest.main()
