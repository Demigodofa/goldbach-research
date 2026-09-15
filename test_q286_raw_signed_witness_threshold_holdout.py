import json
import unittest
from pathlib import Path


class Q286RawSignedWitnessThresholdHoldoutTests(unittest.TestCase):
    def test_fresh_holdout_preserves_but_does_not_prove_threshold(self):
        path = Path("evidence/q286-raw-signed-witness-threshold-holdout.json")
        receipt = json.loads(path.read_text(encoding="utf-8"))

        self.assertFalse(receipt["goldbach_proved"])
        self.assertTrue(receipt["threshold_candidate_preserved"])
        self.assertFalse(receipt["threshold_candidate_proved"])

        previous = receipt["previous_census"]
        self.assertEqual(previous["last_nonpositive_target"], 88346)
        self.assertEqual(previous["positive_suffix_start_target"], 90080)
        self.assertEqual(previous["target_end"], 130118)

        fresh = receipt["fresh_holdout"]
        self.assertEqual(fresh["base_target_minimum"], 130120)
        self.assertEqual(fresh["target_end"], 250238)
        self.assertEqual(fresh["cycle_count"], 12)
        self.assertEqual(fresh["targets_per_cycle"], 5005)
        self.assertEqual(fresh["total_even_targets_scanned"], 60060)
        self.assertEqual(fresh["nonpositive_raw_signed_action_count"], 0)
        self.assertTrue(fresh["all_scanned_targets_positive"])
        self.assertEqual(fresh["cycle_nonpositive_counts"], [0] * 12)

        suffix = receipt["combined_checked_positive_suffix"]
        self.assertEqual(suffix["start_target"], 90080)
        self.assertEqual(suffix["end_target"], 250238)
        self.assertEqual(suffix["even_target_count"], 80080)
        self.assertEqual(
            suffix["nonpositive_raw_signed_action_count_after_start"], 0)
        self.assertIn("falsifies", receipt["falsifier"])


if __name__ == "__main__":
    unittest.main()
