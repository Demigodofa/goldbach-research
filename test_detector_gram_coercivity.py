"""Gram failure, real interpolation and actual arithmetic overlap guards."""
import cmath
import math
from fractions import Fraction as F
import unittest

from detector_gram_coercivity import (
    evaluate_model, interpolate_real_block, model_parameters,
    overlap_exponents, proper_power_overlap_exponents, two_packet_budgets,
)
from detector_prime_product_transfer import (
    convolution_log_vector, truncated_mobius_coefficient,
)


def gram_form(c, d, r):
    """Direct independent complex matrix contraction for a tiny fixture."""
    return sum(c[i].conjugate()*(1 if i == j else r)*d[j]
               for i in range(2) for j in range(2))


class DetectorGramCoercivityTests(unittest.TestCase):
    def test_exact_positive_witness_inside_the_negative_disk(self):
        r = F(19, 20)
        budgets = two_packet_budgets(r)
        self.assertEqual(budgets['witness_norm'], F(7, 20))
        self.assertEqual(budgets['witness_mixed'], F(1, 8))
        c = [1+0j, -1+.5j]
        multipliers = [-1+.5j, -1-.5j]
        weighted = [a*b for a, b in zip(c, multipliers)]
        self.assertAlmostEqual(gram_form(c, c, float(r)).real, float(F(7, 20)))
        self.assertAlmostEqual(gram_form(c, weighted, float(r)).real, float(F(1, 8)))
        self.assertTrue(all(abs(1+h) < .75 and h.real < -.25 for h in multipliers))

    def test_pointwise_inverse_does_not_bound_synthesized_inverse(self):
        previous = F(0)
        for j in (2, 4, 8, 16):
            r = 1-F(1, 10**j)
            values = two_packet_budgets(r)
            ratio = values['inverse_input']/values['inverse_output']
            self.assertGreater(ratio, previous)
            self.assertGreater(values['inverse_input'], 1)
            previous = ratio
        h = [-1+.5j, -1-.5j]
        c = [h[1], -h[0]]
        dc = [h[j]*c[j] for j in range(2)]
        self.assertAlmostEqual(gram_form(c, c, .99).real, float(F(203, 200)))
        self.assertAlmostEqual(gram_form(dc, dc, .99).real, float(F(1, 32)))
        self.assertTrue(all(abs(1/value) < 1 for value in h))

    def test_support_exponent_is_strictly_inside_the_third_bad_gap(self):
        self.assertGreater(F(46, 181), F(49, 200))
        self.assertLess(F(47, 180), F(41, 150))
        # Alternating arctan series bounds, separate from math.atan display.
        lower = F(1, 2)-F(1, 24)+F(1, 160)-F(1, 896)
        upper = F(1, 2)-F(1, 24)+F(1, 160)
        self.assertGreater(lower, F(46, 100))
        self.assertLess(upper, F(47, 100))
        m = model_parameters()['m']
        self.assertGreater(m, float(F(46, 181)))
        self.assertLess(m, float(F(47, 180)))

    def test_real_common_polynomial_interpolates_and_varies_by_a_dilation(self):
        length, beta, gamma, target = 256, .7, 12.5, -1-.5j
        coefficients, receipt = interpolate_real_block(length, beta, gamma, target)
        self.assertLess(abs(receipt['kappa']), .1)
        self.assertTrue(all(type(b) is float and abs(b) <= 1 for b in coefficients.values()))
        self.assertTrue(all(length < n <= 2*length for n in coefficients))
        value = evaluate_model(coefficients, beta, gamma)
        self.assertLess(abs(value-target), 1e-12)
        delta = 1e-4
        shifted = evaluate_model(coefficients, beta, gamma+delta)
        approximation = cmath.exp(-1j*delta*math.log(length))*target
        rigorous_bound = abs(delta)*math.log(2)*sum(abs(b)*n**(-beta)
                                                  for n, b in coefficients.items())
        self.assertLessEqual(abs(shifted-approximation), rigorous_bound+1e-12)

    def test_actual_shaped_phase_has_a_positive_model_limit(self):
        params = model_parameters()
        h1 = -1-.5j
        h2 = h1*cmath.exp(-1j*params['m']*params['t'])
        self.assertLess(abs(h2-(-1+.5j)), 1e-14)
        phase = cmath.exp(1j*params['t'])
        field = 1+phase
        weighted = h1+h2*phase
        self.assertAlmostEqual(abs(field)**2, params['norm_limit'])
        self.assertAlmostEqual((weighted*field.conjugate()).real, params['mixed_limit'])
        self.assertGreater(params['mixed_limit'], 0)

    def test_prime_and_square_diagonals_really_vanish_but_cubes_need_payment(self):
        # Formal rational damping; factor locations only, not an actual zero run.
        cutoff = 5
        mask = {n: F(truncated_mobius_coefficient(n, cutoff), 2)
                for n in range(17, 33)}
        self.assertEqual(convolution_log_vector(101, mask), ())
        self.assertEqual(convolution_log_vector(101**2, mask), ())
        self.assertEqual(convolution_log_vector(31**3, mask), ((31, F(1, 2)),))
        for p in (2, 3, 5):
            self.assertTrue(all(truncated_mobius_coefficient(p**j, cutoff) == 0
                                for j in range(1, 6)))
        self.assertTrue(all(truncated_mobius_coefficient(31**j, cutoff) == 1
                            for j in range(1, 6)))

    def test_diagonal_and_schur_tail_pay_their_normalizations(self):
        budget = overlap_exponents(14)
        self.assertEqual(budget, {'window': F(1, 10), 'diagonal': -F(23, 30),
                                 'tail_log': -10, 'derivative_cost': F(369, 2500)})
        t = F(9, 10)
        self.assertEqual((2*t-1)+(1-2*t), 0)  # prefactor times tail Schur scale
        self.assertEqual(F(5, 2)+F(1, 2)+1-14, -10)
        self.assertEqual(int(F(1000, 9)), 111)

    def test_commutator_identity_and_invalid_inputs(self):
        r = .95
        gram = [[1, r], [r, 1]]
        h = [-1+.5j, -1-.5j]
        commutator = [[gram[i][j]*h[j]-h[i]*gram[i][j] for j in range(2)]
                      for i in range(2)]
        self.assertEqual(commutator[0][0], 0)
        self.assertEqual(commutator[0][1], gram[0][1]*(h[1]-h[0]))
        self.assertNotEqual(commutator[0][1], 0)
        for action in (lambda: two_packet_budgets(F(1)),
                       lambda: overlap_exponents(4),
                       lambda: interpolate_real_block(7, .7, 12.5, -1-.5j)):
            with self.assertRaises(ValueError):
                action()

    def test_proper_power_removal_keeps_divisor_and_square_root_costs(self):
        self.assertEqual(proper_power_overlap_exponents(),
                         {'product_energy': -F(59, 200), 'product_norm': -F(59, 400),
                          'opposite_norm': -F(1, 4),
                          'product_log_energy': 11, 'opposite_log_overlap': 4})
        for e in range(31):
            self.assertEqual((e+1)**2*(e+8)-(e+2)**3, 4*e*e+5*e)
            self.assertLessEqual((e+1)**3, math.comb(e+7, 7))
        # The opposite proper-power norm multiplies the retained full h norm.
        self.assertEqual(F(3, 2)+F(5, 2), 4)
        self.assertEqual(F(11, 2), F(proper_power_overlap_exponents()['product_log_energy'], 2))


if __name__ == '__main__':
    unittest.main()
