import unittest

from lcm_sawtooth_source_fourier_factor import (
    SOURCE_FOURIER_STEPS,
    source_fourier_factorization_receipt,
)


class SourceFourierFactorizationTests(unittest.TestCase):
    def test_guards(self):
        with self.assertRaises(ValueError):
            source_fourier_factorization_receipt(families=((77, 65),))
        with self.assertRaises(ValueError):
            source_fourier_factorization_receipt(spatial_steps=())
        with self.assertRaises(ValueError):
            source_fourier_factorization_receipt(spatial_steps=(0,))
        with self.assertRaises(ValueError):
            source_fourier_factorization_receipt(tolerance=-1)

    def test_actual_source_factorization_and_ramanujan_jumps(self):
        receipt = source_fourier_factorization_receipt()
        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["spatial_steps"], SOURCE_FOURIER_STEPS)
        self.assertEqual(
            tuple(receipt["ramanujan_rows"]), (77, 130, 143, 70))
        self.assertTrue(receipt[
            "all_unit_step_ramanujan_identities_pass"])
        self.assertTrue(receipt[
            "all_interval_step_ramanujan_identities_pass"])
        self.assertTrue(receipt[
            "all_source_fourier_factorizations_pass"])
        self.assertLess(
            receipt["maximum_unit_step_ramanujan_error"], 1e-12)
        self.assertLess(
            receipt["maximum_interval_step_ramanujan_error"], 1e-12)
        self.assertLess(
            receipt[
                "maximum_source_factorization_natural_scale_relative_error"],
            1e-12)
        self.assertTrue(receipt[
            "finite_difference_ramanujan_factorization_identified"])
        self.assertFalse(receipt["uniform_source_sum_estimate_proved"])
        self.assertFalse(receipt["signed_prime_correlation_proved"])


if __name__ == "__main__":
    unittest.main()
