import unittest

from lcm_sawtooth_resonant_source_sectors import (
    fully_resonant_source_sector_receipt,
    leading_lag_fully_resonant_sector_receipt,
)


class ResonantSourceSectorTests(unittest.TestCase):
    def test_guards(self):
        with self.assertRaises(ValueError):
            fully_resonant_source_sector_receipt(lag=0)
        with self.assertRaises(ValueError):
            fully_resonant_source_sector_receipt(
                minimum_mean_zero_sector_mass_fraction=0)
        with self.assertRaises(ValueError):
            fully_resonant_source_sector_receipt(
                minimum_sector_cross_frequency_coherence=0)
        with self.assertRaises(ValueError):
            fully_resonant_source_sector_receipt(
                maximum_sector_recombination_quotient=0)
        with self.assertRaises(ValueError):
            fully_resonant_source_sector_receipt(tolerance=-1)

    def test_lag_182_fully_resonant_sector_decomposition(self):
        receipt = fully_resonant_source_sector_receipt()
        self.assertEqual(receipt["quotient_period"], 55)
        self.assertEqual(receipt["quotient_primes"], (5, 11))
        self.assertEqual(
            receipt["sector_eigenvalues"],
            {(): 27, (5,): -9, (11,): -3, (5, 11): 1})
        self.assertLess(
            receipt["maximum_reconstruction_natural_scale_relative_error"],
            1e-12)
        self.assertEqual(receipt["maximum_off_resonant_sector_value"], 0)
        self.assertTrue(receipt["fully_resonant_sector_identity_passes"])
        self.assertAlmostEqual(
            receipt["direct_fully_resonant_absolute_mass"],
            receipt["reconstructed_fully_resonant_absolute_mass"], places=9)
        expected_masses = {
            (): 7165.205395435115,
            (5,): 3238.5396263388807,
            (11,): 3938.9788713068133,
            (5, 11): 4501.581265974542,
        }
        expected_signed_reals = {
            (): -7104.502499999947,
            (5,): 3196.5949999999775,
            (11,): 3913.0170833333086,
            (5, 11): -4483.909583333306,
        }
        for sector in expected_masses:
            self.assertAlmostEqual(
                receipt["sector_absolute_masses"][sector],
                expected_masses[sector], places=9)
            self.assertAlmostEqual(
                receipt["sector_signed_mean_correlations"][sector][0],
                expected_signed_reals[sector], places=9)
        self.assertAlmostEqual(
            receipt["mean_zero_sector_mass_fraction"],
            .6197681296838912, places=12)
        self.assertFalse(receipt["mean_zero_sector_mass_gate_passes"])
        self.assertAlmostEqual(
            receipt["minimum_observed_sector_cross_frequency_coherence"],
            .9870482899150687, places=12)
        self.assertTrue(receipt[
            "all_sector_cross_frequency_coherence_gates_pass"])
        self.assertTrue(receipt["all_alternating_parity_signs_match"])
        self.assertAlmostEqual(
            receipt["sector_recombination_quotient"],
            .23767392653624825, places=12)
        self.assertTrue(receipt["sector_recombination_gate_passes"])

    def test_all_five_generalizations_fail(self):
        receipt = leading_lag_fully_resonant_sector_receipt()
        self.assertEqual(receipt["lags"], (140, 154, 156, 182, 240))
        expected_recombination = {
            140: .5885702865074277,
            154: .10828557400915777,
            156: .5013118107746192,
            182: .23767392653624825,
            240: .6393288305288406,
        }
        for lag, expected in expected_recombination.items():
            self.assertAlmostEqual(
                receipt["sector_recombination_quotients"][lag],
                expected, places=12)
        self.assertEqual(
            receipt["alternating_parity_sign_gates"],
            {140: True, 154: True, 156: False, 182: True, 240: False})
        self.assertFalse(receipt[
            "all_sector_cross_frequency_coherence_gates_pass"])
        self.assertFalse(receipt["all_sector_recombination_gates_pass"])
        self.assertFalse(receipt[
            "all_alternating_parity_sign_gates_pass"])
        self.assertTrue(receipt[
            "all_fully_resonant_sector_identities_pass"])

    def test_two_prime_quotient_five_discriminator_fails(self):
        expected = {
            286: (35, .24470719651873438, True),
            130: (77, .05717700197074396, True),
            110: (91, .26932831859740486, False),
        }
        for lag, (quotient, recombination, gate) in expected.items():
            receipt = fully_resonant_source_sector_receipt(lag=lag)
            self.assertEqual(receipt["quotient_period"], quotient)
            self.assertAlmostEqual(
                receipt["sector_recombination_quotient"],
                recombination, places=12)
            self.assertEqual(
                receipt["sector_recombination_gate_passes"], gate)


if __name__ == "__main__":
    unittest.main()
