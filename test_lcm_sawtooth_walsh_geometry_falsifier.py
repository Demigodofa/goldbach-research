import unittest

from lcm_sawtooth_walsh_geometry_falsifier import (
    walsh_geometry_resonance,
)


class LcmSawtoothWalshGeometryFalsifierTests(unittest.TestCase):
    def test_resonance_defeats_the_2_to_omega_cost(self):
        receipt = walsh_geometry_resonance(5, 1e-6)
        self.assertAlmostEqual(
            receipt["complement_convolution"], 2e-6)
        self.assertAlmostEqual(receipt["paired_support_majorant"], 2e-6)
        self.assertGreater(
            receipt["ratio_after_2_to_omega_cost"], 7e9)
        self.assertTrue(
            receipt["coefficient_uniform_2_to_omega_bound_falsified"])
        self.assertFalse(receipt["fixed_mobius_polynomial_bound_falsified"])

    def test_ratio_is_unbounded_as_epsilon_shrinks(self):
        coarse = walsh_geometry_resonance(3, 1e-2)
        fine = walsh_geometry_resonance(3, 1e-4)
        self.assertGreater(
            fine["ratio_after_2_to_omega_cost"],
            9000 * coarse["ratio_after_2_to_omega_cost"])

    def test_rejects_invalid_controls(self):
        for arguments in ((0, .1), (2, 0), (2, 1)):
            with self.assertRaises(ValueError):
                walsh_geometry_resonance(*arguments)


if __name__ == "__main__":
    unittest.main()
