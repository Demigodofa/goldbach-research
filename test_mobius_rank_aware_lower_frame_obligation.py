import unittest

import numpy as np

from mobius_rank_aware_lower_frame import rank_aware_lower_frame_receipt
from tools.build_mobius_rank_aware_lower_frame_obligation import (
    build_receipt,
)


class MobiusRankAwareLowerFrameObligationTests(unittest.TestCase):
    def test_full_rank_fixture_matches_ordinary_eigenvalue(self):
        full = np.diag((2.0, 8.0))
        active = np.diag((1.5, 12.0))
        receipt = rank_aware_lower_frame_receipt(active, full)
        self.assertEqual(receipt["full_rank"], 2)
        self.assertEqual(receipt["full_nullity"], 0)
        self.assertAlmostEqual(
            receipt["schur_minimized_positive_range_minimum"], .75)
        self.assertTrue(
            receipt[
                "one_half_lower_frame_certified_with_null_coupling_tolerance"])

    def test_singular_full_fixture_optimizes_harmless_null_direction(self):
        full = np.diag((4.0, 0.0))
        active = np.array(((4.0, 1.0), (1.0, 1.0)))
        receipt = rank_aware_lower_frame_receipt(active, full)
        self.assertEqual(receipt["full_rank"], 1)
        self.assertEqual(receipt["full_nullity"], 1)
        self.assertAlmostEqual(receipt["raw_positive_range_minimum"], 1.0)
        self.assertAlmostEqual(
            receipt["schur_minimized_positive_range_minimum"], .75)
        self.assertTrue(receipt["active_positive_full_null_direction"])
        self.assertTrue(
            receipt[
                "one_half_lower_frame_certified_with_null_coupling_tolerance"])

    def test_builder_names_rank_aware_theorem_obligation(self):
        receipt = build_receipt()
        self.assertEqual(
            receipt["status"],
            "TARGET_rank_aware_positive_range_lower_frame_plus_"
            "support_activation")
        self.assertEqual(receipt["vacuous_pre_support_scales"], (83, 101))
        self.assertEqual(receipt["nonvacuous_scales"], (127, 149, 167, 191))
        self.assertEqual(receipt["rank_deficient_nonvacuous_scales"], (167,))
        self.assertEqual(
            receipt["quotient_above_one_half_nonvacuous_scales"],
            (127, 149, 167, 191))
        self.assertEqual(
            receipt["one_half_certified_nonvacuous_scales"],
            (127, 149, 191))
        self.assertEqual(receipt["null_coupling_attention_scales"], (167,))
        self.assertAlmostEqual(
            receipt["minimum_checked_quotient_eigenvalue"],
            0.8511480691308368)
        self.assertTrue(
            receipt["one_half_survives_checked_nonvacuous_quotient_minima"])
        self.assertFalse(
            receipt["one_half_fully_certified_with_null_coupling_tolerance"])
        self.assertTrue(receipt["finite_diagnostic_only"])
        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["uniform_active_full_lower_frame_proved"])


if __name__ == "__main__":
    unittest.main()
