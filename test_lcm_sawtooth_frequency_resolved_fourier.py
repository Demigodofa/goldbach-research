import unittest

from lcm_sawtooth_frequency_resolved_fourier import (
    CANONICAL_FAMILIES,
    EXACT_ZERO_FAMILIES,
    frequency_resolved_fourier_case_receipt,
    frequency_resolved_fourier_receipt,
)


class FrequencyResolvedFourierTests(unittest.TestCase):
    def test_guards(self):
        with self.assertRaises(ValueError):
            frequency_resolved_fourier_case_receipt(((3, 5),), (1,))
        with self.assertRaises(ValueError):
            frequency_resolved_fourier_case_receipt(
                ((3, 5), (5, 7)), (1,))
        with self.assertRaises(ValueError):
            frequency_resolved_fourier_case_receipt(
                ((3, 5), (3, 5)), (0,))
        with self.assertRaises(ValueError):
            frequency_resolved_fourier_case_receipt(
                ((3, 5), (3, 5)), (1,), tolerance=-1)
        with self.assertRaises(ValueError):
            frequency_resolved_fourier_case_receipt(
                ((3, 5), (3, 5)), (1,), batch_size=0)

    def test_every_resonant_frequency_reconstructs(self):
        receipt = frequency_resolved_fourier_receipt()
        self.assertEqual(receipt["canonical"]["families"], CANONICAL_FAMILIES)
        self.assertEqual(receipt["exact_zero"]["families"], EXACT_ZERO_FAMILIES)
        self.assertEqual(receipt["canonical"]["quotients"], (77, 91))
        self.assertEqual(receipt["exact_zero"]["quotients"], (21, 55))
        self.assertTrue(receipt["all_frequencies_reconstruct"])
        for case in (receipt["canonical"], receipt["exact_zero"]):
            for row in case["rows"].values():
                self.assertTrue(row["every_frequency_reconstructs"])
                self.assertLess(
                    row["maximum_cauchy_scale_relative_error"], 1e-12)
                self.assertAlmostEqual(
                    row["formula_recombined_absolute_mass"],
                    row["direct_recombined_absolute_mass"], places=7)
        self.assertAlmostEqual(
            receipt["exact_zero"]["rows"][21]["formula_signed_total"].real,
            0.0, places=7)
        self.assertAlmostEqual(
            receipt["exact_zero"]["rows"][55]["formula_signed_total"].real,
            0.0, places=7)
        expected_stratum_metrics = {
            ("canonical", 77): (.06298100352659718, 15.859926012513927),
            ("canonical", 91): (.4960806605079712, .7892312818860849),
            ("exact_zero", 21): (.6603773584905617, 1.5142857142857225),
            ("exact_zero", 55): (.7443609022556356, 1.343434343434349),
        }
        for (case, quotient), (coherence, sign_ratio) in (
                expected_stratum_metrics.items()):
            row = receipt[case]["rows"][quotient]
            self.assertTrue(row["divisor_stratum_reconstruction_passes"])
            self.assertAlmostEqual(
                row["within_frequency_divisor_coherence"], coherence,
                places=12)
            self.assertAlmostEqual(
                row["sign_removal_mass_ratio"], sign_ratio, places=12)
        self.assertTrue(receipt["all_divisor_strata_reconstruct"])
        self.assertFalse(receipt[
            "sign_removal_consistently_increases_mass"])
        self.assertFalse(receipt[
            "simple_ramanujan_sign_stratum_mechanism_supported"])
        self.assertFalse(receipt["uniform_frequency_resolved_bound_proved"])
        self.assertFalse(receipt["signed_prime_correlation_proved"])


if __name__ == "__main__":
    unittest.main()
