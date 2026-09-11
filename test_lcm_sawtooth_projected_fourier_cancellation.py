import math
import unittest

from lcm_sawtooth_projected_fourier_cancellation import (
    alternate_geometry_projected_fourier_holdout_receipt,
    bridge_distortion_confirmation_receipt,
    new_period_analog_projected_fourier_holdout_receipt,
    new_period_projected_fourier_holdout_receipt,
    projected_fourier_cancellation_receipt,
    q2310_bridge_distortion_receipt,
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
        with self.assertRaises(ValueError):
            alternate_geometry_projected_fourier_holdout_receipt(
                minimum_spearman_correlation=2)
        with self.assertRaises(ValueError):
            new_period_projected_fourier_holdout_receipt(
                minimum_spearman_correlation=2)
        with self.assertRaises(ValueError):
            new_period_analog_projected_fourier_holdout_receipt(
                minimum_spearman_correlation=2)
        with self.assertRaises(ValueError):
            q2310_bridge_distortion_receipt(minimum_failed_distortion=1)
        with self.assertRaises(ValueError):
            bridge_distortion_confirmation_receipt(
                minimum_unstable_distortion=1.5)

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

    def test_alternate_geometry_rank_gate(self):
        receipt = alternate_geometry_projected_fourier_holdout_receipt()
        self.assertEqual(receipt["families"], ((35, 143), (65, 77)))
        self.assertEqual(receipt["quotients"], (35, 55, 65, 77, 91, 143))
        expected_fourier_quotients = {
            35: .000411050504581161,
            55: .0006575542046656703,
            65: .0018985106434786139,
            77: .016937294036465392,
            91: .025097070129322056,
            143: .014480420356702415,
        }
        expected_count_four_quotients = {
            35: .012964790897655157,
            55: .022032024950575643,
            65: .05159105243056866,
            77: .5443296939839037,
            91: .4838958192651274,
            143: .4693160590983769,
        }
        for quotient, expected in expected_fourier_quotients.items():
            self.assertAlmostEqual(
                receipt["fourier_cancellation_quotients"][quotient],
                expected, places=14)
        for quotient, expected in expected_count_four_quotients.items():
            self.assertAlmostEqual(
                receipt["count_four_recombination_quotients"][quotient],
                expected, places=14)
        self.assertAlmostEqual(
            receipt["spearman_correlation"],
            .9428571428571428, places=14)
        self.assertTrue(receipt["rank_gate_passes"])
        self.assertTrue(receipt["all_projected_fourier_identities_pass"])
        self.assertLess(
            receipt[
                "maximum_reconstruction_natural_scale_relative_error"],
            1e-12)
        self.assertFalse(receipt["signed_prime_correlation_proved"])

    def test_new_period_rank_gate_fails(self):
        receipt = new_period_projected_fourier_holdout_receipt()
        self.assertEqual(receipt["families"], ((15, 77), (35, 33)))
        self.assertEqual(receipt["arithmetic_period"], 2310)
        self.assertEqual(receipt["quotients"], (15, 21, 33, 35, 55, 77))
        expected_fourier_quotients = {
            15: .0033126468776086444,
            21: .010432176963204387,
            33: .04248417187258904,
            35: .017946519708990034,
            55: .04835249627943382,
            77: .02069656442173454,
        }
        expected_count_four_quotients = {
            15: .19063100974135774,
            21: .4546991458454955,
            33: .8543139343134691,
            35: .8244946861984153,
            55: .74187635170919,
            77: .47766150264034346,
        }
        for quotient, expected in expected_fourier_quotients.items():
            self.assertAlmostEqual(
                receipt["fourier_cancellation_quotients"][quotient],
                expected, places=14)
        for quotient, expected in expected_count_four_quotients.items():
            self.assertAlmostEqual(
                receipt["count_four_recombination_quotients"][quotient],
                expected, places=14)
        self.assertAlmostEqual(
            receipt["spearman_correlation"],
            .7142857142857143, places=14)
        self.assertFalse(receipt["rank_gate_passes"])
        self.assertTrue(receipt["all_projected_fourier_identities_pass"])
        self.assertLess(
            receipt[
                "maximum_reconstruction_natural_scale_relative_error"],
            1e-12)
        self.assertFalse(receipt["signed_prime_correlation_proved"])

    def test_new_period_analog_rank_gate_passes(self):
        receipt = new_period_analog_projected_fourier_holdout_receipt()
        self.assertEqual(receipt["families"], ((77, 15), (33, 35)))
        self.assertEqual(receipt["arithmetic_period"], 2310)
        expected_fourier_quotients = {
            15: .06897732535159747,
            21: .04120228305920141,
            33: .05194975718913018,
            35: .03582127107421742,
            55: .054841459620561916,
            77: .06156797992215486,
        }
        expected_count_four_quotients = {
            15: .34979821428574304,
            21: .2045342414078927,
            33: .2913249193588369,
            35: .16215960958670428,
            55: .2541893677464353,
            77: .3018103161208625,
        }
        for quotient, expected in expected_fourier_quotients.items():
            self.assertAlmostEqual(
                receipt["fourier_cancellation_quotients"][quotient],
                expected, places=14)
        for quotient, expected in expected_count_four_quotients.items():
            self.assertAlmostEqual(
                receipt["count_four_recombination_quotients"][quotient],
                expected, places=14)
        self.assertAlmostEqual(
            receipt["spearman_correlation"],
            .9428571428571428, places=14)
        self.assertTrue(receipt["rank_gate_passes"])
        self.assertTrue(receipt["all_projected_fourier_identities_pass"])
        self.assertLess(
            receipt[
                "maximum_reconstruction_natural_scale_relative_error"],
            1e-12)
        self.assertFalse(receipt["signed_prime_correlation_proved"])

    def test_q2310_exploratory_bridge_distortion_pattern(self):
        receipt = q2310_bridge_distortion_receipt()
        self.assertEqual(receipt["arithmetic_period"], 2310)
        self.assertTrue(receipt["failed_distortion_gate_passes"])
        self.assertTrue(receipt["passing_distortion_gate_passes"])
        self.assertTrue(receipt[
            "exploratory_bridge_distortion_pattern_passes"])
        for geometry in receipt["geometries"].values():
            self.assertTrue(geometry[
                "all_projected_fourier_identities_pass"])
            self.assertLess(
                geometry["maximum_bridge_identity_absolute_error"],
                1e-12)
        self.assertFalse(receipt["signed_prime_correlation_proved"])

    def test_bridge_distortion_classifier_on_fresh_geometry(self):
        receipt = bridge_distortion_confirmation_receipt()
        self.assertEqual(receipt["families"], ((21, 55), (55, 21)))
        self.assertEqual(receipt["exact_zero_quotients"], (21, 55))
        self.assertTrue(receipt["distortion_classifier_is_conclusive"])
        self.assertFalse(receipt["predicted_rank_gate_passes"])
        self.assertFalse(receipt["observed_rank_gate_passes"])
        self.assertTrue(receipt[
            "distortion_classifier_prediction_matches"])
        self.assertEqual(receipt["bridge_distortion_range"], math.inf)
        self.assertTrue(receipt["all_projected_fourier_identities_pass"])
        for quotient in receipt["exact_zero_quotients"]:
            self.assertEqual(
                receipt["rows"][quotient][
                    "exact_unscaled_signed_numerator"], 0)
            self.assertEqual(
                receipt["rows"][quotient][
                    "fourier_cancellation_quotient"], 0.0)
            self.assertIsNone(receipt["rows"][quotient][
                "bridge_identity_absolute_error"])
        self.assertFalse(receipt["signed_prime_correlation_proved"])


if __name__ == "__main__":
    unittest.main()
