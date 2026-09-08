"""Independent finite checks for the cubic-cutoff sieve."""
from math import isqrt
import unittest

from cubic_sieve import cubic_sieve_block,cubic_sieve_count,event_masks,exact_floor_cuberoot
from redistribution import sieve,trial_prime


def direct_ordered_odd_prime_pairs(target: int) -> int:
    if target == 4:
        return 1
    return sum(trial_prime(a) and trial_prime(target - a)
               for a in range(3, target - 2, 2))


def independent_residual_memberships(target: int) -> list[int]:
    """Recreate event membership by divisibility, without using bit masks."""
    if target == 4:
        return [0]
    high = target - 3
    cutoff = exact_floor_cuberoot(high)
    primes = [p for p in range(3, isqrt(high) + 1, 2) if trial_prime(p)]
    memberships = []
    for candidate in range(3, high + 1, 2):
        reflected = target - candidate
        pre = any((candidate >= p * p and candidate % p == 0) or
                  (reflected >= p * p and reflected % p == 0)
                  for p in primes if p <= cutoff)
        if pre:
            continue
        memberships.append(sum((candidate >= p * p and candidate % p == 0) or
                               (reflected >= p * p and reflected % p == 0)
                               for p in primes if p > cutoff))
    return memberships


class CubicSieveTests(unittest.TestCase):
    def test_exact_count_matches_direct_trial_pairs_through_2000(self):
        for target in range(4, 2001, 2):
            with self.subTest(target=target):
                result = cubic_sieve_count(target)
                self.assertEqual(result["result"], direct_ordered_odd_prime_pairs(target))
                self.assertEqual(result["result"], result["union_bound_raw"] + result["S2"])

    def test_exact_floor_cuberoot_boundaries(self):
        for root in range(0, 50):
            self.assertEqual(exact_floor_cuberoot(root ** 3), root)
            if root:
                self.assertEqual(exact_floor_cuberoot(root ** 3 - 1), root - 1)
                self.assertEqual(exact_floor_cuberoot(root ** 3 + 1), root)
        self.assertEqual(exact_floor_cuberoot(1), 1)

    def test_independent_residual_event_multiplicity_is_at_most_two(self):
        for target in range(6, 1001, 2):
            with self.subTest(target=target):
                self.assertLessEqual(max(independent_residual_memberships(target), default=0), 2)

    def test_prime_argument_is_preserved_and_same_factor_both_arguments_is_one_event(self):
        prime_case = event_masks(42)
        prime_index = (5 - 3) // 2
        reflected_prime_index = prime_case["M_slots"] - 1 - prime_index
        for mask in prime_case["event_masks"].values():
            self.assertFalse(mask & (1 << prime_index))
            self.assertFalse(mask & (1 << reflected_prime_index))

        same_factor = event_masks(264)
        mask = same_factor["event_masks"][11]
        for candidate in (121, 143):
            index = (candidate - 3) // 2
            self.assertTrue(mask & (1 << index))
            self.assertEqual(sum(bool(other & (1 << index))
                                 for other in same_factor["event_masks"].values()), 1)
        self.assertEqual(cubic_sieve_count(264)["result"], direct_ordered_odd_prime_pairs(264))

    def test_event_masks_use_only_odd_primes_through_square_root(self):
        built = event_masks(1000)
        self.assertEqual(list(built["event_masks"]),
                         [p for p in range(3, isqrt(built["H"]) + 1, 2) if sieve(isqrt(built["H"]))[p]])

    def test_block_tallies_already_computed_raw_union_bounds(self):
        block = cubic_sieve_block(4, 12)
        self.assertEqual(block["nonpositive_union_bounds"],
                         sum(row["union_bound_raw"] <= 0 for row in block["rows"]))


if __name__ == "__main__":
    unittest.main()
