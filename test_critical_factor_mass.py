"""Finite adversarial guards for the analytic critical-region argument."""
from fractions import Fraction as F
import unittest

from critical_factor_mass import affine_pair_root_density, critical_bands, in_residual_region


def partitions(vector):
    if not vector:
        yield ()
        return
    for tail in partitions(vector[1:]):
        yield (vector[0],)+tail
        for j in range(len(tail)):
            yield tail[:j]+(tail[j]+vector[0],)+tail[j+1:]


class CriticalFactorMassTests(unittest.TestCase):
    def test_all_coagulations_of_two_and_three_large_factor_fixtures(self):
        e=F(1, 100)
        thirds, halves=critical_bands(e)
        seeds=((F(1, 2),F(1, 2)), (F(1, 3),)*3,
               tuple(F(t,1000) for t in (498,498,4)),
               tuple(F(t,1000) for t in (331,333,334,2)),
               tuple(F(t,1000) for t in (328,332,336,1,3)))
        observed=set()
        for seed in seeds:
            self.assertTrue(in_residual_region(seed,e))
            for result in partitions(seed):
                if len(result)<2 or min(result)<F(1,3)-2*e:
                    continue
                observed.add(len(result))
                if len(result)==2:
                    self.assertTrue(any(a<=min(result)<=b for a,b in (thirds,halves)))
                else:
                    self.assertEqual(len(result),3)
                    self.assertTrue(all(thirds[0]<=t<=thirds[1] for t in result))
        self.assertEqual(observed,{2,3})
        # Individually tiny coordinates can collectively hit a forbidden sum.
        self.assertFalse(in_residual_region(tuple(F(t,1000) for t in (490,495,5,5,5)),e))
        self.assertFalse(in_residual_region((F(1,4),)*4,e))

    def test_last_prime_scale_and_small_sieve_moduli_are_separated(self):
        for e in (F(1,100),F(1,1000),F(1,10**8)):
            thirds,_=critical_bands(e)
            self.assertGreater(1-2*thirds[1],F(1,4))
            self.assertGreater(thirds[0],F(1,100))
            self.assertLess(2*e,F(1,3)-e)
            self.assertLess(e,F(1,3)-2*e)
        with self.assertRaises(ValueError):
            critical_bands(F(1,99))

    def test_two_affine_forms_have_the_required_local_root_counts(self):
        for target,multiplier in ((60,77),(202,143),(330,323)):
            for prime in (2,3,5,7,11,13,17,19,23):
                actual,predicted=affine_pair_root_density(target,multiplier,prime)
                self.assertEqual(actual,predicted)
                self.assertLess(actual,1)
        with self.assertRaises(ValueError):
            affine_pair_root_density(60,15,3)


if __name__=='__main__':
    unittest.main()
