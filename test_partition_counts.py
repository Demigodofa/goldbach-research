"""Exact checks for prime-safe candidate clips and location-only partitions."""
from math import comb
import unittest

from exclusion_counts import candidate_window,count_target,partition_target
from redistribution import trial_prime


class PartitionCountTests(unittest.TestCase):
    TARGET=4412
    DEGREE=4

    def test_partition_moments_add_to_global_fixed_degree_moments(self):
        for parts in (1,2,4,8,16):
            result=partition_target(self.TARGET,parts,self.DEGREE)
            baseline=result["global_fixed_degree_baseline"]["moments"]
            self.assertEqual(result["fixed_degree"],len(baseline)-1)
            self.assertEqual([sum(row["moments"][j] for row in result["part_rows"])
                              for j in range(len(baseline))],baseline)

    def test_partition_bounds_enclose_direct_prime_counts(self):
        result=partition_target(self.TARGET,8,self.DEGREE)
        for row in result["part_rows"]:
            direct=sum(trial_prime(a) and trial_prime(self.TARGET-a)
                       for a in range(row["first_odd"],row["last_odd"]+1,2))
            self.assertLessEqual(row["lower"],direct)
            self.assertGreaterEqual(row["upper"],direct)

    def test_partition_has_exact_adjacent_coverage(self):
        result=partition_target(self.TARGET,16,self.DEGREE)
        window=result["window"]
        rows=result["part_rows"]
        flattened=[a for row in rows for a in range(row["first_odd"],row["last_odd"]+1,2)]
        self.assertEqual(flattened,list(range(window["first_odd"],window["last_odd"]+1,2)))
        self.assertEqual(sum(row["candidate_count"] for row in rows),window["candidate_count"])
        self.assertLessEqual(max(row["candidate_count"] for row in rows)-
                             min(row["candidate_count"] for row in rows),1)

    def test_clips_reject_nonodd_outside_and_malformed(self):
        window=candidate_window(self.TARGET)
        lo,hi=window["first_odd"],window["last_odd"]
        valid=count_target(self.TARGET,max_degree=self.DEGREE,stop_when_positive=False,
                           candidate_clip=(lo,lo))
        self.assertEqual(valid["candidate_clip"]["candidate_count"],1)
        for clip in ((lo-2,hi),(lo,hi+2),(lo+1,hi),(hi,lo),(lo,True),[lo,hi]):
            with self.subTest(clip=clip),self.assertRaises(ValueError):
                count_target(self.TARGET,candidate_clip=clip)

    def test_empty_local_layer_pads_only_proven_zero_moments(self):
        result=partition_target(1000,100,4,bound_strategy="root_family",cap_strategy="split")
        baseline=result["global_fixed_degree_baseline"]["moments"]
        self.assertEqual([sum(row["moments"][j] for row in result["part_rows"])
                          for j in range(len(baseline))],baseline)
        self.assertTrue(any(row["observed_stopping_degree"]<result["fixed_degree"]
                            for row in result["part_rows"]))
        for row in result["part_rows"]:
            self.assertEqual(len(row["moments"]),result["fixed_degree"]+1)
            if row["observed_stopping_degree"]<result["fixed_degree"]:
                self.assertTrue(row["exact_closure"])
                self.assertTrue(all(value==0 for value in row["moments"][row["observed_stopping_degree"]+1:]))
            direct=sum(trial_prime(a) and trial_prime(1000-a)
                       for a in range(row["first_odd"],row["last_odd"]+1,2))
            self.assertLessEqual(row["lower"],direct)
            self.assertGreaterEqual(row["upper"],direct)


if __name__=="__main__":
    unittest.main()
