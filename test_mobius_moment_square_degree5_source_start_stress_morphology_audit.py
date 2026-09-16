import json
import unittest
from pathlib import Path

from tools.build_mobius_moment_square_degree5_source_start_stress_morphology_audit import (
    SCALES,
)


EVIDENCE = Path(
    "evidence/"
    "mobius-moment-square-degree5-source-start-stress-morphology-audit.json")


class MobiusMomentSquareDegree5SourceStartStressMorphologyAuditTests(
        unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = json.loads(EVIDENCE.read_text(encoding="utf-8"))

    def test_receipt_preserves_boundaries(self):
        self.assertEqual(
            self.receipt["status"],
            "AUDIT_degree5_source_start_stress_morphology")
        self.assertEqual(self.receipt["scales"], list(SCALES))
        self.assertTrue(self.receipt["finite_morphology_audit_only"])
        self.assertTrue(self.receipt["finite_diagnostic_only"])
        self.assertFalse(self.receipt["goldbach_proved"])
        self.assertFalse(self.receipt["source_start_theorem_proved"])
        self.assertFalse(self.receipt["prime_block_theorem_proved"])

    def test_all_complete_sweeps_are_included_and_pass(self):
        self.assertEqual(self.receipt["scale_count"], 4)
        self.assertEqual(
            [row["scale_modulus"]
             for row in self.receipt["scale_summaries"]],
            [229, 251, 293, 331])
        self.assertTrue(
            self.receipt["all_complete_sweeps_pass_signed_dominance"])
        self.assertEqual(
            [row["prime_row_count"]
             for row in self.receipt["scale_summaries"]],
            [39, 42, 45, 55])

    def test_weakest_sequence_downgrades_fixed_prime_rule(self):
        sequence = self.receipt["weakest_sequence"]
        self.assertEqual(
            [(row["scale_modulus"], row["weakest_prime_modulus"])
             for row in sequence],
            [(229, 379), (251, 379), (293, 461), (331, 599)])
        self.assertFalse(
            self.receipt["single_fixed_weakest_prime_rule_survives"])
        self.assertEqual(
            self.receipt["weakest_prime_counts"],
            {"379": 2, "461": 1, "599": 1})

    def test_weakest_label_and_prime_block_morphology(self):
        self.assertTrue(self.receipt["all_weakest_labels_are_0012"])
        self.assertEqual(
            self.receipt["weakest_label_counts"], {"00,12": 4})
        self.assertTrue(
            self.receipt["all_tightest_prime_blocks_are_row_coherent"])
        for summary in self.receipt["scale_summaries"]:
            self.assertTrue(summary["tightest_prime_block_is_row_coherent"])
            first_four = summary["top_rows"][:4]
            self.assertEqual(
                len({row["prime_modulus"] for row in first_four}), 1)
            self.assertEqual(
                {row["label"] for row in first_four},
                {"00,12", "01,02", "01,11", "TOTAL"})

    def test_candidate_next_target_is_not_promoted(self):
        target = self.receipt["candidate_next_theorem_target"]
        self.assertEqual(
            target["name"], "source-start prime-block lower-frame control")
        self.assertEqual(target["novelty_label"], "new-to-this-task")
        self.assertIn("future M=353", target["prediction"])


if __name__ == "__main__":
    unittest.main()
