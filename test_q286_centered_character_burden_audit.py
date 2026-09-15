import json
import unittest
from pathlib import Path


class Q286CenteredCharacterBurdenAuditTests(unittest.TestCase):
    def test_character_burden_descends_to_three_dominant_supports(self):
        path = Path("evidence/q286-centered-character-burden-audit.json")
        receipt = json.loads(path.read_text(encoding="utf-8"))

        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["signed_prime_correlation_estimate_proved"])
        self.assertTrue(receipt["centered_character_burden_measured"])
        self.assertTrue(receipt["three_dominant_support_problem_defined"])

        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["unit_group_order"], 2880)
        self.assertEqual(receipt["factor_primes"], [5, 7, 11, 13])
        self.assertFalse(receipt["full_modulus_10010_support_present"])
        self.assertTrue(
            receipt["all_nonzero_supports_descend_to_lower_moduli"])
        self.assertLess(
            receipt["maximum_support_descent_relative_error"], 1e-12)
        self.assertLess(
            receipt["component_reconstruction_relative_error"], 1e-12)

        self.assertEqual(
            receipt["nonzero_natural_moduli"],
            [10, 14, 22, 26, 70, 130, 154, 286])
        self.assertEqual(
            receipt["dominant_99_percent_energy_support_count"], 3)
        self.assertGreater(
            receipt["top_three_support_energy_fraction"], 0.99)
        self.assertGreater(
            receipt["largest_support_energy_fraction"], 0.69)

        labels = [
            row["support_label"]
            for row in receipt["dominant_99_percent_energy_support_rows"]
        ]
        self.assertEqual(labels, ["11x13", "7x11", "5x7"])

        self.assertGreater(
            receipt["full_local_to_principal_ratio_summary"]["minimum"], 0.0)
        self.assertIn("286, 154, and 70", receipt["smallest_new_problem"])


if __name__ == "__main__":
    unittest.main()
