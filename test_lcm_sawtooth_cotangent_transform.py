import unittest

from lcm_sawtooth_cotangent_transform import (
    _primitive_cotangent_transform_formula,
    cotangent_sawtooth_count_four_receipt,
    primitive_cotangent_transform_receipt,
)


class CotangentTransformTests(unittest.TestCase):
    def test_guards(self):
        with self.assertRaises(ValueError):
            primitive_cotangent_transform_receipt(denominators=())
        with self.assertRaises(ValueError):
            primitive_cotangent_transform_receipt(tolerance=-1)
        with self.assertRaises(ValueError):
            cotangent_sawtooth_count_four_receipt(lags=(0,))

    def test_primitive_cotangent_transform(self):
        receipt = primitive_cotangent_transform_receipt()
        self.assertEqual(receipt["denominators"], (77, 130, 143, 70))
        self.assertEqual(
            {_pair: _primitive_cotangent_transform_formula(*_pair)
             for _pair in ((77, 0), (77, 1), (77, 11),
                           (143, 1), (143, 11))},
            {(77, 0): 0j, (77, 1): 61j, (77, 11): 56j,
             (143, 1): 121j, (143, 11): 130j})
        self.assertLess(
            receipt["maximum_transform_natural_scale_relative_error"],
            1e-12)
        self.assertLess(receipt["maximum_inverse_relative_error"], 1e-12)
        self.assertTrue(receipt[
            "all_primitive_cotangent_sawtooth_identities_pass"])

    def test_q77_q91_count_four_sawtooth_reconstruction(self):
        receipt = cotangent_sawtooth_count_four_receipt()
        self.assertEqual(receipt["lags"], (130, 110))
        self.assertEqual(
            {lag: row["quotient_period"]
             for lag, row in receipt["rows"].items()},
            {130: 77, 110: 91})
        self.assertLess(receipt["maximum_source_relative_error"], 2.2e-14)
        self.assertTrue(receipt[
            "all_count_four_sawtooth_reconstructions_pass"])
        for row in receipt["rows"].values():
            self.assertLess(
                row["maximum_sector_natural_scale_relative_error"], 1e-12)
            self.assertLess(
                row[
                    "maximum_direct_reconstruction_natural_scale_relative_error"],
                1e-12)
        self.assertFalse(receipt[
            "classical_two_cotangent_product_formula_used"])
        self.assertFalse(receipt["signed_prime_correlation_proved"])


if __name__ == "__main__":
    unittest.main()
