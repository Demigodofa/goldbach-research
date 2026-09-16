import json
import unittest
from pathlib import Path


class Q286WbssK286ZeroResidueRawCoverageAuditTests(unittest.TestCase):
    def load_receipt(self):
        return json.loads(Path(
            "evidence/q286-wbss-k286-zero-residue-raw-coverage-audit.json"
        ).read_text(encoding="utf-8"))

    def test_receipt_is_coverage_audit_not_proof(self):
        receipt = self.load_receipt()

        self.assertEqual(
            receipt["status"],
            "AUDIT_zero_residue_no_discount_lane_uncovered_by_raw_finite_calibration")
        self.assertFalse(
            receipt["zero_residue_raw_adverse_drag_theorem_proved"])
        self.assertFalse(receipt["universal_pointwise_raw_bound_proved"])
        self.assertFalse(receipt["binary_prime_moment_theorem_proved"])
        self.assertFalse(receipt["q286_threshold_theorem_proved"])
        self.assertFalse(receipt["strict_central_goldbach_theorem_proved"])
        self.assertFalse(receipt["goldbach_proved"])

    def test_zero_residue_is_unique_no_discount_lane(self):
        receipt = self.load_receipt()
        no_discount = receipt["reflection_no_discount_residues"]
        zero = receipt["residue_zero_reflection_row"]

        self.assertEqual(len(no_discount), 1)
        self.assertEqual(no_discount[0]["target_mod_286"], 0)
        self.assertAlmostEqual(
            no_discount[0]["reflection_even_energy_fraction"],
            1.0,
            places=12)
        self.assertAlmostEqual(
            no_discount[0]["reflection_odd_energy_fraction"],
            1.8822507657823637e-28,
            places=30)
        self.assertAlmostEqual(
            zero["centered_full_l2"], 50.09192896531902, places=12)
        self.assertAlmostEqual(
            zero["reflection_even_l2"], 50.09192896531902, places=12)

    def test_raw_calibration_does_not_sample_zero_residue(self):
        receipt = self.load_receipt()
        coverage = receipt["raw_calibration_coverage"]

        self.assertEqual(coverage["row_count"], 348)
        self.assertEqual(coverage["sampled_mod_286_residue_count"], 27)
        self.assertEqual(coverage["zero_residue_raw_row_count"], 0)
        self.assertEqual(coverage["missing_no_discount_residues"], [0])
        self.assertNotIn(0, coverage["sampled_mod_286_residues"])

    def test_finite_stress_classes_are_not_substitutes(self):
        receipt = self.load_receipt()
        coverage = receipt["raw_calibration_coverage"]
        highest = coverage["highest_raw_adverse_drag_ratio_class"]
        tightest = coverage["tightest_gap_over_target_class"]

        self.assertEqual(highest["target_mod_286"], 90)
        self.assertAlmostEqual(
            highest["raw_adverse_drag_ratio_summary"]["maximum"],
            0.23148438379145228,
            places=12)
        self.assertEqual(tightest["target_mod_286"], 134)
        self.assertAlmostEqual(
            tightest["raw_adverse_gate_gap_over_target_summary"]["minimum"],
            0.26310340793692394,
            places=12)
        self.assertIn("N == 0 mod 286",
                      receipt["necessary_subtheorem"]["statement"])
        self.assertIn("Do not use the 348-row raw margin summary",
                      receipt["decision"])


if __name__ == "__main__":
    unittest.main()
