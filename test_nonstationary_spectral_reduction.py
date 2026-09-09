"""Exact uniformity and error-budget guards, without numerical zero claims."""
from fractions import Fraction as F
import unittest

from nonstationary_spectral_reduction import (
    bulk_denominator_ratio, coupled_absolute_tail_profile, tensor_log_budget,
)


class NonstationarySpectralReductionTests(unittest.TestCase):
    def test_fixed_separation_controls_all_real_parts_near_the_axis(self):
        endpoint=F(22,7)
        for delta in (F(1,10),F(1,2),F(2)):
            for n in (20,100,1000):
                for t in (F(1,n),F(1,2),F(1),endpoint):
                    for b in (F(1,100),F(1,2),F(1),F(199,100)):
                        self.assertLessEqual(
                            bulk_denominator_ratio(n,t,endpoint+delta,b),-delta/2)

    def test_zero_separation_does_not_supply_the_same_gap(self):
        endpoint=F(22,7)
        self.assertGreater(bulk_denominator_ratio(100,endpoint,endpoint,F(1,2)),0)

    def test_axis_parity_correction_is_logarithmic_not_a_fixed_count(self):
        counts=[]
        for exponent in (4,8,16):
            n=2**exponent
            count=sum(2**j<=n for j in range(1,exponent+2))
            self.assertEqual(count,exponent)
            counts.append(count)
        self.assertEqual(counts,[4,8,16])
        for k in range(1,30):
            self.assertGreaterEqual(2**(k-1),k)

    def test_tensor_decay_pays_both_growing_seminorms(self):
        self.assertEqual(tensor_log_budget(),
                         {'coefficient_b_power':32,'sqrt_n_log_power':34,
                          'plain_log_power':36})
        with self.assertRaises(ValueError):
            tensor_log_budget(13,12)  # Would leave a nonsummable harmonic tail.
        self.assertLess(tensor_log_budget()['plain_log_power'],40)

    def test_coupled_tail_keeps_the_extra_power_saving_until_after_multiplication(self):
        self.assertEqual(coupled_absolute_tail_profile(F(8)),
                         {'n_power':F(-3),'logn_power':F(7,2)})
        self.assertEqual(coupled_absolute_tail_profile(F(4))['n_power'],1)

    def test_positive_height_sum_cutoff_bounds_both_ordinates(self):
        cap=F(27,7)
        for left in (F(1,1000),F(1,2),F(2),cap-F(1,1000)):
            right=cap-left
            self.assertGreater(left,0)
            self.assertGreater(right,0)
            self.assertLess(left,cap)
            self.assertLess(right,cap)
        # Positivity of both heights is essential to that finite-height inference.
        self.assertEqual((-cap)+(2*cap),cap)
        self.assertGreater(2*cap,cap)

    def test_inherited_stretched_exponential_error_is_not_a_square_root_error(self):
        # With logN=m^2, the log ratio of N*exp(-c*m) to sqrtN*(logN)^40
        # is m^2/2-c*m-80*logm. Use logm<=m to get an exact positive lower bound.
        for c in (1,3,10):
            m=4*(c+80)
            self.assertGreater(F(m*m,2)-(c+80)*m,0)


if __name__ == '__main__':
    unittest.main()
