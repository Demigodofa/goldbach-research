import json
import unittest
from pathlib import Path


EVIDENCE = Path(
    "evidence/"
    "mobius-moment-square-degree5-q46189-kernel-cooccurrence-relaxation-audit.json")


class MobiusMomentSquareDegree5Q46189KernelCooccurrenceTests(
        unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = json.loads(EVIDENCE.read_text(encoding="utf-8"))

    def test_receipt_preserves_boundaries(self):
        self.assertEqual(
            self.receipt["status"],
            "AUDIT_q46189_kernel_cooccurrence_relaxation")
        self.assertTrue(
            self.receipt[
                "finite_kernel_cooccurrence_relaxation_audit_only"])
        self.assertTrue(self.receipt["finite_diagnostic_only"])
        self.assertFalse(
            self.receipt["pairwise_cooccurrence_bound_theorem_proved"])
        self.assertFalse(
            self.receipt["triple_cooccurrence_bound_theorem_proved"])
        self.assertFalse(self.receipt["goldbach_proved"])

    def test_low_order_relaxations_still_fail_target(self):
        observed = self.receipt["observed_true_nonadverse_boundary"]
        relax = self.receipt["relaxations"]
        classification = self.receipt["classification"]

        self.assertAlmostEqual(
            observed["minimum_total"],
            -0.8472931845861708,
            places=15,
        )
        self.assertGreater(observed["minimum_total"], -1.0)
        self.assertAlmostEqual(
            relax["box_only"]["minimum_relaxed_total"],
            -1.8966400770509377,
            places=15,
        )
        self.assertAlmostEqual(
            relax["pair_lower"]["minimum_relaxed_total"],
            -1.2838731540875807,
            places=15,
        )
        self.assertAlmostEqual(
            relax["pair_and_triple_lower"]["minimum_relaxed_total"],
            -1.0464818684588788,
            places=15,
        )
        self.assertTrue(classification["pair_cooccurrence_relaxation_fails"])
        self.assertTrue(classification["triple_cooccurrence_relaxation_fails"])
        self.assertTrue(classification["low_order_cooccurrence_insufficient"])

    def test_pair_and_triple_bounds_are_recorded(self):
        self.assertEqual(len(self.receipt["pair_subset_bounds"]), 6)
        self.assertEqual(len(self.receipt["triple_subset_bounds"]), 4)
        weakest_pair = min(
            self.receipt["pair_subset_bounds"],
            key=lambda row: row["minimum_sum"],
        )
        self.assertEqual(
            weakest_pair["bucket_subset"],
            ["middle_A_to_10A", "far_10A_to_100A"],
        )
        self.assertAlmostEqual(
            weakest_pair["minimum_sum"],
            -0.9185789211298325,
            places=15,
        )

    def test_next_action_requires_full_packet_geometry(self):
        action = self.receipt["candidate_next_action"]
        self.assertEqual(action["name"], "full packet geometry invariant")
        self.assertIn("high-prime support", action["mechanism"])


if __name__ == "__main__":
    unittest.main()
