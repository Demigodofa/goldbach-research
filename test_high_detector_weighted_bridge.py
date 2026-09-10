"""Exact guards for source losses, actual lengths and the near-one cap."""
from fractions import Fraction as F
import unittest

from mixed_detector_weighted_mask import BAD_GAPS
from high_detector_weighted_bridge import (
    bad_holder, bad_power, density_energy, fixed_beta_bins,
    good_holder, relative_u_bins,
)
from weighted_detector_mask_bridge import moment_power


def bad_samples():
    values = [lo+(hi-lo)*F(j, 16) for lo, hi in BAD_GAPS for j in range(1, 16)]
    values.extend((F(39, 100)-F(1, 100000), F(39, 100),
                   F(39, 100)+F(1, 100000), F(2, 5)))
    return values


class HighDetectorWeightedBridgeTests(unittest.TestCase):
    def test_stronger_density_repairs_the_zero_saving_corner(self):
        u, h = F(1, 6), F(2, 5)
        self.assertEqual(density_energy(u, 'huxley'), -F(1, 30))
        self.assertEqual(density_energy(u, 'ivic'), -F(19, 300))
        for s, new_bound in ((2, -F(3, 200)), (3, -F(1, 50))):
            moment = moment_power(u, s*h)
            self.assertEqual(F(s-1, s)*density_energy(u, 'huxley')+moment/s, 0)
            self.assertEqual(F(s-1, s)*density_energy(u, 'ivic')+moment/s, new_bound)

    def test_lower_high_type_ii_needs_the_new_switch(self):
        for h in bad_samples():
            for u in (F(1, 5), F(11, 50), F(6, 25)):
                self.assertLessEqual(bad_holder(u, h, 'type_ii'), -F(1, 250))
        self.assertEqual(bad_holder(F(1, 5), F(39, 100), 'type_ii'), -F(1, 250))
        # Reusing the earlier .38 switch here would leave a POSITIVE cost.
        u, h = F(1, 5), F(19, 50)
        self.assertEqual((-u/5+moment_power(u, 2*h))/2, F(1, 500))

    def test_good_moments_pay_full_lower_high_strip_without_detection(self):
        for u in (F(1, 5), F(21, 100), F(11, 50), F(23, 100), F(6, 25)):
            for p in (F(41, 50), F(17, 20), F(9, 10), F(49, 50)):
                for k in (2, 3, 7, 100):
                    self.assertLessEqual(good_holder(u, p, k), -F(11, 3500))
        self.assertEqual(good_holder(F(1, 5), F(41, 50), 2), -F(11, 3500))
        self.assertEqual(good_holder(F(6, 25), F(41, 50), 2), -F(211, 42500))
        self.assertLess(-F(11, 3500)+F(29, 100000), -F(1, 400))

    def test_compact_grids_charge_both_weight_and_source_epsilon(self):
        for left, right, count in ((F(19, 25), F(4, 5), 400),
                                   (F(4, 5), F(7, 8), 750)):
            bins = fixed_beta_bins(left, right)
            self.assertEqual(len(bins), count)
            self.assertEqual((bins[0][0], bins[-1][1]), (left, right))
            self.assertTrue(all(hi-lo == F(1, 10000) for lo, hi in bins))
            self.assertTrue(all(bins[j-1][1] == bins[j][0] for j in range(1, count)))
        loss = 2*F(1, 10000)+F(9, 10)*F(1, 10000)
        self.assertEqual(loss, F(29, 100000))
        self.assertLess(-F(11, 1600)+loss, -F(1, 200))
        self.assertLess(-F(1, 250)+F(1, 5000), -F(1, 400))

    def test_upper_high_powers_keep_the_long_length_cost(self):
        for h in bad_samples():
            s = bad_power(h)
            self.assertGreater(s*h, F(9, 10))
            coefficient = F(s-1, s)*(-F(5, 16))+2*h-F(2, s)
            self.assertLessEqual(coefficient, -F(11, 200))
            for u in (F(1, 8), F(1, 6), F(1, 5)):
                self.assertLessEqual(bad_holder(u, h, 'ivic'), -F(11, 200)*u)
        self.assertGreater(moment_power(F(1, 6), 3*F(2, 5)), 0)

    def test_near_one_relative_bins_and_last_truncated_bin(self):
        delta = F(1, 1000)
        bins = relative_u_bins(delta)
        self.assertEqual(bins[0][1], F(1, 8))
        self.assertLess(bins[-1][0], delta)
        self.assertGreaterEqual(bins[-1][1], delta)
        for j, (lo, hi) in enumerate(bins):
            self.assertEqual(lo, F(99, 100)*hi)
            if j:
                self.assertEqual(bins[j-1][0], hi)
            exponent = -F(47, 650)*hi+2*(hi-lo)
            self.assertEqual(exponent, -F(17, 325)*hi)
            self.assertLess(exponent, -hi/20)
            self.assertLessEqual(exponent, -delta/20)
        for h in bad_samples():
            for u in (F(1, 8), F(1, 100), F(1, 1000000)):
                self.assertLessEqual(bad_holder(u, h, 'huxley'), -F(47, 650)*u)

    def test_extended_gamma_interval_stays_away_from_a_pole(self):
        for beta in (F(19, 25), F(39, 50), F(4, 5)):
            delta = beta-F(1, 2)
            self.assertGreaterEqual(delta, F(13, 50))
            self.assertLessEqual(delta, F(3, 10))
            self.assertGreater(1-delta, 0)
            self.assertLess(F(1, 2)-beta, 0)
        self.assertLess(F(3831, 4791), F(4, 5))

    def test_invalid_sources_and_unlicensed_powers_are_rejected(self):
        for action in (lambda: density_energy(F(1, 100), 'ivic'),
                       lambda: good_holder(F(1, 5), F(41, 50), 1),
                       lambda: bad_power(F(41, 100)),
                       lambda: relative_u_bins(F(0))):
            with self.assertRaises(ValueError):
                action()


if __name__ == '__main__':
    unittest.main()
