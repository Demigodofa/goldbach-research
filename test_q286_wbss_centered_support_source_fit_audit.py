import json
import unittest
from pathlib import Path


class Q286WbssCenteredSupportSourceFitAuditTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/q286-wbss-centered-support-source-fit-audit.json"
        ).read_text(encoding="utf-8"))

    def test_receipt_is_source_fit_hold_not_proof(self):
        receipt = self.load_receipt()

        self.assertEqual(
            receipt["status"],
            "SOURCE_FIT_no_existing_centered_bucket_bridge")
        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["external_pointwise_bridge_found"])
        self.assertFalse(receipt["ordinary_positive_mass_suffices"])
        self.assertFalse(receipt["source_theorem_fit_proved"])
        self.assertFalse(
            receipt["pointwise_centered_error_estimate_proved"])
        self.assertFalse(receipt["universal_pointwise_bound_proved"])

    def test_required_shape_is_raw_bucket_pointwise(self):
        receipt = self.load_receipt()
        shape = receipt["required_theorem_shape"]

        self.assertIn("every sufficiently large covered even N",
                      shape["quantifier"])
        self.assertIn("before division by actual T_N",
                      shape["raw_scale"])
        self.assertEqual(
            shape["bucket_set"],
            ["dominant_286", "dominant_154", "dominant_70", "tail"])
        self.assertIn("P0_a(N)>0 or T_N>0 is not enough",
                      shape["ordinary_mass_boundary"])
        self.assertIn("explicit threshold", shape["finite_remainder"])

    def test_ledger_budget_is_preserved(self):
        receipt = self.load_receipt()
        budget = receipt["ledger_budget"]

        self.assertAlmostEqual(
            budget["weakest_local_factor_ratio"],
            0.6039353780830684,
            places=12)
        self.assertAlmostEqual(
            budget["allocated_negative_budget_total"],
            0.5435418402747616,
            places=12)
        self.assertAlmostEqual(
            budget["unallocated_reserve_ratio"],
            0.06039353780830681,
            places=12)
        self.assertEqual(budget["bucket_count"], 4)

    def test_bucket_table_has_no_named_source_bridge(self):
        receipt = self.load_receipt()
        rows = receipt["bucket_source_fit_table"]

        self.assertEqual([row["bucket"] for row in rows], [
            "dominant_286", "dominant_154", "dominant_70", "tail"])
        self.assertTrue(all(
            row["source_fit_status"] == "no_named_source_bridge"
            for row in rows))
        self.assertIn("-0.1759037368828583*P0_a(N)",
                      rows[0]["required_raw_lower_bound"])
        self.assertIn("pointwise raw signed binary-prime correlation",
                      rows[0]["missing_theorem_shape"])

    def test_external_sources_do_not_pay_direct_bridge(self):
        receipt = self.load_receipt()
        table = {row["id"]: row for row in receipt["source_fit_table"]}

        self.assertEqual(receipt["fit_summary"]["evaluated_source_count"], 6)
        self.assertEqual(
            receipt["fit_summary"]["external_direct_bridge_count"], 0)
        self.assertEqual(
            table["BMOR_2018_explicit_AP_prime_counts"][
                "fit_to_centered_support_ledger"],
            "insufficient")
        self.assertEqual(
            table["ordinary_strict_central_positive_mass_theorem"][
                "fit_to_centered_support_ledger"],
            "insufficient_without_bucket_bounds")
        self.assertFalse(
            receipt["fit_summary"]["ordinary_positive_mass_is_sufficient"])

    def test_decision_names_next_nonfinite_step_and_sleep_conditions(self):
        receipt = self.load_receipt()

        self.assertIn("K_286", receipt["decision"])
        self.assertIn("sign-indefinite centered bucket weights",
                      receipt["decision"])
        self.assertIn("proves ordinary T_N>0",
                      " ".join(receipt["sleep_conditions"]))
        self.assertIn("bespoke_bucket_circle_method",
                      receipt["surviving_work"])
        self.assertIn("not a theorem", receipt["status_boundary"])


if __name__ == "__main__":
    unittest.main()
