import unittest

from lcm_sawtooth_frequency_resolved_fourier import (
    ALTERNATE_FAMILIES,
    CANONICAL_FAMILIES,
    EXACT_ZERO_FAMILIES,
    frequency_resolved_fourier_case_receipt,
    frequency_resolved_fourier_receipt,
    dirichlet_character_energy_holdout_receipt,
    quadratic_character_factor_reallocation_receipt,
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
        with self.assertRaises(ValueError):
            quadratic_character_factor_reallocation_receipt(
                minimum_mod5_winning_cells=9)
        with self.assertRaises(ValueError):
            dirichlet_character_energy_holdout_receipt(
                minimum_leading_four_energy_fraction=0)

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
        expected_sign_cells = {
            ("canonical", 77): (8, 4, .13082025554378435),
            ("canonical", 91): (8, 4, .305691950547537),
            ("exact_zero", 21): (16, 16, 0.0),
            ("exact_zero", 55): (16, 16, 0.0),
        }
        for (case, quotient), (active, stable, maximum_mixed) in (
                expected_sign_cells.items()):
            cells = receipt[case]["rows"][quotient][
                "divisor_stratum_sign_cells"]
            self.assertEqual(cells["active_cell_count"], active)
            self.assertEqual(cells["real_cell_count"], active)
            self.assertEqual(cells["stable_sign_cell_count"], stable)
            self.assertAlmostEqual(
                cells["maximum_opposite_sign_mass_fraction"],
                maximum_mixed, places=12)
        self.assertTrue(receipt[
            "all_active_sign_cells_are_numerically_real"])
        self.assertFalse(receipt[
            "all_active_sign_cells_have_stable_sign"])
        self.assertFalse(receipt[
            "coarse_gcd_divisor_sign_table_supported"])
        expected_quadratic_fits = {
            ("canonical", 77): (0, .07934640183001507),
            ("canonical", 91): (0, .2499155658369732),
            ("exact_zero", 21): (4, 0.0),
            ("exact_zero", 55): (4, 0.0),
        }
        for (case, quotient), (perfect_count, worst_minority) in (
                expected_quadratic_fits.items()):
            fits = receipt[case]["rows"][quotient][
                "primitive_quadratic_character_fits"]
            self.assertEqual(fits["active_divisor_count"], 4)
            self.assertEqual(fits["perfect_fit_divisor_count"], perfect_count)
            self.assertAlmostEqual(
                fits["maximum_best_twisted_minority_mass_fraction"],
                worst_minority, places=12)
        q77_d1 = receipt["canonical"]["rows"][77][
            "primitive_quadratic_character_fits"]["divisor_rows"][1]
        self.assertEqual(q77_d1["best_character_primes"], (5,))
        self.assertAlmostEqual(
            q77_d1["best_character_alignment"], .9691380010385221,
            places=12)
        q91_d91 = receipt["canonical"]["rows"][91][
            "primitive_quadratic_character_fits"]["divisor_rows"][91]
        self.assertEqual(q91_d91["best_character_primes"], (5,))
        self.assertAlmostEqual(
            q91_d91["best_character_alignment"], .5001688683260535,
            places=12)
        self.assertFalse(receipt[
            "all_primitive_divisors_have_perfect_quadratic_sign_fit"])
        self.assertFalse(receipt[
            "quadratic_character_sign_mechanism_supported"])
        self.assertFalse(receipt["uniform_frequency_resolved_bound_proved"])
        self.assertFalse(receipt["signed_prime_correlation_proved"])

    def test_mod5_character_clue_fails_factor_reallocation_holdout(self):
        receipt = quadratic_character_factor_reallocation_receipt()
        self.assertEqual(receipt["families"], ALTERNATE_FAMILIES)
        self.assertEqual(receipt["quotients"], (77, 91))
        self.assertEqual(receipt["minimum_mod5_winning_cells"], 6)
        self.assertEqual(receipt[
            "active_primitive_divisor_cell_count"], 8)
        self.assertTrue(receipt[
            "all_eight_primitive_divisor_cells_are_active"])
        self.assertEqual(receipt["mod5_winning_cells"], (
            (77, 1), (77, 7), (77, 11), (91, 91)))
        self.assertEqual(receipt["mod5_winning_cell_count"], 4)
        expected_characters = {
            (77, 1): (5,),
            (77, 7): (5,),
            (77, 11): (5,),
            (77, 77): (),
            (91, 1): (),
            (91, 7): (),
            (91, 13): (),
            (91, 91): (5,),
        }
        for (quotient, divisor), expected in expected_characters.items():
            actual = receipt["rows"][quotient][
                "primitive_quadratic_character_fits"][
                    "divisor_rows"][divisor]["best_character_primes"]
            self.assertEqual(actual, expected)
        self.assertFalse(receipt[
            "mod5_factor_reallocation_prediction_passes"])
        self.assertFalse(receipt[
            "orientation_stable_mod5_component_supported"])
        self.assertFalse(receipt["uniform_frequency_resolved_bound_proved"])
        self.assertFalse(receipt["signed_prime_correlation_proved"])

    def test_four_character_energy_is_not_low_rank(self):
        receipt = dirichlet_character_energy_holdout_receipt()
        self.assertEqual(receipt["minimum_leading_four_energy_fraction"], .9)
        self.assertEqual(receipt["active_cell_count"], 16)
        self.assertEqual(receipt["passing_cell_count"], 0)
        self.assertEqual(receipt["passing_cells"], ())
        self.assertAlmostEqual(
            receipt["minimum_observed_leading_four_energy_fraction"],
            .20558068443802235, places=12)
        self.assertEqual(
            receipt["characters_for_ninety_percent_energy_range"], (12, 31))
        self.assertAlmostEqual(
            receipt["effective_character_rank_range"][0],
            11.215577271870771, places=11)
        self.assertAlmostEqual(
            receipt["effective_character_rank_range"][1],
            27.96018345266816, places=11)
        expected_fractions = {
            ("canonical", 77): {
                1: .20558068443802235,
                7: .219652715072,
                11: .237732099573,
                77: .207319967865,
            },
            ("canonical", 91): {
                1: .244509895632,
                7: .2409200854182761,
                13: .309497610936,
                91: .301935434884,
            },
            ("alternate", 77): {
                1: .245214825778,
                7: .2426317296426457,
                11: .278331040196,
                77: .262289456197,
            },
            ("alternate", 91): {
                1: .405222101455,
                7: .3790910631128297,
                13: .494365769703,
                91: .423828577974,
            },
        }
        for (case, quotient), fractions in expected_fractions.items():
            energy = receipt["cases"][case]["rows"][quotient][
                "primitive_dirichlet_character_energy"]
            self.assertEqual(
                energy["unit_group_order"], 48 if quotient == 77 else 40)
            self.assertTrue(energy["all_character_expansions_reconstruct"])
            self.assertLess(energy["maximum_parseval_relative_error"], 1e-12)
            self.assertLess(
                energy["maximum_reconstruction_natural_scale_relative_error"],
                1e-12)
            for divisor, expected in fractions.items():
                self.assertAlmostEqual(
                    energy["divisor_rows"][divisor][
                        "leading_character_energy_fraction"],
                    expected, places=11)
        self.assertTrue(receipt["all_character_expansions_reconstruct"])
        self.assertFalse(receipt["all_sixteen_cells_pass_low_rank_gate"])
        self.assertFalse(receipt[
            "four_character_low_rank_mechanism_supported"])
        self.assertFalse(receipt[
            "uniform_character_large_sieve_estimate_proved"])
        self.assertFalse(receipt["signed_prime_correlation_proved"])


if __name__ == "__main__":
    unittest.main()
