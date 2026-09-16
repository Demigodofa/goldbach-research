import json
import unittest
from pathlib import Path


EVIDENCE = Path(
    "evidence/"
    "mobius-moment-square-degree5-q46189-exception-bound-audit.json")


class MobiusMomentSquareDegree5Q46189ExceptionBoundAuditTests(
        unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = json.loads(EVIDENCE.read_text(encoding="utf-8"))

    def test_receipt_preserves_boundaries(self):
        self.assertEqual(
            self.receipt["status"],
            "HOLD_q46189_simple_cauchy_bound_insufficient")
        self.assertTrue(self.receipt["finite_q46189_exception_audit_only"])
        self.assertTrue(self.receipt["finite_diagnostic_only"])
        self.assertFalse(self.receipt["simple_cauchy_theorem_proved"])
        self.assertFalse(self.receipt["phase_defect_theorem_proved"])
        self.assertFalse(self.receipt["clearance_family_theorem_proved"])
        self.assertFalse(self.receipt["goldbach_proved"])

    def test_fixture_is_q46189_middle_exception(self):
        fixture = self.receipt["fixture"]

        self.assertEqual(fixture["scale_modulus"], 229)
        self.assertEqual(fixture["prime_modulus"], 379)
        self.assertEqual(fixture["reduced_denominator"], 46189)
        self.assertEqual(
            fixture["reduced_denominator_factorization"],
            {"11": 1, "13": 1, "17": 1, "19": 1})
        self.assertEqual(fixture["row_count_A"], 43)
        self.assertEqual(fixture["threshold_p_times_A"], 16297)
        self.assertAlmostEqual(
            fixture["clearance_ratio_q_over_pA"],
            2.8342026139780327)
        self.assertEqual(fixture["target_label"], "00,12")

    def test_exact_target_component_is_pinned(self):
        target = self.receipt["target_component"]

        self.assertEqual(target["label"], "00,12")
        self.assertAlmostEqual(
            target["active_contribution"],
            -1560644479591.6313)
        self.assertAlmostEqual(
            target["full_contribution"],
            -3138178401642.2075)
        self.assertAlmostEqual(
            target["margin_full_over_2_minus_active"],
            -8444721229.472412)
        self.assertAlmostEqual(
            target["adverse_over_abs_half_full"],
            0.0053819255304627)

    def test_simple_cauchy_bound_is_too_weak(self):
        target = self.receipt["target_component"]
        classification = self.receipt["classification"]

        self.assertFalse(target["cauchy_bound_proves_nonadverse"])
        self.assertFalse(
            classification["simple_cauchy_bound_proves_nonadverse"])
        self.assertTrue(
            classification["active_cross_term_cauchy_saturated_negative"])
        self.assertTrue(
            classification["full_cross_term_cauchy_saturated_negative"])
        self.assertGreater(
            target["cauchy_budget_over_actual_adverse"], 370.0)
        self.assertTrue(classification["phase_defect_estimate_required"])

    def test_clearance_context_records_small_but_real_exception(self):
        context = self.receipt["clearance_context"]

        self.assertAlmostEqual(
            context["q46189_middle_adverse_over_middle_far_positive"],
            0.00035683847866709636)
        self.assertAlmostEqual(
            context["q46189_middle_adverse_over_all_negative_margin"],
            0.34560555171301166)
        self.assertGreater(
            context["middle_far_total_margin_sum"],
            context["near_negative_abs"])

    def test_next_action_is_phase_defect_not_more_cauchy(self):
        action = self.receipt["candidate_next_action"]

        self.assertEqual(action["name"], "q46189 phase-defect bound")
        self.assertIn("missing small primes 2,3,5,7",
                      action["smallest_next_test"])
        self.assertEqual(action["novelty_label"], "new-to-this-task")


if __name__ == "__main__":
    unittest.main()
