"""Independent symbolic logarithm controls, with no asymptotic test claim."""
from collections import defaultdict
from fractions import Fraction as F
from functools import lru_cache
from math import isqrt
import unittest

from character_partner_weight import negative_hyperbola_terms, negative_log_coefficients
from exceptional_character_model import character_values
from redistribution import trial_prime


@lru_cache(maxsize=None)
def trial_factors(n):
    result = {}
    divisor = 2
    while divisor*divisor <= n:
        while n % divisor == 0:
            result[divisor] = result.get(divisor, 0)+1
            n //= divisor
        divisor += 1
    if n > 1:
        result[n] = result.get(n, 0)+1
    return result


def direct_divisor_coefficients(n, chi):
    """Expand every term chi(d)*log(n/d), independently of the support formula."""
    result = defaultdict(int)
    for d in range(1, isqrt(n)+1):
        if n % d:
            continue
        divisors = (d,) if d*d == n else (d, n//d)
        for divisor in divisors:
            for prime, exponent in trial_factors(n//divisor).items():
                result[prime] += chi[divisor % len(chi)]*exponent
    return {prime: coefficient for prime, coefficient in result.items() if coefficient}


def add_product(polynomial, first_prime, coefficients):
    for prime, coefficient in coefficients.items():
        polynomial[tuple(sorted((first_prime, prime)))] += coefficient


class CharacterPartnerWeightTests(unittest.TestCase):
    def test_complete_negative_units_match_both_divisor_expansions(self):
        for conductor, sign in ((31, 1), (33, 1), (40, 1), (40, -1)):
            chi = character_values(conductor, two_sign=sign)
            for n in range(2, 1201):
                if chi[n % conductor] != -1:
                    continue
                direct = direct_divisor_coefficients(n, chi)
                self.assertEqual(dict(negative_log_coefficients(n, conductor, two_sign=sign)),
                                 direct)
                paired = defaultdict(int)
                for d, value in negative_hyperbola_terms(n, conductor, two_sign=sign):
                    self.assertLess(d*d, n)
                    self.assertEqual(n % d, 0)
                    for prime, exponent in trial_factors(n).items():
                        paired[prime] += value*exponent
                    for prime, exponent in trial_factors(d).items():
                        paired[prime] -= 2*value*exponent
                self.assertEqual({p: c for p, c in paired.items() if c}, direct)

    def test_prime_powers_and_zero_weight_composite_guards(self):
        cases = {11: ((11, 1),), 1331: ((11, 2),), 209: ((11, 2),),
                 215: ((43, 2),), 5*19*11: ((11, 4),), 11*17*43: (),
                 11*43**2: ((11, 1),), 11**3*5**2*19**4: ((11, 30),)}
        for n, expected in cases.items():
            self.assertEqual(negative_log_coefficients(n, 31), expected)
        # The first hyperbola term is log(n)>0 although the full weight is zero.
        # A partial signed divisor sum is therefore not a valid lower bound.
        self.assertEqual(negative_hyperbola_terms(11*17*43, 31)[0], (1, 1))
        self.assertEqual(negative_log_coefficients(11*17*43, 31), ())

    def test_exact_prime_large_factor_and_repeated_factor_decomposition(self):
        chi = character_values(31)
        saw_large = saw_repeated = False
        for upper, target, cutoff, bound in ((400, 558, 4, 10),
                                             (350, 496, 4, 10),
                                             (2100, 2790, 10, 50)):
            total, prime_part, large, repeated, full_prime = (defaultdict(int) for _ in range(5))
            for p in range(upper//2+1, upper+1):
                n = target-p
                if not upper//2 < n <= upper or not trial_prime(p):
                    continue
                if trial_prime(n):
                    add_product(full_prime, p, {n: 1})
                if chi[p % 31] != 1 or chi[n % 31] == 0:
                    continue
                self.assertEqual(chi[n % 31], -1)
                factors = trial_factors(n)
                if any(q <= cutoff or (chi[q % 31] == 1 and q <= bound) for q in factors):
                    continue
                weight = direct_divisor_coefficients(n, chi)
                add_product(total, p, weight)
                if trial_prime(n):
                    self.assertEqual(weight, {n: 1})
                    add_product(prime_part, p, weight)
                elif any(exponent > 1 for exponent in factors.values()):
                    add_product(repeated, p, weight)
                elif weight:
                    negative = [q for q in factors if chi[q % 31] == -1]
                    positive = [q for q in factors if chi[q % 31] == 1]
                    self.assertEqual(len(negative), 1)
                    self.assertTrue(positive)
                    self.assertTrue(all(q > bound for q in positive))
                    self.assertEqual(weight, {negative[0]: 2**len(positive)})
                    add_product(large, p, weight)
            combined = defaultdict(int)
            for part in (prime_part, large, repeated):
                for key, value in part.items():
                    combined[key] += value
            self.assertEqual(dict(total), dict(combined))
            self.assertEqual(dict(full_prime), {key: 2*value for key, value in prime_part.items()})
            saw_large |= bool(large)
            saw_repeated |= bool(repeated)
        self.assertTrue(saw_large)
        self.assertTrue(saw_repeated)

    def test_rough_repeated_factor_union_bound_counts_partners_once(self):
        upper = 3000
        for cutoff in (2, 10, 50):
            partners = [n for n in range(2, upper+1)
                        if all(q > cutoff for q in trial_factors(n))
                        and any(a > 1 for a in trial_factors(n).values())]
            integer_union_bound = sum(upper//(q*q) for q in range(cutoff+1, isqrt(upper)+1))
            self.assertLessEqual(len(partners), integer_union_bound)
            self.assertLessEqual(integer_union_bound, F(upper, cutoff-1))

    def test_exact_domain_rejects_positive_sign_and_nonunits(self):
        for function in (negative_log_coefficients, negative_hyperbola_terms):
            for n, conductor, sign in ((True, 31, 1), (11.0, 31, 1), (1, 31, 1),
                                       (0, 31, 1), (121, 31, 1), (31, 31, 1),
                                       (11, 25, 1), (11, True, 1), (11, 31, True)):
                with self.assertRaises(ValueError):
                    function(n, conductor, two_sign=sign)


if __name__ == "__main__":
    unittest.main()
