import json
import unittest
from pathlib import Path


EVIDENCE = Path(
    "evidence/"
    "mobius-moment-square-degree5-q46189-selector-provenance-holdout-audit.json")


class MobiusMomentSquareDegree5Q46189SelectorProvenanceHoldoutTests(
        unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = json.loads(EVIDENCE.read_text(encoding="utf-8"))

    def test_receipt_preserves_boundaries(self):
        self.assertEqual(
            self.receipt["status"],
            "AUDIT_q46189_selector_provenance_holdout")
        self.assertTrue(
            self.receipt["finite_selector_provenance_holdout_audit_only"])
        self.assertTrue(self.receipt["finite_diagnostic_only"])
        self.assertFalse(self.receipt["natural_selector_theorem_proved"])
        self.assertFalse(self.receipt["fresh_conductor_holdout_proved"])
        self.assertFalse(
            self.receipt["distance_slice_positive_share_theorem_proved"])
        self.assertFalse(self.receipt["goldbach_proved"])

    def test_selector_is_explicitly_post_hoc(self):
        provenance = self.receipt["selector_provenance"]
        classification = self.receipt["classification"]
        self.assertTrue(
            provenance["coarse_10A_slice_boundaries_natural_from_active_scale_A"])
        self.assertTrue(provenance["coarse_10A_slice_choice_was_post_hoc"])
        self.assertTrue(
            provenance["selected_coarse_slice_not_predeclared_acceptance_condition"])
        self.assertTrue(
            provenance["microblock_choice_inside_50A_to_60A_was_nested_post_hoc"])
        self.assertFalse(
            provenance["natural_conductor_geometry_selector_proved"])
        self.assertTrue(classification["post_hoc_selector"])
        self.assertTrue(
            classification["selector_supported_only_as_finite_hypothesis"])
        self.assertFalse(classification["natural_selector_theorem_proved"])

    def test_coarse_leave_one_out_selects_50a_to_60a_every_time(self):
        coarse = self.receipt["leave_one_denominator_out"][
            "coarse_10A_far_band_slices"]
        self.assertEqual(coarse["heldout_row_count"], 10)
        self.assertEqual(coarse["heldout_pass_count"], 10)
        self.assertTrue(coarse["all_heldout_rows_pass"])
        self.assertEqual(
            coarse["selected_block_counts"], {"50A_to_60A": 10})
        self.assertAlmostEqual(
            coarse["minimum_heldout_positive_fraction_gap"],
            0.041455517777469975,
            places=15)
        self.assertAlmostEqual(
            coarse["minimum_heldout_total_gap"],
            0.06613384233919847,
            places=15)
        self.assertTrue(
            self.receipt["classification"][
                "coarse_selector_leave_one_out_survives"])

    def test_nested_microblock_holdout_survives_but_varies(self):
        micro = self.receipt["leave_one_denominator_out"][
            "contiguous_microblocks_inside_50A_to_60A"]
        self.assertEqual(micro["heldout_row_count"], 10)
        self.assertEqual(micro["heldout_pass_count"], 10)
        self.assertTrue(micro["all_heldout_rows_pass"])
        self.assertEqual(
            micro["selected_block_counts"],
            {
                "50A_to_58A": 7,
                "50A_to_60A": 1,
                "56A_to_57A": 1,
                "56A_to_58A": 1,
            })
        self.assertAlmostEqual(
            micro["minimum_heldout_positive_fraction_gap"],
            0.006780195258194677,
            places=15)
        self.assertAlmostEqual(
            micro["minimum_heldout_total_gap"],
            0.008428105120766007,
            places=15)
        self.assertTrue(
            self.receipt["classification"][
                "nested_microblock_leave_one_out_survives"])


if __name__ == "__main__":
    unittest.main()
