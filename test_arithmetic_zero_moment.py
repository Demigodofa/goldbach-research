"""Exact off-critical, cutoff and sampling guards; no computed zeros/primes."""
from fractions import Fraction as F
import unittest

from arithmetic_zero_moment import (
    analytic_real_imag_recombination, cutoff_error_powers, integer_window_weight,
    prime_sample_slope_bounds, scaled_complex_zero_argument,
)
from spectral_count_resonance_model import lattice_carrier_turns


class ArithmeticZeroMomentTests(unittest.TestCase):
    def test_off_critical_argument_retains_the_correct_imaginary_sign(self):
        right=scaled_complex_zero_argument(F(3,4),F(17),100)
        left=scaled_complex_zero_argument(F(1,4),F(-17),100)
        critical=scaled_complex_zero_argument(F(1,2),F(17),100)
        self.assertEqual(right,{'real':F(17,100),'imag':-F(1,400)})
        self.assertEqual(left,{'real':-F(17,100),'imag':F(1,400)})
        self.assertEqual(critical['imag'],0)

    def test_global_zero_weight_and_archimedean_tails_are_both_paid(self):
        powers=cutoff_error_powers()
        self.assertEqual(powers['complex_shift'],F(1,2))
        self.assertEqual(powers['whole_zero_tail'],-F(1,2))
        self.assertEqual(powers['archimedean_tail'],-1)
        insufficient=cutoff_error_powers(4)
        self.assertGreater(insufficient['whole_zero_tail'],F(1,2))

    def test_prime_samples_keep_uniform_spacing_across_the_frequency_interval(self):
        for x in (F(1,3),F(2,5),F(1,2),F(2,3)):
            bounds=prime_sample_slope_bounds(x)
            self.assertGreaterEqual(bounds['lower'],F(3,4))
            self.assertLessEqual(bounds['upper'],6)
        self.assertEqual(prime_sample_slope_bounds(F(1,2)),{'lower':F(1),'upper':F(4)})

    def test_integer_sampling_does_not_require_an_integral_center(self):
        for center in (F(0),F(1,2),F(1,1000),F(10,3),F(9999,2)):
            self.assertLessEqual(integer_window_weight(center),4)

    def test_smooth_prime_weights_avoid_a_window_length_loss(self):
        for radius in (1,10,100):
            self.assertLessEqual(integer_window_weight(F(1,2),radius),4)
        # A flat weight would instead count all2*radius+1 samples.
        self.assertGreater(2*100+1,4)

    def test_complex_linearity_preserves_the_analytic_test(self):
        for h,reflected in ((F(2),F(7)),(F(-3,2),F(1,4)),(F(0),F(5))):
            parts=analytic_real_imag_recombination(h,reflected)
            self.assertEqual(sum(parts.values()),h)

    def test_mock_single_and_pair_carriers_have_different_phases(self):
        for k in (0,1,101):
            single=F(k)+F(1,4)
            self.assertEqual(single-(single.numerator//single.denominator),F(1,4))
            pair=lattice_carrier_turns(k,k)
            self.assertEqual(pair-(pair.numerator//pair.denominator),F(1,2))


if __name__ == '__main__':
    unittest.main()
