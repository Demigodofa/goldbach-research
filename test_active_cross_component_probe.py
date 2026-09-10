import unittest

from active_cross_component_probe import (
    finite_cross_components,
    single_modulus_cross_components,
)


class ActiveCrossComponentProbeTests(unittest.TestCase):
    def test_single_reconstructs_exactly(self):
        receipt = single_modulus_cross_components(1009, 5, 9, 3, 8)
        self.assertLess(receipt["reconstruction_error_max"], 1e-7)
        self.assertGreaterEqual(
            receipt["separate_component_bound_over_total"], 1)
        self.assertGreaterEqual(
            receipt["equality_unequal_frobenius_cosine"], -1 - 1e-12)
        self.assertLessEqual(
            receipt["equality_unequal_frobenius_cosine"], 1 + 1e-12)

    def test_finite_reconstructs_exactly(self):
        receipt = finite_cross_components(32000, modulus_limit=3)
        self.assertLess(receipt["reconstruction_error_max"], 1e-6)
        self.assertGreaterEqual(
            receipt["separate_component_bound_over_total"], 1)


if __name__ == "__main__":
    unittest.main()
