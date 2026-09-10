"""Source-sign, energy and detector-partition guards, not numerical zeros."""
from fractions import Fraction as F
from math import gamma
import unittest

from zero_detector_band_reduction import (
    first_detecting_length, gamma_contour_realpart,
    type_ii_band_budget, type_ii_energy_exponent,
)


class ZeroDetectorBandTests(unittest.TestCase):
    def test_density_weight_has_a_uniform_strict_power_saving(self):
        for j in range(121):
            beta=F(16,25)+F(j,1000)
            power=type_ii_energy_exponent(beta)
            self.assertEqual(power,-(1-beta)/5)
            self.assertLessEqual(power,-F(6,125))
        self.assertEqual(type_ii_energy_exponent(F(16,25)),-F(9,125))

    def test_the_gram_square_root_is_paid_before_the_band_claim(self):
        b=type_ii_band_budget()
        self.assertEqual(b['column'],F(122,125))
        self.assertEqual(b['intersection'],F(119,125))
        self.assertGreater(b['column'],b['intersection'])
        self.assertGreater(b['column'],b['finite_period'])
        self.assertEqual(b['beta_endpoint'],-F(7,10))

    def test_gamma_argument_has_the_contour_sign_and_a_positive_recurrence(self):
        for beta in (F(16,25),F(7,10),F(19,25)):
            z=gamma_contour_realpart(beta)
            self.assertEqual(z+beta,F(1,2))
            self.assertLess(z,0)
            self.assertGreater(1+z,0)
            self.assertAlmostEqual(gamma(float(z)),gamma(float(1+z))/float(z))
            self.assertNotEqual(gamma(float(z)),gamma(float(-z)))

    def test_detector_threshold_is_inclusive_and_length_choice_is_unique(self):
        threshold=F(1,900)
        values={32:2*threshold,8:threshold,16:3*threshold,4:threshold/2}
        self.assertEqual(first_detecting_length(values,threshold),8)
        self.assertIsNone(first_detecting_length({4:threshold/2,8:F(0)},threshold))

    def test_original_source_types_can_overlap(self):
        # Two source predicates are not a partition. The NOT-I set is disjoint.
        records=((True,False),(False,True),(True,True))
        detected=[i for i,(type_i,type_ii) in enumerate(records) if type_i]
        nondetected=[i for i,(type_i,type_ii) in enumerate(records) if not type_i]
        self.assertEqual(detected,[0,2])
        self.assertEqual(nondetected,[1])
        self.assertTrue(all(records[i][1] for i in nondetected))
        self.assertNotEqual(nondetected,[i for i,r in enumerate(records) if r[1]])

    def test_first_detector_rectangles_retain_every_ordered_copy_pair(self):
        threshold=F(1,9)
        # The first two equal records represent coincident copies, not one zero.
        records=({4:threshold,8:threshold},{4:threshold,8:threshold},
                 {4:F(0),8:2*threshold},{4:F(0),8:F(0)})
        groups={}
        for index,record in enumerate(records):
            length=first_detecting_length(record,threshold)
            if length is not None:
                groups.setdefault(length,[]).append(index)
        pairs=[(i,j) for left in groups.values() for right in groups.values()
               for i in left for j in right]
        self.assertEqual(len(pairs),9)
        self.assertEqual(len(set(pairs)),9)
        self.assertIn((0,1),pairs)
        self.assertIn((1,0),pairs)

    def test_unlicensed_realparts_and_nondyadic_tags_are_rejected(self):
        with self.assertRaises(ValueError):
            type_ii_energy_exponent(F(4,5))
        with self.assertRaises(ValueError):
            first_detecting_length({6:F(1)},F(1,9))
        with self.assertRaises(ValueError):
            first_detecting_length({4:F(1)},F(0))


if __name__ == '__main__':
    unittest.main()
