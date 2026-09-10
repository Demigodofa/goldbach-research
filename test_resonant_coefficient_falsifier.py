import unittest

from resonant_coefficient_falsifier import (
    single_modulus_resonant_falsifier,
)


class ResonantCoefficientFalsifierTests(unittest.TestCase):
    def test_exact_optimizer_dominates_named_resonances(self):
        receipt = single_modulus_resonant_falsifier(457, 2, 9, 2, 4)
        self.assertAlmostEqual(
            receipt["frame_norm_of_resonant_coefficients"], 1.0, places=11)
        self.assertAlmostEqual(
            receipt["optimal_resonant_quotient"],
            receipt["eigensolver_quotient"], places=10)
        self.assertGreaterEqual(
            receipt["optimal_resonant_quotient"],
            receipt["best_single_mode_locked_quotient"] - 1e-10)
        self.assertGreaterEqual(
            receipt["optimal_resonant_quotient"],
            receipt["mobius_quotient"] - 1e-10)
        self.assertGreaterEqual(
            receipt["optimal_resonant_quotient"],
            receipt["flat_frame_phase_resonant_quotient"] - 1e-10)
        magnitudes = [
            (real ** 2 + imag ** 2) ** .5
            for _, real, imag in
            receipt["flat_frame_phase_whitened_coefficients"]]
        self.assertAlmostEqual(max(magnitudes), min(magnitudes), places=11)
        self.assertFalse(receipt["uniform_asymptotic_inequality_proved"])

    def test_rejects_composite_modulus(self):
        with self.assertRaisesRegex(ValueError, "prime"):
            single_modulus_resonant_falsifier(1001, 5, 9, 2, 8)


if __name__ == "__main__":
    unittest.main()
