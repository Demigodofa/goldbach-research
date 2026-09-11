import unittest

from lcm_sawtooth_projected_fourier_cancellation import (
    projected_fourier_cancellation_receipt,
    three_prime_projected_fourier_holdout_receipt,
    two_prime_projected_fourier_holdout_receipt,
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
        with self.assertRaises(ValueError):
            two_prime_projected_fourier_holdout_receipt(
                minimum_holdout_spearman_correlation=2)
        with self.assertRaises(ValueError):
            three_prime_projected_fourier_holdout_receipt(
                minimum_spearman_correlation=2)

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

    def test_two_prime_holdout_rank_gate(self):
        receipt = two_prime_projected_fourier_holdout_receipt()
        self.assertEqual(receipt["discovery_quotients"], (77, 91))
        self.assertEqual(receipt["holdout_quotients"], (35, 55, 65, 143))
        self.assertTrue(receipt["all_projected_fourier_identities_pass"])
        expected_fourier_quotients = {
            35: .010906884721340548,
            55: .024560020667301303,
            65: .0005487547365190931,
            77: .0045059566848989745,
            91: .04566543309435243,
            143: .006101857449924944,
        }
        for quotient, expected in expected_fourier_quotients.items():
            self.assertAlmostEqual(
                receipt["fourier_cancellation_quotients"][quotient],
                expected, places=14)
        self.assertEqual(receipt["holdout_spearman_correlation"], 1.0)
        self.assertEqual(receipt["all_six_spearman_correlation"], 1.0)
        self.assertTrue(receipt["holdout_rank_gate_passes"])
        self.assertEqual(
            receipt["holdout_rank_gate_passes"],
            receipt["holdout_spearman_correlation"] >= .8)
        self.assertFalse(receipt["signed_prime_correlation_proved"])

    def test_three_prime_holdout_rank_gate(self):
        receipt = three_prime_projected_fourier_holdout_receipt()
        self.assertEqual(receipt["quotients"], (385, 455, 715, 1001))
        expected_fourier_quotients = {
            385: .008277163423608182,
            455: .037707562483578885,
            715: .014421299900784999,
            1001: .0324706638039624,
        }
        for quotient, expected in expected_fourier_quotients.items():
            self.assertAlmostEqual(
                receipt["fourier_cancellation_quotients"][quotient],
                expected, places=14)
        self.assertEqual(receipt["spearman_correlation"], 1.0)
        self.assertTrue(receipt["rank_gate_passes"])
        self.assertTrue(receipt["all_projected_fourier_identities_pass"])
        self.assertLess(
            receipt[
                "maximum_reconstruction_natural_scale_relative_error"],
            1e-12)
        self.assertFalse(receipt["signed_prime_correlation_proved"])


if __name__ == "__main__":
    unittest.main()
