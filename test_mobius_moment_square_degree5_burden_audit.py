import unittest

from tools.build_mobius_moment_square_degree5_burden_audit import (
    build_receipt,
    degree_contributors,
)


class MobiusMomentSquareDegree5BurdenAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = build_receipt()

    def test_degree_contributors_finds_degree_five_pairs(self):
        active = [[0.0 for _ in range(6)] for _ in range(6)]
        full = [[0.0 for _ in range(6)] for _ in range(6)]
        active[0][4] = active[4][0] = 3.0
        active[1][2] = active[2][1] = 5.0
        active[1][3] = active[3][1] = 7.0
        contributors = degree_contributors(active, full)
        self.assertEqual(
            [(row["left_label"], row["right_label"]) for row in contributors],
            [("00", "12"), ("01", "02"), ("01", "11")])
        self.assertEqual(
            sum(row["half_frame_contribution"] for row in contributors),
            30.0)

    def test_receipt_preserves_boundaries(self):
        self.assertEqual(
            self.receipt["status"],
            "MEASURE_degree5_weak_row_coefficient_burden")
        self.assertTrue(
            self.receipt["finite_degree5_burden_diagnostic_only"])
        self.assertTrue(self.receipt["finite_diagnostic_only"])
        self.assertFalse(self.receipt["goldbach_proved"])
        self.assertFalse(self.receipt["degree5_coefficient_theorem_proved"])
        self.assertFalse(
            self.receipt["robust_margin_universal_theorem_proved"])

    def test_weak_row_degree5_has_three_same_sign_contributors(self):
        burden = self.receipt["weak_scale_burden"]
        self.assertEqual(burden["scale_modulus"], 167)
        self.assertEqual(len(burden["contributors"]), 3)
        self.assertTrue(burden["same_sign_half_frame_contributions"])
        self.assertEqual(
            [
                (row["left_label"], row["right_label"])
                for row in burden["contributors"]
            ],
            [("00", "12"), ("01", "02"), ("01", "11")])
        self.assertEqual(
            (
                burden["top_abs_half_frame_contributor"]["left_label"],
                burden["top_abs_half_frame_contributor"]["right_label"],
            ),
            ("01", "11"))

    def test_weak_row_degree5_matches_source_provenance_delta(self):
        self.assertEqual(
            self.receipt[
                "weak_scale_provenance_minus_source_degree5_delta_decimal"],
            "-0.02000000000000000000000000000000000000000")
        self.assertIn(
            "not reliable",
            self.receipt["weak_scale_binary_float_delta_warning"])
        self.assertAlmostEqual(
            self.receipt[
                "weak_scale_sensitivity_degree5_margin_contribution"],
            -2.861012380558363e-05,
            places=16)

    def test_checked_summary_marks_degree_five_as_sensitivity_driver(self):
        weak = next(
            row for row in self.receipt["checked_scale_degree5_summary"]
            if row["scale_modulus"] == 167)
        self.assertEqual(weak["sensitivity_dominant_degree"], 5)
        self.assertEqual(
            weak["sensitivity_nonzero_coefficient_delta_count"], 1)


if __name__ == "__main__":
    unittest.main()
