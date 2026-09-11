import unittest

from lcm_sawtooth_high_d_assignment import residual_bessel_probe
from lcm_sawtooth_residual_block_probe import (
    dyadic_multi_residual_probe,
    project_dyadic_multi_residual_probe,
)


class LcmSawtoothResidualBlockProbeTests(unittest.TestCase):
    def test_dyadic_blocks_partition_multi_residual_energy(self):
        receipt = dyadic_multi_residual_probe(101, 70, 4, 20)
        bessel = residual_bessel_probe(101, 70, 4, 20)
        self.assertAlmostEqual(
            receipt["multi_residual_quotient"],
            bessel["multi_residual_bessel_ratio"])
        self.assertAlmostEqual(
            sum(block["all_diagonal_fraction"]
                for block in receipt["blocks"]), 1.0)
        self.assertAlmostEqual(
            sum(block["high_diagonal_fraction"]
                for block in receipt["blocks"]), 1.0)
        self.assertTrue(receipt["dyadic_multi_residual_identity_proved"])
        self.assertFalse(
            receipt["dyadic_multi_residual_subpower_bound_proved"])

    def test_block_ranges_and_counts_are_well_formed(self):
        receipt = dyadic_multi_residual_probe(101, 70, 4, 20)
        self.assertGreater(len(receipt["blocks"]), 0)
        for block in receipt["blocks"]:
            lower, upper = block["conductor_range"]
            self.assertEqual(upper, 2 * lower)
            self.assertGreaterEqual(block["all_coordinate_count"], 1)
            self.assertGreaterEqual(
                block["all_coordinate_count"],
                block["high_coordinate_count"])
            self.assertGreaterEqual(block["maximum_all_residual"], 1)
            if block["high_coordinate_count"]:
                self.assertGreaterEqual(block["maximum_high_residual"], 1)
            else:
                self.assertEqual(block["maximum_high_residual"], 0)

    def test_project_sampler_reports_finite_measurement_only(self):
        receipt = project_dyadic_multi_residual_probe(101, 3)
        self.assertEqual(len(receipt["sampled_moduli"]), 3)
        self.assertTrue(
            receipt["finite_project_dyadic_residual_measurement"])
        self.assertFalse(
            receipt["dyadic_multi_residual_subpower_bound_proved"])
        self.assertGreater(
            receipt["worst_sampled_block"]["coordinate_count"], 0)


if __name__ == "__main__":
    unittest.main()
