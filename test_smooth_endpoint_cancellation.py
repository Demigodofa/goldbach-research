"""Exact finite guards for the independently reviewed parity cancellation."""
from fractions import Fraction as F
import unittest

from smooth_endpoint_cancellation import endpoint_coefficients, prime_parity_components


class SmoothEndpointCancellationTests(unittest.TestCase):
    def test_parity_correction_retains_all_even_prime_powers(self):
        coefficients={2:F(3),4:F(3),8:F(3),16:F(3),3:F(5),9:F(5),
                      27:F(5),5:F(7),25:F(7),7:F(11)}
        weights={n:F(n*n+1,11) for n in coefficients}
        total,alternating,correction=prime_parity_components(coefficients,weights)
        self.assertEqual(alternating,total-correction)
        self.assertEqual(correction,6*sum(weights[n] for n in (2,4,8,16)))
        # Generic even coefficients would not obey the prime-power identity.
        coefficients[6]=F(1)
        weights[6]=F(2)
        total,alternating,correction=prime_parity_components(coefficients,weights)
        self.assertEqual(alternating-(total-correction),-4)

    def test_endpoint_second_term_has_the_integrated_sign(self):
        result=endpoint_coefficients(F(6),F(1),F(1))
        self.assertEqual(result,{'leading_imaginary':F(1,5),
                                 'secondary_real':F(31,125)})

    def test_real_parts_enter_only_linearly_in_the_second_term(self):
        k,p=F(52),F(3)
        first=endpoint_coefficients(k,F(1,2),p)
        second=endpoint_coefficients(k,F(3,2),p)
        self.assertEqual(first['leading_imaginary'],second['leading_imaginary'])
        self.assertEqual(second['secondary_real']-first['secondary_real'],
                         -1/(p*(1-k/p)**2))

    def test_leading_real_main_cancels_without_replacing_a_square_by_a_norm(self):
        for real_main in (-17,-3,0,5,23):
            for error in (1+2j,-2+3j,4-1j):
                pair_sum=real_main+error
                self.assertEqual((-1j*pair_sum).real,error.imag)
                self.assertNotEqual(abs(pair_sum),(-1j*pair_sum).real)

    def test_tensor_real_main_requires_the_complete_complex_factors(self):
        masses=[2,3,5]
        u=[1+2j,3-1j,-2+1j]
        v=[2-1j,-1+3j,4+2j]
        left=sum(m*z for m,z in zip(masses,u))
        right=sum(m*z for m,z in zip(masses,v))
        main=sum(masses[j]*masses[k]*(u[j]*v[k]).real
                 for j in range(3) for k in range(3))
        self.assertEqual(main,(left*right).real)
        self.assertNotEqual(main,left.real*right.real)

    def test_linear_then_tensor_budget_pays_the_real_sum_before_squaring(self):
        for root_n in (10,100,1000):
            n=root_n**2
            log_proxy=F(3)
            error=root_n*log_proxy
            structured=((n+error)**2-n*n)/n
            self.assertEqual(structured,2*error+error**2/n)
            absolute_mass=root_n**3*log_proxy
            direct_pair_replacement=absolute_mass**2/n**2
            self.assertEqual(direct_pair_replacement,n*log_proxy**2)
            self.assertGreater(direct_pair_replacement,structured)


if __name__ == '__main__':
    unittest.main()
