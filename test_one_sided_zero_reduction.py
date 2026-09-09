"""Finite sign/algebra guards for the reviewed one-sided analytic reduction."""
from fractions import Fraction as F
import unittest

from one_sided_zero_reduction import (
    cross_log_saving, gamma_exponential_rate, radial_norm_power,
    reflected_square_terms,
)


class OneSidedZeroTests(unittest.TestCase):
    def test_damped_height_sign_reverses_on_the_other_half(self):
        for denominator in (4,20,200,2000):
            angle=F(1,2)-F(1,denominator)
            self.assertLessEqual(gamma_exponential_rate(-1,angle),-F(1,2))
            self.assertEqual(gamma_exponential_rate(1,angle),-F(1,denominator))
            self.assertEqual(gamma_exponential_rate(-1,angle),
                             gamma_exponential_rate(1,-angle))
        self.assertEqual(gamma_exponential_rate(-1,F(0)),-F(1,2))

    def test_radial_bound_keeps_off_line_zeros_and_avoids_half_line_singularity(self):
        for beta in (F(1,10),F(49,100),F(1,2),F(51,100),F(3,4)):
            self.assertEqual(radial_norm_power(beta),F(1,4))
        self.assertEqual(radial_norm_power(F(9,10)),F(2,5))
        self.assertEqual(radial_norm_power(F(999,1000)),F(499,1000))
        with self.assertRaises(ValueError):
            radial_norm_power(F(1))

    def test_two_half_integral_factor_and_ordered_cross_term(self):
        # These small Gaussian integers have exactly represented binary arithmetic.
        for p in (1+2j,-2+3j,3-1j):
            for q in (0j,1j,-1+2j):
                for phase in (1,1j,-1,-1j):
                    terms=reflected_square_terms(p,q,phase)
                    direct=phase*(p+q)**2+(phase*(p+q)**2).conjugate()
                    self.assertEqual(direct.imag,0)
                    self.assertEqual(direct.real,terms['full'])
                    self.assertEqual(terms['full'],terms['retained']+terms['discarded'])
        terms=reflected_square_terms(2,3,1)
        self.assertEqual(terms,{'full':50,'retained':8,'discarded':42})

    def test_retained_square_can_be_negative_even_with_zero_discarded_part(self):
        terms=reflected_square_terms(1j,0j,1)
        self.assertEqual(terms,{'full':-2,'retained':-2,'discarded':0})
        self.assertEqual(2*abs(1j)**2,2)

    def test_cross_budget_pays_the_total_norm_log_loss(self):
        self.assertEqual(cross_log_saving(F(1,4)),-F(1,4))
        for target in (1,3,10):
            self.assertEqual(cross_log_saving(F(target)+F(1,2)),target)
            self.assertGreater(cross_log_saving(F(target+1)),target)


if __name__ == '__main__':
    unittest.main()
