"""Independent finite tests for canonical count-prefix bootstrapping."""
from copy import deepcopy
import unittest
from unittest.mock import patch

from count_bootstrap import build_chain, compact_receipt, replay_chain, replay_receipt
from redistribution import trial_prime


def direct_ordered_counts(last_even: int) -> list[int]:
    return [sum(trial_prime(addend) and trial_prime(target - addend)
                for addend in range(3, target - 2, 2))
            for target in range(6, last_even + 1, 2)]


class CountBootstrapTests(unittest.TestCase):
    def test_chain_counts_match_independent_trial_prime_pairs_through_2626(self):
        chain = build_chain([26, 626, 2626])
        self.assertEqual(chain["final_end"], 2626)
        self.assertEqual(chain["ordered_counts"], direct_ordered_counts(2626))
        self.assertTrue(replay_chain(chain))

    def test_first_safe_endpoint_is_exactly_26_and_28_is_rejected(self):
        chain = build_chain([26])
        self.assertEqual(chain["ordered_counts"], direct_ordered_counts(26))
        self.assertEqual(chain["stage_receipts"][0]["safe_target_limit"], 26)
        with self.assertRaises(ValueError):
            build_chain([28])

    def test_early_stages_need_no_recovered_odd_divisors_then_match_direct_counts(self):
        chain = build_chain([8, 10, 12, 26])
        self.assertEqual(chain["ordered_counts"], direct_ordered_counts(26))
        self.assertEqual(chain["stage_receipts"][0]["recovered_count_prefix_length"], 0)
        self.assertEqual(chain["stage_receipts"][1]["recovered_count_prefix_length"], 0)
        self.assertEqual(chain["stage_receipts"][-1]["newly_generated_even_count"], 7)

    def test_rejects_malformed_or_nonincreasing_stage_endpoints(self):
        for endpoints in ([], [True], [6], [25], [26, 26], [26, 625],
                          [26, 628], (26,)):
            with self.subTest(endpoints=endpoints):
                with self.assertRaises(ValueError):
                    build_chain(endpoints)

    def test_replay_rejects_tampering_with_canonical_json_type_distinction(self):
        chain = build_chain([26, 626])
        for path, replacement in ((["ordered_counts", 0], True),
                                  (["stage_receipts", 0, "counts_sha256"], "0" * 64),
                                  (["stage_ends", 0], 25)):
            altered = deepcopy(chain)
            target = altered
            for key in path[:-1]:
                target = target[key]
            target[path[-1]] = replacement
            with self.subTest(path=path), self.assertRaises(ValueError):
                replay_chain(altered)

    def test_compact_receipt_replays_and_rejects_tampering(self):
        receipt = compact_receipt(build_chain([8, 10, 12, 26, 626]))
        self.assertNotIn("ordered_counts", receipt)
        self.assertTrue(replay_receipt(receipt))
        altered = deepcopy(receipt)
        altered["stage_receipts"][1]["previous_counts_sha256"] = "0" * 64
        with self.assertRaises(ValueError):
            replay_receipt(altered)

    def test_production_chain_does_not_call_standard_sieve_builder(self):
        def forbidden(*_args, **_kwargs):
            raise AssertionError("ordinary sieve builder was called")
        with patch("redistribution.sieve", forbidden), patch("packed_goldbach.sieve", forbidden):
            chain = build_chain([26])
        self.assertEqual(chain["final_end"], 26)


if __name__ == "__main__":
    unittest.main()
