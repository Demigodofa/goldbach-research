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
        self.assertFalse(receipt["uniform_frequency_resolved_bound_proved"])
        self.assertFalse(receipt["signed_prime_correlation_proved"])


if __name__ == "__main__":
    unittest.main()
