import json
import unittest
from pathlib import Path


class Q286RawSignedWitnessCensusTests(unittest.TestCase):
    def test_raw_signed_witness_census_falsifies_from_10000_threshold(self):
        path = Path("evidence/q286-raw-signed-witness-census.json")
        receipt = json.loads(path.read_text(encoding="utf-8"))

        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["eventual_signed_witness_threshold_proved"])
        self.assertTrue(
            receipt["naive_from_10000_signed_witness_positivity_falsified"])
        self.assertTrue(receipt["raw_signed_witness_census_measured"])

        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertTrue(receipt["full_cycles_scanned"])
        self.assertEqual(receipt["cycle_count"], 12)
        self.assertEqual(receipt["targets_per_cycle"], 5005)
        self.assertEqual(receipt["total_even_targets_scanned"], 60060)
        self.assertEqual(receipt["nonpositive_raw_signed_action_count"], 89)
        self.assertEqual(receipt["last_nonpositive_target"], 88346)
        self.assertEqual(receipt["contiguous_positive_suffix_start_cycle"], 8)
        self.assertEqual(
            receipt["contiguous_positive_suffix_start_target"], 90080)
        self.assertEqual(receipt["nonpositive_cycle_indices"], [0, 1, 2, 3, 7])

        cycle_counts = [
            row["negative_or_zero_weighted_sum_count"]
            for row in receipt["cycle_rows"]
        ]
        self.assertEqual(cycle_counts, [75, 3, 5, 4, 0, 0, 0, 2, 0, 0, 0, 0])
        self.assertIn(
            "strict positivity",
            receipt["signed_witness_implication"])


if __name__ == "__main__":
    unittest.main()
