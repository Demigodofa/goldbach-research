import json
import unittest
from pathlib import Path


EVIDENCE = Path(
    "evidence/"
    "mobius-moment-square-degree5-q46189-source-pair-bucket-compensation-audit.json")


class MobiusMomentSquareDegree5Q46189SourcePairBucketTests(
        unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = json.loads(EVIDENCE.read_text(encoding="utf-8"))
        cls.q46189, cls.q38038 = cls.receipt["rows"]

    def test_receipt_preserves_boundaries(self):
        self.assertEqual(
            self.receipt["status"],
            "AUDIT_q46189_source_pair_bucket_compensation")
        self.assertTrue(
            self.receipt["finite_source_pair_bucket_compensation_audit_only"])
        self.assertTrue(self.receipt["finite_diagnostic_only"])
        self.assertFalse(
            self.receipt["source_pair_bucket_compensation_theorem_proved"])
        self.assertFalse(
            self.receipt["mirror_source_pair_compensation_theorem_proved"])
        self.assertFalse(
            self.receipt["replacement_packet_compensation_theorem_proved"])
        self.assertFalse(self.receipt["goldbach_proved"])

    def test_cross_terms_reconstruct_aggregate(self):
        classification = self.receipt["classification"]
        self.assertTrue(
            classification["q38038_cross_terms_reconstruct_aggregate"])
        self.assertTrue(
            classification["q46189_cross_terms_reconstruct_aggregate"])
        self.assertLess(
            self.q38038[
                "cross_term_reconstruction_relative_to_diagonal_half"],
            1e-15,
        )
        self.assertLess(
            self.q46189[
                "cross_term_reconstruction_relative_to_diagonal_half"],
            1e-15,
        )

    def test_q38038_bucket_compensation_is_localized(self):
        comparison = self.receipt["comparison"]
        classification = self.receipt["classification"]
        self.assertEqual(self.q38038["reduced_denominator"], 38038)
        self.assertAlmostEqual(
            self.q38038["aggregate_middle_A_to_10A"],
            -0.939992990438763,
            places=15,
        )
        self.assertAlmostEqual(
            self.q38038["aggregate_non_middle_sum"],
            0.09269980585259228,
            places=15,
        )
        self.assertAlmostEqual(
            self.q38038["off_diagonal_over_diagonal_half"],
            -0.8472931845861708,
            places=15,
        )
        self.assertGreater(comparison["q38038_top_four_non_middle_share"], .8)
        self.assertTrue(
            classification[
                "q38038_compensation_localizes_to_mirror_source_pair_block"])

    def test_top_four_terms_are_mirror_block(self):
        expected = {
            ((143, 266), (143, 266)),
            ((143, 266), (266, 143)),
            ((266, 143), (143, 266)),
            ((266, 143), (266, 143)),
        }
        observed = {
            (
                tuple(row["left_source_pair"]),
                tuple(row["right_source_pair"]),
            )
            for row in self.q38038[
                "top_non_middle_compensation_terms"][:4]
        }
        self.assertEqual(observed, expected)

    def test_q46189_lacks_non_middle_rescue(self):
        classification = self.receipt["classification"]
        self.assertEqual(self.q46189["reduced_denominator"], 46189)
        self.assertAlmostEqual(
            self.q46189["aggregate_non_middle_sum"],
            -0.7213404420565929,
            places=15,
        )
        self.assertTrue(
            classification[
                "q46189_lacks_positive_aggregate_non_middle_compensation"])

    def test_next_action_targets_mirror_source_pair_theorem(self):
        action = self.receipt["candidate_next_action"]
        self.assertEqual(
            action["name"],
            "mirror-source-pair compensation theorem target")
        self.assertIn("(143,266)", action["mechanism"])
        self.assertIn("all 34 replacement packets", action["smallest_next_test"])


if __name__ == "__main__":
    unittest.main()
