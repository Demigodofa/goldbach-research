import unittest

from mobius_aligned_covariance_probe import finite_aligned_covariance_split
from mobius_aligned_lag_probe import finite_aligned_lag_probe


class MobiusAlignedLagProbeTests(unittest.TestCase):
    def test_lags_recombine_previous_same_and_cross_row_split(self):
        lag = finite_aligned_lag_probe(32000)
        previous = finite_aligned_covariance_split(32000)
        self.assertAlmostEqual(lag["normalized_total_off"],
                               previous["normalized"]["total_off"], places=11)
        self.assertAlmostEqual(lag["normalized_same_row"],
                               (previous["normalized"]["point"]
                                + previous["normalized"]["same_row_nonpoint"]),
                               places=11)
        self.assertAlmostEqual(lag["normalized_cross_row"],
                               previous["normalized"]["cross_row"], places=11)
        self.assertEqual(len(lag["normalized_lag_contributions"]),
                         lag["cofactor_left"])
        self.assertGreater(lag["positive_cross_mass"], 0)
        self.assertGreater(lag["positive_mass_last_half_fraction"], .2)
        self.assertGreaterEqual(lag["furthest_positive_lag"],
                                lag["cofactor_left"] - 2)
        self.assertFalse(lag["bounded_lag_cancellation_proved"])


if __name__ == "__main__":
    unittest.main()
