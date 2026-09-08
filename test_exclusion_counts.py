"""Independent checks of exact intersections and polynomial survivor bounds."""
from itertools import product
from math import comb
import unittest

from exclusion_counts import candidate_window,count_target,moment_bounds,split_threshold,zero_histogram_from_three
from redistribution import trial_prime


class ExclusionCountTests(unittest.TestCase):
    def test_bounds_on_arbitrary_multiplicity_histograms(self):
        for cap in range(0,7):
            for histogram in product(range(3),repeat=cap+1):
                moments=[sum(n*comb(k,j) for k,n in enumerate(histogram) if k>=j)
                         for j in range(cap+1)]
                for degree in range(cap+1):
                    z=moment_bounds(moments[:degree+1],cap)
                    self.assertLessEqual(z["lower"],histogram[0])
                    self.assertGreaterEqual(z["upper"],histogram[0])
                self.assertEqual(z["lower"],histogram[0])
                self.assertEqual(z["upper"],histogram[0])

    def test_CRT_moments_against_direct_divisibility(self):
        for target in range(6,1002,2):
            z=count_target(target,stop_when_positive=False)
            w=z["window"]
            multiplicities=[sum(a%r==0 or (target-a)%r==0 for r in w["odd_wheel_primes"])
                            for a in range(w["first_odd"],w["last_odd"]+1,2)]
            self.assertLessEqual(max(multiplicities,default=0),w["multiplicity_cap"])
            for stage in z["stages"]:
                j=stage["degree"]
                expected=sum(comb(k,j) for k in multiplicities if k>=j)
                self.assertEqual(stage["intersection_sum"],expected)
            actual=sum(k==0 for k in multiplicities)
            self.assertEqual(z["survivor_lower"],actual)
            self.assertEqual(z["survivor_upper"],actual)
            prime_pairs=sum(trial_prime(a) and trial_prime(target-a)
                            for a in range(w["first_odd"],w["last_odd"]+1,2))
            self.assertEqual(actual,prime_pairs)

    def test_odd_truncations_need_not_improve(self):
        moments=[comb(10,j) for j in range(4)]
        degree1=moments[0]-moments[1]
        degree3=degree1+moments[2]-moments[3]
        self.assertEqual((degree1,degree3),(-9,-84))
        self.assertEqual(moment_bounds(moments,10)["lower"],0)

    def test_split_cap_and_integrated_polynomials(self):
        self.assertEqual(split_threshold((3,5,7,11,13)),248)
        self.assertEqual(candidate_window(246,13)["multiplicity_cap"],5)
        self.assertEqual(candidate_window(246,13,"split")["multiplicity_cap"],4)
        for target in range(6,1002,2):
            z=count_target(target,bound_strategy="root_family",cap_strategy="split")
            w=z["window"]
            counts=[sum(a%r==0 or (target-a)%r==0 for r in w["odd_wheel_primes"])
                    for a in range(w["first_odd"],w["last_odd"]+1,2)]
            self.assertLessEqual(max(counts,default=0),w["multiplicity_cap"])
            actual=counts.count(0)
            self.assertLessEqual(z["survivor_lower"],actual)
            self.assertGreaterEqual(z["survivor_upper"],actual)

    def test_prime_safe_window_cannot_claim_outside_coverage(self):
        z=count_target(600,p=13,stop_when_positive=False)
        self.assertEqual(z["status"],"unresolved_by_window")
        self.assertEqual(z["survivor_upper"],0)
        with self.assertRaises(ValueError):
            count_target(401)
        with self.assertRaises(ValueError):
            count_target(400,p=15)

    def test_integer_zero_histogram_proves_aggregate_ambiguity(self):
        moments=[253,504,408,184]
        histogram=zero_histogram_from_three(moments,5)
        self.assertEqual(histogram,[0,132,18,76,27,0])
        self.assertEqual([sum(n*comb(k,j) for k,n in enumerate(histogram) if k>=j)
                          for j in range(4)],moments)
        self.assertIsNone(zero_histogram_from_three([468,902,724,296],5))
        for cap in range(0,7):
            for histogram in product(range(2),repeat=cap):
                known=[0]+list(histogram)
                moments=[sum(n*comb(k,j) for k,n in enumerate(known) if k>=j)
                         for j in range(4)]
                self.assertIsNotNone(zero_histogram_from_three(moments,cap))


if __name__=="__main__":
    unittest.main()
