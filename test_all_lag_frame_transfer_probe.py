import unittest

from all_lag_frame_transfer_probe import all_lag_frame_transfer_probe


class AllLagFrameTransferProbeTests(unittest.TestCase):
    def test_probe_includes_adversarial_candidates_and_open_scope(self):
        receipt = all_lag_frame_transfer_probe(
            (101, 103), 3, 5, 6, 3, 14,
            ((1, 2), (3, 6)), random_trials=8, random_seed=7)
        self.assertGreaterEqual(receipt["candidate_count"], 16)
        self.assertEqual(len(receipt["lag_blocks"]), 2)
        for block in receipt["lag_blocks"]:
            self.assertGreater(
                block["minimum_tested_exact_over_frame_lag_budget"], 0)
            self.assertGreater(block["candidate_aggregate_exact_over_frame"], 0)
        self.assertFalse(receipt["weighted_all_lag_lower_frame_proved"])

    def test_seeded_probe_is_reproducible(self):
        arguments = ((101,), 3, 5, 5, 3, 12, ((1, 3),))
        first = all_lag_frame_transfer_probe(
            *arguments, random_trials=4, random_seed=19)
        second = all_lag_frame_transfer_probe(
            *arguments, random_trials=4, random_seed=19)
        self.assertEqual(first["lag_blocks"], second["lag_blocks"])

    def test_invalid_lag_and_modulus_are_rejected(self):
        with self.assertRaises(ValueError):
            all_lag_frame_transfer_probe(
                (101,), 3, 5, 6, 3, 14, ((0, 2),), random_trials=0)
        with self.assertRaisesRegex(ValueError, "prime"):
            all_lag_frame_transfer_probe(
                (105,), 3, 5, 6, 3, 14, ((1, 2),), random_trials=0)


if __name__ == "__main__":
    unittest.main()
