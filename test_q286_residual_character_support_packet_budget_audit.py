import json
import unittest
from pathlib import Path


class Q286ResidualCharacterSupportPacketBudgetAuditTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/q286-residual-character-support-packet-budget-audit.json"
        ).read_text(encoding="utf-8"))

    def test_receipt_preserves_boundaries(self):
        receipt = self.load_receipt()

        self.assertEqual(
            receipt["status"],
            "HOLD_adverse_packet_route_fails_signed_packet_route_survives_budget")
        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["support_packet_theorem_proved"])
        self.assertFalse(receipt["character_sum_theorem_proved"])
        self.assertFalse(
            receipt["signed_binary_prime_correlation_theorem_proved"])
        self.assertTrue(receipt["universal_bound_open"])
        self.assertIn("signed support-packet", receipt["decision"])

    def test_packet_dictionary_is_small_and_exact(self):
        receipt = self.load_receipt()
        summary = receipt["summary"]

        self.assertEqual(summary["selected_target_count"], 7)
        self.assertEqual(summary["actual_full_positive_count"], 5)
        self.assertEqual(
            summary["support_packet_count_summary"]["minimum"], 15)
        self.assertEqual(
            summary["support_packet_count_summary"]["maximum"], 15)
        self.assertLess(
            summary["maximum_packet_reconstruction_error"], 1e-12)

    def test_tight_row_signed_budget_survives_but_adverse_packet_fails(self):
        receipt = self.load_receipt()
        tight = receipt["summary"]["tightest_positive_signed_packet_budget_row"]

        self.assertEqual(tight["target"], 94856)
        self.assertAlmostEqual(
            tight["signed_packet_error_budget_with_aligned_exact"],
            0.055452588891044076)
        self.assertGreater(
            tight["signed_packet_error_budget_with_aligned_exact"], 0.05)
        self.assertLess(tight["rowwise_adverse_packet_margin"], 0.0)
        self.assertFalse(tight["rowwise_adverse_packet_certifies"])
        self.assertAlmostEqual(
            tight["positive_rows_component_envelope_margin"],
            -0.09568220367997388)
        self.assertFalse(tight["positive_rows_component_envelope_certifies"])

    def test_packet_route_is_not_the_full_character_triangle_route(self):
        receipt = self.load_receipt()
        tight = receipt["summary"]["tightest_positive_signed_packet_budget_row"]

        self.assertAlmostEqual(
            tight["packet_triangle_bound"],
            1.4697575197612691)
        self.assertAlmostEqual(
            tight["signed_packet_abs_sum"],
            0.22679673835446376)
        self.assertGreater(
            tight["packet_triangle_to_packet_abs_ratio"], 6.0)
        self.assertEqual(
            receipt["positive_rows_component_envelope"][
                "positive_certified_targets"],
            [1222142, 1240888, 1242118, 1379072])


if __name__ == "__main__":
    unittest.main()
