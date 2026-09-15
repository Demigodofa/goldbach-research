import json
import unittest
from pathlib import Path


class Q286LocalMainTermPositivityAuditTests(unittest.TestCase):
    def test_local_main_term_bridge_is_positive_but_not_a_proof(self):
        path = Path("evidence/q286-local-main-term-positivity-audit.json")
        receipt = json.loads(path.read_text(encoding="utf-8"))

        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["eventual_signed_witness_threshold_proved"])
        self.assertFalse(receipt["pointwise_centered_error_estimate_proved"])
        self.assertTrue(receipt["local_main_term_positivity_measured"])

        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["unit_group_order"], 2880)
        self.assertEqual(receipt["even_target_residue_count"], 5005)
        self.assertEqual(receipt["nonpositive_local_main_term_count"], 0)
        self.assertEqual(receipt["nonpositive_local_main_term_residues"], [])
        self.assertTrue(
            receipt["all_even_residue_local_main_terms_positive"])

        summary = receipt["local_main_term_to_principal_ratio_summary"]
        self.assertEqual(summary["count"], 5005)
        self.assertGreater(summary["minimum"], 0.0)
        self.assertGreater(summary["maximum"], summary["minimum"])
        self.assertLess(
            receipt["local_main_term_imag_abs_summary"]["maximum"], 1e-7)

        self.assertIn("CenteredError_a", receipt["smallest_new_problem"])
        self.assertIn("finite local coefficient audit only",
                      receipt["status_boundary"])


if __name__ == "__main__":
    unittest.main()
