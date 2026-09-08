"""Checks of CRT stress witnesses, distinct from the infinite theorem."""
from copy import deepcopy
from math import gcd
import unittest

from distance_nine_stress import build_pattern, find_prime_witness, verify_witness
from redistribution import trial_prime


class DistanceNineTests(unittest.TestCase):
    def test_patterns_cover_palette_and_preceding_prime_gap(self):
        for cap in (3, 7, 17, 29, 43):
            pattern = build_pattern(cap)
            needed = {2, 4, 6, 8} | {9-p for p in range(3, cap+1, 2) if trial_prime(p)}
            self.assertEqual({r["offset"] for r in pattern["constraints"]}, needed)
            self.assertNotIn(0, needed)
            self.assertEqual(gcd(pattern["q_residue"], pattern["modulus"]), 1)
            primes = []
            for row in pattern["constraints"]:
                self.assertTrue(trial_prime(row["prime_divisor"]))
                self.assertEqual((pattern["q_residue"]+row["offset"]) % row["prime_divisor"], 0)
                primes.append(row["prime_divisor"])
            self.assertEqual(len(set(primes)), len(primes))

    def test_explicit_representable_witness_and_actual_minimum(self):
        pattern = build_pattern(17)
        result = verify_witness(pattern, 4_304_309, pair_left=127)
        target = result["target_even"]
        self.assertEqual(target, 4_304_318)
        self.assertFalse(any(trial_prime(n) for n in range(4_304_310, target)))
        self.assertFalse(any(trial_prime(p) and trial_prime(target-p) for p in range(2, 127)))
        self.assertEqual(result["verified_goldbach_pair"], [127, 4_304_191])

    def test_bounded_search_reports_found_or_limit_without_claiming_disproof(self):
        result = find_prime_witness(17)
        self.assertEqual(result["status"], "found")
        self.assertEqual(result["witness"]["preceding_prime"], 4_304_309)
        limited = find_prime_witness(17, maximum_trial_root=1)
        self.assertEqual(limited["status"], "search_limit")
        self.assertEqual(limited["tested_candidates"], 0)

    def test_forged_pattern_bad_prime_and_invalid_pair_rejected(self):
        pattern = build_pattern(17)
        bad = deepcopy(pattern)
        bad["constraints"][0]["offset"] += 2
        with self.assertRaises(ValueError):
            verify_witness(bad, 4_304_309)
        with self.assertRaises(ValueError):
            verify_witness(pattern, 4_304_311)
        with self.assertRaises(ValueError):
            verify_witness(pattern, 4_304_309, pair_left=17)
        for cap in (True, 2, 17.0):
            with self.assertRaises(ValueError):
                build_pattern(cap)


if __name__ == "__main__":
    unittest.main()
