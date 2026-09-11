import unittest

from lcm_sawtooth_complete_cube_mobius import (
    complete_cube_mobius_reduction,
)


class LcmSawtoothCompleteCubeMobiusTests(unittest.TestCase):
    def test_transformed_sum_matches_direct_complete_cubes(self):
        for modulus, limit in ((1, 1), (6, 20), (30, 50), (210, 90)):
            receipt = complete_cube_mobius_reduction(
                modulus, limit, 12.0, 11.0)
            self.assertLess(abs(receipt["reduction_error"]), 2e-12)
            self.assertTrue(
                receipt["complete_cube_mobius_reduction_proved"])
            self.assertFalse(
                receipt["uniform_coprime_mobius_estimate_proved"])
            self.assertFalse(receipt["boundary_truncated_cube_control_proved"])

    def test_rejects_nonsquarefree_excluded_modulus(self):
        with self.assertRaisesRegex(ValueError, "squarefree"):
            complete_cube_mobius_reduction(12, 20, 4.0, 5.0)


if __name__ == "__main__":
    unittest.main()
