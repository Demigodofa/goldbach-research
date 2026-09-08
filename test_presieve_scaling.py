"""Direct membership checks for variable-cutoff raw union bounds."""
import unittest
from math import isqrt

from presieve_scaling import raw_union_profile
from redistribution import trial_prime


def direct_counts(target, cutoff):
    if target == 4:
        return 1, 0, 1, 1
    primes = [p for p in range(3, isqrt(target - 3) + 1, 2) if trial_prime(p)]
    M = S1 = Q = G = 0
    for a in range(3, target - 2, 2):
        events = [p for p in primes if (a % p == 0 and a >= p*p)
                  or ((target-a) % p == 0 and target-a >= p*p)]
        if any(p <= cutoff for p in events):
            continue
        M += 1
        S1 += len(events)
        Q += trial_prime(a)
        G += trial_prime(a) and trial_prime(target-a)
    return M, S1, Q, G


class PresieveScalingTests(unittest.TestCase):
    def test_arbitrary_cutoffs_match_direct_membership_and_give_lower_bounds(self):
        for target in range(4, 502, 2):
            for row in raw_union_profile(target, [0, 2, 3, 7, isqrt(target)]):
                M, S1, _, G = direct_counts(target, row["presieve_cutoff"])
                self.assertEqual((row["M_after_presieve"], row["S1"]), (M, S1))
                self.assertLessEqual(row["raw_lower_bound"], G)

    def test_power_of_two_prime_leading_bound_without_semiprime_assumption(self):
        for exponent in range(3, 11):
            target = 2**exponent
            for row in raw_union_profile(target, [2, exponent, isqrt(target)]):
                M, S1, Q, _ = direct_counts(target, row["presieve_cutoff"])
                self.assertLessEqual(M-S1, 2*Q-M)

    def test_moving_more_events_into_presieve_never_decreases_raw_bound(self):
        for target in [12, 54, 128, 256, 1000]:
            rows = raw_union_profile(target, list(range(isqrt(target)+1)))
            bounds = [row["raw_lower_bound"] for row in rows]
            self.assertEqual(bounds, sorted(bounds))
        # This candidate meets three distinct square-start events. A general
        # low cutoff must not silently reuse the cubic two-overlap identity.
        self.assertEqual([p for p in [3, 5, 7] if 105 % p == 0 and 105 >= p*p],
                         [3, 5, 7])

    def test_special_base_and_invalid_parameters(self):
        self.assertEqual(raw_union_profile(4, [0, 2])[0]["raw_lower_bound"], 1)
        for target, cutoffs in [(True, [2]), (5, [2]), (6, []), (6, [True]),
                                (6, [-1]), (6, [2.0]), (6, (2,))]:
            with self.subTest(target=target, cutoffs=cutoffs):
                with self.assertRaises(ValueError):
                    raw_union_profile(target, cutoffs)


if __name__ == "__main__":
    unittest.main()
