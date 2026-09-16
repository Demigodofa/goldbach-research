import json
import unittest
from pathlib import Path


EVIDENCE = Path(
    "evidence/"
    "mobius-moment-square-degree5-moving-prime-band-audit.json")


class MobiusMomentSquareDegree5MovingPrimeBandAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = json.loads(EVIDENCE.read_text(encoding="utf-8"))

    def test_receipt_preserves_boundaries(self):
        self.assertEqual(
            self.receipt["status"],
            "AUDIT_degree5_moving_prime_band_stress")
        self.assertTrue(self.receipt["finite_band_audit_only"])
        self.assertFalse(self.receipt["goldbach_proved"])
        self.assertFalse(self.receipt["source_start_theorem_proved"])
        self.assertFalse(self.receipt["moving_prime_block_theorem_proved"])
        self.assertFalse(self.receipt["sigma_band_theorem_proved"])

    def test_all_seven_sweeps_are_included(self):
        self.assertEqual(
            self.receipt["scales"], [229, 251, 293, 331, 353, 379, 383])
        self.assertEqual(self.receipt["scale_count"], 7)
        self.assertEqual(self.receipt["prime_block_count"], 357)
        self.assertEqual(self.receipt["dominance_row_count"], 1428)

    def test_band_minima_are_pinned(self):
        summaries = self.receipt["band_summaries"]
        expected = {
            "sigma_1_00_1_25": (97, 388, 0.4168496626998832, 229, 283),
            "sigma_1_25_1_50": (83, 332, 0.426291195360443, 331, 479),
            "sigma_1_50_1_75": (93, 372, 0.40189096624031384, 229, 379),
            "sigma_1_75_2_00": (84, 336, 0.40479256047704726, 331, 599),
        }
        for name, (block_count, row_count, slack, scale, prime) in (
                expected.items()):
            summary = summaries[name]
            self.assertEqual(summary["block_count"], block_count)
            self.assertEqual(summary["row_count"], row_count)
            self.assertAlmostEqual(summary["minimum_block_slack"], slack)
            self.assertEqual(
                summary["weakest_block"]["scale_modulus"], scale)
            self.assertEqual(
                summary["weakest_block"]["prime_modulus"], prime)

    def test_endpoint_only_simplification_is_not_supported(self):
        self.assertTrue(self.receipt["all_bands_have_positive_block_slack"])
        self.assertTrue(self.receipt["endpoint_bands_have_no_failures"])
        self.assertTrue(self.receipt["interior_bands_have_no_failures"])
        self.assertFalse(
            self.receipt["endpoint_only_simplification_supported"])
        self.assertAlmostEqual(
            self.receipt["endpoint_minimum_block_slack"],
            0.40479256047704726)
        self.assertAlmostEqual(
            self.receipt["interior_minimum_block_slack"],
            0.40189096624031384)

    def test_replacement_target_is_sigma_banded(self):
        target = self.receipt["candidate_next_theorem_target"]
        self.assertEqual(
            target["name"],
            "sigma-banded moving prime-block lower-frame control")
        self.assertIn("covering [1,2]", target["mechanism"])
        self.assertEqual(target["novelty_label"], "new-to-this-task")


if __name__ == "__main__":
    unittest.main()
