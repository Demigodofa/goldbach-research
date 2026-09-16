import json
import unittest
from pathlib import Path


EVIDENCE = Path(
    "evidence/"
    "mobius-moment-square-degree5-puncture-endpoint-swap-audit.json")


class MobiusMomentSquareDegree5PunctureEndpointSwapAuditTests(
        unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = json.loads(EVIDENCE.read_text(encoding="utf-8"))
        cls.summary = cls.receipt["puncture_summaries"][0]

    def test_receipt_preserves_boundaries(self):
        self.assertEqual(
            self.receipt["status"],
            "AUDIT_degree5_puncture_endpoint_swap")
        self.assertTrue(self.receipt["finite_endpoint_swap_audit_only"])
        self.assertTrue(self.receipt["finite_diagnostic_only"])
        self.assertFalse(self.receipt["goldbach_proved"])
        self.assertFalse(self.receipt["endpoint_swap_theorem_proved"])
        self.assertFalse(
            self.receipt["source_window_implication_theorem_proved"])

    def test_left_neighbor_to_failure_is_row_0_to_32_swap(self):
        swap = self.summary["left_neighbor_to_failure_swap"]
        self.assertEqual(swap["window_delta"], "start1 - start0")
        self.assertEqual(swap["outgoing_row"], 0)
        self.assertEqual(swap["incoming_row"], 32)
        self.assertAlmostEqual(
            swap["total_delta"],
            26772898181.83592,
            places=3)
        self.assertEqual(swap["dominant_denominator"], 30030)
        top = swap["denominator_rows"][0]
        self.assertEqual(top["reduced_denominator"], 30030)
        self.assertAlmostEqual(
            top["incoming_minus_outgoing"],
            19921005797.544834,
            places=3)
        self.assertGreater(top["signed_share_of_total_delta"], 0.70)

    def test_right_neighbor_to_failure_is_row_33_to_1_swap(self):
        swap = self.summary["right_neighbor_to_failure_swap"]
        self.assertEqual(swap["window_delta"], "start1 - start2")
        self.assertEqual(swap["outgoing_row"], 33)
        self.assertEqual(swap["incoming_row"], 1)
        self.assertAlmostEqual(
            swap["total_delta"],
            5659356386.238037,
            places=3)
        self.assertEqual(swap["dominant_denominator"], 10010)
        rows = swap["denominator_rows"]
        self.assertEqual(rows[0]["reduced_denominator"], 10010)
        self.assertEqual(rows[1]["reduced_denominator"], 6006)
        self.assertEqual(rows[2]["reduced_denominator"], 30030)
        self.assertGreater(rows[0]["incoming_minus_outgoing"], 0.0)
        self.assertGreater(rows[1]["incoming_minus_outgoing"], 0.0)
        self.assertLess(rows[2]["incoming_minus_outgoing"], 0.0)

    def test_candidate_is_endpoint_swap_mechanism(self):
        candidate = self.receipt["candidate"]
        self.assertEqual(
            candidate["name"],
            "endpoint-swap denominator-phase admissibility")
        self.assertEqual(candidate["novelty_label"], "new-to-this-task")
        self.assertIn("incoming/outgoing row phase swaps",
                      candidate["mechanism"])
        self.assertIn("cannot be accounted for by the endpoint swap",
                      candidate["falsifier"])


if __name__ == "__main__":
    unittest.main()
