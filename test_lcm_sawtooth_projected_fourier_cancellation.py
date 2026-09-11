import unittest

from lcm_sawtooth_projected_fourier_cancellation import (
    projected_fourier_cancellation_receipt,
)


class ProjectedFourierCancellationTests(unittest.TestCase):
    def test_guards(self):
        with self.assertRaises(ValueError):
            projected_fourier_cancellation_receipt(lags=(130,))
        with self.assertRaises(ValueError):
            projected_fourier_cancellation_receipt(
                strong_maximum_cancellation_quotient=0)
        with self.assertRaises(ValueError):
            projected_fourier_cancellation_receipt(
                weak_minimum_cancellation_quotient=2)
        with self.assertRaises(ValueError):
            projected_fourier_cancellation_receipt(tolerance=-1)

    def test_q77_q91_projected_fourier_discriminator(self):
        receipt = projected_fourier_cancellation_receipt()
        self.assertEqual(receipt["strong_quotient"], 77)
        self.assertEqual(receipt["weak_quotient"], 91)
        self.assertTrue(receipt["all_projected_fourier_identities_pass"])
        self.assertAlmostEqual(
            receipt["rows"][130]["fourier_cancellation_quotient"],
            .0045059566848989745, places=14)
        self.assertAlmostEqual(
            receipt["rows"][110]["fourier_cancellation_quotient"],
            .04566543309435243, places=14)
        for row in receipt["rows"].values():
            self.assertLess(
                row["reconstruction_natural_scale_relative_error"], 1e-12)
        self.assertEqual(
            receipt["fourier_cancellation_discriminator_passes"],
            receipt["strong_cancellation_gate_passes"]
            and receipt["weak_cancellation_gate_passes"])
        self.assertTrue(receipt["strong_cancellation_gate_passes"])
        self.assertFalse(receipt["weak_cancellation_gate_passes"])
        self.assertFalse(receipt[
            "fourier_cancellation_discriminator_passes"])
        self.assertFalse(receipt["uniform_source_sum_estimate_proved"])
        self.assertFalse(receipt["signed_prime_correlation_proved"])


if __name__ == "__main__":
    unittest.main()
