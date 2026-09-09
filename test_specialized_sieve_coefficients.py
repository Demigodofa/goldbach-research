"""Exact moving-boundary, multiplicity and source-input guards."""
from fractions import Fraction as F
import unittest

from factored_linear_barrier import log_enclosure
from major_arc_kernel import _factorization, _mobius_phi
from specialized_sieve_coefficients import (
    mobius_cofactor_terms, parity_region_constants, prime_slot_weight, specialized_state,
)
from unexceptional_vaughan_gate import _divisors


class SpecializedSieveCoefficientTests(unittest.TestCase):
    def test_radical_complement_matches_direct_sieve_weight(self):
        for e in (F(1,100),F(1,200)):
            ga,nu=F(1,2)-e,F(1,3)-2*e
            for n in (2,12,60,420,660,780,990,1170,2310,30030,510510,2**20):
                state=specialized_state(n,e)
                direct=sum(_mobius_phi(d)[0] for d in _divisors(n)
                           if d**ga.denominator<=n**ga.numerator and
                           all(p**nu.denominator<n**nu.numerator
                               for p,_ in _factorization(d)))
                self.assertEqual(state['h'],direct)
                if state['u']>1:
                    self.assertEqual(state['h'],state['reflected'])
                if state['category']=='vanishing':
                    self.assertEqual(state['h'],0)
                if state['category']=='prime_smooth':
                    self.assertEqual(_factorization(state['v']),((state['v'],1),))

    def test_pure_smooth_and_nonsquarefree_cofactor_cannot_be_omitted(self):
        repeated=specialized_state(420)
        self.assertEqual((repeated['u'],repeated['v'],repeated['radical'],repeated['h']),
                         (60,7,30,1))
        self.assertEqual(_mobius_phi(repeated['u'])[0],0)
        pure=specialized_state(2310)
        self.assertEqual((pure['category'],pure['v'],pure['h']),('pure_smooth',1,2))
        self.assertEqual(specialized_state(2**20)['category'],'vanishing')

    def test_prime_smooth_kernel_has_a_rank_two_minor(self):
        matrix=[]
        for u in (60,90):
            row=[]
            for v in (11,13):
                state=specialized_state(u*v)
                self.assertEqual((state['u'],state['v']),(u,v))
                row.append(state['h'])
            matrix.append(row)
        self.assertEqual(matrix,[[1,1],[1,0]])
        self.assertEqual(matrix[0][0]*matrix[1][1]-matrix[0][1]*matrix[1][0],-1)

    def test_prime_slot_powers_and_uniform_pruning_margin(self):
        self.assertEqual([prime_slot_weight(n) for n in (13,49,64,12)],
                         [F(1),F(1,2),F(1,6),F(0)])
        for e in (F(1,100),F(1,1000)):
            ga,nu=F(1,2)-e,F(1,3)-2*e
            self.assertGreater(2*nu,1-ga)
            self.assertEqual(1-ga-nu,F(1,6)+3*e)
            self.assertLessEqual(1-nu/2+F(1,100),F(64,75))

    def test_parity_smooth_sector_has_a_positive_main_scale_coefficient(self):
        ratio,triprime_bound=parity_region_constants(F(1,100))
        self.assertEqual(ratio,F(103,47))
        self.assertGreater(triprime_bound,0)
        self.assertLess(triprime_bound,F(1,100))
        _,log2_upper=log_enclosure(2)
        self.assertLess(log2_upper,F(7,10))
        self.assertLess(F(7,10)+F(9,94),F(4,5))
        for e in (F(1,1000),F(1,10000)):
            r,j3=parity_region_constants(e)
            self.assertTrue(2<r<ratio)
            self.assertLess(j3,triprime_bound)

    def test_localized_squarefree_cofactor_expansion_preserves_sign_and_support(self):
        for n,y in ((15015,2),(5005,3),(105*101,2),(105*53,2)):
            state=specialized_state(n)
            terms=mobius_cofactor_terms(n,y)
            self.assertTrue(terms)
            self.assertEqual(sum(sign for _,_,_,sign in terms),-state['h'])
            for t,r,v,sign in terms:
                self.assertEqual(t*r*v,n)
                self.assertEqual((t*r,v),(state['u'],state['v']))
                self.assertEqual(sign,_mobius_phi(r)[0])
        # These omissions are only justified analytically after step8/9.
        self.assertEqual(mobius_cofactor_terms(420,2),())
        self.assertEqual(mobius_cofactor_terms(3**2*5*7*101,2),())
        self.assertEqual(mobius_cofactor_terms(101,2),())
        for e in (F(1,100),F(1,1000)):
            self.assertLess(F(1,2)-e+e/4,F(1,2))


if __name__=='__main__':
    unittest.main()
