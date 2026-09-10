import unittest
from fractions import Fraction as F

from mobius_covariance_source_gate import covariance_source_scale_receipt


class MobiusCovarianceSourceGateTests(unittest.TestCase):
    def test_source_ranges_are_close_but_not_an_application(self):
        result = covariance_source_scale_receipt()
        self.assertEqual(result["classical_Q_squared_in_N"], F(59, 50))
        self.assertEqual(result["product_in_Q"], F(100, 59))
        self.assertEqual(result["balanced_factor_in_Q"], F(50, 59))
        self.assertEqual(result["mobius_cutoff_in_Q"], F(15, 59))
        self.assertEqual(result["active_band_length_in_Q"], F(49, 59))
        self.assertEqual(result["product_below_Q_squared_margin_in_N"], F(9, 50))
        self.assertEqual(result["balanced_factor_below_Q_margin_in_N"], F(9, 100))
        self.assertFalse(result["standard_large_sieve_controls_signed_covariance"])
        self.assertFalse(result["asymptotic_large_sieve_theorem_directly_applies"])
        self.assertFalse(result["local_prime_modulus_adaptation_proved"])


if __name__ == "__main__":
    unittest.main()
