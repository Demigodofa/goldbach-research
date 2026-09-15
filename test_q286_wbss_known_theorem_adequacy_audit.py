import json
import unittest
from pathlib import Path


class Q286WbssKnownTheoremAdequacyAuditTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/q286-wbss-known-theorem-adequacy-audit.json"
        ).read_text(encoding="utf-8"))

    def test_audit_is_hold_not_theorem(self):
        receipt = self.load_receipt()

        self.assertEqual(
            receipt["status"],
            "HOLD_external_known_theorems_do_not_pay_budget")
        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["known_source_pays_budget"])
        self.assertFalse(receipt["pointwise_adverse_drag_theorem_proved"])
        self.assertFalse(
            receipt[
                "fixed_modulus_binary_prime_discrepancy_theorem_proved"])

    def test_budget_numbers_are_carried_from_coefficient_hold(self):
        receipt = self.load_receipt()
        budget = receipt["active_budget"]

        self.assertAlmostEqual(budget["minimum_local_main"],
                               0.6039353780830684,
                               places=12)
        self.assertAlmostEqual(budget["total_l1_norm"],
                               372.962002076135,
                               places=12)
        self.assertAlmostEqual(budget["equal_eta_cap"],
                               0.0016192946592982506,
                               places=15)
        self.assertIn("sum_d max(0,B_d(N)) < local_main(N)",
                      budget["direct_one_sided_condition"])

    def test_all_evaluated_known_sources_fail_to_pay_budget(self):
        receipt = self.load_receipt()
        sources = receipt["evaluated_sources"]

        self.assertEqual(len(sources), 4)
        self.assertTrue(all(
            not source["pays_q286_wbss_budget"] for source in sources))
        source_ids = {source["id"] for source in sources}
        self.assertIn("BMOR_2018_explicit_AP_prime_counts", source_ids)
        self.assertIn("BHMS_2017_Goldbach_AP_averages", source_ids)
        self.assertIn("Salmensuu_2021_almost_all_AP_Goldbach", source_ids)
        self.assertIn(
            "Lichtman_2023_level_distribution_upper_bounds", source_ids)

    def test_failure_reasons_preserve_quantifier_boundaries(self):
        receipt = self.load_receipt()
        by_id = {source["id"]: source for source in
                 receipt["evaluated_sources"]}

        self.assertIn("Marginal prime counts",
                      by_id["BMOR_2018_explicit_AP_prime_counts"][
                          "why_not_enough"])
        self.assertIn("Average asymptotics",
                      by_id["BHMS_2017_Goldbach_AP_averages"][
                          "why_not_enough"])
        self.assertIn("Almost-all coverage",
                      by_id["Salmensuu_2021_almost_all_AP_Goldbach"][
                          "why_not_enough"])
        self.assertIn("Upper bounds",
                      by_id[
                          "Lichtman_2023_level_distribution_upper_bounds"][
                          "why_not_enough"])

    def test_next_candidate_has_falsifier_and_smallest_test(self):
        receipt = self.load_receipt()
        candidate = receipt["candidate"]

        self.assertEqual(candidate["novelty_label"], "new-to-this-task")
        self.assertIn("signed-character", candidate["name"])
        self.assertIn("collapses back", candidate["falsifier"])
        self.assertIn("character-mode burden audit",
                      candidate["smallest_test"])


if __name__ == "__main__":
    unittest.main()
