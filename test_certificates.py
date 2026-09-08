"""Load-bearing corruption and composition checks, including optimized Python."""
import copy
import unittest

import interval_certificates as ic
import stacked_cover as sc
from redistribution import sieve


class CertificateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.block=sc.cover_block(4,100)

    def test_valid_block_and_base(self):
        self.assertEqual(sc.verify_block(self.block)["covered_count"],100)
        self.assertEqual(sc.verify_block(sc.cover_block(4,1))["covered_count"],1)

    def test_empty_forged_certificate_is_rejected(self):
        forged={"first_even":6,"last_even":6,"count":1,"certificates":[],
                "unresolved":[],"covered_count":1,"certificate_count":0,"status":"certified"}
        with self.assertRaises(ValueError):
            sc.verify_block(forged)

    def test_structural_corruption(self):
        for field,value in [("first_even",5),("count",0),("count",True),
                            ("last_even",202.0),("covered_count",99)]:
            forged=copy.deepcopy(self.block)
            forged[field]=value
            with self.subTest(field=field,value=value),self.assertRaises(ValueError):
                sc.verify_block(forged)

    def test_composite_AP_inputs_are_rejected(self):
        # This has correct sum arithmetic and a full mask, but9 is composite.
        forged={"first_even":12,"last_even":12,"count":1,"certificates":[
            {"kind":"prime_AP_sum","left":{"first":9,"step":2,"count":1},
             "right":{"first":3,"step":2,"count":1},
             "output":{"first":12,"step":2,"count":1},"newly_covered":1}],
            "unresolved":[],"covered_count":1,"certificate_count":1,"status":"certified"}
        with self.assertRaises(ValueError):
            sc.verify_block(forged)

    def test_composer_does_not_fill_a_gap(self):
        later=sc.cover_block(206,100)
        with self.assertRaises(ValueError):
            sc.compose([self.block,later])

    def test_serialized_hole_certificate(self):
        flags=sieve(100)
        good=ic.certify(ic.count_interval(3,13,flags),ic.count_interval(3,7,flags))
        self.assertEqual(ic.verify_serialized(good,flags)["covered_even_count"],6)
        for field,value in [("covered_even_last",20),("total_holes",0),("guarantee",False)]:
            forged=copy.deepcopy(good)
            forged[field]=value
            with self.assertRaises(ValueError):
                ic.verify_serialized(forged,flags)
        forged=copy.deepcopy(good)
        forged["left"]["prime_count"]=6
        with self.assertRaises(ValueError):
            ic.verify_serialized(forged,flags)


if __name__=="__main__":
    unittest.main()
