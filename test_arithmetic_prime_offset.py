"""Exact offset orientation, normalization-budget and sign-certificate guards."""
from fractions import Fraction as F
import unittest

from arithmetic_prime_offset import (
    balanced_phase_interval, certifies_negative_cosine_interval,
    product_error_exponents, ratio_replacement, window_arguments,
)


class ArithmeticPrimeOffsetTests(unittest.TestCase):
    def test_two_local_windows_have_the_required_opposite_orientations(self):
        for a in (F(1,3),F(1,2),F(2,3)):
            first,second=window_arguments(a,F(0),F(100))
            self.assertEqual(first,0)
            self.assertGreater(second,0)
            first,second=window_arguments(a,F(-100),F(100))
            self.assertGreater(first,0)
            self.assertEqual(second,0)

    def test_ratio_change_matches_direct_subtraction_for_both_offset_signs(self):
        for n,m,scale in ((47,53,100),(47,55,100),(47,51,100),(2,3,101)):
            values=ratio_replacement(n,m,scale)
            self.assertEqual(values['symmetric']-values['old'],values['difference'])
            swapped=ratio_replacement(m,n,scale)
            self.assertEqual(values['symmetric']+swapped['symmetric'],1)

    def test_the_sharpened_replacement_is_needed_for_a_sublinear_error(self):
        current=product_error_exponents()
        self.assertEqual(current['cross_N'],F(1,2))
        self.assertEqual(current['cross_log'],F(13,2))
        self.assertEqual(current['square_N'],0)
        self.assertEqual(current['square_log'],12)
        old=product_error_exponents(F(1,2),F(1))
        self.assertEqual(old['cross_N'],1)
        self.assertEqual(old['square_N'],1)

    def test_a_nonnegative_smooth_weight_has_a_certified_negative_even_offset(self):
        c=F(1,100)
        lower=7*c/5
        upper=8*c/5
        self.assertGreater(lower,c)
        self.assertLess(upper,2*c)
        offset=100
        self.assertEqual(offset%2,0)
        phase=balanced_phase_interval(lower,upper,offset)
        self.assertEqual(phase,(F(14,5),F(16,5)))
        self.assertTrue(certifies_negative_cosine_interval(*phase))

    def test_the_cosine_certificate_does_not_accept_a_positive_or_crossing_interval(self):
        self.assertFalse(certifies_negative_cosine_interval(F(1,10),F(1,5)))
        self.assertFalse(certifies_negative_cosine_interval(F(0),F(5)))


if __name__ == '__main__':
    unittest.main()
