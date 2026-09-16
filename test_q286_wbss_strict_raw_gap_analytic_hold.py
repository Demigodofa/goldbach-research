import json
import unittest
from pathlib import Path


class Q286WbssStrictRawGapAnalyticHoldTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/q286-wbss-strict-raw-gap-analytic-hold.json"
        ).read_text(encoding="utf-8"))

    def test_receipt_is_hold_not_proof(self):
        receipt = self.load_receipt()

        self.assertEqual(
            receipt["status"],
            "HOLD_for_strict_raw_binary_pair_estimate")
        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["strict_raw_gap_theorem_proved"])
        self.assertFalse(
            receipt["direct_raw_signed_binary_pair_theorem_proved"])
        self.assertFalse(receipt["positive_mass_theorem_proved"])
        self.assertTrue(receipt["universal_bound_open"])

    def test_zero_mass_barrier_is_explicit(self):
        receipt = self.load_receipt()
        bridge = receipt["bridge"]

        self.assertIn("G_raw(N)=L_raw(N)-A_raw_-(N)>0",
                      bridge["strict_raw_gap"])
        self.assertIn("T_N=0", bridge["zero_mass_barrier"])
        self.assertIn("G_raw(N)=0", bridge["zero_mass_barrier"])
        self.assertIn("strict positive raw quantity",
                      bridge["zero_mass_barrier"])

    def test_sufficient_routes_keep_mass_boundary(self):
        receipt = self.load_receipt()
        routes = receipt["sufficient_analytic_routes"]

        direct = routes["direct_signed_binary_pair_sum"]
        split = routes["mass_plus_one_sided_projection_control"]
        normalized = routes["normalized_projection_discrepancy"]

        self.assertTrue(direct["non_circular"])
        self.assertFalse(direct["separate_positive_mass_needed"])
        self.assertTrue(split["non_circular"])
        self.assertTrue(split["separate_positive_mass_needed"])
        self.assertFalse(normalized["non_circular"])
        self.assertTrue(normalized["separate_positive_mass_needed"])

    def test_inherits_exact_coefficient_budget(self):
        receipt = self.load_receipt()
        budget = receipt["coefficient_budget_inherited"]

        self.assertEqual(budget["moduli"], ["70", "130", "154", "286"])
        self.assertAlmostEqual(
            budget["total_l1_norm"],
            372.962002076135,
            places=12)
        self.assertAlmostEqual(
            budget["minimum_local_main_over_even_residues"],
            0.6039353780830684,
            places=12)
        self.assertAlmostEqual(
            budget["global_equal_residue_error_cap"],
            0.0016192946592982506,
            places=15)

    def test_rejects_finite_and_marginal_substitutes(self):
        receipt = self.load_receipt()
        names = {
            item["name"]
            for item in receipt["rejected_acceptance_substitutes"]
        }

        self.assertIn("more finite q286 rows", names)
        self.assertIn("fitted residual absorption constants", names)
        self.assertIn("normalized L2 or L1 discrepancy alone", names)
        self.assertIn("one-dimensional AP prime estimates alone", names)
        self.assertIn("almost-all or averaged estimates", names)

    def test_finite_context_is_calibration_only(self):
        receipt = self.load_receipt()
        finite = receipt["finite_context"]

        self.assertEqual(finite["role"], "calibration_and_falsifier_only")
        self.assertEqual(finite["row_count"], 348)
        self.assertEqual(finite["positive_strict_raw_gap_count"], 348)
        self.assertEqual(finite["nonpositive_strict_raw_gap_count"], 0)
        self.assertEqual(finite["tightest_strict_raw_gap_target"], 1059514)
        self.assertAlmostEqual(
            finite["tightest_strict_raw_gap"],
            286929.1729900494,
            places=6)


if __name__ == "__main__":
    unittest.main()
