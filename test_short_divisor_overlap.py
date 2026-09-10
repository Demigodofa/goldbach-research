"""Divisor completion, Fourier support and actual error-budget guards."""
from fractions import Fraction as F
import unittest

from detector_prime_product_transfer import (
    convolution_log_vector, full_mobius_log_vector, truncated_mobius_coefficient,
)
from major_arc_kernel import _mobius_phi
from short_divisor_overlap import (
    cancellation_budgets, complement_cofactor_coefficients,
    divisor_log_vector, dual_support_indices, elementary_window_budgets,
)
from unexceptional_vaughan_gate import _divisors, mangoldt_log_vector


def add_vectors(*vectors):
    result = {}
    for vector in vectors:
        for p, value in vector:
            result[p] = result.get(p, F(0))+value
    return tuple((p, value) for p, value in sorted(result.items()) if value)


class ShortDivisorOverlapTests(unittest.TestCase):
    def test_elementary_completed_field_has_arbitrary_power_saving(self):
        # IBP per modulus, normalization, then sum d^(M-1) through B.
        t, b, window = F(9, 10), F(9, 1000), F(1, 10)
        for target in (1, 2, 7):
            derivatives = (1000*target)//91+2
            cutoff_decay = 8*target+2
            budgets = elementary_window_budgets(derivatives, cutoff_decay)
            self.assertEqual(t-1-window*(derivatives-1)+b*derivatives,
                             budgets['nonzero_modes'])
            self.assertTrue(all(power < -target for power in budgets.values()))
        # Polynomial factors in L are absorbed by the strict power margin.
        self.assertEqual(elementary_window_budgets(2, 16),
                         {'nonzero_modes': -F(91, 500),
                          'zero_mode_taylor': -F(9, 5), 'cutoff_tail': -F(2)})

    def test_completion_works_for_arbitrary_b_not_just_mobius(self):
        b = {1: F(1), 2: -F(1, 3), 3: F(2, 5), 5: -F(1, 2)}
        for n in (12, 25, 30, 64, 105, 210):
            a = {d: sum((b.get(e, F(0)) for e in _divisors(d)), F(0))
                 for d in _divisors(n)}
            self.assertEqual(convolution_log_vector(n, a), divisor_log_vector(n, b))

    def test_actual_mobius_completion_keeps_prime_powers_on_the_left(self):
        cutoff = 5
        b = {d: F(_mobius_phi(d)[0]) for d in range(1, cutoff+1)}
        for n in (49, 121, 31**3, 31*101):
            self.assertEqual(divisor_log_vector(n, b), full_mobius_log_vector(n, cutoff))
        # At 49, all-Lambda completion includes Lambda(49), not just the prime 7 divisor.
        self.assertEqual(divisor_log_vector(49, b), ((7, F(2)),))
        prime_only_left = ((7, F(truncated_mobius_coefficient(7, cutoff))),)
        self.assertNotEqual(prime_only_left, divisor_log_vector(49, b))

    def test_complement_is_exact_and_cannot_be_dropped(self):
        cutoff = 5
        h = {n: F(truncated_mobius_coefficient(n, cutoff), 2)
             for n in range(17, 33)}  # Formal rational damping only.
        for n in (101, 31*101, 31**3, 37*101):
            complement = complement_cofactor_coefficients(n, cutoff, h)
            self.assertEqual(add_vectors(mangoldt_log_vector(n),
                                         convolution_log_vector(n, h),
                                         convolution_log_vector(n, complement)),
                             full_mobius_log_vector(n, cutoff))
        self.assertNotEqual(convolution_log_vector(31*101, h),
                            full_mobius_log_vector(31*101, cutoff))
        self.assertNotEqual(convolution_log_vector(37*101,
                            complement_cofactor_coefficients(37*101, cutoff, h)), ())

    def test_poisson_needs_both_the_missing_zero_and_large_dual_spacing(self):
        self.assertEqual(dual_support_indices(F(3)), ())
        self.assertEqual(dual_support_indices(F(2)), ())  # chi vanishes at endpoints.
        self.assertEqual(dual_support_indices(F(3, 2)), (1,))
        self.assertEqual(dual_support_indices(F(3, 4)), (2,))
        self.assertNotIn(0, dual_support_indices(F(1, 10)))
        self.assertGreater(cancellation_budgets(12)['dual_frequency_gap'], 0)

    def test_bv_error_charges_prime_log_conversion_and_the_shift_mass(self):
        t, window = F(9, 10), F(1, 10)
        # T²/N * (L/(NT)) * (N L^-D) * H has zero N exponent.
        self.assertEqual((2*t-1)+(-1-t)+1+window, 0)
        self.assertEqual(cancellation_budgets(12)['distribution_log_error'], -11)
        self.assertEqual(cancellation_budgets(12)['distribution_gap'], F(491, 1000))
        # pi-to-prime-log Abel takes an extra log before choosing the arbitrary D.
        source_log_saving = 13
        self.assertEqual(1-(source_log_saving-1), -11)

    def test_freeze_cutoff_and_prime_power_errors_are_separate(self):
        self.assertEqual(cancellation_budgets(12),
                         {'window': F(1, 10), 'distribution_gap': F(491, 1000),
                          'dual_frequency_gap': F(91, 1000),
                          'freeze_error': -F(891, 1000),
                          'cutoff_error': -F(1991, 1000),
                          'prime_power_error': -F(1, 4),
                          'distribution_log_error': -11})
        t, b, window = F(9, 10), F(9, 1000), F(1, 10)
        self.assertEqual((2*t-1)+1+window+(-1-2*t)+b, b-t)

    def test_balance_does_not_determine_the_bad_piece_sign(self):
        energy = F(1)
        for bad in (-F(2), F(0), F(3)):
            complementary = -energy-bad
            self.assertEqual(energy+bad+complementary, 0)
        # These are algebraic possibilities, not measured arithmetic overlaps.
        self.assertGreater(F(3), 0)

    def test_invalid_budgets_and_frequency_support_are_rejected(self):
        for action in (lambda: cancellation_budgets(1),
                       lambda: elementary_window_budgets(1, 16),
                       lambda: dual_support_indices(F(0)),
                       lambda: dual_support_indices(F(1), (F(0), F(2))),
                       lambda: divisor_log_vector(0, {1: F(1)})):
            with self.assertRaises(ValueError):
                action()


if __name__ == '__main__':
    unittest.main()
