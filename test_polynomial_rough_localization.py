"""Retained small-prime factors, exact valuations and changed-coefficient guards."""
from fractions import Fraction as F
from math import gcd
import unittest

from polynomial_rough_localization import (
    affine_local_case, exact_prime_power_part, kernel_moment,
    localization_parameters, polynomial_factor_pattern, radical_weight,
)


class PolynomialRoughLocalizationTests(unittest.TestCase):
    def test_extract_entire_prime_power_before_dropping_coprimality(self):
        local = {3:F(1,10), 5:F(2,3), 7:F(3,2)}
        for n in (3*5*7, 3**4*5*7, 3**2*5**2):
            q, m = exact_prime_power_part(n, 3)
            self.assertEqual(q*m, n)
            self.assertEqual(gcd(3, m), 1)
            self.assertEqual(radical_weight(n, local), local[3]*radical_weight(m, local))
        n = 3**2*5
        # Extracting only one copy and then multiplying by a_p is FALSE.
        self.assertNotEqual(radical_weight(n, local), local[3]*radical_weight(n//3, local))

    def test_prime_power_leading_coefficient_does_not_change_local_cases(self):
        target = 22
        for coefficient in (3, 9, 81):
            for ell, expected_rho in ((2,1), (3,1), (5,2), (11,1)):
                for b in (F(0), F(1), F(3,2)):
                    a = F(2,3)
                    rho, factor = affine_local_case(ell,target,coefficient,a,b)
                    direct_roots = sum(m*(target-coefficient*m) % ell == 0 for m in range(ell))
                    self.assertEqual(rho, direct_roots)
                    self.assertEqual(rho, expected_rho)
                    # Positive local exponents select exactly the divisibility events.
                    event_mean = sum((a if m%ell==0 else 1)*(b if (target-coefficient*m)%ell==0 else 1)
                                     for m in range(ell) if m*(target-coefficient*m)%ell==0)/ell
                    self.assertEqual(factor, 1+event_mean)

    def test_third_kernel_moment_is_paid(self):
        self.assertEqual(kernel_moment(0), F(2,9))
        self.assertEqual(kernel_moment(2), F(200,7))
        self.assertEqual(kernel_moment(3), F(1000,3))
        with self.assertRaises(ValueError):
            kernel_moment(9)

    def test_uniform_tail_and_strict_factor_count(self):
        for kappa in (F(1,20), F(1,40), F(3,100)):
            data = localization_parameters(F(49,100), kappa)
            self.assertLessEqual(data['tail_exponent'], F(39,40))
            self.assertGreater(data['local_length_exponent'], F(1,4))
            self.assertGreater(data['cutoff_margin'],0)
            count = data['max_prime_factors']
            self.assertLess(count*kappa,1)
            self.assertGreaterEqual((count+1)*kappa,1)
        self.assertEqual(localization_parameters(F(49,100),F(1,20))['max_prime_factors'],19)

    def test_new_polynomial_coefficient_retains_new_composite_terms(self):
        gamma, degree, a = F(49,100), 9, F(1,5)
        value = polynomial_factor_pattern((a,1-a),gamma,degree)
        self.assertEqual(value,1-(1-a/gamma)**degree)
        self.assertGreater(value,0)
        # Old hard H has small part with one factor a<nu<gamma, so1-1=0.
        self.assertLess(a,F(47,150))
        self.assertNotEqual(value,1-1)
        self.assertEqual(polynomial_factor_pattern((F(1),),gamma,degree),1)
        self.assertEqual(polynomial_factor_pattern((F(1,2),F(1,2)),gamma,degree),1)


if __name__ == '__main__':
    unittest.main()
