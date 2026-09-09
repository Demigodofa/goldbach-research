"""Exact displacement and Schur-budget guards; no computed primes or zeros."""
from fractions import Fraction as F
import unittest

from arithmetic_zero_energy import first_weight_power, finite_schur_energy, localized_taylor_powers


class ArithmeticZeroEnergyTests(unittest.TestCase):
    def test_density_weight_has_the_factored_slack_in_the_correct_variable(self):
        for j in range(101):
            u=F(j,200)
            slack=(F(1,2)-u)*(1-u)/(1+u)
            self.assertEqual(1-first_weight_power(u),slack)
            self.assertGreaterEqual(slack,0)
        self.assertEqual(first_weight_power(F(1,2)),1)
        self.assertEqual(first_weight_power(F(0)),F(1,2))

    def test_unlocalized_first_order_error_does_not_pay_the_energy_budget(self):
        current=localized_taylor_powers()
        self.assertEqual(current['localized_first_term'],0)
        self.assertEqual(current['global_remainder'],-F(1,2))
        self.assertEqual(current['global_cutoff_tail'],-F(1,2))
        self.assertEqual(current['pole_remainder'],-F(3,2))
        old=localized_taylor_powers(remainder_order=1)
        self.assertEqual(2*old['global_remainder'],1)
        # Its retained log^2 factor is worse than the target N logN.
        self.assertLess(2*current['global_remainder'],2*old['global_remainder'])

    def test_coherent_matrix_attains_schur_bound_and_needs_both_factors(self):
        result=finite_schur_energy([[F(1)]*3]*2,[F(1,10)]*2,[F(1)]*3)
        self.assertEqual(result['energy'],F(9,5))
        self.assertEqual(result['energy'],result['bound'])
        self.assertEqual(result['row_bound'],3)
        self.assertEqual(result['column_bound'],F(1,5))

    def test_sign_changing_kernel_and_coefficients_still_obey_absolute_schur(self):
        matrix=[[F(1),F(-1,2),F(1,3)],
                [F(-1,2),F(1),F(-1,2)],
                [F(1,3),F(-1,2),F(1)]]
        for coefficients in ([F(1),F(-2),F(3)],[F(3),F(3),F(3)],[F(0),F(1),F(0)]):
            result=finite_schur_energy(matrix,[F(1,100)]*3,coefficients)
            self.assertLessEqual(result['energy'],result['bound'])

    def test_da_and_dx_measures_differ_by_the_scale(self):
        matrix=[[F(1),F(1,2)],[F(1,3),F(1)]]
        coefficients=[F(1),F(-3)]
        a=finite_schur_energy(matrix,[F(1,100)]*2,coefficients)
        x=finite_schur_energy(matrix,[F(1)]*2,coefficients)
        self.assertEqual(x['energy'],100*a['energy'])
        self.assertEqual(x['bound'],100*a['bound'])

    def test_a_flat_growing_window_cannot_claim_uniform_row_summability(self):
        small=finite_schur_energy([[F(1)]*2]*2,[F(1,100)]*2,[F(1)]*2)
        large=finite_schur_energy([[F(1)]*20]*20,[F(1,100)]*20,[F(1)]*20)
        self.assertEqual(large['row_bound'],10*small['row_bound'])
        self.assertEqual(large['column_bound'],10*small['column_bound'])
        self.assertEqual(large['bound'],1000*small['bound'])


if __name__ == '__main__':
    unittest.main()
