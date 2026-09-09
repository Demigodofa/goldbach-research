"""Exact density and discrete-sampling guards, not computed zeta evidence."""
from fractions import Fraction as F
import unittest

from discrete_spectral_cancellation import (
    classical_density_coefficient, copy_occupancy_schur_probe,
    energy_relative_exponent, transfer_scale_powers,
)
from stationary_spectral_core import entropy_phase_hessian


class DiscreteSpectralCancellationTests(unittest.TestCase):
    def test_density_branches_match_and_pay_a_uniform_twelve_fifths(self):
        for j in range(101):
            sigma=F(1,2)+F(j,200)
            self.assertLessEqual(classical_density_coefficient(sigma),F(12,5))
        self.assertEqual(classical_density_coefficient(F(3,4)),F(12,5))
        self.assertEqual(classical_density_coefficient(F(1)),F(3,2))

    def test_energy_margin_is_linear_in_the_actual_zero_free_gap(self):
        for u in (F(0),F(1,1000),F(1,4),F(1,2)):
            self.assertEqual(energy_relative_exponent(u),-F(2,5)*u)
        self.assertEqual(energy_relative_exponent(F(1,10),F(5,6)),0)
        self.assertGreater(energy_relative_exponent(F(1,10),F(9,10)),0)

    def test_operator_and_stationary_powers_cancel_without_losing_occupancy(self):
        powers=transfer_scale_powers()
        self.assertEqual(powers['continuous_T']+powers['stationary_T'],powers['combined_T'])
        self.assertEqual(powers['occupancy_power'],1)
        self.assertEqual(powers['discrete_tail_T'],-3)

    def test_clustered_and_coincident_copies_obey_the_schur_count(self):
        for heights in ([F(0)]*9,
                        [F(0)]*3+[F(1,1000)]*2+[F(2),F(11,5),F(10)],
                        [F(j,3) for j in range(-20,21)]):
            probe=copy_occupancy_schur_probe(heights)
            self.assertLessEqual(probe['max_row_sum'],7*probe['copy_occupancy'])
        repeated=copy_occupancy_schur_probe([F(0)]*9)
        self.assertEqual(repeated['max_row_sum'],9)
        self.assertEqual(repeated['copy_occupancy'],9)
        self.assertGreater(repeated['max_row_sum'],7)  # Counting one distinct location would fail.

    def test_mixed_derivative_stays_usable_despite_rank_one_hessian(self):
        for x,y in ((F(1,2),F(3)),(F(1),F(2)),(F(3),F(3))):
            hess=entropy_phase_hessian(x,y)
            self.assertGreaterEqual(-hess['ge'],F(1,6))
            self.assertLessEqual(-hess['ge'],1)
            self.assertEqual(hess['gg']*hess['ee'],hess['ge']**2)

    def test_a_fixed_epsilon_loss_would_destroy_the_near_one_budget(self):
        # This exact exponent witness guards against replacing log powers by N^epsilon.
        u=F(1,10000)
        self.assertLess(energy_relative_exponent(u),0)
        self.assertGreater(energy_relative_exponent(u)+F(1,1000),0)


if __name__ == '__main__':
    unittest.main()
