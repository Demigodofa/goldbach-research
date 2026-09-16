import json
import unittest
from pathlib import Path


EVIDENCE = Path(
    "evidence/"
    "mobius-moment-square-degree5-q46189-kernel-envelope-obstruction-audit.json")


class MobiusMomentSquareDegree5Q46189KernelEnvelopeObstructionTests(
        unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = json.loads(EVIDENCE.read_text(encoding="utf-8"))

    def test_receipt_preserves_boundaries(self):
        self.assertEqual(
            self.receipt["status"],
            "AUDIT_q46189_kernel_envelope_obstruction")
        self.assertTrue(
            self.receipt["finite_kernel_envelope_obstruction_audit_only"])
        self.assertTrue(self.receipt["finite_diagnostic_only"])
        self.assertFalse(self.receipt["simple_bucket_bound_theorem_proved"])
        self.assertFalse(self.receipt["simple_rank_bound_theorem_proved"])
        self.assertFalse(self.receipt["goldbach_proved"])

    def test_disconnected_envelopes_are_too_weak(self):
        bucket = self.receipt["bucket_componentwise_envelope"]
        rank = self.receipt["top_negative_rank_componentwise_envelope"]
        observed = self.receipt["observed_true_nonadverse_boundary"]
        classification = self.receipt["classification"]

        self.assertAlmostEqual(
            observed["minimum_nonadverse_off_diagonal_over_diagonal_half"],
            -0.8472931845861708,
            places=15,
        )
        self.assertGreater(
            observed["minimum_nonadverse_off_diagonal_over_diagonal_half"],
            -1.0,
        )
        self.assertAlmostEqual(
            bucket["disconnected_worst_sum"],
            -1.8966400770509377,
            places=15,
        )
        self.assertAlmostEqual(
            rank["disconnected_worst_sum"],
            -1.4111403765125132,
            places=15,
        )
        self.assertTrue(
            classification[
                "bucket_componentwise_envelope_refutes_simple_bucket_bound"])
        self.assertTrue(
            classification[
                "top_negative_rank_envelope_refutes_simple_rank_bound"])
        self.assertTrue(
            classification[
                "true_rows_survive_but_disconnected_envelopes_fail"])

    def test_worst_bucket_contributors_are_not_one_row(self):
        rows = self.receipt["bucket_componentwise_envelope"]["rows"]
        self.assertEqual(
            [row["bucket"] for row in rows],
            [
                "near_1_to_A",
                "middle_A_to_10A",
                "far_10A_to_100A",
                "tail_over_100A",
            ],
        )
        self.assertEqual(
            [row["worst_denominator"] for row in rows],
            [21318, 38038, 67830, 19019],
        )

    def test_next_action_requires_cooccurrence(self):
        action = self.receipt["candidate_next_action"]
        self.assertEqual(
            action["name"],
            "co-occurrence constrained kernel envelope")
        self.assertIn("simultaneously bad", action["mechanism"])


if __name__ == "__main__":
    unittest.main()
