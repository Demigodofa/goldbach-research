"""Signed-disk, inversion, endpoint and overlapping-energy guards."""
from fractions import Fraction as F
from math import ceil, floor, log
import unittest

from detector_power_length_filter import merged_power_intervals
from signed_zero_detector import (
    crude_residual_exponents, disk_consequences, finite_inverse,
    union_energy_bound,
)


class SignedZeroDetectorTests(unittest.TestCase):
    def test_common_disk_has_correct_sign_and_reciprocal_budget(self):
        self.assertEqual(disk_consequences(F(3,4)),
            {'real_upper':-F(1,4),'modulus_lower':F(1,4),
             'modulus_upper':F(7,4),'reciprocal_upper':F(4)})
        self.assertEqual(F(3,4)-F(2,3),F(1,12))
        with self.assertRaises(ValueError):
            disk_consequences(F(1))

    def test_complex_boundary_values_and_inverse_remainder(self):
        for unit in (1,-1,1j,-1j,complex(.6,.8)):
            h=-1+.75*unit
            self.assertLessEqual(h.real,-.25+1e-12)
            self.assertGreaterEqual(abs(h),.25-1e-12)
            for degree in (1,2,7,19):
                approx=finite_inverse(h,degree)
                self.assertLessEqual(abs(1/h-approx),4*.75**degree+1e-12)
                self.assertLess(abs(1-h*approx-(1+h)**degree),1e-12)

    def test_geometric_sign_and_identity_are_exact_for_rational_fixtures(self):
        for h in (-F(1,4),-F(1),-F(7,4),-F(5,8)):
            for degree in range(1,13):
                approx=finite_inverse(h,degree)
                self.assertEqual(1,h*approx+(1+h)**degree)
                self.assertEqual(1/h-approx,(1+h)**degree/h)
        self.assertEqual(finite_inverse(-F(1),9),-F(1))
        with self.assertRaises(ValueError):
            finite_inverse(-1,0)

    def test_dyadic_count_bound_pays_both_endpoints(self):
        # Count via logarithms; no enormous T or zero sample is constructed.
        for log_t in (100,200,1000,10000):
            lower=.01*log_t/log(2)
            upper=(.5*log_t+2*log(log_t))/log(2)
            count=floor(upper)-ceil(lower)+1
            bound=(.49*log_t+2*log(log_t))/log(2)+1
            self.assertLessEqual(count,bound)
            self.assertLess(bound,log_t)
        # Inclusive endpoints can add one block to the interval length.
        self.assertEqual(floor(20)-ceil(10)+1,11)

    def test_all_bad_gaps_end_below_the_common_support_majorant(self):
        intervals=merged_power_intervals()
        gaps=[(intervals[j][1],intervals[j+1][0]) for j in range(4)]
        self.assertEqual(max(right for left,right in gaps),F(41,100))
        self.assertTrue(all(left < right for left,right in gaps))
        self.assertLess(F(41,100),F(9,20))

    def test_overlap_is_an_inequality_and_copies_are_separate(self):
        energy={'copy1':F(1,7),'copy2':F(2,7),'copy3':F(3,7)}
        actual,majorant=union_energy_bound(energy,
            ({'copy1'},{'copy2','copy3'},{'copy3'}))
        self.assertEqual(actual,F(6,7))
        self.assertEqual(majorant,F(9,7))
        self.assertLess(actual,majorant)

    def test_logarithmic_degree_pays_the_crude_norm_not_just_scalar_error(self):
        budgets=crude_residual_exponents()
        self.assertEqual(budgets,{'energy':F(21,50),'norm':F(21,100)})
        for log_n in (10,100,1000):
            sigma=.02
            degree=ceil((float(budgets['norm']+F(1,50))*log_n
                         +2*log(log_n))/log(4/3))
            log_bound=degree*log(.75)+float(budgets['norm'])*log_n+log(log_n)
            self.assertLessEqual(log_bound,-sigma*log_n)


if __name__ == '__main__':
    unittest.main()
