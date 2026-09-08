"""Exact controls for Henriot's corrected local divisor conditions."""
from fractions import Fraction
import unittest

from radical_majorant_correlation import (local_divisor_factor,
                                         truncated_local_divisor_factor)


def direct_tuple_density(p, target, a, b, depth):
    """Literal corrected condition, counted separately for every tuple."""
    modulus = p**(depth+1)
    answer = Fraction(1)
    for i in range(depth+1):
        for j in range(depth+1):
            if i == j == 0:
                continue
            count = 0
            for n in range(modulus):
                # In a nonzero tuple the erratum also enforces the zeros.
                if (n % p**i == 0 and n % p**(i+1) != 0 and
                        (target-n) % p**j == 0 and (target-n) % p**(j+1) != 0):
                    count += 1
            answer += Fraction(count, modulus)*(a if i else 1)*(b if j else 1)
    return answer


class RadicalMajorantCorrelationTests(unittest.TestCase):
    def test_corrected_tuple_density_with_zero_and_repeated_valuations(self):
        for p in (2, 3, 5):
            for target in (0, 1, p, p*p, -p*p, p**3+p):
                for a, b in ((0, 2), (2, 0), (Fraction(1, 3), Fraction(7, 4)), (2, 2)):
                    for depth in (0, 1, 2):
                        self.assertEqual(truncated_local_divisor_factor(p, target, a, b, depth),
                                         direct_tuple_density(p, target, a, b, depth))

    def test_exact_tail_proves_the_local_limit_in_both_root_cases(self):
        for p in (2, 3, 5, 7):
            for target in (0, 1, p, p*p, p**3, -p, 2*p+1):
                for a, b in ((0, 0), (0, 2), (Fraction(3, 2), Fraction(2, 7)), (2, 2)):
                    previous = Fraction(1)
                    for depth in range(4):
                        modulus = p**(depth+1)
                        if target % p:
                            tail = Fraction(a+b, modulus)
                        else:
                            tail = Fraction(a*b*(2-int(target % modulus == 0)), modulus)
                        partial = truncated_local_divisor_factor(p, target, a, b, depth)
                        self.assertEqual(partial+tail, local_divisor_factor(p, target, a, b))
                        self.assertGreaterEqual(partial, previous)
                        previous = partial

    def test_erratum_excludes_single_positive_valuation_at_shared_root(self):
        # At p|target, setting b=0 annihilates every nonzero corrected
        # tuple; the old rhohat would incorrectly retain a/p here.
        for p in (2, 3, 5):
            self.assertEqual(local_divisor_factor(p, p*p, 2, 0), 1)
            self.assertEqual(truncated_local_divisor_factor(p, p*p, 2, 0, 3), 1)
        self.assertEqual(local_divisor_factor(3, 6, 2, 2), Fraction(7, 3))
        self.assertEqual(local_divisor_factor(3, 7, 2, 2), Fraction(7, 3))
        self.assertEqual(local_divisor_factor(3, 6, Fraction(1, 2), 2), Fraction(4, 3))
        self.assertEqual(local_divisor_factor(3, 7, Fraction(1, 2), 2), Fraction(11, 6))

    def test_exact_input_and_bounded_enumeration_contract(self):
        for p, target, a, b in ((1, 6, 1, 1), (4, 6, 1, 1), (True, 6, 1, 1),
                                (3, True, 1, 1), (3, 6, 0.5, 1), (3, 6, True, 1),
                                (3, 6, -1, 1), (3, 6, 1, 3)):
            with self.assertRaises(ValueError):
                local_divisor_factor(p, target, a, b)
        for depth in (-1, True, 1.0, 1000000):
            with self.assertRaises(ValueError):
                truncated_local_divisor_factor(2, 6, 1, 1, depth)
        with self.assertRaises(ValueError):
            truncated_local_divisor_factor(101, 6, 1, 1, 3)
        self.assertIn("does not certify", local_divisor_factor.__doc__)


if __name__ == "__main__":
    unittest.main()
