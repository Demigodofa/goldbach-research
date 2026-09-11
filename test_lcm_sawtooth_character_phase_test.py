import unittest

from lcm_sawtooth_character_phase_test import (
    character_sign_holdout_receipt,
    project_cluster_shared_factor_character_receipt,
    quadratic_character,
)


class LcmSawtoothCharacterPhaseTests(unittest.TestCase):
    def test_character_and_holdout_orientation(self):
        self.assertEqual(quadratic_character(3, 11), 1)
        self.assertEqual(quadratic_character(2, 11), -1)
        rows = tuple(
            {"modulus": modulus,
             "off_diagonal_window_cross_rayleigh": value}
            for modulus, value in ((2, -2), (3, 1), (5, 1), (7, -1)))
        receipt = character_sign_holdout_receipt(rows, 11, 2, .5)
        self.assertEqual(receipt["selected_character_orientation"], 1)
        self.assertEqual(receipt["held_out_correct_sign_count"], 2)
        self.assertTrue(receipt[
            "held_out_character_sign_hypothesis_passes"])

    def test_m127_shared_factor_rule_fails_cluster_generalization(self):
        receipt = project_cluster_shared_factor_character_receipt(
            127, (((55, 143), 11), ((77, 143), 11), ((78, 143), 13)))
        rows = {row["conductors"]: row for row in receipt["rows"]}
        self.assertEqual(rows[(55, 143)]["held_out_correct_sign_count"], 5)
        self.assertEqual(rows[(77, 143)]["held_out_correct_sign_count"], 9)
        self.assertEqual(rows[(78, 143)]["held_out_correct_sign_count"], 8)
        self.assertEqual(rows[(77, 143)]["selected_character_orientation"], -1)
        self.assertAlmostEqual(
            rows[(77, 143)]["held_out_fair_sign_tail_probability"],
            299 / 4096)
        self.assertEqual(receipt["passing_pairs"], ((77, 143),))
        self.assertFalse(receipt[
            "shared_factor_character_cluster_hypothesis_passes"])
        self.assertFalse(receipt["signed_prime_correlation_proved"])

    def test_guards_character_and_holdout_inputs(self):
        with self.assertRaises(ValueError):
            quadratic_character(2, 9)
        with self.assertRaises(ValueError):
            character_sign_holdout_receipt((), 11, 0)
        with self.assertRaises(ValueError):
            project_cluster_shared_factor_character_receipt(127, ())


if __name__ == "__main__":
    unittest.main()
