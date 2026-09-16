import json
import math
import unittest
from pathlib import Path


class Q286WbssCenteredSupportInequalityLedgerTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/q286-wbss-centered-support-inequality-ledger.json"
        ).read_text(encoding="utf-8"))

    def test_receipt_is_ledger_not_proof(self):
        receipt = self.load_receipt()

        self.assertEqual(
            receipt["status"],
            "TARGET_centered_support_inequality_ledger_open")
        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["source_theorem_fit_proved"])
        self.assertFalse(receipt["major_minor_arc_estimate_proved"])
        self.assertFalse(
            receipt["pointwise_centered_error_estimate_proved"])
        self.assertFalse(receipt["universal_pointwise_bound_proved"])

    def test_raw_objects_avoid_normalized_tn_bridge(self):
        receipt = self.load_receipt()
        raw = receipt["raw_objects"]

        self.assertIn("P0_a(N)", raw["ordinary_principal_scale"])
        self.assertIn("before any division by actual T_N",
                      raw["component_raw_contribution"])
        self.assertIn("sum_B beta_B < m_a_ratio",
                      raw["sufficient_ledger_inequality"])
        self.assertIn("first assumes actual T_N>0",
                      raw["zero_mass_boundary"])

    def test_budget_has_reserve_below_weakest_local_factor(self):
        receipt = self.load_receipt()
        budget = receipt["budget_model"]

        self.assertEqual(
            budget["name"],
            "coefficient_max_abs_proportional_with_10_percent_reserve")
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
            0.060393537808306826,
            places=12)
        self.assertTrue(budget["budget_passes_weakest_local_factor"])

    def test_bucket_obligations_cover_dominants_and_tail(self):
        receipt = self.load_receipt()
        buckets = receipt["bucket_obligations"]
        names = [row["bucket"] for row in buckets]

        self.assertEqual(
            names,
            ["dominant_286", "dominant_154", "dominant_70", "tail"])
        self.assertEqual(
            [row["natural_moduli"] for row in buckets[:3]],
            [[286], [154], [70]])
        self.assertEqual(
            buckets[3]["natural_moduli"], [10, 14, 22, 26, 130])
        self.assertTrue(all(
            row["allocated_negative_budget_ratio"] > 0
            for row in buckets))
        self.assertAlmostEqual(
            math.fsum(row["allocated_negative_budget_ratio"]
                      for row in buckets),
            receipt["budget_model"]["allocated_negative_budget_total"],
            places=15)

    def test_tail_detail_is_explicit(self):
        receipt = self.load_receipt()
        tail = receipt["tail_detail"]

        self.assertEqual(
            tail["tail_supports"], ["7", "13", "5x13", "5", "11"])
        self.assertEqual(tail["tail_natural_moduli"], [10, 14, 22, 26, 130])
        self.assertAlmostEqual(
            tail["tail_energy_fraction"],
            0.003967120777371179,
            places=12)
        self.assertIn("split the tail supports",
                      tail["tail_bound_required"])

    def test_decision_names_four_bucket_raw_target(self):
        receipt = self.load_receipt()

        self.assertIn("four-bucket raw inequality ledger",
                      receipt["decision"])
        self.assertIn("286, 154, 70, and the tail",
                      receipt["decision"])
        self.assertIn("not a theorem", receipt["status_boundary"])


if __name__ == "__main__":
    unittest.main()
