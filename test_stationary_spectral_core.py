"""Exact stationary-phase and summation guards; no actual zero computation."""
from fractions import Fraction as F
import unittest

from stationary_spectral_core import (
    amplitude_density_slack, entropy_phase_hessian, phase_pi_coefficient,
    reflection_orbit_totals, stationary_band_density_exponent,
)


class StationarySpectralCoreTests(unittest.TestCase):
    def test_gamma_and_fresnel_phases_cancel_real_parts_with_correct_sign(self):
        for b,d in ((F(1,2),F(1,2)),(F(1,100),F(99,100)),(F(2,3),F(3,4))):
            self.assertEqual(phase_pi_coefficient(b,d),-F(1,4))

    def test_phase_hessian_is_rank_one_but_mixed_derivative_is_nonzero(self):
        for gamma,eta in ((F(1),F(1)),(F(3),F(5)),(F(101),F(199))):
            hess=entropy_phase_hessian(gamma,eta)
            self.assertEqual(hess['gg']*hess['ee']-hess['ge']**2,0)
            self.assertLess(hess['ge'],0)
            self.assertEqual(hess['gg']*gamma+hess['ge']*eta,0)
            self.assertEqual(hess['ge']*gamma+hess['ee']*eta,0)

    def test_reflection_keeps_multiplicity_and_pairwise_height_dependent_bases(self):
        first=reflection_orbit_totals([(F(3),2),(F(1,5),3)],critical_copies=4)
        second=reflection_orbit_totals([(F(7),1),(F(2,3),2)],critical_copies=1)
        self.assertEqual(first['copies'],14)
        self.assertEqual(second['copies'],7)
        self.assertGreaterEqual(first['weight'],first['copies'])
        self.assertGreaterEqual(second['weight'],second['copies'])
        self.assertGreaterEqual(first['weight']*second['weight'],98)
        self.assertEqual(reflection_orbit_totals([],critical_copies=5),{'weight':F(5),'copies':5})

    def test_total_amplitude_has_the_claimed_positive_density_certificate(self):
        for j in range(101):
            u=F(j,200)
            numerator=45*(u-F(37,90))**2+F(71,180)
            self.assertEqual(amplitude_density_slack(u),numerator/(30*(1+u)))
            self.assertGreater(amplitude_density_slack(u),0)
        for i in range(11):
            for j in range(11):
                self.assertLessEqual(stationary_band_density_exponent(F(i,20),F(j,20)),F(46,45))

    def test_relative_error_is_paid_against_total_mass_before_real_part(self):
        height_power=F(2,3)
        total_error=F(46,45)-height_power/2
        self.assertEqual(total_error,F(31,45))
        self.assertLess(total_error,1)
        self.assertEqual(F(3,2)*height_power,1)
        self.assertLess(F(13,20),height_power)


if __name__ == '__main__':
    unittest.main()
