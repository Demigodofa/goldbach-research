import unittest

from lcm_sawtooth_cotangent_count import (
    cotangent_count_discriminator_receipt,
    cotangent_count_source_receipt,
    three_prime_cotangent_count_receipt,
    two_prime_cotangent_count_receipt,
)


class CotangentCountTests(unittest.TestCase):
    def test_guards(self):
        with self.assertRaises(ValueError):
            cotangent_count_source_receipt(lag=0)
        with self.assertRaises(ValueError):
            cotangent_count_source_receipt(tolerance=-1)

    def test_q77_q143_count_discriminator(self):
        receipt = cotangent_count_discriminator_receipt()
        self.assertEqual(receipt["strong_quotient"], 77)
        self.assertEqual(receipt["weak_quotient"], 143)
        self.assertTrue(receipt["both_reconstructions_pass"])
        self.assertAlmostEqual(
            receipt["strong_count_two_shapley_loss_fraction"],
            .19841380650018023, places=12)
        self.assertAlmostEqual(
            receipt["weak_count_two_shapley_loss_fraction"],
            .06763065573289252, places=12)
        self.assertFalse(receipt["strong_count_two_gate_passes"])
        self.assertTrue(receipt["weak_count_two_gate_passes"])
        self.assertFalse(receipt["cotangent_count_discriminator_passes"])

    def test_two_prime_count_four_and_mass_ratio_rules_fail(self):
        receipt = two_prime_cotangent_count_receipt()
        self.assertEqual(receipt["quotients"], (35, 55, 65, 77, 91, 143))
        expected_count_four_quotients = {
            35: .16118908808873234,
            55: .3024507788824479,
            65: .014327564985042195,
            77: .06505818067801658,
            91: .5047491987897079,
            143: .09820822341044044,
        }
        expected_mass_ratios = {
            35: .09315224653361054,
            55: .15579973512438464,
            65: .3859820853423725,
            77: .3177572729091074,
            91: .44136064908417894,
            143: 1.3719260813945435,
        }
        expected_count_four_shares = {
            35: 1.0171872565269635,
            55: .8434390124898529,
            65: .8141118340901425,
            77: .81729424215736,
            91: .8723514969826882,
            143: .9437989120860197,
        }
        expected_full_quotients = {
            35: .24470719651873438,
            55: .23767392653624825,
            65: .10828557400915777,
            77: .05717700197074396,
            91: .26932831859740486,
            143: .5885702865074277,
        }
        for quotient, expected in expected_count_four_quotients.items():
            self.assertAlmostEqual(
                receipt["count_four_recombination_quotients"][quotient],
                expected, places=12)
        for quotient, expected in expected_mass_ratios.items():
            self.assertAlmostEqual(
                receipt["count_two_to_four_sector_mass_ratios"][quotient],
                expected, places=12)
        for quotient, expected in expected_count_four_shares.items():
            self.assertAlmostEqual(
                receipt["count_four_shapley_loss_fractions"][quotient],
                expected, places=12)
        for quotient, expected in expected_full_quotients.items():
            self.assertAlmostEqual(
                receipt["full_recombination_quotients"][quotient],
                expected, places=12)
        self.assertFalse(receipt[
            "all_count_four_recombination_gates_pass"])
        self.assertEqual(
            receipt["mass_ratio_classifier_matches"],
            {35: True, 55: True, 65: True,
             77: True, 91: False, 143: True})
        self.assertFalse(receipt[
            "all_mass_ratio_classifier_predictions_match"])
        self.assertTrue(receipt["all_reconstructions_pass"])

    def test_three_prime_count_four_rules_fail(self):
        receipt = three_prime_cotangent_count_receipt()
        self.assertEqual(receipt["quotients"], (385, 455, 715, 1001))
        expected_shares = {
            385: 1.0325006383402588,
            455: .7445336910069194,
            715: .42628706912934505,
            1001: .5557110297061323,
        }
        expected_full_quotients = {
            385: .5013118107746221,
            455: .24840921606041405,
            715: .022976628574723844,
            1001: .6393288305288424,
        }
        expected_count_four_quotients = {
            385: .11745372514454311,
            455: .4861020851341751,
            715: .21612322122320057,
            1001: .4110607307856016,
        }
        for quotient, expected in expected_shares.items():
            self.assertAlmostEqual(
                receipt["count_four_shapley_loss_fractions"][quotient],
                expected, places=12)
        for quotient, expected in expected_full_quotients.items():
            self.assertAlmostEqual(
                receipt["full_recombination_quotients"][quotient],
                expected, places=12)
        for quotient, expected in expected_count_four_quotients.items():
            self.assertAlmostEqual(
                receipt["count_four_recombination_quotients"][quotient],
                expected, places=12)
        self.assertFalse(receipt[
            "leading_dimension_stability_gate_passes"])
        self.assertEqual(
            receipt["contains_five_predictions_match"],
            {385: True, 455: False, 715: False, 1001: True})
        self.assertFalse(receipt["all_contains_five_predictions_match"])
        self.assertTrue(receipt["all_reconstructions_pass"])


if __name__ == "__main__":
    unittest.main()
