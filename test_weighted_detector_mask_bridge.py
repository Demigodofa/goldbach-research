"""Real-part bins, moment switches, signed identity and kernel guards."""
from fractions import Fraction as F
import unittest

from mixed_detector_weighted_mask import BAD_GAPS
from weighted_detector_mask_bridge import (
    beta_bins, large_detector_holder_power, moment_power,
    multiplier_power, type_ii_holder_power, weighted_kernel_powers,
)


def bad_samples():
    values=[left+(right-left)*F(j,20) for left,right in BAD_GAPS for j in range(1,20)]
    values.extend((F(19,50)-F(1,100000),F(19,50),F(19,50)+F(1,100000)))
    return tuple(values)


class WeightedDetectorMaskBridgeTests(unittest.TestCase):
    def test_bins_cover_the_interval_and_charge_the_upper_weight(self):
        bins=beta_bins()
        self.assertEqual(len(bins),360)
        self.assertEqual(bins[0][0],F(16,25))
        self.assertEqual(bins[-1][1],F(19,25))
        for j,(lo,hi) in enumerate(bins):
            self.assertEqual(2*hi-2-(2*lo-2),F(1,1500))
            if j:
                self.assertEqual(bins[j-1][1],lo)
        self.assertEqual(-F(1,375)+F(1,1500),-F(1,500))

    def test_pure_moment_switch_retains_long_polynomial_cost(self):
        for h in bad_samples():
            s=multiplier_power(h)
            if s >= 3:
                self.assertGreater(s*h,F(49,50))
            else:
                self.assertLess(s*h,F(41,50))
                self.assertLess(s*h,F(9,10))
        self.assertGreater(moment_power(F(6,25),3*F(7,20)),0)
        self.assertEqual(moment_power(F(6,25),3*F(7,20)),F(3,125))

    def test_type_ii_holder_pays_every_bad_gap_with_bin_loss(self):
        for h in bad_samples():
            for u in (F(6,25),F(3,10),F(9,25)):
                raw=type_ii_holder_power(u,h)
                self.assertLessEqual(raw,-F(6,625))
                self.assertLessEqual(raw+F(1,1500),-F(1,125))
        self.assertEqual(type_ii_holder_power(F(6,25),F(19,50)),-F(6,625))
        self.assertEqual(-F(6,625)+F(1,1500),-F(67,7500))

    def test_initial_large_detector_component_is_preserved(self):
        for h in bad_samples():
            for m in (F(11,25),F(9,20)):
                for u in (F(6,25),F(9,25)):
                    self.assertLessEqual(large_detector_holder_power(m,u,h)
                                         +F(1,1500),-F(1,500))
        self.assertEqual(large_detector_holder_power(F(11,25),F(6,25),F(19,50)),
                         -F(1,375))

    def test_low_exterior_uses_actual_products_and_beta_zero_baseline(self):
        for h in bad_samples():
            k=multiplier_power(h,low_exterior=True)
            p=k*h
            self.assertLessEqual(F(49,75),p)
            self.assertLessEqual(p,F(41,50))
            for beta in (F(0),F(1,2),F(16,25)):
                self.assertLessEqual(moment_power(1-beta,p),-F(11,3750))
            self.assertLessEqual(4*k*k+6,70)
        self.assertLess(-F(9,1700),-F(11,3750))
        self.assertEqual(moment_power(F(9,25),F(49,75)),-F(11,3750))

    def test_good_moments_need_no_new_detection_threshold(self):
        eta=F(4,625)
        for k in range(1,101):
            moment_log=4*k*k+6
            holder_log=F(k-1,k)*40220+F(moment_log,k)
            self.assertLessEqual(holder_log,40220)
            self.assertEqual(F(k-1,k)*(-eta)+F(1,k)*(-eta),-eta)
        # H=-A-1+I, with |I|<1/3. The constant term must be paid.
        for a in (0,1,-2,1+2j):
            for integral in (0,.3,-.3,.3j):
                h=-a-1+integral
                self.assertLessEqual(abs(h)**2,2*abs(a)**2+F(9,2))
        self.assertNotEqual(-1,0)  # A=I=0 still leaves H=-1.

    def test_actual_kernel_powers_follow_each_weighted_energy(self):
        self.assertEqual(weighted_kernel_powers(F(1,125)),
            {'central':F(249,250),'finite_period':F(473,500),'endpoint':-F(427,500)})
        self.assertEqual(weighted_kernel_powers(F(4,625)),
            {'central':F(623,625),'finite_period':F(2367,2500),'endpoint':-F(2133,2500)})
        self.assertEqual(weighted_kernel_powers(F(11,3750)),
            {'central':F(7489,7500),'finite_period':F(3557,3750),'endpoint':-F(3193,3750)})
        self.assertLess(-F(59,200),-F(11,7500))

    def test_bad_gap_endpoints_and_invalid_bin_parameters_are_rejected(self):
        with self.assertRaises(ValueError):
            multiplier_power(F(41,100))
        with self.assertRaises(ValueError):
            type_ii_holder_power(F(1,5),F(7,20))
        with self.assertRaises(ValueError):
            weighted_kernel_powers(F(0))


if __name__ == '__main__':
    unittest.main()
