"""Exact validity checks for the requested root-polynomial family."""
from fractions import Fraction
from itertools import combinations, product
from math import comb
import unittest

import moment_polynomials as mp


def solve_unique_fraction_system(rows, rhs):
    """Independent reduced-row solve; None means inconsistent or non-unique."""
    width=len(rows[0]) if rows else 0
    table=[[Fraction(value) for value in row]+[Fraction(value_rhs)]
           for row,value_rhs in zip(rows,rhs)]
    pivot_row=0
    for column in range(width):
        pivot=next((row for row in range(pivot_row,len(table)) if table[row][column]),None)
        if pivot is None:
            continue
        table[pivot_row],table[pivot]=table[pivot],table[pivot_row]
        factor=table[pivot_row][column]
        table[pivot_row]=[value/factor for value in table[pivot_row]]
        for row in range(len(table)):
            if row!=pivot_row and table[row][column]:
                factor=table[row][column]
                table[row]=[left-factor*right for left,right in zip(table[row],table[pivot_row])]
        pivot_row+=1
    if any(all(value==0 for value in row[:width]) and row[-1] for row in table):
        return None
    if pivot_row!=width:
        return None
    solution=[Fraction() for _ in range(width)]
    for row in table:
        pivot=next((column for column,value in enumerate(row[:width]) if value),None)
        if pivot is not None:
            solution[pivot]=row[-1]
    return solution


def primal_lp_zero_minimum(moments, cap):
    """Enumerate LP vertices independently: supports have at most d+1 points."""
    degree=len(moments)-1
    best=None
    for size in range(1,min(cap+1,degree+1)+1):
        for support in combinations(range(cap+1),size):
            rows=[[comb(k,j) if k>=j else 0 for k in support] for j in range(degree+1)]
            weights=solve_unique_fraction_system(rows,moments)
            if weights is None or any(weight<0 for weight in weights):
                continue
            value=weights[support.index(0)] if 0 in support else Fraction()
            best=value if best is None or value<best else best
    if best is None:
        raise AssertionError("fixture moments unexpectedly infeasible")
    return best


class MomentPolynomialTests(unittest.TestCase):
    def test_every_family_polynomial_has_required_sign(self):
        for cap in range(1,13):
            for degree in range(0,7):
                for polynomial in mp.coefficient_families(cap,degree):
                    self.assertEqual(mp.evaluate(polynomial,0),Fraction(1))
                    self.assertTrue(all(mp.evaluate(polynomial,k)<=0 for k in range(1,cap+1)))
                    self.assertEqual(len(polynomial.roots),len(set(polynomial.roots)))
                    self.assertTrue(all(1<=root<=cap for root in polynomial.roots))

    def test_bounds_on_generic_histograms(self):
        for cap in range(0,7):
            for histogram in product(range(3),repeat=cap+1):
                moments=[sum(count*comb(k,j) for k,count in enumerate(histogram) if k>=j)
                         for j in range(cap+1)]
                for degree in range(cap+1):
                    result=mp.strongest_lower(moments[:degree+1],cap)
                    self.assertLessEqual(result["lower"],histogram[0])

    def test_optimal_real_lower_matches_independent_primal_LP(self):
        # Frozen feasible histograms, including degree zero and full degree.
        fixtures=[
            (0,(7,),0),
            (1,(3,4),0),
            (1,(3,4),1),
            (3,(2,1,3,4),2),
            (4,(5,0,2,1,3),3),
            (5,(1,2,0,3,1,2),5),
            (6,(4,1,2,0,3,1,2),4),
            (6,(4,1,2,0,3,1,2),6),
        ]
        for cap,histogram,degree in fixtures:
            moments=[sum(count*comb(k,j) for k,count in enumerate(histogram) if k>=j)
                     for j in range(degree+1)]
            result=mp.strongest_lower(moments,cap)
            self.assertEqual(Fraction(result["numerator"],result["denominator"]),
                             primal_lp_zero_minimum(moments,cap))

    def test_cubic_supplied_moments(self):
        result=mp.strongest_lower([468,902,724,296],5)
        self.assertEqual(result["lower"],22)
        self.assertEqual(result["degree"],3)
        self.assertEqual(result["roots"],[1,3,4])
        self.assertEqual((result["numerator"],result["denominator"]),(64,3))

    def test_stage_one_and_zero_floor(self):
        self.assertEqual(mp.strongest_lower([10,4],5)["lower"],6)
        self.assertEqual(mp.strongest_lower([10],5)["lower"],0)
        self.assertEqual(mp.strongest_lower([0,0,0],2)["lower"],0)
        self.assertEqual(mp.strongest_lower([7,0,0],0)["lower"],7)

    def test_cache_and_validation(self):
        self.assertIs(mp.coefficient_families(5,4),mp.coefficient_families(5,4))
        with self.assertRaises(ValueError):
            mp.coefficient_families(5,-1)
        with self.assertRaises(ValueError):
            mp.strongest_lower([],3)
        with self.assertRaises(ValueError):
            mp.strongest_lower([1,-1],3)
        with self.assertRaises(ValueError):
            mp.strongest_lower([1,0,1],1)


if __name__=="__main__":
    unittest.main()
