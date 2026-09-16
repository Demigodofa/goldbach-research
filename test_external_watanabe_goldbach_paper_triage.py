import json
import unittest
from pathlib import Path


EVIDENCE = Path("evidence/external-watanabe-goldbach-paper-triage.json")


class ExternalWatanabeGoldbachPaperTriageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = json.loads(EVIDENCE.read_text(encoding="utf-8"))

    def test_preserves_authority_boundaries(self):
        self.assertEqual(
            self.receipt["status"],
            "TRIAGE_external_watanabe_goldbach_paper")
        self.assertTrue(self.receipt["external_paper_triage_only"])
        self.assertTrue(self.receipt["finite_diagnostic_only"])
        self.assertFalse(self.receipt["classification"][
            "accepted_as_goldbach_proof"])
        self.assertFalse(self.receipt["goldbach_proved"])

    def test_public_source_metadata_is_recorded(self):
        source = self.receipt["public_source"]
        self.assertEqual(source["arxiv_id"], "1811.02415v7")
        self.assertEqual(source["doi"], "10.48550/arXiv.1811.02415")
        self.assertIn("Watanabe", source["author"])
        self.assertTrue(self.receipt["classification"][
            "public_arxiv_source_can_be_cited_with_attribution"])

    def test_finite_checks_keep_both_positive_and_adverse_results(self):
        checks = self.receipt["finite_checks"]
        self.assertEqual(checks["check_limit"], 200000)
        self.assertEqual(len(checks["first_error_envelope_failures"]), 0)
        self.assertEqual(
            len(checks["first_positive_lower_bound_failures_after_622"]),
            0,
        )
        self.assertGreater(
            len(checks["lower_bound_counterexamples_by_prime_square_block"]),
            0,
        )
        self.assertTrue(self.receipt["classification"][
            "broad_rough_lower_bound_story_refuted_in_checked_blocks"])

    def test_candidate_reuse_is_diagnostic_not_theorem(self):
        candidate = self.receipt["candidate_reuse"]
        self.assertEqual(candidate["name"],
                         "roughness-product baseline diagnostic")
        self.assertIn("Q46189", candidate["smallest_next_test"])
        self.assertTrue(self.receipt["classification"][
            "rough_product_baseline_useful_as_diagnostic"])


if __name__ == "__main__":
    unittest.main()
