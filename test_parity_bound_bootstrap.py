"""Independent finite checks of lower-bound/parity recursion and input meaning."""
from math import isqrt
import unittest
from unittest.mock import patch

from cubic_sieve import cubic_sieve_count
from parity_bound_bootstrap import generate_prefix, parity_batch, recover_parity_primes
from redistribution import trial_prime


class ParityBoundTests(unittest.TestCase):
    def test_complete_canonical_prefix_has_both_invariants_through_2000(self):
        record = generate_prefix(2000)
        flags = [trial_prime(n) for n in range(2001)]
        for i, lower in enumerate(record["lower_bounds"]):
            n = 6 + 2 * i
            g = sum(flags[a] and flags[n - a] for a in range(3, n - 2, 2))
            with self.subTest(target=n):
                self.assertLessEqual(lower, g)
                self.assertEqual(lower % 2, g % 2)
                self.assertEqual(lower % 2, flags[n // 2])
        endpoint, classified, primes = recover_parity_primes(record["lower_bounds"])
        self.assertEqual((endpoint, classified), (2000, 999))
        self.assertEqual(primes, [p for p in range(3, 1000, 2) if flags[p]])
        self.assertEqual(record["lower_bounds"][(24 - 6) // 2], 4)
        self.assertEqual(sum(flags[a] and flags[24 - a] for a in range(3, 22, 2)), 6)

    def test_canonical_base_small_progress_and_every_stage_uses_earlier_labels(self):
        self.assertEqual(generate_prefix(6)["lower_bounds"], [1])
        record = generate_prefix(2000)
        self.assertEqual(record["stages"][0]["target_end"], 10)
        self.assertEqual(record["lower_bounds"][:3], [1, 2, 3])
        prior = 6
        for stage in record["stages"]:
            self.assertEqual(stage["previous_end"], prior)
            self.assertGreater(stage["target_end"], prior)
            self.assertLessEqual(stage["cubic_cutoff"], stage["classified_last_odd"])
            self.assertLessEqual(stage["required_cofactor_limit"], stage["classified_last_odd"])
            self.assertLessEqual(2 * stage["classified_last_odd"], prior)
            prior = stage["target_end"]
        self.assertEqual(prior, 2000)

    def test_negative_truthful_bounds_propagate_the_same_parity_without_exact_counts(self):
        prefix = generate_prefix(200)["lower_bounds"]
        lowered = [value - 100 for value in prefix]
        self.assertTrue(all(value < 0 for value in lowered))
        self.assertEqual(recover_parity_primes(prefix), recover_parity_primes(lowered))
        ordinary = parity_batch(prefix, 220, 63)
        negative = parity_batch(lowered, 220, 63)
        self.assertEqual(ordinary["rows"], negative["rows"])
        self.assertIn("conditional", negative["input_meaning"])

    def test_diagonal_composite_correction_matches_independent_factorization(self):
        prefix = generate_prefix(200)["lower_bounds"]
        rows = {row["target_even"]: row for row in parity_batch(prefix, 220, 63)["rows"]}
        for n in (242, 254, 264, 290, 338):
            row = rows[n]
            center = n // 2
            least = next((p for p in range(3, isqrt(center) + 1, 2)
                          if center % p == 0), center)
            diagonal = int(center % 2 == 1 and least != center and least > 6)
            reference = cubic_sieve_count(n)
            self.assertEqual(row["composite_diagonal"], diagonal)
            self.assertLessEqual(row["L"], reference["union_bound_raw"])
            self.assertEqual((reference["result"] - row["L"]) % 2, 0)
        self.assertEqual(rows[242]["composite_diagonal"], 1)  # 121+121
        self.assertEqual(rows[338]["composite_diagonal"], 1)  # 169+169
        self.assertEqual(rows[254]["composite_diagonal"], 0)  # 127+127

    def test_unsafe_ranges_band_edges_and_malformed_prefixes_are_rejected(self):
        for endpoint in (4, 7, True, 10.0):
            with self.subTest(endpoint=endpoint), self.assertRaises(ValueError):
                generate_prefix(endpoint)
        for values in ([], [True], [1.0], [0]):
            with self.subTest(values=values), self.assertRaises(ValueError):
                recover_parity_primes(values)
        with self.assertRaises(ValueError):
            parity_batch([1], 12, 10)  # crosses a band at30
        with self.assertRaises(ValueError):
            parity_batch([1], 20, 1)  # insufficient cofactor range
        with self.assertRaises(ValueError):
            parity_batch([1], 6, 1)  # input is not earlier
        prefix = generate_prefix(200)["lower_bounds"]
        with self.assertRaises(ValueError):
            parity_batch(prefix, 342, 3)  # H=339..343 crosses the cube343

    def test_production_recursion_calls_no_full_count_or_prime_oracle(self):
        def forbidden(*_args, **_kwargs):
            raise AssertionError("forbidden exact-count or prime-oracle route")
        with patch("redistribution.sieve", forbidden), patch("cubic_sieve.sieve", forbidden), \
                patch("packed_goldbach.sieve", forbidden), \
                patch("packed_goldbach.build_prime_square", forbidden), \
                patch("count_bootstrap.build_chain", forbidden), \
                patch("cubic_batch.build_chain", forbidden), \
                patch("cubic_batch.recover_binary_flags", forbidden), \
                patch("count_reconstruction.recover_binary_flags", forbidden):
            record = generate_prefix(2000)
            refined = generate_prefix(2000, same_factor=True)
        self.assertEqual(record["final_end"], 2000)
        self.assertEqual(len(record["lower_bounds"]), 998)
        self.assertEqual(refined["final_end"], 2000)

    def test_refined_prefix_keeps_both_invariants_and_the_pointwise_ceiling(self):
        base = generate_prefix(2000)["lower_bounds"]
        refined = generate_prefix(2000, same_factor=True)["lower_bounds"]
        flags = [trial_prime(n) for n in range(2001)]
        improved = 0
        for i, (lower, value) in enumerate(zip(base, refined)):
            n = 6 + 2 * i
            g = sum(flags[p] and flags[n - p] for p in range(3, n - 2, 2))
            # Independent integer cube-root calculation, avoiding the producer.
            z = 1
            while (z + 1) ** 3 <= n - 3:
                z += 1
            with self.subTest(target=n):
                self.assertLessEqual(lower, value)
                self.assertLessEqual(value, g)
                self.assertEqual(value % 2, flags[n // 2])
                self.assertLessEqual(value - lower, n // (z + 1))
                if n & (n - 1) == 0:
                    self.assertEqual(value, lower)
            improved += value > lower
        self.assertGreater(improved, 0)
        for n in (24, 90, 242, 338, 486, 512, 600, 1000):
            self.assertLessEqual(refined[(n - 6) // 2],
                                 cubic_sieve_count(n)["union_bound_raw"])

    def test_refinement_uses_earlier_values_without_requiring_exact_counts(self):
        prefix = generate_prefix(14)["lower_bounds"]
        normal = parity_batch(prefix, 24, 1, same_factor=True)["rows"][0]
        weaker = prefix.copy()
        weaker[(8 - 6) // 2] -= 2  # Truthful lower value, unchanged prime parities.
        lowered = parity_batch(weaker, 24, 1, same_factor=True)["rows"][0]
        self.assertEqual(recover_parity_primes(prefix), recover_parity_primes(weaker))
        self.assertEqual((normal["base_L"], normal["L"], lowered["L"]), (4, 6, 4))
        negative = [value - 100000 for value in generate_prefix(200)["lower_bounds"]]
        refined = parity_batch(negative, 220, 63, same_factor=True)
        ordinary = parity_batch(negative, 220, 63)
        self.assertEqual([row["L"] for row in refined["rows"]],
                         [row["L"] for row in ordinary["rows"]])
        diagonal = next(row for row in refined["rows"] if row["target_even"] == 242)
        self.assertEqual(diagonal["composite_diagonal"], 1)
        self.assertEqual(diagonal["same_factor_gain"], 0)
        self.assertEqual(diagonal["M"] % 2, 1)
        self.assertEqual(diagonal["L"] % 2, 0)  # 121 is composite: its bit cancels M's diagonal.

    def test_refinement_checks_ranges_and_reports_only_earlier_dependencies(self):
        for invalid in (1, None, "yes"):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                generate_prefix(6, same_factor=invalid)
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                parity_batch([1], 8, 2, same_factor=invalid)
        with self.assertRaises(ValueError):
            parity_batch([1], 18, 1, same_factor=True)
        prefix = generate_prefix(200, same_factor=True)["lower_bounds"]
        batch = parity_batch(prefix, 220, 63, same_factor=True)
        self.assertLessEqual(batch["largest_correction_input"], 200)
        self.assertGreater(batch["same_factor_terms"], 0)
        self.assertIn("LOWER bounds", batch["input_meaning"])


if __name__ == "__main__":
    unittest.main()
