"""Independent factorization checks of the shared-prime correction identity."""
from math import gcd, isqrt
import unittest

from parity_bound_bootstrap import generate_prefix, parity_batch, recover_parity_primes
from redistribution import trial_prime
from shared_prime_correction import shared_prime_gain


class SharedPrimeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bounds = generate_prefix(200, same_factor=True)["lower_bounds"]
        cls.flags = [trial_prime(n) for n in range(1100)]
        # Exact counts are an independent validation input only.
        cls.exact = [sum(cls.flags[p] and cls.flags[n-p] for p in range(3, n-2, 2))
                     for n in range(6, 201, 2)]

    def test_exact_common_prime_identity_and_conditional_bound_on_one_band(self):
        base = parity_batch(self.bounds, 220, 63)["rows"]
        least = parity_batch(self.bounds, 220, 63, same_factor=True)["rows"]
        for row, old in zip(base, least):
            n = row["target_even"]
            composites = set()
            for c in range(3, n-2, 2):
                if self.flags[c]:
                    continue
                least_factor = next(p for p in range(3, isqrt(c)+1, 2) if c % p == 0)
                if least_factor > 6:
                    composites.add(c)
            common = sum(n-c in composites and gcd(c, n-c) > 1 and c != n-c
                         for c in composites)
            coprime = sum(n-c in composites and gcd(c, n-c) == 1 for c in composites)
            g = sum(self.flags[p] and self.flags[n-p] for p in range(3, n-2, 2))
            exact_gain = shared_prime_gain(self.bounds, n, exact=True)
            lower_gain = shared_prime_gain(self.bounds, n)
            with self.subTest(target=n):
                self.assertEqual(exact_gain["gain"], common)
                self.assertEqual(shared_prime_gain(self.exact, n)["gain"], common)
                self.assertEqual(row["L"] + common, g - coprime)
                value = row["L"] + lower_gain["gain"]
                self.assertLessEqual(old["L"], value)
                self.assertLessEqual(value, g)
                self.assertEqual(value % 2, g % 2)
                self.assertLessEqual(lower_gain["largest_prior_target"], 200)

    def test_nonleast_shared_prime_and_prime_above_square_root(self):
        for n, ell, left, right in ((234, 13, 91, 143), (984, 41, 451, 533)):
            with self.subTest(target=n):
                correction = shared_prime_gain(self.bounds, n)
                base = parity_batch(self.bounds, n, 1)["rows"][0]["L"]
                old = parity_batch(self.bounds, n, 1, same_factor=True)["rows"][0]["L"]
                self.assertEqual(gcd(left, right), ell)
                self.assertEqual(left + right, n)
                self.assertEqual(correction["gain"], 2)
                self.assertEqual(old, base)
                self.assertEqual(correction["terms"][0]["shared_prime"], ell)
        self.assertGreater(41, isqrt(984-3))
        self.assertEqual(parity_batch(self.bounds, 234, 1)["rows"][0]["L"] + 2, 30)

    def test_squares_two_factor_diagonal_negative_bounds_and_powers_of_two(self):
        for n, expected_terms in ((242, 1), (286, 2), (338, 1)):
            with self.subTest(target=n):
                record = shared_prime_gain(self.exact, n)
                self.assertEqual(len(record["terms"]), expected_terms)
                self.assertTrue(all(term["cofactor_diagonal"] == 1 for term in record["terms"]))
        negative = [value - 10000 for value in self.bounds]
        for n in (234, 242, 286, 338, 984):
            self.assertEqual(shared_prime_gain(negative, n)["gain"], 0)
            self.assertEqual(shared_prime_gain(negative, n, exact=True)["gain"],
                             shared_prime_gain(self.bounds, n, exact=True)["gain"])
        for n in (256, 512, 1024):
            self.assertEqual(shared_prime_gain(self.bounds, n)["gain"], 0)

    def test_input_boundary_and_base_bound_attachment(self):
        for bounds, target in (([], 234), ([1], 18), (self.bounds, 200)):
            with self.subTest(target=target), self.assertRaises(ValueError):
                shared_prime_gain(bounds, target)
        self.assertEqual(shared_prime_gain([1], 8)["gain"], 0)
        with self.assertRaises(ValueError):
            shared_prime_gain(self.bounds, 234, exact=1)
        result = shared_prime_gain(self.bounds, 234)
        self.assertIn("LOWER bounds", result["input_meaning"])
        self.assertIn("replaces", result["add_to"])

    def test_fixed_quartet_repairing_cannot_supply_universal_strict_descent(self):
        """A checked falsifier for descent by re-pairing unchanged factors.

        For a<b<c<d the only targets are U=ab+cd, V=ac+bd, W=ad+bc.
        U-V=(c-b)(d-a)>0 and V-W=(b-a)(d-c)>0. Thus the lowest W has
        no smaller target in this orbit. Cubic validity at U implies it
        at V,W because their cutoffs are smaller. This does not exclude
        changing factors or another descent. Reviewed by Sol, 2026-09-08.
        """
        _, _, earlier_primes = recover_parity_primes(self.bounds)
        quartet = [7, 11, 13, 17]
        self.assertTrue(set(quartet) <= set(earlier_primes))
        witnesses = {}
        for partner in range(1, 4):
            other = [i for i in range(1, 4) if i != partner]
            left = quartet[0] * quartet[partner]
            right = quartet[other[0]] * quartet[other[1]]
            n = left + right
            self.assertEqual(gcd(left, right), 1)
            self.assertTrue(6**3 <= n-3 < 7**3)
            self.assertGreater(min(quartet), 6)
            witnesses[n] = (left, right)
        self.assertEqual(sorted(witnesses), [262, 278, 298])
        self.assertEqual(witnesses[262], (119, 143))
        a, b, c, d = quartet
        self.assertEqual((a*b+c*d)-(a*c+b*d), (c-b)*(d-a))
        self.assertEqual((a*c+b*d)-(a*d+b*c), (b-a)*(d-c))
        # Smaller possible least factors cannot meet the cubic condition:
        # validity requires even N<a**3+3, whereas these are minimum W.
        for a, b, c, d in ((3, 5, 7, 11), (5, 7, 11, 13)):
            self.assertGreater(a*d+b*c, a**3+2)
        # This is composite-pair loss, not a Goldbach counterexample.
        base = parity_batch(self.bounds, 262, 1)["rows"][0]["L"]
        gain = shared_prime_gain(self.bounds, 262, exact=True)["gain"]
        g = sum(self.flags[p] and self.flags[262-p] for p in range(3, 260, 2))
        self.assertEqual((base, gain, g), (15, 0, 17))
        # A minimal pairing has no automatic prime-center escape either.
        a, b, c, d = 11, 13, 19, 31
        for n in (a*b+c*d, a*c+b*d, a*d+b*c):
            self.assertTrue(n-3 < a**3)
            self.assertEqual((n//2) % 3, 0)
            self.assertFalse(self.flags[n//2])


if __name__ == "__main__":
    unittest.main()
