"""Exact density, multiplicity and union-mask guards; not numerical zeros."""
from fractions import Fraction as F
import unittest

from zero_packet_realpart_localization import (
    deleted_realpart, gm_grid_budget, normalized_density_exponent,
    reflected_phase_derivatives,
)


class ZeroPacketRealpartTests(unittest.TestCase):
    def test_reflected_phase_has_the_required_dilation_derivative(self):
        for a in (F(1,4),F(1,3),F(1,2),F(2,3),F(3,4)):
            for t in (F(1),F(3,2),F(2)):
                d=reflected_phase_derivatives(a,t)
                self.assertEqual(d['dilation'],d['first']+a*d['second'])
                self.assertGreater(d['first'],1)
                self.assertGreater(d['dilation'],1)
                self.assertLessEqual(d['third'],256)

    def test_low_density_factorization_and_worst_endpoint(self):
        for j in range(141):
            u=F(9,25)+F(j,1000)
            power=normalized_density_exponent(u,'ingham')
            self.assertEqual(power,u*(F(7,10)-2*u)/(1+u))
            self.assertLessEqual(power,-F(9,1700))
        self.assertEqual(normalized_density_exponent(F(9,25),'ingham'),-F(9,1700))

    def test_gm_monotonicity_and_nonzero_source_loss(self):
        powers=[]
        for j in range(401):
            u=F(1,5)+F(j,10000)
            power=normalized_density_exponent(u,'gm')
            self.assertEqual(power,u*(10*u-F(5,2))/(8-5*u))
            self.assertGreater(108/(8-5*u)**2-2,0)
            self.assertLess(120/(8-5*u)**2,3)
            powers.append(power)
        self.assertEqual(max(powers),-F(3,850))
        b=gm_grid_budget()
        self.assertEqual(b['charged_max'],b['raw_max']+F(9,10)*(
            b['source_epsilon']+b['derivative_bound']*b['grid_mesh']))
        self.assertLess(b['charged_max'],b['claimed_max'])
        self.assertGreater(b['charged_max'],b['raw_max'])

    def test_huxley_keeps_a_gap_proportional_to_zero_free_distance(self):
        for j in range(201):
            u=F(j,1000)
            self.assertLessEqual(normalized_density_exponent(u,'huxley'),-u/14)
        self.assertEqual(normalized_density_exponent(F(1,5),'huxley'),-F(1,70))

    def test_unbuffered_transition_has_no_power_saving(self):
        self.assertEqual(normalized_density_exponent(F(7,20),'ingham'),0)
        # The selected GM expression vanishes at u=1/4, outside our paid range.
        u=F(1,4)
        self.assertEqual(F(9,10)*15*u/(8-5*u)-2*u,0)
        with self.assertRaises(ValueError):
            normalized_density_exponent(u,'gm')

    def test_union_requires_the_intersection_subtraction(self):
        betas=(F(1,2),F(7,10),F(4,5))
        mask=[deleted_realpart(b) for b in betas]
        values=((1+2j,2-3j,4+1j),(5-2j,6+7j,8-3j),(9+2j,1-4j,3+5j))
        full=sum(v for row in values for v in row)
        kept=sum(values[i][j] for i in range(3) for j in range(3)
                 if not mask[i] and not mask[j])
        row=sum(values[i][j] for i in range(3) for j in range(3) if mask[i])
        col=sum(values[i][j] for i in range(3) for j in range(3) if mask[j])
        intersection=sum(values[i][j] for i in range(3) for j in range(3)
                         if mask[i] and mask[j])
        self.assertEqual(full-kept,row+col-intersection)
        self.assertNotEqual(full-kept,row+col)

    def test_coincident_copies_require_the_occupancy_factor(self):
        # Three identical unit packets: Gram norm3, not1. No spacing assumption.
        coeffs=(1+2j,1+2j,1+2j)
        energy=sum(abs(c)**2 for c in coeffs)
        synthesis=abs(sum(coeffs))**2
        self.assertGreater(synthesis,energy)
        self.assertAlmostEqual(synthesis,3*energy)

    def test_direct_l1_cost_exceeds_the_projection_budget(self):
        lower=F(9,10)-F(1,2)
        upper=1-F(1,2)
        self.assertEqual(lower,F(2,5))
        self.assertGreater(lower,F(1,44))
        self.assertLess(lower,upper)
        self.assertTrue(deleted_realpart(F(16,25)))
        self.assertTrue(deleted_realpart(F(19,25)))
        self.assertFalse(deleted_realpart(F(7,10)))


if __name__ == '__main__':
    unittest.main()
