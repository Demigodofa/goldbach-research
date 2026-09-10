import unittest
from fractions import Fraction as F

from mobius_balanced_trilinear_source_gate import (
    DUAL_TARGET,
    balanced_trilinear_budget,
)


class BalancedTrilinearSourceGateTests(unittest.TestCase):
    def test_central_threshold_box_keeps_every_source_term_above_parseval(self):
        result = balanced_trilinear_budget(F(3, 4), F(1, 2))
        self.assertEqual(result["localization"], F(1, 4))
        self.assertEqual(result["box_count"], F(1, 4))
        self.assertEqual(result["ordered_cell_supports"],
                         (F(49, 100), F(1, 4), F(1, 4)))
        self.assertTrue(result["mpss_theorem_6_1_applicable"])
        self.assertGreater(result["ps_theorem_1_3"], result["parseval_dual"])
        self.assertGreater(result["optimistic_ps_theorem_1_1"],
                           result["parseval_dual"])
        self.assertGreater(result["mpss_6_1_first"], result["parseval_dual"])
        self.assertGreater(result["mpss_6_1_second"], result["parseval_dual"])

    def test_exact_uniform_gap_and_paid_rank_term_on_grid(self):
        smallest_pairwise_gap = None
        smallest_optimistic_gap = None
        smallest_refined_first_gap = None
        smallest_refined_second_gap = None
        for y_tick in range(750, 1001):
            y = F(y_tick, 1000)
            for alpha_tick in range(411, 590):
                alpha = F(alpha_tick, 1000)
                result = balanced_trilinear_budget(y, alpha)
                gaps = (
                    result["ps_1_3_excess_over_parseval"],
                    result["ps_1_1_excess_over_parseval"],
                )
                smallest_pairwise_gap = (gaps[0] if smallest_pairwise_gap is None
                                           else min(smallest_pairwise_gap, gaps[0]))
                smallest_optimistic_gap = (gaps[1] if smallest_optimistic_gap is None
                                            else min(smallest_optimistic_gap, gaps[1]))
                if result["mpss_theorem_6_1_applicable"]:
                    first = result["mpss_6_1_first_excess_over_parseval"]
                    second = result["mpss_6_1_second_excess_over_parseval"]
                    smallest_refined_first_gap = (
                        first if smallest_refined_first_gap is None
                        else min(smallest_refined_first_gap, first))
                    smallest_refined_second_gap = (
                        second if smallest_refined_second_gap is None
                        else min(smallest_refined_second_gap, second))
                self.assertTrue(result["low_projector_fits_target"])
                self.assertLessEqual(result["low_projector_rank_term"], F(131, 200))
                self.assertFalse(result["wright_2_2_upper_range_possible"])

        self.assertGreaterEqual(smallest_pairwise_gap, F(1298, 3200))
        self.assertGreaterEqual(smallest_optimistic_gap, F(53, 200))
        self.assertGreater(smallest_refined_first_gap, F(2, 5))
        self.assertGreaterEqual(smallest_refined_second_gap, F(1665, 4000))

    def test_target_is_half_the_energy_exponent(self):
        self.assertEqual(2 * DUAL_TARGET, F(1499, 1000))

    def test_input_boundaries(self):
        with self.assertRaises(ValueError):
            balanced_trilinear_budget(F(1499, 2000), F(1, 2))
        with self.assertRaises(ValueError):
            balanced_trilinear_budget(F(3, 4), F(41, 100))
        with self.assertRaises(ValueError):
            balanced_trilinear_budget(F(3, 4), F(1, 2), F(3, 5))


if __name__ == "__main__":
    unittest.main()
