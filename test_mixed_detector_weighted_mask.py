"""Exact mixed-length, Holder, assignment and weighted-kernel guards."""
from fractions import Fraction as F
import unittest

from detector_power_length_filter import eligible_powers, power_window_exponents
from mixed_detector_weighted_mask import (
    BAD_GAPS, covered_kernel_exponents, largest_good_slice_witness,
    least_covering_detector, mixed_log_budget, mixed_witnesses,
)


class MixedDetectorWeightedMaskTests(unittest.TestCase):
    def test_integer_witnesses_keep_actual_product_length_and_endpoints(self):
        cases=((F(9,20),F(1,5)),(F(9,20),F(7,20)),
               (F(11,25),F(19,50)),(F(11,25),F(27,100)),
               (F(9,1000),F(1,5)))
        for m,h in cases:
            brute=tuple((r,s) for r in range(1,100) for s in range(1,101-r)
                        if F(41,50) <= r*m+s*h <= F(49,50))
            self.assertEqual(mixed_witnesses(m,h),brute)
        self.assertIn((1,1),mixed_witnesses(F(11,25),F(19,50)))
        self.assertIn((1,2),mixed_witnesses(F(11,25),F(27,100)))

    def test_complete_largest_good_slice_matches_strip_enumeration(self):
        for m in (F(11,25),F(89,200),F(9,20)):
            self.assertIn(2,eligible_powers(m))
            values=[]
            for left,right in BAD_GAPS:
                values.extend(left+(right-left)*F(j,10) for j in range(1,10))
            for edge in ((F(49,50)-m)/2,F(41,50)-m):
                values.extend((edge-F(1,100000),edge,edge+F(1,100000)))
            for h in values:
                witness=largest_good_slice_witness(m,h)
                self.assertEqual(mixed_witnesses(m,h),() if witness is None else (witness,))

    def test_uncovered_rectangle_is_robust_and_stays_in_actual_domains(self):
        for m in (F(11,25),F(89,200),F(9,20)):
            for h in (F(17,50),F(7,20),F(9,25)):
                self.assertTrue(eligible_powers(m))
                self.assertFalse(eligible_powers(h))
                self.assertLessEqual(m+h,F(81,100))
                self.assertGreaterEqual(min(2*m+h,m+2*h),F(28,25))
                self.assertEqual(mixed_witnesses(m,h),())

    def test_any_good_detector_can_cover_even_if_least_good_one_cannot(self):
        first,later,h=F(8,25),F(11,25),F(39,100)
        self.assertTrue(eligible_powers(first))
        self.assertTrue(eligible_powers(later))
        self.assertEqual(mixed_witnesses(first,h),())
        self.assertTrue(mixed_witnesses(later,h))
        self.assertEqual(least_covering_detector((later,first,first),h),later)
        self.assertIsNone(least_covering_detector((F(9,20),),F(7,20)))

    def test_weighted_holder_uses_the_measure_once_not_its_sth_power(self):
        fixtures=(((F(1,7),F(2,7),F(4,7)),(F(1,3),F(2),F(7,5))),
                  ((F(0),F(0)),(F(2),F(3))),
                  ((F(1,11),F(0)),(F(5,2),F(9))))
        for weights,values in fixtures:
            for s in range(1,6):
                left=sum((w*x for w,x in zip(weights,values)),F(0))**s
                right=sum(weights,F(0))**(s-1)*sum((w*x**s for w,x in zip(weights,values)),F(0))
                self.assertLessEqual(left,right)

    def test_threshold_and_holder_logs_fit_one_uniform_fixed_budget(self):
        for k in range(2,101):
            for r in range(1,k):
                s=k-r
                budget=mixed_log_budget(r,s)
                self.assertEqual(budget['threshold'],2*r)
                self.assertLessEqual(budget['moment']+budget['threshold'],40204)
                self.assertLessEqual(budget['holder']+3,40230)
        self.assertEqual(mixed_log_budget(1,2)['threshold'],2)
        self.assertNotEqual(mixed_log_budget(1,2)['threshold'],6)

    def test_normalized_moment_and_weighted_actual_kernel_have_savings(self):
        for beta in (F(16,25),F(7,10),F(19,25)):
            for p in (F(41,50),F(9,10),F(49,50)):
                bounds=power_window_exponents(beta,p)
                self.assertLessEqual(bounds['time'],-F(4,625))
                self.assertLessEqual(bounds['length'],-F(6,625))
        self.assertEqual(covered_kernel_exponents(),
            {'energy':-F(4,625),'norm':-F(2,625),'central':F(623,625),
             'finite_period':F(2367,2500),'endpoint':-F(2133,2500)})
        self.assertLess(covered_kernel_exponents()['finite_period'],
                        covered_kernel_exponents()['central'])

    def test_fractional_powers_and_bad_gap_endpoints_are_not_silently_accepted(self):
        with self.assertRaises(ValueError):
            mixed_log_budget(F(1),2)
        with self.assertRaises(ValueError):
            mixed_log_budget(100,1)
        with self.assertRaises(ValueError):
            largest_good_slice_witness(F(9,20),F(41,100))


if __name__ == '__main__':
    unittest.main()
