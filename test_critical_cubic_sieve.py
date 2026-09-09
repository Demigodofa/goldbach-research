"""Moving-cutoff, parity, triprime and paid-tail guards; no prime-count claim."""
from fractions import Fraction as F
import unittest

from critical_cubic_sieve import (
    complement_identity, critical_pattern, fixed_x_pattern,
    moving_prime_factor_majorant, reduced_cubic_pattern, tail_log_profile,
)
from polynomial_joint_majorant import polynomial_cofactor_samples


class CriticalCubicSieveTests(unittest.TestCase):
    def test_complement_identity_and_correct_parity_class(self):
        for degree in (2,3,4,5):
            for count in range(1,9):
                shares = tuple(F(j, count*(count+1)//2) for j in range(1,count+1))
                left, right = complement_identity(shares,degree)
                self.assertEqual(left,right)
                if count > degree:
                    self.assertEqual(right,0)
                    if (count+degree)%2 == 0:
                        self.assertEqual(critical_pattern(shares,degree),0)

    def test_triprime_formula_including_unbalanced_factors(self):
        for shares in ((F(1,3),)*3,(F(1,10),F(1,5),F(7,10)),
                       (F(1,20),F(9,20),F(1,2))):
            self.assertEqual(critical_pattern(shares),reduced_cubic_pattern(shares))
        self.assertEqual(critical_pattern((F(1,3),)*3),F(8,9))
        self.assertEqual(critical_pattern((F(1),)),1)

    def test_odd_composites_vanish_but_even_signs_remain(self):
        for count in (5,7,9,11):
            shares = (F(1,count),)*count
            self.assertEqual(critical_pattern(shares),0)
            self.assertEqual(reduced_cubic_pattern(shares),0)
        self.assertEqual(critical_pattern((F(1,4),)*4),F(1,2))
        self.assertEqual(critical_pattern((F(1,6),)*6),F(-2,9))
        self.assertEqual(reduced_cubic_pattern((F(1,6),)*6),F(-2,9))

    def test_fixed_x_and_nonsquarefree_shortcuts_destroy_the_zero(self):
        shares = (F(1,5),)*5
        self.assertEqual(critical_pattern(shares),0)
        self.assertNotEqual(fixed_x_pattern(shares,F(99,100)),0)
        # Five distinct-factor shares, with the first repeated: total exponent
        # mass is1, but the radical's mass is5/6, so complementation fails.
        radical_shares = (F(1,6),)*5
        self.assertEqual(polynomial_cofactor_samples(tuple(2*s for s in radical_shares),3),F(-1,9))
        with self.assertRaises(ValueError):
            critical_pattern(radical_shares)

    def test_cubic_crude_tail_reaches_prime_precision(self):
        self.assertFalse(tail_log_profile(2)['vanishes_at_prime_scale'])
        self.assertEqual(tail_log_profile(3),
                         {'logx_power':-1,'loglogx_power':4,'vanishes_at_prime_scale':True})
        for degree in (3,4,5):
            epsilon = F(1,100)
            for n_ratio in (F(99,100),F(1)):
                for d_ratio in (F(1,2)-epsilon,F(1,2)-epsilon/2,F(1,2)):
                    moving_weight = max(F(0),1-2*d_ratio/n_ratio)**degree
                    self.assertLessEqual(moving_weight,(2*epsilon)**degree)

    def test_fixed_multiplicative_majorant_preserves_small_prime_saturation(self):
        for alpha in (F(1,1000),F(1,100),F(1,20)):
            for n_ratio in (F(1,2),F(99,100),F(1)):
                for t in (F(1),F(10),F(100)):
                    moving, fixed = moving_prime_factor_majorant(alpha,n_ratio,t)
                    self.assertLessEqual(moving,fixed)
                    self.assertLessEqual(fixed,2)


if __name__ == '__main__':
    unittest.main()
