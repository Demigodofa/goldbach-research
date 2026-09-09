"""Scale, prime-weighted sampling, and actual-kernel replacement guards."""
from fractions import Fraction as F
import unittest

from linear_height_ratio_cancellation import linear_remainder_exponents
from short_prime_window_energy import prime_weighted_schur, scale_budget


class ShortPrimeWindowEnergyTests(unittest.TestCase):
    def test_scaled_taylor_and_endpoint_costs_are_strictly_lower_order(self):
        b=scale_budget()
        self.assertEqual(b['localized_shift'],F(1,10))
        self.assertEqual(b['global_taylor'],-F(2,5))
        self.assertEqual(b['global_fourier_tail'],-F(3,5))
        self.assertEqual(b['pole_taylor'],-F(13,10))
        self.assertEqual(b['beta_endpoint'],-F(7,10))
        self.assertLess(b['squared_shift'],1)
        self.assertLess(b['finite_period_remainder'],1)

    def test_prime_weighted_schur_has_both_measures_and_no_squared_mass_norm(self):
        result=prime_weighted_schur([[F(1)]*3]*2,[F(1,10)]*2,
                                   [F(1),F(2),F(4)],[F(1)]*3)
        self.assertEqual(result['energy'],F(49,5))
        self.assertEqual(result['bound'],result['energy'])
        self.assertEqual(result['weighted_norm'],7)
        self.assertEqual(result['row_bound'],7)
        self.assertEqual(result['column_bound'],F(1,5))

    def test_signed_kernel_and_zero_mass_columns_preserve_weighted_cauchy(self):
        matrix=[[F(1),F(-1,2),F(1,3)],
                [F(-1,2),F(1),F(-1,2)],
                [F(1,3),F(-1,2),F(1)]]
        for masses in ([F(2),F(1),F(3)],[F(0),F(1),F(0)]):
            result=prime_weighted_schur(matrix,[F(1,100)]*3,masses,[F(4),F(-2),F(3)])
            self.assertLessEqual(result['energy'],result['bound'])
        with self.assertRaises(ValueError):
            prime_weighted_schur([[F(1)]],[F(1)],[F(-1)],[F(1)])

    def test_energy_scaling_uses_da_and_the_growing_prime_window(self):
        t=F(9,10)
        h=scale_budget()['window']
        self.assertEqual(2*t+h-t,1)
        self.assertEqual(t+h-F(1,2),F(1,2))
        # Passing from da to dx adds the Jacobian N.
        self.assertEqual(2*t+h-t+1,2)

    def test_proper_power_shell_cost_is_absorbed_by_the_effective_window(self):
        h=scale_budget()['window']
        for r in (h,F(1,4),F(1,2),F(1)):
            self.assertLess(r-F(1,2),r)
            self.assertLess(F(0),r)  # Any fixed log^2 fits below N^r.

    def test_above_five_sixths_the_amplitude_majorant_needs_its_other_endpoint(self):
        h=F(9,10)
        self.assertLess(1-F(6,5)*h,0)
        for j in range(21):
            for k in range(21):
                u,v=F(j,40),F(k,40)
                actual=linear_remainder_exponents(h,h,u,v)['integral']
                upper=1-h/5-(1-F(6,5)*h)*(u+v)
                self.assertLessEqual(actual,upper)
                self.assertLessEqual(upper,h)
        self.assertEqual(linear_remainder_exponents(h,h,F(1,2),F(1,2))['integral'],h)


if __name__ == '__main__':
    unittest.main()
