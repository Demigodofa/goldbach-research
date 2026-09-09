"""Exact shift and exponent guards, plus diagnostic phase identities."""
from cmath import exp
from fractions import Fraction as F
from math import cos, sin
import unittest

from varying_prime_phase import shift_budget, shift_energy_rhs, telescoping_phase_sum


class VaryingPrimePhaseTests(unittest.TestCase):
    def test_shift_inequality_keeps_diagonal_and_triangular_weights(self):
        fixtures = ((F(1),), (F(1),F(-1)), (F(1),F(2),F(3)),
                    (F(1,2),F(-2,3),F(0),F(4,5),F(-1)))
        for values in fixtures:
            for shifts in (1,2,3,7):
                self.assertGreaterEqual(shift_energy_rhs(values,shifts),sum(values)**2)
            self.assertEqual(shift_energy_rhs(values,1),len(values)*sum(z*z for z in values))

    def test_exact_shift_average_cauchy_matches_the_expanded_rhs(self):
        values, shifts = (F(2),F(-3,2),F(1,4),F(5)),3
        def value(k):
            return values[k] if 0 <= k < len(values) else F(0)
        averages = [sum((value(j+r) for r in range(shifts)),F(0))
                    for j in range(1-shifts,len(values))]
        self.assertEqual(sum(averages),shifts*sum(values))
        expanded = F(len(values)+shifts-1,shifts**2)*sum(a*a for a in averages)
        self.assertEqual(expanded,shift_energy_rhs(values,shifts))

    def test_discrete_summation_by_parts_keeps_the_last_endpoint(self):
        # Positive derivatives need not be monotone in this fixture.
        phases = [0.07*n+0.01*sin(n) for n in range(21)]
        values = [exp(1j*x) for x in phases]
        amplitudes = [1+0.02j*n for n in range(21)]
        direct = sum(a*z for a,z in zip(amplitudes,values))
        self.assertAlmostEqual(abs(telescoping_phase_sum(values,amplitudes)-direct),0,places=12)
        self.assertEqual(telescoping_phase_sum([1j],[2]),2j)

    def test_derivative_ranges_are_nonresonant_and_logs_have_a_strict_margin(self):
        b = shift_budget()
        self.assertEqual(b['type_i_derivative'],-F(1,110))
        self.assertEqual(b['type_ii_derivative'],-F(3,55))
        self.assertEqual(b['type_i_sum'],F(1,10))
        self.assertEqual(b['type_ii_diagonal'],F(43,44))
        self.assertEqual(b['type_ii_off_diagonal'],F(171,220))
        self.assertEqual(b['spare'],F(3,1100))
        self.assertLess(b['type_ii_off_diagonal'],b['type_ii_diagonal'])

    def test_varying_sine_family_includes_affine_phases_with_uniform_bounds(self):
        for slope in (2.5,3.0,3.5):
            for epsilon in (0,0.01,0.5,1):
                for j in range(21):
                    u = 0.25+j/40
                    first = slope+epsilon*(cos(u-0.5)-1)
                    second = -epsilon*sin(u-0.5)
                    self.assertGreaterEqual(first,79/32-1e-14)
                    self.assertGreaterEqual(first+u*second,73/32-1e-14)
        self.assertEqual(3+0*cos(0.1),3)

    def test_log_phase_fails_the_actual_first_dilation_condition(self):
        for u in (F(1,4),F(1,2),F(3,4)):
            first,second = 1/u,-1/(u*u)
            self.assertNotEqual(first,0)
            self.assertEqual(first+u*second,0)

    def test_invalid_or_resonant_fixture_inputs_are_rejected(self):
        for values,shifts in (((),2),((F(1),),0),((1,),2)):
            with self.assertRaises(ValueError):
                shift_energy_rhs(values,shifts)
        with self.assertRaises(ValueError):
            telescoping_phase_sum([1,1],[1,1])


if __name__ == '__main__':
    unittest.main()
