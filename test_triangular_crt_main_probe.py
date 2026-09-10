import unittest

from triangular_crt_main_probe import (
    _triangular_kernel_direct,
    _triangular_kernel_fejer,
    triangular_crt_main_probe,
)


class TriangularCrtMainProbeTests(unittest.TestCase):
    def test_fejer_formula_matches_direct_sum(self):
        for gcd_value in (1, 2, 5, 14):
            for mode in (1, 17, 103):
                self.assertAlmostEqual(
                    abs(_triangular_kernel_direct(1009, gcd_value, mode)
                        - _triangular_kernel_fejer(1009, gcd_value, mode)),
                    0, places=7)

    def test_probe_preserves_open_scope(self):
        receipt = triangular_crt_main_probe(457, 3, 9, 2, 4)
        self.assertGreater(receipt["remainder_frobenius_over_equality"], 0)
        self.assertFalse(receipt["triangular_main_theorem_proved"])
        self.assertFalse(receipt["remainder_theorem_proved"])


if __name__ == "__main__":
    unittest.main()
