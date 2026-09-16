import json
import unittest
from pathlib import Path


class Q286WbssSingleWeightMajorArcFloorAuditTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/q286-wbss-single-weight-major-arc-floor-audit.json"
        ).read_text(encoding="utf-8"))

    def test_receipt_is_shortcut_falsifier_not_proof(self):
        receipt = self.load_receipt()

        self.assertEqual(
            receipt["status"],
            "FALSIFIER_pointwise_positive_single_weight_floor")
        self.assertFalse(receipt["goldbach_proved"])
        self.assertFalse(
            receipt["single_weight_pointwise_floor_theorem_proved"])
        self.assertFalse(receipt["signed_distribution_theorem_proved"])
        self.assertFalse(receipt["adverse_drag_theorem_proved"])
        self.assertFalse(receipt["universal_pointwise_bound_proved"])

    def test_global_weight_has_negative_and_positive_residues(self):
        receipt = self.load_receipt()
        summary = receipt["global_weight_summary"]

        self.assertAlmostEqual(summary["mean"], 1.0, places=12)
        self.assertAlmostEqual(
            summary["minimum"], -11.747067126163136, places=12)
        self.assertAlmostEqual(
            summary["maximum"], 40.228810300155935, places=12)
        self.assertEqual(summary["negative_unit_count"], 1228)
        self.assertEqual(summary["zero_unit_count"], 0)
        self.assertEqual(summary["positive_unit_count"], 1652)

    def test_every_even_target_has_negative_admissible_weight(self):
        receipt = self.load_receipt()
        target = receipt["target_residue_summary"]

        self.assertEqual(target["even_target_residue_count"], 5005)
        self.assertEqual(target["rows_with_negative_admissible_weight"], 5005)
        self.assertEqual(target["rows_with_pointwise_positive_floor"], 0)
        self.assertAlmostEqual(
            target["admissible_weight_mean_summary"]["minimum"],
            0.6039353780830684,
            places=12)
        self.assertAlmostEqual(
            target["negative_weight_fraction_summary"]["maximum"],
            0.47205387205387206,
            places=12)

    def test_logical_consequence_demotes_support_only_route(self):
        receipt = self.load_receipt()
        consequence = receipt["logical_consequence"]

        self.assertTrue(consequence["support_only_route_falsified"])
        self.assertIn("existence of some strict-central prime pair",
                      consequence["why"])
        self.assertIn("signed distribution estimate",
                      consequence["surviving_requirement"])
        self.assertIn("unnormalized scale",
                      consequence["collapse_warning"])
        self.assertIn("support-only shortcut is falsified",
                      receipt["decision"])

    def test_candidate_has_falsifier_and_smallest_test(self):
        receipt = self.load_receipt()
        candidate = receipt["candidate"]

        self.assertEqual(candidate["novelty_label"], "new-to-this-task")
        self.assertIn("support alone", candidate["mechanism"])
        self.assertIn("positive minimum weight", candidate["prediction"])
        self.assertIn("all even target residues", candidate["falsifier"])
        self.assertIn("negative fraction", candidate["smallest_test"])


if __name__ == "__main__":
    unittest.main()
