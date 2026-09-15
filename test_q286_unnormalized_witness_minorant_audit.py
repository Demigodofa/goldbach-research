import json
import unittest
from pathlib import Path


class Q286UnnormalizedWitnessMinorantAuditTests(unittest.TestCase):
    def test_minorant_shortcut_is_demoted_but_signed_witness_survives(self):
        path = Path("evidence/q286-unnormalized-witness-minorant-audit.json")
        receipt = json.loads(path.read_text(encoding="utf-8"))

        self.assertFalse(receipt["goldbach_proved"])
        self.assertTrue(receipt["minorant_shortcut_falsified"])
        self.assertTrue(receipt["signed_witness_route_preserved"])
        self.assertFalse(receipt["raw_coefficient_is_nonnegative"])
        self.assertFalse(
            receipt["positive_scalar_multiple_can_be_nonnegative_minorant"])

        self.assertEqual(receipt["arithmetic_period"], 10010)
        self.assertEqual(receipt["unit_group_order"], 2880)
        self.assertEqual(receipt["even_target_residue_count"], 5005)
        self.assertGreater(receipt["negative_unit_count"], 0)
        self.assertGreater(receipt["positive_unit_count"], 0)
        self.assertEqual(receipt["zero_unit_count"], 0)

        self.assertTrue(receipt["every_even_target_support_sign_indefinite"])
        self.assertEqual(
            receipt["target_residue_supports_with_no_negative_coefficients"],
            [])
        self.assertEqual(
            receipt["target_residue_supports_with_no_positive_coefficients"],
            [])
        self.assertLess(
            receipt["coefficient_real_summary"]["minimum"], 0.0)
        self.assertGreater(
            receipt["coefficient_real_summary"]["maximum"], 0.0)
        self.assertIn(
            "pointwise signed binary-prime correlation theorem",
            receipt["decision"])


if __name__ == "__main__":
    unittest.main()
