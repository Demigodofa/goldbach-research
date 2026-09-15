import json
import unittest
from pathlib import Path


class Q286WbssFourModulusDirectHoldoutDecompositionTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/"
            "q286-wbss-four-modulus-direct-holdout-decomposition.json"
        ).read_text(encoding="utf-8"))

    def test_receipt_preserves_boundaries(self):
        receipt = self.load_receipt()

        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(receipt["projection_theorem_proved"])
        self.assertFalse(receipt["signed_discrepancy_theorem_proved"])
        self.assertTrue(receipt["universal_bound_open"])
        self.assertIn("finite q286-WBSS four-modulus",
                      receipt["status_boundary"])

    def test_aggregate_signed_projection_survives_split_failures(self):
        receipt = self.load_receipt()
        summary = receipt["holdout"]["summary"]

        self.assertTrue(receipt["direct_witness_survives_holdout"])
        self.assertTrue(
            receipt["aggregate_signed_error_survives_top20_failures"])
        self.assertEqual(summary["row_count"], 116)
        self.assertEqual(summary["actual_positive_count"], 116)
        self.assertEqual(summary["actual_nonpositive_count"], 0)
        self.assertEqual(summary["top20_nonnegative_count"], 70)
        self.assertEqual(summary["top20_nonnegative_raw_positive_count"], 70)

    def test_tightest_row_and_signed_load_are_recorded(self):
        receipt = self.load_receipt()
        summary = receipt["holdout"]["summary"]

        self.assertEqual(summary["tightest_row"]["target"], 965362)
        self.assertAlmostEqual(
            summary["actual_expectation_summary"]["minimum"],
            0.674072332014222,
            places=12)
        self.assertAlmostEqual(
            summary["lambda_phi_summary"]["maximum"],
            0.213151501463302,
            places=12)
        self.assertAlmostEqual(
            summary["local_uniform_main_summary"]["minimum"],
            0.717245423802844,
            places=12)

    def test_four_modulus_formula_reconstructs_direct_receipt(self):
        receipt = self.load_receipt()
        summary = receipt["holdout"]["summary"]

        self.assertLess(
            summary["formula_reconstruction_error_summary"]["maximum"],
            1e-12)

    def test_no_single_modulus_is_required_on_this_holdout(self):
        receipt = self.load_receipt()
        removal = receipt["holdout"]["single_modulus_removal_summary"]

        self.assertEqual(set(removal), {"70", "130", "154", "286"})
        for row in removal.values():
            self.assertEqual(row["removed_positive_count"], 116)
            self.assertEqual(row["removed_nonpositive_count"], 0)
            self.assertEqual(row["only_positive_count"], 116)
            self.assertEqual(row["only_nonpositive_count"], 0)

    def test_modulus_errors_are_mixed_signed(self):
        receipt = self.load_receipt()
        moduli = receipt["holdout"]["modulus_summaries"]

        for row in moduli.values():
            self.assertGreater(row["negative_count"], 0)
            self.assertGreater(row["positive_count"], 0)


if __name__ == "__main__":
    unittest.main()
