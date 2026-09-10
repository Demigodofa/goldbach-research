"""Coefficient-moment, power-gap and actual-band normalization guards."""
from fractions import Fraction as F
from math import comb
import unittest

from detector_power_length_filter import (
    eligible_powers, merged_power_intervals, power_window_exponents,
    source_threshold_log_loss,
)


class DetectorPowerLengthTests(unittest.TestCase):
    def test_both_mean_value_terms_have_the_claimed_distinct_worst_corners(self):
        for i in range(25):
            beta=F(16,25)+F(i,200)
            for j in range(33):
                p=F(41,50)+F(j,200)
                e=power_window_exponents(beta,p)
                self.assertLessEqual(e['time'],-F(4,625))
                self.assertLessEqual(e['length'],-F(6,625))
        self.assertEqual(power_window_exponents(F(19,25),F(41,50))['time'],-F(4,625))
        self.assertEqual(power_window_exponents(F(19,25),F(49,50))['length'],-F(6,625))

    def test_gram_square_root_and_intersection_are_separate(self):
        energy=-F(4,625)
        self.assertEqual(1+energy/2,F(623,625))
        self.assertEqual(1+energy,F(621,625))
        self.assertGreater(1+energy/2,1+energy)
        self.assertGreater(1+energy/2,F(9,10))

    def test_divisor_square_majorant_on_prime_powers(self):
        for r in range(1,13):
            for e in range(31):
                self.assertLessEqual(comb(e+r-1,r-1)**2,comb(e+r*r-1,r*r-1))

    def test_finite_integer_power_coverage_leaves_four_actual_range_gaps(self):
        merged=merged_power_intervals()
        self.assertEqual(merged,((F(41,5000),F(49,300)),
            (F(41,250),F(49,250)),(F(41,200),F(49,200)),
            (F(41,150),F(49,150)),(F(41,100),F(49,100)),
            (F(41,50),F(49,50))))
        for left,right in zip(merged[:4],merged[1:5]):
            midpoint=(left[1]+right[0])/2
            self.assertEqual(eligible_powers(midpoint),())
            self.assertTrue(eligible_powers(left[1]))
            self.assertTrue(eligible_powers(right[0]))

    def test_critical_middle_length_is_not_saved_by_a_fractional_power(self):
        self.assertEqual(eligible_powers(F(7,20)),())
        self.assertEqual(eligible_powers(F(9,20)),(2,))
        self.assertTrue(eligible_powers(F(9,1000)))
        for j in range(10,161):
            self.assertTrue(eligible_powers(F(j,1000)))

    def test_any_good_detector_removes_even_if_first_detector_was_bad(self):
        detectors=(F(7,20),F(9,20))
        self.assertFalse(eligible_powers(detectors[0]))
        self.assertTrue(any(eligible_powers(m) for m in detectors))
        self.assertLess(F(41,5000),F(9,1000))
        self.assertLess(F(9,20),F(49,100))

    def test_powered_threshold_and_every_log_cost_fit_the_recorded_budget(self):
        for k in range(1,101):
            self.assertEqual(source_threshold_log_loss(k),2*k)
            count_log=4*k*k+5+source_threshold_log_loss(k)
            energy_log=count_log+1+1  # layer cake and dyadic length union.
            self.assertLessEqual(energy_log,40220)
        with self.assertRaises(ValueError):
            source_threshold_log_loss(101)
        with self.assertRaises(ValueError):
            power_window_exponents(F(19,25),F(1))


if __name__ == '__main__':
    unittest.main()
