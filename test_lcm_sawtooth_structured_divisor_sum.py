import unittest

from lcm_sawtooth_exact_gcd_factorization import (
    lcm_sawtooth_exact_gcd_factorization_probe,
)
from lcm_sawtooth_structured_divisor_sum import (
    structured_divisor_energy_probe,
    structured_divisor_sum_expansion,
)


class LcmSawtoothStructuredDivisorSumTests(unittest.TestCase):
    def test_original_divisor_expansion_matches_direct_sum(self):
        for target in (1, 2, 3, 5, 6, 10, 14, 15, 21, 35):
            receipt = structured_divisor_sum_expansion(
                101, 70, 4, 20, target)
            self.assertAlmostEqual(
                receipt["direct_structured_sum"],
                receipt["expanded_structured_sum"], places=8)
            self.assertTrue(receipt["original_divisor_expansion_proved"])
            self.assertFalse(
                receipt["structured_sum_asymptotic_bound_proved"])

    def test_dyadic_energy_matches_exact_complete_energy(self):
        structured = structured_divisor_energy_probe(101, 70, 4, 20)
        exact = lcm_sawtooth_exact_gcd_factorization_probe(101, 70, 4, 20)
        self.assertAlmostEqual(
            structured["positive_complete_period_energy"],
            exact["exact_signed_complete_energy"], places=7)
        self.assertAlmostEqual(
            structured["low_d_energy_fraction"]
            + structured["high_d_energy_fraction"], 1.0, places=12)
        self.assertAlmostEqual(
            sum(structured["dyadic_energy_fractions"].values()),
            1.0, places=12)
        self.assertTrue(structured["positive_dyadic_factorization_proved"])
        self.assertFalse(structured["dyadic_structured_sum_bound_proved"])

    def test_invalid_target_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "squarefree"):
            structured_divisor_sum_expansion(101, 70, 4, 20, 12)

    def test_zero_energy_support_is_rejected_explicitly(self):
        with self.assertRaisesRegex(ArithmeticError, "zero complete-period"):
            structured_divisor_energy_probe(101, 70, 4, 5)


if __name__ == "__main__":
    unittest.main()
