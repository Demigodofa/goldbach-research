"""Compare independent exact simplex and moment routes; preserve the arithmetic gap."""
from fractions import Fraction as F
from math import comb, factorial
import unittest

from cubic_positivity_obstruction import dickman_main_enclosure
from formal_weight_conservation import (accessible_main_enclosure, dickman_moments,
                                        formal_dickman_main, formal_factor_integrals)
from log_weight_barrier import type_i_endpoint_coefficient


def multiply_series(left, right, degree):
    out = [F(0)]*(degree+1)
    for i, a in enumerate(left):
        for j, b in enumerate(right[:degree-i+1]):
            out[i+j] += a*b
    return out


def moments_from_product_of_exponentials(degree):
    # M(t)=product_{j>=1}exp(t^j/(j*j!)). Expand each exponential directly,
    # with no use of the moment recurrence in the implementation.
    result = [F(1)]+[F(0)]*degree
    for j in range(1, degree+1):
        factor = [F(0)]*(degree+1)
        for k in range(degree//j+1):
            factor[k*j] = F(1, factorial(k)*(j*factorial(j))**k)
        result = multiply_series(result, factor, degree)
    return tuple(value*factorial(j) for j, value in enumerate(result))


class FormalWeightConservationTests(unittest.TestCase):
    def test_general_polynomials_by_independent_simplex_and_moment_routes(self):
        for degree in range(1, 11):
            monomial = (0,)*degree+(1,)
            # This comparison covers every monomial in the polynomial
            # identity, including even degrees and near-cutoff values.
            for theta in (F(0), F(1, 1000), F(1, 2*degree), F(99, 100*degree)):
                integrals = formal_factor_integrals(monomial, theta)
                self.assertEqual(integrals[0], (1, F(1)))
                self.assertEqual(sum(value for _, value in integrals),
                                 formal_dickman_main(monomial, theta))
                self.assertTrue(all(k % 2 == 1 and k <= degree for k, _ in integrals))
            self.assertEqual(formal_dickman_main(monomial, F(0)),
                             type_i_endpoint_coefficient(monomial))
        signed = (0, 9, -5, 7, -10)
        for theta in (F(0), F(1, 100), F(1, 5)):
            self.assertEqual(sum(value for _, value in formal_factor_integrals(signed, theta)),
                             formal_dickman_main(signed, theta))

    def test_moment_recurrence_against_direct_exponential_product(self):
        self.assertEqual(dickman_moments(4), (F(1), F(1), F(3, 2), F(17, 6), F(19, 3)))
        self.assertEqual(dickman_moments(18), moments_from_product_of_exponentials(18))
        self.assertEqual(dickman_moments(0), (F(1),))

    def test_quintic_cutoff_conservation_and_signed_mass(self):
        for kappa in (F(0), F(1), F(100), F(7, 3)):
            f = (0, 1, -kappa, 4*kappa, -5*kappa, 2*kappa)
            for theta in (F(0), F(1, 1000), F(1, 100), F(1, 10), F(19, 100)):
                integrals = dict(formal_factor_integrals(f, theta))
                triple = -kappa*(1-3*theta)**2*(1+10*theta-15*theta**2)/12
                five = kappa*(1-5*theta)**4/12
                # kappa0 lowers the actual degree to1; absent terms are zero.
                self.assertEqual(integrals.get(3, 0), triple)
                self.assertEqual(integrals.get(5, 0), five)
                expected = (1-2*kappa*theta+18*kappa*theta**2
                            -F(170, 3)*kappa*theta**3+F(190, 3)*kappa*theta**4)
                self.assertEqual(formal_dickman_main(f, theta), expected)
                self.assertEqual(triple+five, expected-1)
        self.assertLess(formal_dickman_main((0, 10, 0, -9), F(0)), 0)
        # An increased endpoint main also increases the FORMAL composite
        # total; it is not an independent certificate for actual primes.
        self.assertEqual(formal_factor_integrals((0, 0, 0, 1), F(0)),
                         ((1, F(1)), (3, F(1, 2))))

    def test_factorial_enclosure_and_separate_fixed_sieve_error(self):
        theta, endpoint = F(1, 100), F(12, 25)
        for kappa in (F(1), F(100), F(7, 3)):
            f = (0, 1+kappa, 0, -kappa)
            lower, upper = accessible_main_enclosure(f, theta, endpoint)
            old_lower, old_upper = dickman_main_enclosure(kappa, theta, endpoint)
            self.assertGreaterEqual(lower, old_lower/2)
            self.assertLessEqual(upper, old_upper/2)
            self.assertLessEqual(lower, formal_dickman_main(f, theta))
            self.assertGreaterEqual(upper, formal_dickman_main(f, theta))
        f = (0, 1, -100, 400, -500, 200)
        lower, upper = accessible_main_enclosure(f, F(1, 1000), endpoint)
        self.assertGreater(lower, F(4, 5))
        self.assertLess(upper-lower, F(1, 10**100))
        # Independently check the positive series ratio used by the tail
        # proof over the degree64 verifier's endpoint boundary cases.
        for j in range(65):
            m = max(2, 2*j)
            for n in (m, m+1, m+9):
                ratio = F(n+2, n+1)**j/F(n+1)
                self.assertLessEqual(ratio, F(2, 3))
            finite_tail = sum(F((n+1)**j, factorial(n)) for n in range(m, m+20))
            self.assertLessEqual(finite_tail, F(3*(m+1)**j, factorial(m)))
        self.assertIn('no interval for the actual prime sum', accessible_main_enclosure.__doc__)

    def test_cutoff_and_exact_domains(self):
        # Outside theta<1/d the omitted support really changes the answer:
        # f=x^3, theta=2/5 leaves no triple simplex, hence total1; the
        # untruncated Dickman polynomial would instead return51/50.
        theta = F(2, 5)
        self.assertGreater(3*theta, 1)
        self.assertEqual(F(3, 2)-3*theta+F(9, 2)*theta**2, F(51, 50))
        for function in (formal_dickman_main, formal_factor_integrals):
            for f, theta in (((0, 0, 0, 1), F(1, 3)), ((0, 1), True),
                             ((0, 1), 0.1), ((0, 1), F(-1)), ((0, 2), F(0)),
                             ((0, True), F(0)), ([0, 1], F(0))):
                with self.assertRaises(ValueError):
                    function(f, theta)
        # Trailing zeros do not pretend that the actual degree increased.
        self.assertEqual(formal_dickman_main((0, 1, 0, 0), F(1, 2)), 1)
        with self.assertRaises(ValueError):
            formal_factor_integrals((0,)*13+(1,), F(0))
        for order in (True, -1, 65, 2.0):
            with self.assertRaises(ValueError):
                dickman_moments(order)
        for theta, endpoint in ((F(0), F(1, 2)), (F(1, 100), 0.5),
                                (F(1, 100), F(3, 4)), (F(1, 10), F(1, 2)),
                                (F(1, 100000), F(1, 2))):
            with self.assertRaises(ValueError):
                accessible_main_enclosure((0, 1, -100, 400, -500, 200), theta, endpoint)


if __name__ == '__main__':
    unittest.main()
