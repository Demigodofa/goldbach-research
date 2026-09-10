import math
import unittest

from mobius_structured_endpoint_probe import (finite_structured_endpoint_probe,
                                              progression_index_interval)


class MobiusStructuredEndpointProbeTests(unittest.TestCase):
    def test_progression_index_interval_matches_divisible_cofactors(self):
        for cofactor_left in range(1, 20):
            for divisor in range(1, 12):
                first, last = progression_index_interval(cofactor_left, divisor)
                expected = tuple(n // divisor
                                 for n in range(cofactor_left + 1,
                                                2 * cofactor_left + 1)
                                 if n % divisor == 0)
                actual = tuple(range(first, last + 1)) if first <= last else ()
                self.assertEqual(actual, expected)

    def test_affine_families_stay_central_and_return_finite_ratios(self):
        result = finite_structured_endpoint_probe(32000)
        self.assertGreater(result["prime_count"], 0)
        self.assertEqual(len(result["families"]), 6)
        self.assertFalse(
            result["arbitrary_interval_family_needed_by_physical_endpoints"])
        self.assertFalse(result["actual_weighted_shift_sum_estimated"])
        for receipt in result["families"].values():
            self.assertTrue(math.isfinite(receipt["off_over_diagonal"]))
            self.assertLessEqual(receipt["positive_modulus_count"],
                                 result["prime_count"])
            self.assertLessEqual(receipt["individual_ratio_min"],
                                 receipt["individual_ratio_max"])


if __name__ == "__main__":
    unittest.main()
